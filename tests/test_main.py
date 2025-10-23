import pytest
from unittest.mock import patch

from src import main

@patch('src.api.get_random_joke')
def test_main_random_success(mock_get, capsys):
	mock_get.return_value = {"id": "1", "value": "a funny joke"}
	rc = main.main(["random"])
	captured = capsys.readouterr()
	assert rc == 0
	assert "funny joke" in captured.out

def test_main_search_empty_query(capsys):
	# Passing empty string as query should produce an error exit code
	rc = main.main(["search", ""])  # argparse will accept empty but our handler rejects it
	captured = capsys.readouterr()
	assert rc == 2
	assert "search query cannot be empty" in captured.err.lower()
import pytest
from unittest.mock import patch

from src import main

@patch('src.api.get_random_joke')
def test_main_random_success(mock_get, capsys):
	mock_get.return_value = {"id": "1", "value": "a funny joke"}
	rc = main.main(["random"])
	captured = capsys.readouterr()
	assert rc == 0
	assert "funny joke" in captured.out

def test_main_search_empty_query(capsys):
	# Passing empty string as query should produce an error exit code
	rc = main.main(["search", ""])  # argparse will accept empty but our handler rejects it
	captured = capsys.readouterr()
	assert rc == 2
	assert "search query cannot be empty" in captured.err.lower()
