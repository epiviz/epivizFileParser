import pytest
import os
import pandas as pd
import json
import statistics
from epivizFileParser import BigWig
bb = BigWig("https://obj.umiacs.umd.edu/bigwig-files/39031.bigwig")

@pytest.mark.skip(reason="skip")
def test_case_1():
    data = []
    data.append(['chr1',1,10,5])
    data.append(['chr1',10,100,9])
    data.append(['chr1',100,200,20])
    data.append(['chr1',200,210,9])
    result = bb.simplify_data(data=data,result_type="mean")
    assert len(result)==1

    assert result[0]['start'] ==1 and result[0]['end']==210 and round(result[0]['score'],3)==10.750

    result = bb.simplify_data(data=data, result_type="weighted_mean")
    assert len(result) == 1

    assert result[0]['start'] == 1 and result[0]['end']==210 and round(result[0]['score'], 3) == 14.229

@pytest.mark.skip(reason="skip")
def test_case_2():
    data = []
    data.append(['chr1',1,10,5])
    data.append(['chr1',10,100,9])
    data.append(['chr1',120,200,20])
    data.append(['chr1',200,210,9])
    result = bb.simplify_data(data=data,result_type="mean")
    assert len(result) == 2
    assert result[0]['start'] == 1 and result[0]['end'] == 100 and round(result[0]['score'], 3) == 7.000
    assert result[1]['start'] == 120 and result[1]['end'] == 210 and round(result[1]['score'], 3) == 14.500
    result = bb.simplify_data(data=data, result_type="weighted_mean")
    assert len(result) == 2
    assert result[0]['start'] == 1 and result[0]['end'] == 100 and round(result[0]['score'], 3) == 8.690
    assert result[1]['start'] == 120 and result[1]['end'] == 210 and round(result[1]['score'], 3) == 18.890

@pytest.mark.skip(reason="skip")
def test_case_3():
    data = []
    data.append(['chr1',1,10,5])
    result = bb.simplify_data(data=data,result_type="mean")
    assert len(result) == 1
    assert result[0]['start'] == 1 and result[0]['end'] == 10 and round(result[0]['score'], 3) == 5.000
    result = bb.simplify_data(data=data, result_type="weighted_mean")
    assert len(result) == 1
    assert result[0]['start'] == 1 and result[0]['end'] == 10 and round(result[0]['score'], 3) == 5.000


def test_case_4():
    data = []
    data.append(['chr1',1,10,5])
    data.append(['chr1',11,100,9])
    data.append(['chr1',120,200,20])
    data.append(['chr1',201,210,9])
    result = bb.simplify_data(data=data,result_type="mean")
    assert len(result) == 4
    assert result[0]['start'] == 1 and result[0]['end'] == 10 and round(result[0]['score'], 3) == 5.000
    assert result[1]['start'] == 11 and result[1]['end'] == 100 and round(result[1]['score'], 3) == 9.000
    assert result[2]['start'] == 120 and result[2]['end'] == 200 and round(result[2]['score'], 3) == 20.000
    assert result[3]['start'] == 201 and result[3]['end'] == 210 and round(result[3]['score'], 3) == 9.000

    result = bb.simplify_data(data=data, result_type="weighted_mean")
    assert len(result) == 4
    assert result[0]['start'] == 1 and result[0]['end'] == 10 and round(result[0]['score'], 3) == 5.000
    assert result[1]['start'] == 11 and result[1]['end'] == 100 and round(result[1]['score'], 3) == 9.000
    assert result[2]['start'] == 120 and result[2]['end'] == 200 and round(result[2]['score'], 3) == 20.000
    assert result[3]['start'] == 201 and result[3]['end'] == 210 and round(result[3]['score'], 3) == 9.000

def test_case_5():
    data = []
    data.append(['chr1',1,10,5])
    data.append(['chr1',10,100,9])
    data.append(['chr1',100,200,20])
    data.append(['chr1',201,210,9])
    result = bb.simplify_data(data=data,result_type="mean")
    assert len(result) == 2
    assert result[0]['start'] == 1 and result[0]['end'] == 200 and round(result[0]['score'], 3) == 11.333
    assert result[1]['start'] == 201 and result[1]['end'] == 210 and round(result[1]['score'], 3) == 9.000

    result = bb.simplify_data(data=data, result_type="weighted_mean")
    assert len(result) == 2
    assert result[0]['start'] == 1 and result[0]['end'] == 200 and round(result[0]['score'], 3) == 14.445
    assert result[1]['start'] == 201 and result[1]['end'] == 210 and round(result[1]['score'], 3) == 9.000