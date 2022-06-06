#!/usr/bin/env python3
import os

import py
import pytest


def pytest_configure(config):
    pytest.dname = os.path.dirname(__file__)
    pytest.project = os.path.dirname(pytest.dname)
    pytest.cookie_template = py.path.local(pytest.dname).join(os.pardir)
