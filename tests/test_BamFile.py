# -*- coding: utf-8 -*-

import pytest
import os

from epivizFileParser import BamFile
from epivizFileParser import SplicingBamFile

__author__ = "jkanche, alexanv8"
__copyright__ = "jkanche"
__license__ = "mit"

"""
    The file test.bigBed and test assertions 
    come from the pyBigWig library
"""

bb = BamFile("tests/data/test.bam")
bb2 = SplicingBamFile("tests/data/test.bam")


def test_res():
    res, err = bb.getRange("chr10", 1, 100000000)
    res2, err2 = bb2.getRange("chr10", 1, 100000000)

    assert(err == None)
    assert(err2 == None)

    assert(len(bb.columns) == 4)
    assert(len(bb2.columns) == 6)

    assert(bb.columns == ["chr", "start", "end", "value"])
    assert(bb2.columns == ["chr", "region1_start", "region2_start",
                           "region1_end", "region2_end", "value"])

    assert(len(res) == 8)
    assert(len(res2) == 14)


def test_ch_error():
    res, err = bb.getRange("chr11", 1, 100000000)
    res2, err2 = bb2.getRange("chr11", 1, 100000000)

    assert(res == None)
    assert(res2 == None)

    assert(err == "Didn't find chromId with the given name")
    assert(err2 == "Didn't find chromId with the given name")


def test_range_error():
    res, err = bb.getRange("chr10", 1, 10000000)
    res2, err2 = bb2.getRange("chr10", 1, 10000000)

    assert(res == None)
    assert(res2 == None)

    assert(err == "No data in given range.")
    assert(err2 == "No data in given range.")
