# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for parser.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

import pytest

def pytest_addoption(parser):
    parser.addoption("--run-remote",
        action="store_true",
        default=False,
        help="run tests requiring remote connection")

def pytest_configure(config):
    config.addinivalue_line("markers",
        "remote: this mark selects remote tests")

def pytest_runtest_setup(item):
    remote_markers = item.iter_markers(name="remote")
    has_remote_mark = len(list(remote_markers)) > 0
    if has_remote_mark:
        print(f"has remote: {item}")
        
    if not item.config.getoption("--run-remote") and has_remote_mark:
        pytest.skip("Test skipped because it requires a remote connection") 