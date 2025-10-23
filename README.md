# Chuck Norris Jokes CLI

[![Tests](https://github.com/username/chuck-norris-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/username/chuck-norris-cli/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A command-line interface for fetching and displaying Chuck Norris jokes from [chucknorris.io](https://api.chucknorris.io/). Get random jokes, search by keyword, browse categories, and more.

## Features

- 🎲 Get random Chuck Norris jokes
- 🔍 Search jokes by keyword
- 📂 Browse available joke categories
- 💾 JSON output support
- 🎨 Rich formatting options

## Installation

1. Ensure you have Python 3.10 or newer installed:
```bash
python --version
```

2. Clone this repository:
```bash
git clone https://github.com/username/chuck-norris-cli.git
cd chuck-norris-cli
```

3. Create and activate a virtual environment:
```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Unix/macOS
python -m venv .venv
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Get a Random Joke
```bash
python -m src.main random
```

### Get a Random Joke from a Category
```bash
python -m src.main random --category dev
```

### List Available Categories
```bash
python -m src.main categories
```

### Search Jokes
```bash
python -m src.main search "python"
python -m src.main search "debug" --limit 5
```

### Output Options
- Use `--verbose` or `-v` for detailed output:
  ```bash
  python -m src.main random --verbose
  ```
- Use `--json` for machine-readable JSON output:
  ```bash
  python -m src.main random --json
  ```

## Development

### Setting Up Development Environment

1. Clone and install development dependencies:
```bash
git clone https://github.com/username/chuck-norris-cli.git
cd chuck-norris-cli
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### Running Tests

Run the test suite:
```bash
pytest
```

Run with verbosity:
```bash
pytest -v
```

### Project Structure

- `src/main.py` - CLI entrypoint and argument parsing
- `src/api.py` - API interaction functions
- `src/models.py` - Data models and type hints
- `tests/` - Test suite

## Environment Variables

- `CHUCK_API_BASE_URL`: Override default API URL (default: https://api.chucknorris.io)
- `CHUCK_CLI_TIMEOUT`: Custom timeout in seconds (default: 10)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [chucknorris.io](https://api.chucknorris.io/) for providing the jokes API
- Chuck Norris for being Chuck Norris
