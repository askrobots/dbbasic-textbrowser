# DBBasic TextBrowser Tests

This directory contains comprehensive unit and integration tests for DBBasic TextBrowser.

## Running Tests

To run all tests:

```bash
pytest tests/ -v
```

To run specific test files:

```bash
pytest tests/test_browser.py -v
pytest tests/test_integration.py -v
```

To run tests with coverage:

```bash
pytest tests/ --cov=browser --cov-report=html
```

## Test Structure

### `test_browser.py` - Unit Tests (11 tests)
Basic unit tests for core functionality:
- **URL Detection**: Valid and invalid URL identification
- **Color Mapping**: Basic and extended color mapping
- **AI Integration**: API key handling, client initialization
- **Browser Initialization**: Default state verification
- **Form Handling**: Initial form state
- **Link Handling**: Initial link state
- **Page Fetching**: HTTP requests, protocol handling

### `test_integration.py` - Integration Tests (17 tests)
Comprehensive integration tests for real functionality:

**Form Submission (3 tests)**
- Form detection from HTML
- GET form submission with parameters
- POST form submission with data

**Link Navigation (3 tests)**
- Link extraction from HTML (filtering anchors, javascript:, mailto:)
- Link navigation and URL changes
- Relative URL to absolute URL conversion

**AI Commands (3 tests)**
- AI disabled without API key (graceful failure)
- AI command processing with API key
- AI function calling for navigation

**Page Rendering (2 tests)**
- Basic page rendering without errors
- Scroll position handling

**Keyboard Input (4 tests)**
- Quit key (Q) functionality
- Help key (H) functionality
- Number keys (0-9) for link navigation
- Arrow keys for scrolling

**Color Rendering (2 tests)**
- Font color tag parsing from HTML
- Colored text rendering with terminal color codes

## Writing New Tests

When adding new functionality to the browser, please add corresponding tests:

1. Create a new test class that inherits from `unittest.TestCase`
2. Use `setUp()` to initialize mock objects (especially `mock_stdscr`)
3. Test both success and failure cases
4. Use descriptive test method names starting with `test_`
5. Mock external dependencies (HTTP requests, OpenAI API, file I/O)

### Example Test Pattern

```python
def test_new_feature(self):
    """Test description"""
    with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
        browser = Browser(self.mock_stdscr)

        # Setup test data

        # Execute functionality

        # Assert expectations
        self.assertEqual(expected, actual)
```

## Test Coverage

Current test coverage: **28 tests, all passing** ✅

### Covered Areas:
- ✅ URL detection and validation
- ✅ Color mapping (basic and extended colors)
- ✅ AI integration (enabled/disabled states)
- ✅ Browser initialization
- ✅ Form detection and submission (GET/POST)
- ✅ Link extraction and navigation
- ✅ Relative URL handling
- ✅ AI command processing
- ✅ AI function calling
- ✅ Page rendering
- ✅ Scroll position management
- ✅ Keyboard input handling (quit, help, numbers, arrows)
- ✅ HTML color parsing and rendering

### Future Enhancement Areas:
- Configuration file loading
- History and back button functionality
- Bookmarks management
- Download handling
- Session restore
- Tab support
- Search within page
- Error recovery and retry logic
- Network timeout handling

## Test Statistics

- **Total Tests**: 28
- **Unit Tests**: 11
- **Integration Tests**: 17
- **Pass Rate**: 100%
- **Average Runtime**: ~0.5 seconds
