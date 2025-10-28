#!/usr/bin/env python3
"""
DBBasic TextBrowser: A text-mode web browser with AI assistance
"""

import curses
import requests
from bs4 import BeautifulSoup
from typing import Optional
import html2text
import sys
import os
from openai import OpenAI
import re
import json


class Browser:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.current_url = ""
        self.page_content = []
        self.page_text = ""  # Raw text content for AI processing
        self.scroll_offset = 0
        self.running = True
        self.forms = []  # Store forms found on the page
        self.current_soup = None  # Store parsed HTML for form submission
        self.links = []  # Store numbered links from the page

        # Initialize OpenAI client if API key is available
        api_key = os.getenv('OPENAI_API_KEY')
        self.ai_enabled = bool(api_key)
        if self.ai_enabled:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None

        # Initialize colors
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)     # Status bar / cyan
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)    # Command box, links / green
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Help bar / yellow
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # Headings / magenta
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)    # Bold text / white
        curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)     # Secondary links / blue
        curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)      # Emphasis / red

        # Color name to curses color pair mapping
        self.color_map = {
            'red': 7,
            'green': 2,
            'blue': 6,
            'yellow': 3,
            'cyan': 1,
            'magenta': 4,
            'white': 5,
            'black': 0,  # Will need special handling
            # Extended colors (map to closest)
            'orange': 3,  # Yellow
            'purple': 4,  # Magenta
            'pink': 4,    # Magenta
            'brown': 3,   # Yellow
            'gray': 5,    # White
            'grey': 5,    # White
        }

        # Hide cursor
        curses.curs_set(0)

    def fetch_page(self, url: str) -> bool:
        """Fetch and parse a web page"""
        try:
            # Handle local file:// URLs or .html files
            if url.startswith('file://'):
                file_path = url.replace('file://', '')
                with open(file_path, 'r') as f:
                    html_content = f.read()
                soup = BeautifulSoup(html_content, 'html.parser')
            elif url.endswith('.html') and not url.startswith('http'):
                # Local file path
                import os
                file_path = os.path.join(os.path.dirname(__file__), url)
                with open(file_path, 'r') as f:
                    html_content = f.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                url = f"file://{file_path}"
            else:
                # Add https:// if no protocol specified
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url

                headers = {
                    'User-Agent': 'Lynx/2.9.0dev.6 libwww-FM/2.14 SSL-MM/1.4.1'
                }

                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                # Parse HTML to text
                soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Store soup for form handling
            self.current_soup = soup

            # Extract links with numbering
            self.links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and not href.startswith(('#', 'javascript:', 'mailto:')):
                    # Convert relative URLs to absolute
                    from urllib.parse import urljoin
                    abs_url = urljoin(url, href)
                    link_text = link.get_text(strip=True)
                    if link_text:  # Only add links with visible text
                        self.links.append({
                            'url': abs_url,
                            'text': link_text[:50]  # Truncate long link text
                        })

            # Extract forms
            self.forms = []
            for idx, form in enumerate(soup.find_all('form')):
                form_data = {
                    'index': idx,
                    'action': form.get('action', ''),
                    'method': form.get('method', 'get').upper(),
                    'fields': []
                }

                # Get all input fields
                for input_tag in form.find_all(['input', 'textarea']):
                    input_type = input_tag.get('type', 'text')
                    if input_type not in ['hidden', 'submit', 'button']:
                        form_data['fields'].append({
                            'name': input_tag.get('name', ''),
                            'type': input_type,
                            'placeholder': input_tag.get('placeholder', ''),
                            'value': input_tag.get('value', '')
                        })

                if form_data['fields']:  # Only add forms with visible fields
                    self.forms.append(form_data)

            # Get terminal width for wrapping
            try:
                height, width = self.stdscr.getmaxyx()
                wrap_width = width - 4  # Leave some margin
            except:
                wrap_width = 78  # Default fallback

            # Process font color tags before conversion
            for font_tag in soup.find_all('font'):
                color = font_tag.get('color', '').lower()
                if color and color in self.color_map:
                    # Wrap text with special markers that we can detect later
                    text = font_tag.get_text()
                    font_tag.string = f"«{color}»{text}«/{color}»"

            # Number the links in the HTML before conversion
            link_counter = 0
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and not href.startswith(('#', 'javascript:', 'mailto:')):
                    link_text = link.get_text(strip=True)
                    if link_text and link_counter < len(self.links):
                        # Add number before the link
                        link.string = f"[{link_counter}] {link_text}"
                        link_counter += 1

            # Convert to text using html2text for better formatting
            h = html2text.HTML2Text()
            h.ignore_links = True  # We're handling links ourselves
            h.ignore_images = True
            h.body_width = wrap_width  # Wrap to terminal width
            h.unicode_snob = True  # Use unicode characters
            h.mark_code = True  # Mark code blocks
            text = h.handle(str(soup))

            # Add links list at the end
            if self.links:
                text += "\n\n" + "=" * 60 + "\n"
                text += f"LINKS: {len(self.links)} link(s) found\n"
                text += "=" * 60 + "\n"
                text += "Type a number (0-{}) to follow a link\n\n".format(len(self.links) - 1)

                # Show first 20 links in the list
                for idx, link in enumerate(self.links[:20]):
                    text += f"[{idx}] {link['text']}\n"

                if len(self.links) > 20:
                    text += f"\n... and {len(self.links) - 20} more links (see inline numbers)\n"

            # Add form information to the display
            if self.forms:
                text += "\n\n" + "=" * 60 + "\n"
                text += f"FORMS DETECTED: {len(self.forms)} form(s) found\n"
                text += "=" * 60 + "\n"
                for idx, form in enumerate(self.forms):
                    text += f"\n[Form {idx}] {form['method']} → {form['action'] or '(same page)'}\n"
                    for field in form['fields']:
                        placeholder = f" ({field['placeholder']})" if field['placeholder'] else ""
                        text += f"  - {field['name']}: {field['type']}{placeholder}\n"
                text += f"\nPress 'F' to fill out a form\n"

            self.page_content = text.split('\n')
            self.page_text = text  # Store for AI processing

            # Detect if page is too empty (likely JS-heavy)
            content_lines = [line.strip() for line in self.page_content if line.strip()]
            if len(content_lines) < 10:
                self.page_content = [
                    "⚠️  JAVASCRIPT-HEAVY SITE DETECTED",
                    "",
                    f"URL: {url}",
                    "",
                    "This site appears to require JavaScript to display content.",
                    "Text browsers cannot execute JavaScript.",
                    "",
                    "Possible solutions:",
                    "",
                    "1. Ask AI for help (Ctrl-K):",
                    "   - 'find a text-friendly alternative to this site'",
                    "   - 'search for [topic] on a simpler site'",
                    "   - 'what is this site about?'",
                    "",
                    "2. Try alternative sites:",
                    "   - YouTube → Invidious instances (yewtu.be, inv.riverside.rocks)",
                    "   - Twitter → Nitter instances (nitter.net)",
                    "   - Reddit → old.reddit.com or teddit instances",
                    "   - Instagram → bibliogram instances",
                    "",
                    "3. Use yt-dlp for YouTube:",
                    "   - Command line tool to download/stream videos",
                    "",
                    "Press Ctrl-K to try a different site or ask AI for alternatives.",
                    "",
                    "=" * 60,
                    "",
                    "Raw content detected:",
                    ""
                ] + self.page_content[:50]  # Show first 50 lines for debugging

            self.current_url = url
            self.scroll_offset = 0

            return True

        except Exception as e:
            self.page_content = [
                f"Error loading page: {str(e)}",
                "",
                "Press Ctrl-K to enter a new URL"
            ]
            return False

    def is_url(self, text: str) -> bool:
        """Check if the input looks like a URL"""
        # Check for common URL patterns
        url_pattern = re.compile(
            r'^(https?://)?'  # Optional protocol
            r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # Domain
            r'(/.*)?$'  # Optional path
        )
        return bool(url_pattern.match(text.strip()))

    def process_ai_command(self, command: str):
        """Process an AI command on the current page"""
        if not self.ai_enabled:
            self.page_content = [
                "AI features are not enabled!",
                "",
                "To enable AI features, set your OpenAI API key:",
                "  export OPENAI_API_KEY=your-key-here",
                "",
                "Then restart the browser.",
                "",
                "Press Ctrl-K to continue browsing."
            ]
            self.scroll_offset = 0
            return

        # Allow AI commands even without a loaded page for navigation
        page_context = ""
        if self.page_text:
            # Truncate page content if too long (OpenAI has token limits)
            max_chars = 12000
            truncated_content = self.page_text[:max_chars]
            if len(self.page_text) > max_chars:
                truncated_content += "\n\n[Content truncated...]"
            page_context = f"Current page URL: {self.current_url}\n\nPage content:\n{truncated_content}\n\n"

        # Show loading message
        self.page_content = [
            f"AI Processing: {command}",
            "",
            "Please wait..."
        ]
        self.scroll_offset = 0
        self.render()

        try:
            # Define function tools for the AI
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "navigate_to_url",
                        "description": "Navigate the browser to a specific URL. Use this when the user wants to visit a website or when you need to look up information that requires visiting a specific page.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "url": {
                                    "type": "string",
                                    "description": "The full URL to navigate to (e.g., 'https://en.wikipedia.org/wiki/WebDAV')"
                                },
                                "reason": {
                                    "type": "string",
                                    "description": "Brief explanation of why navigating to this URL"
                                }
                            },
                            "required": ["url", "reason"]
                        }
                    }
                }
            ]

            # Call OpenAI API with function calling
            response = self.client.chat.completions.create(
                model="gpt-5-nano",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant for a text-mode web browser. You can navigate to URLs using the navigate_to_url function when appropriate. Provide clear, concise responses formatted for a terminal browser."
                    },
                    {
                        "role": "user",
                        "content": f"{page_context}User request: {command}"
                    }
                ],
                tools=tools,
                max_completion_tokens=2000
            )

            # Check if AI wants to call a function
            message = response.choices[0].message

            if message.tool_calls:
                # Handle function calls
                for tool_call in message.tool_calls:
                    if tool_call.function.name == "navigate_to_url":
                        args = json.loads(tool_call.function.arguments)
                        url = args.get("url")
                        reason = args.get("reason", "AI navigation")

                        # Show what we're doing
                        self.page_content = [
                            f"AI Action: Navigating to URL",
                            "",
                            f"Reason: {reason}",
                            f"URL: {url}",
                            "",
                            "Loading page..."
                        ]
                        self.scroll_offset = 0
                        self.render()

                        # Actually navigate
                        self.fetch_page(url)
                        return

            # No function call, just display the text response
            ai_response = message.content if message.content else "No response from AI."

            # Format the response
            result = [
                f"AI Response to: {command}",
            ]
            if self.current_url:
                result.append(f"Page: {self.current_url}")
            result.extend([
                "=" * 60,
                "",
            ])
            result.extend(ai_response.split('\n'))
            result.extend([
                "",
                "=" * 60,
                "Press Ctrl-K to enter a new command or URL"
            ])

            self.page_content = result
            self.scroll_offset = 0

        except Exception as e:
            self.page_content = [
                "AI Error!",
                "",
                f"Error: {str(e)}",
                "",
                "Press Ctrl-K to try again."
            ]
            self.scroll_offset = 0

    def show_help(self):
        """Load and display the help page"""
        import os
        help_path = os.path.join(os.path.dirname(__file__), 'help.html')

        if os.path.exists(help_path):
            # Load help file like a local page
            with open(help_path, 'r') as f:
                help_html = f.read()

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(help_html, 'html.parser')
            self.current_soup = soup
            self.current_url = f"file://{help_path}"

            # Extract links (though help page shouldn't have many)
            self.links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href:
                    link_text = link.get_text(strip=True)
                    if link_text:
                        self.links.append({
                            'url': href,
                            'text': link_text[:50]
                        })

            # Number the links
            link_counter = 0
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href:
                    link_text = link.get_text(strip=True)
                    if link_text and link_counter < len(self.links):
                        link.string = f"[{link_counter}] {link_text}"
                        link_counter += 1

            # Get terminal width
            try:
                height, width = self.stdscr.getmaxyx()
                wrap_width = width - 4
            except:
                wrap_width = 78

            # Convert to text
            import html2text
            h = html2text.HTML2Text()
            h.ignore_links = True
            h.ignore_images = True
            h.body_width = wrap_width
            h.unicode_snob = True
            text = h.handle(str(soup))

            self.page_content = text.split('\n')
            self.page_text = text
            self.forms = []  # Help page has no forms
            self.scroll_offset = 0
        else:
            # Fallback inline help
            self.page_content = [
                "DBBasic TextBrowser Help",
                "",
                "Keyboard Controls:",
                "  Ctrl-K    - Address/AI command box",
                "  0-9       - Follow numbered links",
                "  G         - Go to link by number",
                "  F         - Fill out forms",
                "  H         - Show this help",
                "  Q         - Quit",
                "",
                "AI Commands (Ctrl-K):",
                "  summarize this page",
                "  what are the main points?",
                "  go to wikipedia for [topic]",
                "  translate to [language]",
                "",
                "help.html not found - reinstall browser"
            ]
            self.links = []
            self.forms = []
            self.scroll_offset = 0

    def goto_link(self):
        """Go to a link by entering its number"""
        if not self.links:
            self.page_content = ["No links found on this page!"]
            self.scroll_offset = 0
            return

        height, width = self.stdscr.getmaxyx()

        # Create input window
        input_win = curses.newwin(5, width - 4, height // 2 - 2, 2)
        input_win.box()
        input_win.addstr(0, 2, " Go to Link ", curses.color_pair(2) | curses.A_BOLD)
        input_win.addstr(2, 2, f"Enter link number (0-{len(self.links)-1}): ")
        input_win.refresh()

        curses.echo()
        curses.curs_set(1)
        try:
            link_num_str = input_win.getstr(2, 40, 10).decode('utf-8')
            link_num = int(link_num_str)

            if 0 <= link_num < len(self.links):
                curses.noecho()
                curses.curs_set(0)
                self.fetch_page(self.links[link_num]['url'])
                return
        except:
            pass

        curses.noecho()
        curses.curs_set(0)

    def fill_form(self):
        """Interactive form filling"""
        if not self.forms:
            self.page_content = ["No forms found on this page!"]
            self.scroll_offset = 0
            return

        # If only one form, use it; otherwise ask which one
        if len(self.forms) == 1:
            form_idx = 0
        else:
            # Show form selection
            height, width = self.stdscr.getmaxyx()
            select_win = curses.newwin(len(self.forms) + 4, width - 4, 2, 2)
            select_win.box()
            select_win.addstr(0, 2, " Select Form ", curses.color_pair(2) | curses.A_BOLD)

            for idx, form in enumerate(self.forms):
                select_win.addstr(idx + 2, 2, f"{idx}: {form['method']} → {form['action'] or '(same page)'}"[:width-8])

            select_win.addstr(len(self.forms) + 2, 2, "Enter form number: ")
            select_win.refresh()

            curses.echo()
            curses.curs_set(1)
            try:
                form_idx = int(select_win.getstr().decode('utf-8'))
                if form_idx < 0 or form_idx >= len(self.forms):
                    raise ValueError()
            except:
                curses.noecho()
                curses.curs_set(0)
                return
            curses.noecho()
            curses.curs_set(0)

        # Fill out the selected form
        form = self.forms[form_idx]
        form_values = {}

        height, width = self.stdscr.getmaxyx()

        for field in form['fields']:
            # Create input window
            input_win = curses.newwin(5, width - 4, height // 2 - 2, 2)
            input_win.box()

            label = f" {field['name']} "
            if field['placeholder']:
                label += f"({field['placeholder']}) "
            input_win.addstr(0, 2, label[:width-8], curses.color_pair(2) | curses.A_BOLD)
            input_win.addstr(2, 2, f"Type: {field['type']}")
            input_win.addstr(3, 2, "Value: ")

            input_win.refresh()

            curses.echo()
            curses.curs_set(1)
            value = input_win.getstr(3, 9, width - 16).decode('utf-8')
            curses.noecho()
            curses.curs_set(0)

            if value:
                form_values[field['name']] = value

        # Submit the form
        self.submit_form(form, form_values)

    def submit_form(self, form, values):
        """Submit a form with the given values"""
        try:
            # Construct the target URL
            action = form['action']
            if not action:
                action = self.current_url
            elif not action.startswith('http'):
                # Relative URL
                from urllib.parse import urljoin
                action = urljoin(self.current_url, action)

            headers = {
                'User-Agent': 'Lynx/2.9.0dev.6 libwww-FM/2.14 SSL-MM/1.4.1'
            }

            # Show loading message
            self.page_content = ["Submitting form...", "", f"Target: {action}"]
            self.scroll_offset = 0
            self.render()

            # Submit based on method
            if form['method'] == 'POST':
                response = requests.post(action, data=values, headers=headers, timeout=10)
            else:  # GET
                response = requests.get(action, params=values, headers=headers, timeout=10)

            response.raise_for_status()

            # Parse the response
            soup = BeautifulSoup(response.text, 'html.parser')
            self.current_soup = soup

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get terminal width
            try:
                height, width = self.stdscr.getmaxyx()
                wrap_width = width - 4
            except:
                wrap_width = 78

            # Convert to text
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = True
            h.body_width = wrap_width
            h.unicode_snob = True
            h.mark_code = True
            text = h.handle(str(soup))

            self.page_content = text.split('\n')
            self.page_text = text
            self.current_url = response.url
            self.scroll_offset = 0

        except Exception as e:
            self.page_content = [
                "Form submission error!",
                "",
                f"Error: {str(e)}",
                "",
                "Press Ctrl-K to continue"
            ]
            self.scroll_offset = 0

    def show_command_box(self) -> Optional[str]:
        """Show the Ctrl-K command/address box"""
        height, width = self.stdscr.getmaxyx()

        # Create a window for input at the bottom
        input_win = curses.newwin(3, width - 4, height - 4, 2)
        input_win.box()
        input_win.addstr(0, 2, " Address / AI Command ", curses.color_pair(2) | curses.A_BOLD)

        # Enable cursor for input
        curses.curs_set(1)
        curses.echo()

        input_win.refresh()
        input_win.move(1, 2)

        # Get user input
        user_input = input_win.getstr(1, 2, width - 8).decode('utf-8')

        # Restore cursor state
        curses.noecho()
        curses.curs_set(0)

        return user_input.strip() if user_input else None

    def render_line_with_formatting(self, y: int, line: str, width: int):
        """Render a single line with markdown formatting and colors"""
        if not line:
            return

        x = 0
        line = line[:width]  # Truncate to screen width

        # Check for font color markers
        if '«' in line and '»' in line:
            # Line contains color markers, render with colors
            import re
            parts = re.split(r'(«[a-z]+»|«/[a-z]+»)', line)
            current_color = None

            for part in parts:
                if part.startswith('«') and part.endswith('»'):
                    color_name = part[1:-1]
                    if color_name.startswith('/'):
                        # End color tag
                        current_color = None
                    else:
                        # Start color tag
                        current_color = color_name
                else:
                    # Regular text, render with current color
                    if part and x < width:
                        try:
                            if current_color and current_color in self.color_map:
                                color_pair = self.color_map[current_color]
                                self.stdscr.addstr(y, x, part[:width-x], curses.color_pair(color_pair))
                            else:
                                self.stdscr.addstr(y, x, part[:width-x])
                            x += len(part)
                        except curses.error:
                            pass
            return

        # Detect heading lines (starting with #)
        if line.startswith('#'):
            try:
                self.stdscr.addstr(y, x, line, curses.color_pair(4) | curses.A_BOLD)
            except curses.error:
                pass
            return

        # Detect links [text](url)
        if '[' in line and '](' in line:
            try:
                self.stdscr.addstr(y, x, line, curses.color_pair(2))
            except curses.error:
                pass
            return

        # Detect bold text **text**
        if '**' in line:
            try:
                self.stdscr.addstr(y, x, line, curses.color_pair(5) | curses.A_BOLD)
            except curses.error:
                pass
            return

        # Detect emphasis _text_
        if line.startswith('_') or '_' in line:
            try:
                self.stdscr.addstr(y, x, line, curses.color_pair(7))
            except curses.error:
                pass
            return

        # Detect separator lines (===, ---, etc)
        if line.strip() and all(c in '=-_*' for c in line.strip()):
            try:
                self.stdscr.addstr(y, x, line, curses.color_pair(3))
            except curses.error:
                pass
            return

        # Regular text
        try:
            self.stdscr.addstr(y, x, line)
        except curses.error:
            pass

    def render(self):
        """Render the current page"""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        # Draw status bar at top
        status = f" DBBasic TextBrowser | {self.current_url or 'No page loaded'} "
        self.stdscr.addstr(0, 0, status[:width], curses.color_pair(1) | curses.A_BOLD)

        # Draw help bar at bottom
        link_hint = " | 0-9/G: Links" if self.links else ""
        form_hint = " | F: Form" if self.forms else ""
        help_text = f" Ctrl-K: URL/AI{link_hint}{form_hint} | H: Help | Q: Quit "
        self.stdscr.addstr(height - 1, 0, help_text[:width], curses.color_pair(3))

        # Render page content with formatting
        content_height = height - 2  # Minus status and help bars
        visible_lines = self.page_content[self.scroll_offset:self.scroll_offset + content_height]

        for i, line in enumerate(visible_lines):
            self.render_line_with_formatting(i + 1, line, width)

        # Show scroll indicator if needed
        if len(self.page_content) > content_height:
            scroll_pct = int((self.scroll_offset / len(self.page_content)) * 100)
            indicator = f" [{scroll_pct}%] "
            self.stdscr.addstr(height - 1, width - len(indicator) - 1, indicator, curses.color_pair(2))

        self.stdscr.refresh()

    def handle_input(self, key: int):
        """Handle keyboard input"""
        height, width = self.stdscr.getmaxyx()
        content_height = height - 2
        max_scroll = max(0, len(self.page_content) - content_height)

        # Ctrl-K: Show command box
        if key == 11:  # Ctrl-K
            command = self.show_command_box()
            if command:
                # Detect if input is a URL or AI command
                if self.is_url(command):
                    self.fetch_page(command)
                else:
                    # It's an AI command
                    self.process_ai_command(command)

        # F: Fill form
        elif key in (ord('f'), ord('F')):
            self.fill_form()

        # H: Show help
        elif key in (ord('h'), ord('H')):
            self.show_help()

        # G: Go to link by number
        elif key in (ord('g'), ord('G')):
            self.goto_link()

        # Number keys 0-9: Quick link access
        elif ord('0') <= key <= ord('9'):
            link_num = key - ord('0')
            if link_num < len(self.links):
                self.fetch_page(self.links[link_num]['url'])

        # Q: Quit
        elif key in (ord('q'), ord('Q')):
            self.running = False

        # Up arrow: Scroll up
        elif key == curses.KEY_UP:
            self.scroll_offset = max(0, self.scroll_offset - 1)

        # Down arrow: Scroll down
        elif key == curses.KEY_DOWN:
            self.scroll_offset = min(max_scroll, self.scroll_offset + 1)

        # Page Up
        elif key == curses.KEY_PPAGE:
            self.scroll_offset = max(0, self.scroll_offset - content_height)

        # Page Down
        elif key == curses.KEY_NPAGE:
            self.scroll_offset = min(max_scroll, self.scroll_offset + content_height)

        # Home
        elif key == curses.KEY_HOME:
            self.scroll_offset = 0

        # End
        elif key == curses.KEY_END:
            self.scroll_offset = max_scroll

    def run(self):
        """Main browser loop"""
        # Load homepage
        import os
        homepage_path = os.path.join(os.path.dirname(__file__), 'homepage.html')

        if os.path.exists(homepage_path):
            # Load local homepage
            with open(homepage_path, 'r') as f:
                homepage_html = f.read()

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(homepage_html, 'html.parser')
            self.current_soup = soup
            self.current_url = f"file://{homepage_path}"

            # Extract links
            self.links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href:
                    link_text = link.get_text(strip=True)
                    if link_text:
                        self.links.append({
                            'url': href,
                            'text': link_text[:50]
                        })

            # Number the links
            link_counter = 0
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href:
                    link_text = link.get_text(strip=True)
                    if link_text and link_counter < len(self.links):
                        link.string = f"[{link_counter}] {link_text}"
                        link_counter += 1

            # Get terminal width
            try:
                height, width = self.stdscr.getmaxyx()
                wrap_width = width - 4
            except:
                wrap_width = 78

            # Convert to text
            import html2text
            h = html2text.HTML2Text()
            h.ignore_links = True
            h.ignore_images = True
            h.body_width = wrap_width
            h.unicode_snob = True
            text = h.handle(str(soup))

            self.page_content = text.split('\n')
            self.page_text = text
        else:
            # Fallback to welcome message
            ai_status = "ENABLED" if self.ai_enabled else "DISABLED (set OPENAI_API_KEY to enable)"
            self.page_content = [
                "Welcome to DBBasic TextBrowser!",
                "",
                "A text-mode web browser with AI assistance.",
                f"AI Features: {ai_status}",
                "",
                "Press Ctrl-K to enter a URL or AI command.",
                "",
                "Controls:",
                "  Ctrl-K    - Open address/AI command box",
                "  0-9/G     - Follow numbered links",
                "  F         - Fill forms",
                "  ↑ ↓       - Scroll up/down",
                "  PgUp/PgDn - Scroll page up/down",
                "  Home/End  - Jump to top/bottom",
                "  Q         - Quit",
            ]

        while self.running:
            self.render()
            key = self.stdscr.getch()
            self.handle_input(key)


def main(stdscr):
    browser = Browser(stdscr)
    browser.run()


def cli():
    """Entry point for console script."""
    curses.wrapper(main)


if __name__ == '__main__':
    cli()
