# -*- coding: utf-8 -*-

import os
import tempfile

import pytest

from app import app


@pytest.fixture
def client():
    client = app.test_client()
    yield client
