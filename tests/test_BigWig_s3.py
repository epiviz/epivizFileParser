# -*- coding: utf-8 -*-

import pytest
import os

from efs_parser.BigWig import BigWig

__author__ = "jkanche, elgaml"
__copyright__ = "jkanche"
__license__ = "mit"

"""
    The file test.bigBed and test assertions 
    come from the pyBigWig library
"""

bb = BigWig("s3://encode-public/2010/09/17/908fcd8c-9d81-4134-821e-0e9fae69be77/ENCFF000LMN.bigWig@us-west-2")

def test_header():
    assert(bb.header == {'magic': 2291137574, 'version': 4, 'zoomLevels': 10, 'chromTreeOffset': 344, 'fullDataOffset': 705, 'fullIndexOffset': 212734456, 'fieldCount': 0, 'definedFieldCount': 0, 'autoSqlOffset': 0, 'totalSummaryOffset': 304, 'totalSummaryOffset': 304,'uncompressBufSize':32768})

def test_columns():
    assert(len(bb.columns) == 4)
    assert(bb.columns == ["chr", "start", "end", "score"])

def test_range():

    res, err = bb.getRange(chr="chr4", start=0, end=3)
    assert (err == None)
    assert (len(res) == 0)

def test_get_bytes():
    res = bb.get_bytes(1, 100)
    assert (len(res) == 100)

def test_bin_rows():
    #bb = BigWig("./ENCFF685PIH.bigWig")
    start = 5000000
    end = 10020000
    res, err = bb.getRange(chr="chr1", start=start, end=end)
    v = bb.bin_rows(data=res, chr="chr1", start=start, end=end, columns=['score'], bins=10)
    assert (len(v[0]) == 10)

def test_simplified_bin_rows():
    #bb = BigWig("./39031.bigWig")
    start = 5000000
    end = 10020000
    res, err = bb.getRange(chr="chr1", start=start, end=end)
    v = bb.simplified_bin_rows(data=res, chr="chr1", start=start, end=end, columns=['score'], bins=10)
    assert (len(v[0]) == 10)