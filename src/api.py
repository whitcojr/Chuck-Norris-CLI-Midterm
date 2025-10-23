"""API helper functions for the Chuck Norris CLI.

These functions wrap the chucknorris.io endpoints. They are small and
easy to mock in tests. Keep logic simple: fetch JSON and raise on
HTTP/network errors so the CLI can handle user-friendly messages.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List

import requests

BASE_URL = os.environ.get("CHUCK_API_BASE_URL", "https://api.chucknorris.io")
DEFAULT_TIMEOUT = int(os.environ.get("CHUCK_CLI_TIMEOUT", "10"))


class APIError(Exception):
	"""Raised when an API call fails or returns unexpected data.

	Attributes:
		message: Human-readable message
		original: Optional original exception instance
	"""

	def __init__(self, message: str, original: Exception | None = None) -> None:
		super().__init__(message)
		self.message = message
		self.original = original


def get_random_joke(category: str | None = None, timeout: int | None = None) -> Dict[str, Any]:
	"""Fetch a random joke from the API.

	This function handles common error cases and raises APIError for
	calling code to handle. Network and HTTP errors from `requests` are
	wrapped, JSON decode errors are handled, and the response is
	validated to contain expected fields.

	Raises:
		APIError: on network/HTTP/JSON/validation errors.
	"""
	url = f"{BASE_URL}/jokes/random"
	params = {"category": category} if category else {}
	try:
		resp = requests.get(url, params=params, timeout=timeout or DEFAULT_TIMEOUT)
		resp.raise_for_status()
	except requests.exceptions.Timeout as exc:
		raise APIError("Request timed out while fetching random joke", exc)
	except requests.exceptions.RequestException as exc:
		raise APIError(f"Network error while fetching random joke: {exc}", exc)

	# Parse JSON
	try:
		data = resp.json()
	except ValueError as exc:  # includes simplejson.errors.JSONDecodeError
		raise APIError("Invalid JSON received from API", exc)

	# Basic validation: the API should return a dict with a 'value' key
	if not isinstance(data, dict) or "value" not in data:
		raise APIError("API returned unexpected response shape")

	return data


def get_categories(timeout: int | None = None) -> List[str]:
	"""Return the list of joke categories."""
	url = f"{BASE_URL}/jokes/categories"
	resp = requests.get(url, timeout=timeout or DEFAULT_TIMEOUT)
	resp.raise_for_status()
	return resp.json()


def search_jokes(query: str, limit: int = 10, timeout: int | None = None) -> Dict[str, Any]:
	"""Search jokes by query. Returns the parsed JSON (with keys like 'total' and 'result')."""
	url = f"{BASE_URL}/jokes/search"
	params = {"query": query}
	resp = requests.get(url, params=params, timeout=timeout or DEFAULT_TIMEOUT)
	resp.raise_for_status()
	data = resp.json()
	# The API returns 'result' which can be larger than limit; trim client-side
	if isinstance(data, dict) and "result" in data and isinstance(data["result"], list):
		data["result"] = data["result"][:limit]
	return data
