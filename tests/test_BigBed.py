# -*- coding: utf-8 -*-

import pytest
import os

from epivizFileParser.BigBed import BigBed

__author__ = "jkanche, elgaml"
__copyright__ = "jkanche"
__license__ = "mit"

"""
    The file test.bigBed and test assertions 
    come from the pyBigWig library
"""

bb = BigBed("tests/test.bigBed")

def test_header():
    assert(bb.header == {'magic': 2273964779, 'version': 4, 'zoomLevels': 0, 'chromTreeOffset': 1066, 'fullDataOffset': 1180, 'fullIndexOffset': 1781, 'fieldCount': 9, 'definedFieldCount': 6, 'autoSqlOffset': 304, 'totalSummaryOffset': 962, 'uncompressBufSize': 16384})

def test_columns():
    assert(len(bb.columns) == 9)
    assert(bb.columns == ["chr", "start", "end", "name", "score", "strand", "level", "signif", "score2"])

def test_range():
    res, err = bb.getRange(chr="chr1", start=10000000, end=10020000)
    assert(err == None)
    assert(len(res) == 3)

def test_get_bytes():
    res = bb.get_bytes(1, 100)
    assert (len(res) == 100)
