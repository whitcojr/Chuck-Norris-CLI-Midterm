"""Command-line entrypoint for the Chuck Norris jokes CLI.

Provides three subcommands:
 - random [--category CATEGORY]
 - categories
 - search QUERY [--limit N]

Supports --verbose and --json global flags.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from src import api


def print_joke(j: dict[str, Any], verbose: bool = False, as_json: bool = False) -> None:
	if as_json:
		print(json.dumps(j, ensure_ascii=False, indent=2))
		return

	if verbose:
		parts = [f"ID: {j.get('id')}", f"URL: {j.get('url')}"]
		cats = j.get("categories")
		if cats:
			parts.append(f"Categories: {', '.join(cats)}")
		parts.append("")
		print("\n".join(parts))

	print(j.get("value", "(no joke returned)"))


def handle_random(args: argparse.Namespace) -> int:
	try:
		joke = api.get_random_joke(category=args.category)
	except Exception as e:  # requests exceptions or others
		print(f"Error: failed to fetch random joke - {e}", file=sys.stderr)
		return 2

	print_joke(joke, verbose=args.verbose, as_json=args.json)
	return 0


def handle_categories(args: argparse.Namespace) -> int:
	try:
		cats = api.get_categories()
	except Exception as e:
		print(f"Error: failed to fetch categories - {e}", file=sys.stderr)
		return 2

	if args.json:
		print(json.dumps(cats, ensure_ascii=False, indent=2))
	else:
		for c in cats:
			print(c)
	return 0


def handle_search(args: argparse.Namespace) -> int:
	query = args.query
	if not query or not query.strip():
		print("Error: search query cannot be empty", file=sys.stderr)
		return 2

	try:
		data = api.search_jokes(query=query, limit=args.limit)
	except Exception as e:
		print(f"Error: failed to search jokes - {e}", file=sys.stderr)
		return 2

	results = data.get("result") if isinstance(data, dict) else None
	if args.json:
		print(json.dumps(data, ensure_ascii=False, indent=2))
		return 0

	if not results:
		print("No jokes found.")
		return 0

	for idx, item in enumerate(results, start=1):
		print(f"{idx}. {item.get('value')}")
		if args.verbose:
			print(f"   id: {item.get('id')}")
			cats = item.get("categories")
			if cats:
				print(f"   categories: {', '.join(cats)}")
	return 0


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(prog="chuck", description="Chuck Norris jokes CLI")
	parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
	parser.add_argument("--json", action="store_true", help="Output JSON")

	sub = parser.add_subparsers(dest="command", required=True)

	p_random = sub.add_parser("random", help="Get a single random joke")
	p_random.add_argument("--category", "-c", help="Category to fetch a random joke from")
	p_random.set_defaults(func=handle_random)

	p_cats = sub.add_parser("categories", help="List available joke categories")
	p_cats.set_defaults(func=handle_categories)

	p_search = sub.add_parser("search", help="Search jokes by query")
	p_search.add_argument("query", help="Search query string")
	p_search.add_argument("--limit", "-n", type=int, default=10, help="Limit number of results")
	p_search.set_defaults(func=handle_search)

	return parser


def main(argv: list[str] | None = None) -> int:
	parser = build_parser()
	args = parser.parse_args(argv)

	# pass verbose/json flags to handlers via args
	try:
		return args.func(args)
	except AttributeError:
		parser.print_help()
		return 1


if __name__ == "__main__":
	raise SystemExit(main())

