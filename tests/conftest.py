# -*- coding: utf-8 -*-

import os
import tempfile

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()
    yield client
