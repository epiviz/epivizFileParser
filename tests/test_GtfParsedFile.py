# -*- coding: utf-8 -*-

import pytest
import os

from epivizFileParser.GtfParsedFile import GtfParsedFile

__author__ = "jkanche, elgaml"
__copyright__ = "jkanche"
__license__ = "mit"

bb = GtfParsedFile("https://raw.github.com/epiviz/efs-genomes/master/hg38/genes.tsv.gz")

def test_columns():
    assert (bb.columns==['chr', 'start', 'end', 'width', 'strand', 'geneid', 'exon_starts', 'exon_ends', 'gene'])

def test_range():
    start=11874
    end=944574
    res, err = bb.getRange('chr1', start, end)
    assert (len(res) == 33)
    for i in range(0,33):
        assert ((res['start'][i] >= start and res['start'][i] <= end) or (res['end'][i] >= start and res['end'][i] <= end))

def test_search_gene_max_results_greater_than_actual():
    sg = bb.search_gene('MIR6859-1',maxResults=10)
    assert (len(sg[0])==3)

def test_search_gene_max_results_less_than_actual():
    sg = bb.search_gene('MIR6859-1',maxResults=2)
    assert (len(sg[0])==2)

def test_search_gene_max_results_zero():
    sg = bb.search_gene('MIR6859-1',maxResults=0)
    assert (len(sg[0])==1)

def test_search_existing_gene():
    sg = bb.search_gene('MIR6859-1')
    assert (len(sg[0])==3)
    assert (sg[0][0]['chr']=='chr1')
    assert (sg[0][1]['chr']=='chr15')
    assert (sg[0][2]['chr']=='chr16')

def test_search_existing_gene_not_case_sensitive():
    sg = bb.search_gene('miR6859-1')
    assert (len(sg[0])==3)
    assert (sg[0][0]['chr']=='chr1')
    assert (sg[0][1]['chr']=='chr15')
    assert (sg[0][2]['chr']=='chr16')

def test_search_no_gene():
    sg = bb.search_gene('')
    assert (sg==None)

def test_search_wrong_gene():
    sg = bb.search_gene('ehugslskdjbfiuqe')
    assert (sg==([], None))