import pytest
import os
import pandas as pd

from prophetable import Prophetable

import logging

LOGGER = logging.getLogger(__name__)


@pytest.fixture
def data_dir():
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
    )


@pytest.fixture
def minimal_config_uri(data_dir):
    return os.path.join(data_dir, "config.minimal.json")


def test_split_s3_uri():
    from prophetable.prophetable import _split_s3_uri

    S3_URI = "s3://bucket/object/key"
    PARSED_TUPLE = ("s3", "bucket", "object/key")
    parsed_tuple = _split_s3_uri(S3_URI)

    assert parsed_tuple == PARSED_TUPLE


def test_get_timedelta_from_str(minimal_config_uri):
    TIME_DELTA = "365 days"
    p = Prophetable(config=minimal_config_uri)
    assert p._get_timedelta(TIME_DELTA) == TIME_DELTA


def test_get_timedelta_from_number(minimal_config_uri):
    TIME_DELTA_INT = 365
    TIME_DELTA = pd.Timedelta("365 days 00:00:00")
    p = Prophetable(config=minimal_config_uri)
    assert p._get_timedelta(TIME_DELTA) == TIME_DELTA
