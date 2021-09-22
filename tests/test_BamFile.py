# -*- coding: utf-8 -*-

import pytest
import os

from epivizFileParser import BamFile

__author__ = "jkanche, alexanv8"
__copyright__ = "jkanche"
__license__ = "mit"

"""
    The file test.bigBed and test assertions
    come from the pyBigWig library
"""

bb = BamFile("tests/data/test.bam")


def test_getRange():
    res, error = bb.getRange("chr10", 1, 100000000)
    assert(error == None)
    assert(len(bb.columns) == 4)
    assert(bb.columns == ["chr", "start", "end", "value"])
    assert(len(res) == 8)


def test_input_error():
    res, error = bb.getRange("chr11", 1, 100000000)
    assert(res.empty)
    assert (error == "Invalid input. (chr, start, end)")

    res, error = bb.getRange("chr10", 7, 4)
    assert(res.empty)
    assert (error == "Invalid input. (chr, start, end)")


def test_empty():
    assert(len(bb.getRange("chr10", 4, 7)[0]) == 0)
