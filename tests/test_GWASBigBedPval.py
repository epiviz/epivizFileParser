# -*- coding: utf-8 -*-

import pytest
import os

from epivizFileParser import GWASBigBedPval

__author__ = "jkanche, elgaml"
__copyright__ = "jkanche"
__license__ = "mit"

"""
    The file test.bigBed and test assertions 
    come from the pyBigWig library
"""

bb = GWASBigBedPval("http://hgdownload.soe.ucsc.edu/gbdb/hg38/snp/dbSnp153ClinVar.bb")

def test_header():
    assert(bb.header == {'magic': 2273964779, 'version': 4, 'zoomLevels': 10, 'chromTreeOffset': 2133, 'fullDataOffset': 8889, 'fullIndexOffset': 20362677, 'fieldCount': 17, 'definedFieldCount': 4, 'autoSqlOffset': 304, 'totalSummaryOffset': 2009, 'uncompressBufSize': 140463})

def test_columns():
    assert(len(bb.columns) == 17)
    assert(bb.columns == ['chr', 'start', 'end', 'name', 'ref', 'altCount', 'alts', 'shiftBases', 'freqSourceCount', 'minorAlleleFreq', 'majorAllele', 'minorAllele', 'maxFuncImpact', 'mnv,', 'ucscNotes', '_dataOffset', '_dataLen'])

def test_range():
    res, err = bb.getRange(chr="chr1", start=10000000, end=10020000)
    start = 1010000
    end   = 1050000
    res, err = bb.getRange(chr="chr1", start=start, end=end)
    assert (err == None)
    # assert(len(res) == 495)
    for i, value in res.iterrows():
        assert (res['start'][i] <= end or res['end'][i] >= start)


def test_get_bytes():
    res = bb.get_bytes(1, 100)
    assert (len(res) == 100)
