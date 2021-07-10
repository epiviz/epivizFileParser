# -*- coding: utf-8 -*-

import pytest
import os

from efs_parser.BigBed import BigBed

__author__ = "jkanche, elgaml"
__copyright__ = "jkanche"
__license__ = "mit"

"""
    The file test.bigBed and test assertions 
    come from the pyBigWig library
"""

bb = BigBed("s3://encode-public/2008/11/24/0868284e-8c3c-488d-89e6-487cd89971c3/ENCFF000AAU.broadPeak.bigbed@us-west-2")
def test_split_s3_components():
    bucket_name, region, file_name = bb.split_s3_components("s3://bucket_name/2010/09/17/908fcd8c-9d81-4134-821e-0e9fae69be77/ENCFF000LMN.bigWig@s3_region")
    assert bucket_name == "bucket_name"
    assert region == "s3_region"
    assert file_name == "2010/09/17/908fcd8c-9d81-4134-821e-0e9fae69be77/ENCFF000LMN.bigWig"
    try:
        bucket_name, region, file_name = bb.split_s3_components("s3://bucket_name/2010/09/17/908fcd8c-9d81-4134-821e-0e9fae69be77/ENCFF000LMN.bigWig")
        assert False
    except Exception:
        assert True
    try:
        bucket_name, region, file_name = bb.split_s3_components("s3://bucket_name@s3_region")
        assert False
    except Exception:
        assert True
    try:
        bucket_name, region, file_name = bb.split_s3_components("s3://abs/@")
        assert False
    except Exception:
        assert True
    try:
        bucket_name, region, file_name = bb.split_s3_components("s3://abs/file_name@")
        assert False
    except Exception:
        assert True
def test_header():
    assert(bb.header == {'magic': 2273964779, 'version': 4, 'zoomLevels': 9, 'chromTreeOffset': 1239, 'fullDataOffset': 1600, 'fullIndexOffset': 13614032, 'fieldCount': 9, 'definedFieldCount': 6, 'autoSqlOffset': 304, 'totalSummaryOffset': 1135, 'uncompressBufSize': 16384})

def test_columns():
    assert(len(bb.columns) == 9)
    assert(bb.columns == ["chr", "start", "end", "name", "score", "strand", "signalValue", "pValue", "qValue"])

def test_range():
    res, err = bb.getRange(chr="chr1", start=10000000, end=10020000)
    assert(err == None)
    assert(len(res) == 4)

def test_get_bytes():
    res = bb.get_bytes(1, 100)
    assert (len(res) == 100)
