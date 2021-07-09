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

bb = BigBed("s3://encode-public@us-west-2/2008/11/24/0868284e-8c3c-488d-89e6-487cd89971c3/ENCFF000AAU.broadPeak.bigbed")

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
