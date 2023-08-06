import pytest
from cognite.seismic import CogniteSeismicClient


def test_error_if_no_api_key():
    with pytest.raises(ValueError):
        CogniteSeismicClient(api_key=None)


def test_ok_if_api_key():
    client = CogniteSeismicClient(api_key="SOME_API_KEY")
    assert client is not None
