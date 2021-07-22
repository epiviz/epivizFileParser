# -*- coding: utf-8 -*-

import pytest
import os

from epivizFileParser.BigWig import BigWig

__author__ = "jkanche, elgaml"
__copyright__ = "jkanche"
__license__ = "mit"

"""
    The file test.bigBed and test assertions 
    come from the pyBigWig library
"""

bb = BigWig("https://obj.umiacs.umd.edu/bigwig-files/39031.bigwig")

def test_correct_format():
    assert (bb.header['magic']==2291137574)

def test_header():
    assert(bb.header == {'magic': 2291137574, 'version': 4, 'zoomLevels': 10, 'chromTreeOffset': 344, 'fullDataOffset': 705, 'fullIndexOffset': 582485344, 'fieldCount': 0, 'definedFieldCount': 0, 'autoSqlOffset': 0, 'totalSummaryOffset': 304, 'uncompressBufSize': 32768})

def test_columns():
    #bb.header[fieldCount]==0
    #assert(len(bb.columns) == bb.header['fieldCount'])
    assert(len(bb.columns) == 4)
    assert(bb.columns == ["chr", "start", "end", "score"])

def test_range():
    start = 10000000
    end = 10020000
    res, err = bb.getRange(chr="chr1", start=start, end=end)
    assert(err == None)
    for _, row in res.iterrows():
        assert (row['start'] <= end or row['end'] >= start)

def test_zoom_out_of_range():
    bw_res_100, bw_err_100 = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=100)
    bw_res__1, bw_err__1 = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=-1)
    assert (bw_err_100 == bw_err__1)
    assert (len(bw_res_100) == len(bw_res__1))

def test_zoom_levels():
    for l in range(-1,10):
        if l == 0:
            continue
        res, err = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=l)
        assert (err == None)
        if (l == -1):
            assert (len(res) == 2443)
        elif (l == 0):
            assert (len(res) == 39063)
        elif (l == 1):
            assert (len(res) == 9767)
        elif (l == 2):
            assert (len(res) == 2443)
        if (l == 3):
            assert (len(res) == 611)
        elif (l == 4):
            assert (len(res) == 153)
        elif (l == 5):
            assert (len(res) == 39)
        if (l == 6):
            assert (len(res) == 11)
        elif (l == 7):
            assert (len(res) == 3)
        elif (l == 8):
            assert (len(res) == 1)
        if (l == 9):
            assert (len(res) == 1)

def test_get_bytes():
    res = bb.get_bytes(1, 100)
    assert (len(res) == 100)

def test_bin_rows():
    start = 5000000
    end = 10020000
    res, err = bb.getRange(chr="chr1", start=start, end=end)
    v = bb.bin_rows(data=res, chr="chr1", start=start, end=end, columns=['score'], bins=10)
    assert (len(v[0]) == 10)

@pytest.mark.skip(reason="skip")
def test_simplified_bin_rows():
    start = 5000000
    end = 10020000

    v = bb.simplified_bin_rows(chr="chr1", start=start, end=end)
    assert (len(v[0]) == 1)