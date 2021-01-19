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
bb = BigWig("https://obj.umiacs.umd.edu/bigwig-files/39031.bigwig")
#bb = BigWig("https://obj.umiacs.umd.edu/bigwig-files/ENCFF330GHF.bigBed")

def test_correct_format():
    assert (bb.header['magic']==2291137574)

def test_header():
    assert(bb.header == {'magic': 2291137574, 'version': 4, 'zoomLevels': 10, 'chromTreeOffset': 344, 'fullDataOffset': 705, 'fullIndexOffset': 582485344, 'fieldCount': 0, 'definedFieldCount': 0, 'autoSqlOffset': 0, 'totalSummaryOffset': 304, 'uncompressBufSize': 32768})

def test_columns():
    #bb.header[fieldCount]==0
    assert(len(bb.columns) == bb.header[fieldCount])
    assert(bb.columns == ["chr", "start", "end", "score"])

def test_range():
    res, err = bb.getRange(chr="chr1", start=10000000, end=10020000)
    assert(err == None)
    assert(len(res) == 495)

def test_zoom_out_of_range():
    bw_res_100, bw_err_100 = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=100)
    bw_res__1, bw_err__1 = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=-1)
    assert (bw_err_100 == bw_err__1)
    assert (len(bw_res_100) == len(bw_res__1))

def test_zoom_minus_one():
    res, err = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=-1)
    assert (err == None)
    assert (len(res) == 2443)



def test_zoom_0():
    res, err = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=0)
    assert (err == None)
    assert (len(res) == 39063)

def test_zoom_1():
    res, err = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=1)
    assert (err == None)
    assert (len(res) == 9767)

def test_zoom_2():
    res, err = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=2)
    assert (err == None)
    assert (len(res) == 2443)

def test_zoom_3():
    res, err = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=3)
    assert (err == None)
    assert (len(res) == 611)

def test_zoom_4():
    res, err = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=4)
    assert (err == None)
    assert (len(res) == 153)

def test_zoom_5():
    res, err = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=5)
    assert (err == None)
    assert (len(res) == 39)

def test_zoom_6():
    res, err = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=6)
    assert (err == None)
    assert (len(res) == 11)

def test_zoom_7():
    res, err = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=7)
    assert (err == None)
    assert (len(res) == 3)

def test_zoom_8():
    res, err = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=8)
    assert (err == None)
    assert (len(res) == 1)

def test_zoom_9():
    res, err = bb.getRange(chr="chr1", start=10000000, end=30000000, bins=2000, zoomlvl=9)
    assert (err == None)
    assert (len(res) == 1)