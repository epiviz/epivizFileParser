import pytest
import os

from efs_parser.S3HDF5File import S3HDF5File
u = S3HDF5File("http://dev.susumu.genomics.roche.com/hdf5")
def test_call_getMatrix_1():
    response = u.getMatrix('1:8', '1:6')
    if isinstance(response, list):
        row_cnt = len(response)
        col_cnt = len(response[0])
    assert (row_cnt == 7)
    assert (col_cnt == 5)

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

def test_call_getMatrix_4():
    response = u.getMatrix('1', '1')
    assert (isinstance(response, list) == False)

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

def test_call_getMatrix_7():
    response = u.getMatrix('[1,2,3,5,9]', '[1,7]')
    assert (response == 'error')

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