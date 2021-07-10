"""
    Genomics file classes
"""

import struct
import zlib
import ujson
import pandas as pd
import numpy as np
from urllib.parse import urlparse
import http
import requests
import ssl
import time
import boto3
from botocore import UNSIGNED
from botocore.client import Config

__author__ = "Jayaram Kancherla"
__copyright__ = "jkanche"
__license__ = "mit"

class BaseFile(object):
    """
    Base file class for all parsers

    This class provides various useful methods to make requests, set endian, compress/decompress binary data

    Args:
        file: file location

    Attributes:
        local: if file is local or hosted on a public server
        endian: check for endianess
        compressed: defaults to true and binary blobs are zlib decompressed
        conn: http or https connection object (from http.client module)
    """

    HEADER_STRUCT = struct.Struct("<I2H3Q2H2QIQ")
    SUMMARY_STRUCT = struct.Struct("<Q4d")

    def __init__(self, file):
        self.file = file
        self.bucketname = None
        self.region_name = None
        self.file_source = self.get_file_source(file)
        if self.file_source=="s3":
            self.bucketname, self.region_name, self.file  = self.split_s3_components(file)
        self.endian = "="
        self.compressed = True
        self.conn = None
        self.stats = {
            "iotime"
        }
        self.byteRanges = {}

    def split_s3_components(self,filename):
        phase1 = filename.replace("s3://", "")
        region_start = phase1.find("@")
        if region_start == -1:
            raise Exception('Invalid S3 file name - missing region name')
        file_name_start = phase1.find("/")
        if file_name_start == -1:
            raise Exception('Invalid S3 file name - missing file name')
        bucket_name = phase1[:file_name_start]
        file_name = phase1[file_name_start + 1:region_start]
        if file_name == "":
            raise Exception('Invalid S3 file name - missing file name')
        region = phase1[region_start + 1:]
        if region == "":
            raise Exception('Invalid S3 file name - missing region name')
        return bucket_name, region, file_name

    def get_file_source(self, file):
        """
        Checks if file is local or hosted publicly

        Args:
            file: location of file
        """
        if "http://" in file or "https://" in file or "ftp://" in file:
            return "http"
        elif "s3://" in file:
            return "s3"
        else:
            return "local"

    def parse_header(self):
        raise Exception("NotImplementedException")

    def get_data(self, chr, start, end):
        raise Exception("NotImplementedException")

    def decompress_binary(self, bin_block):
        """decompress a binary string (zlib compression)

        Args:
            bin_block: binary string

        Returns:
            a zlib decompressed binary string
        """
        return zlib.decompress(bin_block)

    def formatAsJSON(self, data):
        """Encode a data object as JSON

        Args:
            data: any data object to encode

        Returns:
            data encoded as JSON
        """
        return ujson.dumps(data)

    def parse_url_http(self, furl=None):
        """
        Create a HTTPConnection or HTTPSConnection object from remote url (from http.client)

        Args:
            furl: file url
        """
        if furl is None:
            furl = self.file
        self.fuparse = urlparse(furl)
        if self.fuparse.scheme in ["ftp", "http"]:
            self.conn = http.client.HTTPConnection(self.fuparse.netloc)
        elif self.fuparse.scheme in ["ftps", "https"]:
            self.conn = http.client.HTTPSConnection(self.fuparse.netloc, context=ssl._create_unverified_context())

    def parse_url(self, furl=None):
        self.conn = requests.Session()

    def get_bytes_http(self, offset, size):
        """
        make Range requests

        Args:
            offset: offset poition in file
            size: size of bytes from offset

        Returns:
            binary string from file
        """
        if self.file_source == "local":
            f = open(self.file, "rb")
            f.seek(offset)
            bin_value = f.read(size)
            f.close()
            return bin_value
        elif self.file_source == "s3":
            response = self.get_bytes_from_s3(offset, size)
            return response
        elif self.file_source == "http":
            headers = {"Range": "bytes=%d-%d" % (offset, offset+size) }

            if not hasattr(self, 'conn') or self.conn is None:
                self.parse_url_http()

            # if connection is disconnect, reconnect
            self.conn.connect()
            self.conn.request("GET", url=self.fuparse.path, headers=headers)
            response = self.conn.getresponse()
            if response.status == 302:
                # connection redirected and found resource - usually https
                new_loc = response.getheader("Location")
                # print("url redirected & found ", new_loc)
                self.parse_url(new_loc)
                self.conn.request("GET", url=self.fuparse.path, headers=headers)
                response = self.conn.getresponse()
                resp = response.read()
            else:
                resp = response.read()
            return resp[:size]

    def get_bytes_from_s3(self, offset, size):
        s3client = boto3.client('s3', region_name=self.region_name, config=Config(signature_version=UNSIGNED))
        #key = self.file.replace(f"s3://{self.bucketname}/","")
        key = self.file
        bytes_range = "bytes=%d-%d" % (offset, offset+size)
        resp = s3client.get_object(Bucket=self.bucketname,Key=key,Range=bytes_range)
        data = resp['Body'].read()
        return data[:size]

    def get_bytes(self, offset, size):
        """Get bytes within a given range [offset:offset+size]

        Args:
            offset (int): byte start position in file
            size (int): size of bytes to access from offset

        Returns:
            bytes from offset to (offset + size)
        """
        if self.file_source == "local":
            f = open(self.file, "rb")
            f.seek(offset)
            bin_value = f.read(size)
            f.close()
            return bin_value
        elif self.file_source == "s3":
            response = self.get_bytes_from_s3(offset,size)
            return response
        elif self.file_source == "http":
            headers = {"Range": "bytes=%d-%d" % (offset, offset+size) }

            start = time.time()
            if not hasattr(self, 'conn') or self.conn is None:
                self.parse_url()

            resp = self.conn.get(self.file, headers=headers)
            end = time.time()
            self.byteRanges[headers["Range"]] = end-start

            if resp.status_code != 206:
                raise Exception("URLError")
                self.byteRanges[headers["Range"]] = "error resp != 206"

            return resp.content[:size]

    def bin_rows(self, data, chr, start, end, columns=None, metadata=None, bins = 400):
        """
        Summarize genomic data by bins parameter

        Args:
            data: data frame with genomic data
            chr: chromosome 
            start: start position
            end: end poition
            columns: names to map columns
            metadata: metadata columns in the data frame
            bins: numbers of bins to create

        Returns:
            a binned pandas dataframe
        """

        if len(data) == 0: 
            return data, None

        freq = round((end-start)/bins)
        if end - start < bins:
            freq = 1

        data = data.set_index(['start', 'end'])
        data.index = pd.IntervalIndex.from_tuples(data.index)

        bins_range = pd.interval_range(start=start, end=end, freq=freq)
        bins_df = pd.DataFrame(index=bins_range)
        bins_df["chr"] = chr

        if metadata:
            for meta in metadata:
                bins_df[meta] = data[meta]

        for col in columns:
            bins_df[col] = None

        # map data to bins
        for index, row in bins_df.iterrows():
            temps = data[(data.index.left <= index.right) & (data.index.right > index.left)]
            if len(temps) > 0:
                for col in columns:
                    row[col] = np.mean(temps[col].astype(float))

        bins_df["start"] = bins_df.index.left
        bins_df["end"] = bins_df.index.right
        return bins_df, None

    def simplified_bin_rows(self, data, chr, start, end, columns=None, metadata=None, bins = 400):
        """
        Summaize genomic data by bins parameter

        Args:
            data: data frame with genomic data
            chr: chromosome 
            start: start position
            end: end poition
            columns: names to map columns
            metadata: metadata columns in the data frame
            bins: numbers of bins to create

        Returns:
            a binned pandas dataframe
        """
        if len(data) == 0 or len(data) <= bins: 
            return data, None

        chunks = np.array_split(data, bins)
        rows = []
        columns = ["score"]
        for chunk in chunks:
            temp = {}
            temp["start"] = chunk["start"].values[0]
            temp["end"] = chunk["end"].values[len(chunk) - 1]
            for col in columns:
                temp[col] = chunk[col].mean()
            rows.append(temp)
        
        return pd.DataFrame(rows), None

    def get_status(self):
        """
        Get file status by accessing the first 64 bytes

        Returns:
            length of response or error
        """
        res = self.get_bytes(0, 64)
        if len(res) > 0 :
            return len(res), None
        else:
            return 0, "Could not read bytes"