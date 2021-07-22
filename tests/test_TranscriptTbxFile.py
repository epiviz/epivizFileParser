# -*- coding: utf-8 -*-

import pytest
import os

from epivizFileParser.TranscriptTbxFile import TranscriptTbxFile

__author__ = "jkanche, elgaml"
__copyright__ = "jkanche"
__license__ = "mit"

pytest.skip("github actions doesn't allow downloading files, skipping this module entirely", allow_module_level=True)

ee = TranscriptTbxFile("https://raw.github.com/epiviz/efs-genomes/master/hg38/transcripts.tsv.bgz")

def test_columns():
    assert (ee.columns==['chr', 'start', 'end', 'strand', 'transcript_id', 'exon_starts', 'exon_ends', 'gene'])

def test_range():
    start = 11874
    end = 944574
    res, err  = ee.getRange('chr1',start,end)
    assert (len(res) == 46)
    st = res['start']
    en = res['end']
    for i in range(0, len(res)):
        range_start = int(st[i])
        range_end = int(en[i])
        assert ((range_start>= start and range_start <= end) or (range_end >= start and range_end <= end))

