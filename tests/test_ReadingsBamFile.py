# -*- coding: utf-8 -*-

import pytest
import os

from epivizFileParser import ReadingsBamFile

__author__ = "jkanche, alexanv8"
__copyright__ = "jkanche"
__license__ = "mit"

"""
    The file test.bigBed and test assertions
    come from the pyBigWig library
"""

bb = ReadingsBamFile("tests/data/test.bam")


def test_getRange():
    reads, error = bb.getRange("chr10", 10265461, 10266657)
    assert(error == None)

    assert(len(bb.columns) == 4)
    assert(bb.columns == ["chr", "name", "start", "length"])
    assert(len(reads) == 4)

    assert (reads['name'].tolist() == ['973:285',
            '1198:1458', '2195:2352', '554:2315'])
    assert (reads['start'].tolist() == [
            10265460, 10266594, 10266600, 10266656])
    assert (reads['length'].tolist() == [914, 172, 186, 152])


def test_input_error():
    res, error = bb.getRange("chr11", 1, 100000000)
    assert(res.empty)
    assert (error == "Invalid input. (chr, start, end)")

    res, error = bb.getRange("chr10", 7, 4)
    assert(res.empty)
    assert (error == "Invalid input. (chr, start, end)")


def test_empty():
    assert(len(bb.getRange("chr10", 4, 7)[0]) == 0)


test_getRange()
test_input_error()
test_empty()
