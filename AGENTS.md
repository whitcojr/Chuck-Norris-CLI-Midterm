# Project Name: Chuck Norris Jokes CLI

## Overview

A command-line tool to fetch and display random Chuck Norris jokes from the chucknorris.io API.
Users can get single jokes, search for jokes by keyword, browse categories, and save favorites to a local file.

## API Integration

- **API:** Chuck Norris Jokes API
- **Base URL:** https://api.chucknorris.io
- **Key endpoints:**
  - `/jokes/random` - Get one random joke
  - `/jokes/random?category={category}` - Get a random joke from a specific category
  - `/jokes/categories` - Get list of all available categories
  - `/jokes/search?query={query}` - Search jokes by keyword
- **Data format:** JSON object with fields: `id`, `icon_url`, `url`, `value` (the joke text), and optional `categories`
- **Rate limiting:** None documented, but implement respectful delays
- **Authentication:** None required (free public API)

## CLI Commands

- `chuck random` - Get a single random joke
- `chuck random --category [category]` - Get a random joke from a specific category
- `chuck categories` - List all available joke categories
- `chuck search [query]` - Search for jokes containing the query string
- `chuck search [query] --limit [N]` - Limit search results (default: 10)

## Technical Stack

- Python 3.10+
- argparse for CLI argument parsing
- requests library for API calls
- pytest for testing with mocking
- Optional: rich library for enhanced terminal output

## Code Organization

- `src/main.py` - Entry point and argparse setup
- `src/api.py` - API interaction functions
- `src/utils.py` - Helper functions (output formatting, file operations)
- `tests/` - Test files with mocked API responses

## Architecture Decisions

### Separation of Concerns
- **CLI Layer** (`main.py`): Handles user input, argument parsing, and output display
- **API Layer** (`api.py`): All HTTP communication with the Chuck Norris API
- **Utils Layer** (`utils.py`): Formatting, file I/O, and helper functions
- **Models** (optional): Data classes for type safety if needed

### Why argparse?
- Standard library (no extra dependencies)
- Automatic help text generation
- Simple for basic CLI needs
- Easy to extend with new commands

### Why flat structure?
- Simple project with limited scope
- Easy navigation and maintenance
- Follows modern Python `src/` layout pattern
- Clear separation without over-engineering

### Error Handling Strategy
- Graceful API failures with user-friendly messages
- Network timeout handling (10-second default)
- Invalid input validation at CLI level
- HTTP error codes mapped to meaningful messages

### Design Patterns Used
- **Function-based approach**: Simple, testable, no unnecessary classes
- **Dependency injection**: API functions accept base URL for testing
- **Command pattern**: Each CLI command maps to a handler function
- **Single Responsibility**: Each function does one thing well

## Standards

- Use docstrings for all functions and classes
- Follow PEP 8 style guidelines
- Type hints for function signatures (Python 3.10+ syntax)
- Handle errors gracefully with try/except blocks
- Mock all API calls in tests (no real requests during testing)
- Keep functions small and focused (max 20-30 lines)
- Use meaningful variable names (no single-letter vars except loop counters)
- Constants in UPPER_CASE (e.g., `BASE_URL`, `DEFAULT_TIMEOUT`)

## Testing Requirements

- **Unit Tests**: Test each API function independently
- **Integration Tests**: Test CLI command parsing and execution
- **Mocking**: Use `requests-mock` or `unittest.mock` for HTTP requests
- **Coverage**: Aim for >80% code coverage
- **Test Data**: Store mock API responses in `tests/fixtures/`
- **Assertions**: Test both success and failure scenarios

## Error Handling Examples

```python
# Network errors
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.Timeout:
    print("Error: Request timed out. Please check your connection.")
    sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"Error: Failed to fetch data - {e}")
    sys.exit(1)

# Invalid user input
if not query or len(query.strip()) == 0:
    print("Error: Search query cannot be empty")
    sys.exit(1)
```

## Output Formatting

- **Simple text output** by default (joke text only)
- **Verbose mode** (`--verbose`): Show ID, URL, categories
- **JSON output** (`--json`): Machine-readable format
- **Color support**: Use ANSI colors or `rich` library for enhanced display
- **Pagination**: For search results with many matches

## File Operations

- Save favorites to `~/.chuck-cli/favorites.json`
- Create directory if it doesn't exist
- JSON format for easy parsing and editing
- Avoid duplicates when saving

## Environment Variables (Optional)

- `CHUCK_API_BASE_URL`: Override default API base URL (for testing)
- `CHUCK_CLI_TIMEOUT`: Custom timeout in seconds (default: 10)
- `CHUCK_CLI_CONFIG`: Path to config file

## Future Enhancements

- Interactive mode with arrow key navigation
- Daily joke with caching (same joke per day)
- Statistics about joke database
- Category-based joke of the day
- Export jokes to different formats (Markdown, HTML)
- Colorized output with `rich` or `colorama`
- Shell completion (bash/zsh)

## Dependencies Rationale

- **requests**: Industry standard for HTTP, simple API, well-tested
- **argparse**: Standard library, zero dependencies
- **pytest**: Most popular Python testing framework
- **requests-mock**: Clean way to mock HTTP requests in tests

## Code Style Examples

```python
# Good: Clear function with docstring and type hints
def get_random_joke(category: str | None = None) -> dict:
    """
    Fetch a random Chuck Norris joke from the API.
    
    Args:
        category: Optional category to filter jokes
        
    Returns:
        dict: JSON response with joke data
        
    Raises:
        requests.exceptions.RequestException: If API request fails
    """
    url = f"{BASE_URL}/jokes/random"
    params = {"category": category} if category else {}
    response = requests.get(url, params=params, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()

# Bad: No docstring, unclear naming, no error handling
def get(c=None):
    return requests.get(f"{BASE_URL}/jokes/random", params={"category": c}).json()
```

## Git Workflow

- Main branch: `main` (stable, deployable code)
- Feature branches: `feature/command-name` or `feature/description`
- Commit messages: Conventional commits format
  - `feat: add search command`
  - `fix: handle empty search results`
  - `docs: update README with examples`
  - `test: add tests for categories command`
  - `refactor: simplify error handling`
- PR reviews required before merging to main
- CI/CD runs tests automatically on all PRs

## Development Workflow

1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Install dev dependencies: `pip install pytest requests-mock`
5. Run tests: `pytest tests/`
6. Run CLI: `python -m src.main [command]`

## API Response Examples

### Random Joke
```json
{
  "icon_url": "https://api.chucknorris.io/img/avatar/chuck-norris.png",
  "id": "8tyLUHVUS2anFY7XL__-lQ",
  "url": "",
  "value": "Chuck Norris doesn't need a debugger, he just stares down the bug until the code confesses."
}
```

### Categories
```json
[
  "animal",
  "career",
  "celebrity",
  "dev",
  "explicit",
  "fashion",
  "food",
  "history",
  "money",
  "movie",
  "music",
  "political",
  "religion",
  "science",
  "sport",
  "travel"
]
```

### Search Results
```json
{
  "total": 3,
  "result": [
    {
      "categories": [],
      "icon_url": "https://api.chucknorris.io/img/avatar/chuck-norris.png",
      "id": "abc123",
      "url": "https://api.chucknorris.io/jokes/abc123",
      "value": "Chuck Norris can write code that writes itself."
    }
  ]
}
```

## Common Pitfalls to Avoid

1. **Don't hardcode values**: Use constants and configuration
2. **Don't ignore errors**: Always handle exceptions gracefully
3. **Don't make real API calls in tests**: Always mock external requests
4. **Don't parse JSON manually**: Use `response.json()` method
5. **Don't forget timeouts**: Always set timeout on requests
6. **Don't print stack traces to users**: Show friendly error messages
7. **Don't commit sensitive data**: Use `.gitignore` properly

## Performance Considerations

- Set reasonable timeouts (10 seconds default)
- Cache categories list (rarely changes)
- Implement request retry logic for transient failures
- Consider rate limiting if making many requests
- Use connection pooling for multiple requests

## Accessibility

- Support color-blind friendly output modes
- Provide plain text mode (no colors/formatting)
- Clear error messages without jargon
- Comprehensive help text for all commands
- Examples in help output

## Security Notes

- API is public, no authentication required
- No user data is collected or stored (except saved favorites locally)
- Validate all user inputs before processing
- Sanitize file paths when saving favorites
- Use HTTPS for all API calls (enforced by API)

## Documentation Requirements

- **README.md**: Installation, usage examples, features
- **AGENTS.md**: This file - context for AI assistants
- **Inline comments**: Explain complex logic, not obvious code
- **Docstrings**: All public functions and classes
- **CHANGELOG.md**: Track version changes and features
- **LICENSE**: MIT or Apache 2.0 recommended

## Version History

- v0.1.0: Initial implementation with basic commands
- v0.2.0: Add search functionality
- v0.3.0: Add category filtering
- v0.4.0: Add favorites/save feature (planned)

---

**Last Updated**: 2025-10-22
**Maintained By**: Project Team
**AI Assistant Note**: This file provides comprehensive context for understanding and contributing to the Chuck Norris Jokes CLI project. Follow these guidelines when generating or modifying code.