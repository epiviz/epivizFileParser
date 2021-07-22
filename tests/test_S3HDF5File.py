import pytest
import os

from epivizFileParser.S3HDF5File import S3HDF5File

__author__ = "Hany Elgaml"
__copyright__ = "mit"
__license__ = "mit"

API_URL = ""
S3_URL = ""
u = S3HDF5File(API_URL, S3_URL)

@pytest.mark.skip(reason="no way of currently testing this")
def test_call_getMatrix_1():
    response = u.getMatrix('1:8', '1:6')
    if isinstance(response, list):
        row_cnt = len(response)
        col_cnt = len(response[0])
    assert (row_cnt == 7)
    assert (col_cnt == 5)

@pytest.mark.skip(reason="no way of currently testing this")
def test_call_getMatrix_2():
    response = u.getMatrix('1:8', '[1,2]')
    if isinstance(response, list):
        row_cnt = len(response)
        if isinstance(response[0], list):
            col_cnt = len(response[0])
        else:
            col_cnt = 1
    assert (row_cnt == 7)
    assert (col_cnt == 2)

@pytest.mark.skip(reason="no way of currently testing this")
def test_call_getMatrix_3():
    response = u.getMatrix('1:8', '1')
    if isinstance(response, list):
        row_cnt = len(response)
        if isinstance(response[0], list):
            col_cnt = len(response[0])
        else:
            col_cnt = 1
    assert (row_cnt == 7)
    assert (col_cnt == 1)

@pytest.mark.skip(reason="no way of currently testing this")
def test_call_getMatrix_4():
    response = u.getMatrix('1', '1')
    assert (isinstance(response, list) == False)

@pytest.mark.skip(reason="no way of currently testing this")
def test_call_getMatrix_5():
    response = u.getMatrix('[1,2,3,5,9]', '1')
    if isinstance(response, list):
        row_cnt = len(response)
        if isinstance(response[0], list):
            col_cnt = len(response[0])
        else:
            col_cnt = 1
    assert (row_cnt == 5)
    assert (col_cnt == 1)

@pytest.mark.skip(reason="no way of currently testing this")
def test_call_getMatrix_6():
    response = u.getMatrix('[1,2,3,5,9]', '1:7')
    if isinstance(response, list):
        row_cnt = len(response)
        if isinstance(response[0], list):
            col_cnt = len(response[0])
        else:
            col_cnt = 1
    assert (row_cnt == 5)
    assert (col_cnt == 6)

@pytest.mark.skip(reason="no way of currently testing this")
def test_call_getMatrix_7():
    response = u.getMatrix('[1,2,3,5,9]', '[1,7]')
    assert (response == 'error')

@pytest.mark.skip(reason="no way of currently testing this")
def test_call_getMatrix_8():
    response = u.getMatrix('1', '1:7')
    if isinstance(response, list):
        col_cnt = len(response)
        if isinstance(response[0], list):
            row_cnt = len(response[0])
        else:
            row_cnt = 1
    assert (row_cnt == 1)
    assert (col_cnt == 6)

@pytest.mark.skip(reason="no way of currently testing this")
def test_call_getMatrix_9():
    response = u.getMatrix('1', '[1,2,3]')
    if isinstance(response, list):
        col_cnt = len(response)
        if isinstance(response[0], list):
            row_cnt = len(response[0])
        else:
            row_cnt = 1
    assert (row_cnt == 1)
    assert (col_cnt == 3)
