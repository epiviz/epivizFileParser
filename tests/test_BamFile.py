# -*- coding: utf-8 -*-

import pytest
import os

import pandas as pd

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
    coverage, error = bb.getRange("chr10", 1, 100000000)
    assert(error == None)

    assert(len(bb.columns) == 4)
    assert(bb.columns == ["chr", "start", "end", "value"])
    assert(len(coverage) == 25)

    assert (coverage['value'].tolist() == [0, 1, 0, 1, 0, 1, 0,
            0, 1, 0, 0, 1, 2, 1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    assert (coverage['start'].tolist() == [10265460, 10265473, 10266155, 10266200, 10266296, 10266311, 10266332, 10266594, 10266646, 10266743, 10266857,
            10267044, 10267063, 10267104, 10267116, 10267117, 10267118, 10267119, 10267121, 10267122, 10267142, 10267224, 10267690, 10267691, 10268169])
    assert (coverage['end'].tolist() == [10265473, 10266155, 10266200, 10266296, 10266311, 10266332, 10266374, 10266646, 10266743, 10266808, 10267044,
            10267063, 10267104, 10267116, 10267117, 10267118, 10267119, 10267121, 10267122, 10267142, 10267224, 10267690, 10267691, 10268169, 10268186])


def test_input_error():
    res, error = bb.getRange("chr11", 1, 100000000)
    assert(res.empty)
    assert (error == "Invalid input. (chr, start, end)")

    res, error = bb.getRange("chr10", 7, 4)
    assert(res.empty)
    assert (error == "Invalid input. (chr, start, end)")


def test_empty():
    assert(len(bb.getRange("chr10", 4, 7)[0]) == 0)
