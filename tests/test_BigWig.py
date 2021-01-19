# -*- coding: utf-8 -*-

import pytest
import os

from efs_parser.BigWig import BigWig

__author__ = "jkanche"
__copyright__ = "jkanche"
__license__ = "mit"

"""
    The file test.bigBed and test assertions 
    come from the pyBigWig library
"""

#bb = BigWig("./test.bw")
bb = BigWig("tests/test.bw")

def test_header():
    assert(bb.header == {'magic': 2291137574, 'version': 4, 'zoomLevels': 1, 'chromTreeOffset': 344, 'fullDataOffset': 400, 'fullIndexOffset': 487, 'fieldCount': 0, 'definedFieldCount': 0, 'autoSqlOffset': 0, 'totalSummaryOffset': 304, 'uncompressBufSize': 32768})

def test_columns():
    assert(len(bb.columns) == 4)
    assert(bb.columns == ["chr", "start", "end", "score"])

def test_range():
    res, err = bb.getRange(chr="1", start=0, end=3)
    assert(err == None)
    assert(len(res) == 3)