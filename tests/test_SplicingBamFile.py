# -*- coding: utf-8 -*-

import pytest
import os

from epivizFileParser import SplicingBamFile

__author__ = "jkanche, alexanv8"
__copyright__ = "jkanche"
__license__ = "mit"

"""
    The file test.bigBed and test assertions
    come from the pyBigWig library
"""

bb = SplicingBamFile("tests/data/test.bam")


def test_getRange():
    coverage, junctions = bb.getRange("chr10", 1, 100000000)

    assert(len(bb.columns) == 6)
    assert(bb.columns == ["chr", "region1_start", "region2_start",
                          "region1_end", "region2_end", "value"])
    assert(len(coverage) == 8)
    assert(len(junctions) == 14)


# same test as bam file (copy paste)
def test_input_error():
    with pytest.raises(Exception) as excinfo:
        bb.getRange("chr11", 1, 100000000)
    assert "Invalid input. (chr, start, end)" == str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        bb.getRange("chr10", 7, 4)
    assert "Invalid input. (chr, start, end)" == str(excinfo.value)


def test_empty():
    coverage, junctions = bb.getRange("chr10", 4, 7)
    assert(len(coverage) == 0)
    assert(len(junctions) == 0)
