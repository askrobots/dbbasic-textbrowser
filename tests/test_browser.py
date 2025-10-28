"""
Unit tests for DBBasic TextBrowser
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path to import browser module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock curses before importing browser with proper key constants
mock_curses = MagicMock()
mock_curses.KEY_UP = 259
mock_curses.KEY_DOWN = 258
mock_curses.KEY_PPAGE = 339
mock_curses.KEY_NPAGE = 338
mock_curses.KEY_HOME = 262
mock_curses.KEY_END = 360
sys.modules['curses'] = mock_curses

from browser import Browser


class TestURLDetection(unittest.TestCase):
    """Test URL detection functionality"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a mock stdscr for Browser initialization
        self.mock_stdscr = Mock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)

    def test_valid_urls(self):
        """Test that valid URLs are correctly identified"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Test various URL formats
            self.assertTrue(browser.is_url("example.com"))
            self.assertTrue(browser.is_url("https://example.com"))
            self.assertTrue(browser.is_url("http://example.com"))
            self.assertTrue(browser.is_url("example.com/path"))
            self.assertTrue(browser.is_url("subdomain.example.com"))
            self.assertTrue(browser.is_url("example.co.uk"))

    def test_invalid_urls(self):
        """Test that non-URLs are correctly identified"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Test non-URL strings
            self.assertFalse(browser.is_url("summarize this page"))
            self.assertFalse(browser.is_url("what are the main points?"))
            self.assertFalse(browser.is_url("hello world"))
            self.assertFalse(browser.is_url("123"))


class TestColorMapping(unittest.TestCase):
    """Test color mapping functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_stdscr = Mock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)

    def test_color_map_exists(self):
        """Test that color map is properly initialized"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Check that basic colors are mapped
            self.assertIn('red', browser.color_map)
            self.assertIn('green', browser.color_map)
            self.assertIn('blue', browser.color_map)
            self.assertIn('yellow', browser.color_map)
            self.assertIn('cyan', browser.color_map)
            self.assertIn('magenta', browser.color_map)
            self.assertIn('white', browser.color_map)

    def test_extended_colors(self):
        """Test that extended colors are mapped to basic colors"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Check extended color mappings
            self.assertIn('orange', browser.color_map)
            self.assertIn('purple', browser.color_map)
            self.assertIn('gray', browser.color_map)
            self.assertIn('grey', browser.color_map)


class TestAIIntegration(unittest.TestCase):
    """Test AI integration functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_stdscr = Mock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)

    def test_ai_disabled_without_key(self):
        """Test that AI is disabled when no API key is set"""
        with patch.dict(os.environ, {}, clear=True):
            if 'OPENAI_API_KEY' in os.environ:
                del os.environ['OPENAI_API_KEY']
            browser = Browser(self.mock_stdscr)
            self.assertFalse(browser.ai_enabled)
            self.assertIsNone(browser.client)

    def test_ai_enabled_with_key(self):
        """Test that AI is enabled when API key is set"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            browser = Browser(self.mock_stdscr)
            self.assertTrue(browser.ai_enabled)
            self.assertIsNotNone(browser.client)


class TestBrowserInitialization(unittest.TestCase):
    """Test browser initialization"""

    def test_browser_initializes(self):
        """Test that browser initializes with default values"""
        mock_stdscr = Mock()
        mock_stdscr.getmaxyx.return_value = (24, 80)

        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(mock_stdscr)

            # Check initial state
            self.assertEqual(browser.current_url, "")
            self.assertEqual(browser.page_content, [])
            self.assertEqual(browser.page_text, "")
            self.assertEqual(browser.scroll_offset, 0)
            self.assertTrue(browser.running)
            self.assertEqual(browser.forms, [])
            self.assertEqual(browser.links, [])


class TestFormHandling(unittest.TestCase):
    """Test form handling functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_stdscr = Mock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)

    def test_no_forms_initially(self):
        """Test that browser starts with no forms"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)
            self.assertEqual(browser.forms, [])


class TestLinkHandling(unittest.TestCase):
    """Test link handling functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_stdscr = Mock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)

    def test_no_links_initially(self):
        """Test that browser starts with no links"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)
            self.assertEqual(browser.links, [])


class TestPageFetching(unittest.TestCase):
    """Test page fetching functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_stdscr = Mock()
        self.mock_stdscr.getmaxyx.return_value = (24, 80)

    @patch('browser.requests.get')
    def test_fetch_page_with_protocol(self, mock_get):
        """Test fetching a page with https protocol"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Mock response
            mock_response = Mock()
            mock_response.text = "<html><body><h1>Test Page</h1></body></html>"
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            # Fetch page
            result = browser.fetch_page("https://example.com")

            # Check that request was made
            mock_get.assert_called_once()
            self.assertTrue(result)

    @patch('browser.requests.get')
    def test_fetch_page_adds_protocol(self, mock_get):
        """Test that https:// is added to URLs without protocol"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': ''}):
            browser = Browser(self.mock_stdscr)

            # Mock response
            mock_response = Mock()
            mock_response.text = "<html><body><h1>Test Page</h1></body></html>"
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            # Fetch page without protocol
            browser.fetch_page("example.com")

            # Check that https:// was added
            call_args = mock_get.call_args
            self.assertTrue(call_args[0][0].startswith('https://'))


if __name__ == '__main__':
    unittest.main()
