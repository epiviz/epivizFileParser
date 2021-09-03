# -*- coding: utf-8 -*-

import pytest
import os

from epivizFileParser import BamFile

__author__ = "jkanche, Victor"
__copyright__ = "jkanche"
__license__ = "mit"

"""
    The file test.bigBed and test assertions 
    come from the pyBigWig library
"""

bb = BamFile("tests/data/test.bam")


def test_res():
    res, err = bb.getRange("chr10", 1, 100000000)
    assert(err == None)
    assert(len(bb.columns) == 4)
    assert(bb.columns == ["chr", "start", "end", "value"])
    assert(len(res) == 8)


def test_ch_error():
    res, err = bb.getRange("chr11", 1, 100000000)
    assert(res == None)
    assert(err == "Didn't find chromId with the given name")


def test_range_error():
    res, err = bb.getRange("chr10", 1, 10000000)
    assert(res == None)
    assert(err == "No data in given range.")
