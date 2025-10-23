import pytest
from unittest.mock import patch, MagicMock

from src import api


@patch('src.api.requests.get')
def test_get_random_joke_success(mock_get):
	mock_resp = MagicMock()
	mock_resp.raise_for_status.return_value = None
	mock_resp.json.return_value = {"id": "1", "value": "a joke"}
	mock_get.return_value = mock_resp

	result = api.get_random_joke()
	assert isinstance(result, dict)
	assert result["value"] == "a joke"


@patch('src.api.requests.get')
def test_get_random_joke_timeout(mock_get):
	# Simulate a timeout exception from requests
	mock_get.side_effect = api.requests.exceptions.Timeout("timeout")

	with pytest.raises(api.APIError) as excinfo:
		api.get_random_joke()
	assert "timed out" in str(excinfo.value).lower()


@patch('src.api.requests.get')
def test_get_random_joke_invalid_json(mock_get):
	mock_resp = MagicMock()
	mock_resp.raise_for_status.return_value = None
	# json() raises a ValueError when invalid
	mock_resp.json.side_effect = ValueError("invalid json")
	mock_get.return_value = mock_resp

	with pytest.raises(api.APIError) as excinfo:
		api.get_random_joke()
	assert "invalid json" in str(excinfo.value).lower()
