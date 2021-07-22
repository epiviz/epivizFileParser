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

bb = BigBed("https://obj.umiacs.umd.edu/bigwig-files/ENCFF330GHF.bigBed")

def test_correct_format():
    assert (bb.header['magic']==2273964779)

def test_header():
    assert(bb.header == {'magic': 2273964779, 'version': 4, 'zoomLevels': 10, 'chromTreeOffset': 953, 'fullDataOffset': 1275, 'fullIndexOffset': 142913985, 'fieldCount': 9, 'definedFieldCount': 9, 'autoSqlOffset': 304, 'totalSummaryOffset': 849, 'uncompressBufSize': 29537})

def test_columns():
    assert(len(bb.columns) == bb.header['fieldCount'])
    #assert(bb.columns == ['chr', 'start', 'end', 'name', 'score', 'strand', 'thickStart',7 'thickEnd', 'reserved'])

def test_range():
    start = 10000000
    end = 10020000
    res, err = bb.getRange(chr="chr1", start=start, end=end)
    assert(err == None)
    for _, row in res.iterrows():
        assert (row['start'] <= end or row['end'] >= start)

def test_get_bytes():
    res = bb.get_bytes(1, 100)
    assert (len(res) == 100)

def test_bin_rows():
    result, err = bb.getRange(chr="chr1", start=10000000, end=10010000, bins=2000, zoomlvl=-2)
    res, err = bb.bin_rows(data=result, chr="chr1", start=10000000, end=10010000, columns=['score'])
    assert (err == None)

def test_groupBy():
    res, err = bb.getRange(chr="chr1", start=10007800, end=10010200, bins=2000, zoomlvl=-2)
    print(res)
    result = bb.groupBy(res, column = "name")
    print(result)
    first_row = True
    valid = True
    for _, row in result.iterrows():
        if first_row:
            prev_name = row['name']
            prev_end = row['end']
            first_row = False
        else:
            # The name of the next row must be different
            if prev_name == row['name']:
                valid = False
                break
            # The start of the next row must be greater than or equal to the end of the previour record
            if row['start'] < prev_end:
                valid = False
                break
            prev_name = row['name']
            prev_end = row['end']

    assert (valid)