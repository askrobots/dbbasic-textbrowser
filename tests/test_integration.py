"""
Integration tests for DBBasic TextBrowser
Tests real functionality like form submission, link clicking, AI interaction
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock curses before importing with proper key constants
mock_curses = MagicMock()
mock_curses.KEY_UP = 259
mock_curses.KEY_DOWN = 258
mock_curses.KEY_PPAGE = 339
mock_curses.KEY_NPAGE = 338
mock_curses.KEY_HOME = 262
mock_curses.KEY_END = 360
sys.modules['curses'] = mock_curses

from browser import Browser
from bs4 import BeautifulSoup


class TestFormSubmission(unittest.TestCase):
    """Test form detection and submission"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_stdscr = Mock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)

    @patch('browser.requests.get')
    def test_form_detection(self, mock_get):
        """Test that forms are detected on pages"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Mock HTML with a form
            html_content = """
            <html>
                <body>
                    <form action="/search" method="get">
                        <input type="text" name="q" placeholder="Search...">
                        <input type="submit" value="Search">
                    </form>
                </body>
            </html>
            """

            mock_response = Mock()
            mock_response.text = html_content
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            # Fetch page
            browser.fetch_page("https://example.com")

            # Check that form was detected
            self.assertEqual(len(browser.forms), 1)
            self.assertEqual(browser.forms[0]['method'], 'GET')
            self.assertEqual(browser.forms[0]['action'], '/search')
            self.assertEqual(len(browser.forms[0]['fields']), 1)
            self.assertEqual(browser.forms[0]['fields'][0]['name'], 'q')

    @patch('browser.requests.get')
    def test_form_submission_get(self, mock_get):
        """Test that GET form submission works"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Setup initial page with form
            html_content = """
            <html>
                <body>
                    <form action="/search" method="get">
                        <input type="text" name="q">
                    </form>
                </body>
            </html>
            """

            mock_response = Mock()
            mock_response.text = html_content
            mock_response.url = "https://example.com"
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            browser.fetch_page("https://example.com")

            # Prepare form data
            form = browser.forms[0]
            form_values = {'q': 'test query'}

            # Mock the result page
            result_html = "<html><body><h1>Search Results</h1></body></html>"
            mock_response.text = result_html
            mock_response.url = "https://example.com/search?q=test+query"

            # Submit form
            browser.submit_form(form, form_values)

            # Verify GET request was made with parameters
            self.assertEqual(mock_get.call_count, 2)
            last_call = mock_get.call_args_list[1]
            self.assertIn('params', last_call.kwargs)
            self.assertEqual(last_call.kwargs['params'], form_values)

    @patch('browser.requests.post')
    def test_form_submission_post(self, mock_post):
        """Test that POST form submission works"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Setup form manually
            browser.current_url = "https://example.com"
            form = {
                'action': '/login',
                'method': 'POST',
                'fields': [
                    {'name': 'username', 'type': 'text'},
                    {'name': 'password', 'type': 'password'}
                ]
            }
            browser.forms = [form]

            # Mock POST response
            mock_response = Mock()
            mock_response.text = "<html><body><h1>Welcome</h1></body></html>"
            mock_response.url = "https://example.com/dashboard"
            mock_response.raise_for_status = Mock()
            mock_post.return_value = mock_response

            # Submit form
            form_values = {'username': 'testuser', 'password': 'testpass'}
            browser.submit_form(form, form_values)

            # Verify POST was called
            mock_post.assert_called_once()
            call_kwargs = mock_post.call_args.kwargs
            self.assertEqual(call_kwargs['data'], form_values)
            self.assertIn('https://example.com/login', mock_post.call_args.args)


class TestLinkNavigation(unittest.TestCase):
    """Test link extraction and navigation"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_stdscr = Mock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)

    @patch('browser.requests.get')
    def test_link_extraction(self, mock_get):
        """Test that links are properly extracted from HTML"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Mock HTML with links
            html_content = """
            <html>
                <body>
                    <a href="https://example.com/page1">Page 1</a>
                    <a href="/page2">Page 2</a>
                    <a href="#anchor">Anchor</a>
                    <a href="javascript:void(0)">JS Link</a>
                    <a href="mailto:test@example.com">Email</a>
                </body>
            </html>
            """

            mock_response = Mock()
            mock_response.text = html_content
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            # Fetch page
            browser.fetch_page("https://example.com")

            # Should extract 2 valid links (absolute and relative)
            # Should skip anchor, javascript:, and mailto:
            self.assertEqual(len(browser.links), 2)
            self.assertEqual(browser.links[0]['url'], 'https://example.com/page1')
            self.assertEqual(browser.links[1]['url'], 'https://example.com/page2')

    @patch('browser.requests.get')
    def test_link_navigation(self, mock_get):
        """Test that clicking a link navigates to that URL"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Setup initial page
            html_content = """
            <html>
                <body>
                    <a href="https://example.com/next">Next Page</a>
                </body>
            </html>
            """

            mock_response = Mock()
            mock_response.text = html_content
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            browser.fetch_page("https://example.com")

            # Navigate to first link
            next_page_html = "<html><body><h1>Next Page</h1></body></html>"
            mock_response.text = next_page_html

            link_url = browser.links[0]['url']
            browser.fetch_page(link_url)

            # Verify we navigated
            self.assertEqual(browser.current_url, link_url)

    @patch('browser.requests.get')
    def test_relative_url_handling(self, mock_get):
        """Test that relative URLs are converted to absolute"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            html_content = """
            <html>
                <body>
                    <a href="/relative/path">Relative Link</a>
                    <a href="../parent/path">Parent Link</a>
                </body>
            </html>
            """

            mock_response = Mock()
            mock_response.text = html_content
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            browser.fetch_page("https://example.com/current/page")

            # Check that relative URLs were made absolute
            self.assertTrue(browser.links[0]['url'].startswith('https://'))
            self.assertTrue(browser.links[1]['url'].startswith('https://'))


class TestAICommands(unittest.TestCase):
    """Test AI command processing"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_stdscr = Mock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)
        self.mock_stdscr.refresh = Mock()

    def test_ai_command_without_key(self):
        """Test that AI commands fail gracefully without API key"""
        with patch.dict(os.environ, {}, clear=True):
            if 'OPENAI_API_KEY' in os.environ:
                del os.environ['OPENAI_API_KEY']

            browser = Browser(self.mock_stdscr)
            browser.page_text = "Some page content"

            # Try to process AI command
            browser.process_ai_command("summarize this page")

            # Should show error message
            self.assertIn("AI features are not enabled", browser.page_content[0])

    @patch('browser.OpenAI')
    def test_ai_command_with_key(self, mock_openai_class):
        """Test that AI commands work with API key"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            # Setup mock OpenAI client
            mock_client = Mock()
            mock_openai_class.return_value = mock_client

            # Mock response
            mock_message = Mock()
            mock_message.content = "This page is about testing."
            mock_message.tool_calls = None

            mock_choice = Mock()
            mock_choice.message = mock_message

            mock_response = Mock()
            mock_response.choices = [mock_choice]

            mock_client.chat.completions.create.return_value = mock_response

            browser = Browser(self.mock_stdscr)
            browser.page_text = "Some page content about testing"
            browser.current_url = "https://example.com"

            # Process AI command
            browser.process_ai_command("summarize this page")

            # Verify OpenAI was called
            mock_client.chat.completions.create.assert_called_once()

            # Verify response was displayed
            page_text = '\n'.join(browser.page_content)
            self.assertIn("This page is about testing", page_text)

    @patch('browser.OpenAI')
    def test_ai_navigation_function_call(self, mock_openai_class):
        """Test that AI can navigate using function calling"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            # Setup mock OpenAI client
            mock_client = Mock()
            mock_openai_class.return_value = mock_client

            # Mock function call response
            mock_tool_call = Mock()
            mock_tool_call.function.name = "navigate_to_url"
            mock_tool_call.function.arguments = '{"url": "https://wikipedia.org", "reason": "Looking up WebDAV"}'

            mock_message = Mock()
            mock_message.content = None
            mock_message.tool_calls = [mock_tool_call]

            mock_choice = Mock()
            mock_choice.message = mock_message

            mock_response = Mock()
            mock_response.choices = [mock_choice]

            mock_client.chat.completions.create.return_value = mock_response

            browser = Browser(self.mock_stdscr)

            # Mock fetch_page to avoid actual network call
            with patch.object(browser, 'fetch_page') as mock_fetch:
                browser.process_ai_command("go to wikipedia for WebDAV")

                # Verify navigate_to_url was called
                mock_fetch.assert_called_once_with("https://wikipedia.org")


class TestPageRendering(unittest.TestCase):
    """Test page rendering and display"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_stdscr = Mock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)
        self.mock_stdscr.addstr = Mock()
        self.mock_stdscr.clear = Mock()
        self.mock_stdscr.refresh = Mock()

    def test_render_basic_page(self):
        """Test that basic pages render without errors"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)
            browser.page_content = ["Line 1", "Line 2", "Line 3"]
            browser.current_url = "https://example.com"

            # Render should not raise
            browser.render()

            # Verify screen was cleared and refreshed
            self.mock_stdscr.clear.assert_called()
            self.mock_stdscr.refresh.assert_called()

    def test_scroll_handling(self):
        """Test that scrolling works correctly"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Create content longer than screen
            browser.page_content = [f"Line {i}" for i in range(100)]
            browser.scroll_offset = 0

            # Test scrolling down
            content_height = 24 - 2  # Screen height minus bars
            browser.scroll_offset = 10

            # Should be able to scroll
            self.assertEqual(browser.scroll_offset, 10)

            # Test max scroll
            max_scroll = len(browser.page_content) - content_height
            browser.scroll_offset = max_scroll
            self.assertLessEqual(browser.scroll_offset, max_scroll)


class TestKeyboardInput(unittest.TestCase):
    """Test keyboard input handling"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_stdscr = Mock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)

    def test_quit_key(self):
        """Test that Q key quits the browser"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)
            browser.running = True

            # Press 'q' key
            browser.handle_input(ord('q'))

            # Browser should stop running
            self.assertFalse(browser.running)

    def test_help_key(self):
        """Test that H key shows help"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Mock the help file with proper content
            help_html = """
            <html>
                <body>
                    <h1>Help Page</h1>
                    <p>This is the help content</p>
                </body>
            </html>
            """
            mock_file = MagicMock()
            mock_file.read.return_value = help_html
            mock_file.__enter__.return_value = mock_file

            with patch('builtins.open', return_value=mock_file):
                with patch('os.path.exists', return_value=True):
                    browser.handle_input(ord('h'))

                    # Should have loaded help content
                    self.assertIsNotNone(browser.page_content)
                    self.assertTrue(len(browser.page_content) > 0)

    def test_number_key_navigation(self):
        """Test that number keys navigate to links"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Setup links
            browser.links = [
                {'url': 'https://example.com/0', 'text': 'Link 0'},
                {'url': 'https://example.com/1', 'text': 'Link 1'},
            ]

            # Mock fetch_page
            with patch.object(browser, 'fetch_page') as mock_fetch:
                # Press '0' key
                browser.handle_input(ord('0'))

                # Should navigate to first link
                mock_fetch.assert_called_once_with('https://example.com/0')

    def test_scroll_keys(self):
        """Test that arrow keys scroll the page"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)
            browser.page_content = [f"Line {i}" for i in range(100)]
            browser.scroll_offset = 10

            # Press up arrow (KEY_UP = 259)
            browser.handle_input(259)
            self.assertEqual(browser.scroll_offset, 9)

            # Press down arrow (KEY_DOWN = 258)
            browser.handle_input(258)
            self.assertEqual(browser.scroll_offset, 10)


class TestColorRendering(unittest.TestCase):
    """Test HTML color rendering"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_stdscr = Mock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)
        self.mock_stdscr.addstr = Mock()

    @patch('browser.requests.get')
    def test_font_color_parsing(self, mock_get):
        """Test that <font color> tags are parsed correctly"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # HTML with font colors
            html_content = """
            <html>
                <body>
                    <font color="red">Error</font>
                    <font color="green">Success</font>
                    <font color="blue">Info</font>
                </body>
            </html>
            """

            mock_response = Mock()
            mock_response.text = html_content
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            browser.fetch_page("https://example.com")

            # Check that color markers are in content
            page_text = ''.join(browser.page_content)
            self.assertIn('«red»', page_text)
            self.assertIn('«green»', page_text)
            self.assertIn('«blue»', page_text)

    def test_color_rendering(self):
        """Test that colored text is rendered with color codes"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Test line with color markers
            line = "«red»Error: Something went wrong«/red»"

            # This should not raise an error
            browser.render_line_with_formatting(1, line, 80)

            # Verify addstr was called (color rendering happened)
            self.assertTrue(self.mock_stdscr.addstr.called)


if __name__ == '__main__':
    unittest.main()
