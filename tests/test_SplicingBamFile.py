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
    (coverage, junctions), error = bb.getRange("chr10", 1, 100000000)
    assert(error == None)

    assert(len(bb.columns) == 6)
    assert(bb.columns == ["chr", "region1_start", "region2_start",
                          "region1_end", "region2_end", "value"])
    assert(len(coverage) == 8)
    assert(len(junctions) == 14)

    assert (coverage['value'].tolist() == [0, 1, 0, 1, 0, 1, 2, 1])
    assert (coverage['start'].tolist() == [10265460, 10265473,
            10266332, 10266646, 10266743, 10267044, 10267063, 10267142])
    assert (coverage['end'].tolist() == [10265473, 10266332,
            10266646, 10266743, 10267044, 10267063, 10267142, 10268169])

    assert (junctions['value'].tolist() == [
            1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    assert (junctions['region2_start'].tolist() == [10266201, 10266312, 10266657, 10266723, 10266972,
            10266978, 10267047, 10266897, 10267023, 10267117, 10267120, 10267123, 10267225, 10267692])
    assert (junctions['region1_end'].tolist() == [10266155, 10266296, 10266641, 10266707, 10266961,
            10266972, 10267043, 10266881, 10267007, 10267104, 10267117, 10267121, 10267118, 10267690])


# same test as bam file (copy paste)
def test_input_error():
    (coverage, junctions), error = bb.getRange("chr11", 1, 100000000)
    assert(coverage.columns.values.tolist() ==
           ['chr', 'start', 'end', 'value'])
    assert(junctions.columns.values.tolist() ==
           ['chr', "region1_start", "region2_start", "region1_end", "region2_end", "value"])
    assert (coverage.empty)
    assert (junctions.empty)
    assert (error == "invalid contig `chr11`")

    (coverage, junctions), error = bb.getRange("chr10", 7, 4)
    assert(coverage.columns.values.tolist() ==
           ['chr', 'start', 'end', 'value'])
    assert(junctions.columns.values.tolist() ==
           ['chr', "region1_start", "region2_start", "region1_end", "region2_end", "value"])
    assert (coverage.empty)
    assert (junctions.empty)
    assert (error == "invalid coordinates: start (7) > stop (4)")


def test_empty():
    (coverage, junctions), error = bb.getRange("chr10", 4, 7)
    assert(error == None)
    assert(len(coverage) == 0)
    assert(len(junctions) == 0)
