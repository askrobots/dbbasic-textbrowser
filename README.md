# DBBasic TextBrowser

A text-mode web browser with AI assistance, inspired by Lynx. **Now with TextFirst.css** - a 13 KB CSS framework for the text-first web.

**Status:** ✅ Production ready with 28 passing tests, comprehensive documentation, and proper packaging.

## Unique Features

🎨 **World's First Color-Enabled Text Browser**
- Supports HTML `<font color>` tags (deprecated since HTML 4.01 but never implemented in text browsers!)
- Bridges 1980s BBS ANSI colors with 1990s HTML color tags
- See the colorful web that should have existed since 1997
- Try `demo.html` to see colored text in action

🤖 **AI-Powered Browsing**
- Natural language commands via Ctrl-K
- GPT-5 nano integration for page analysis, summarization, translation
- AI function calling for navigation ("go to wikipedia for X")
- Makes text browsing intelligent, not just fast

⌨️ **Keyboard-First Design**
- Numbered links (press 0-9 to follow instantly)
- Form support (press F to fill search boxes)
- No mouse needed, ever
- Faster than visual browsers for content sites

## Standard Features

- Text-based web browsing in your terminal
- Lynx user agent for compatibility
- Curated homepage of text-friendly sites
- Clean, readable text rendering with syntax highlighting
- Instant page loads (no JS/CSS/images)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python browser.py
```

### Controls

- **Ctrl-K** - Open address/AI command box
- **0-9** - Follow numbered links instantly
- **G** - Go to link by number (for links 10+)
- **F** - Fill out forms (search boxes, etc.)
- **H** - Show comprehensive help
- **↑ ↓** - Scroll up/down
- **PgUp/PgDn** - Scroll page up/down
- **Home/End** - Jump to top/bottom of page
- **Q** - Quit

### Getting Started

1. Start the browser: `python browser.py`
2. See the curated homepage with text-friendly sites
3. Try the color demo: Type `demo.html` in Ctrl-K box
4. Browse the web: DuckDuckGo, Wikipedia, Hacker News all work great
5. Use AI: After loading a page, press Ctrl-K and ask questions

## AI Features

The Ctrl-K box automatically detects whether you're entering a URL or an AI command.

To enable AI features, set your OpenAI API key:

```bash
export OPENAI_API_KEY=your-key-here
python browser.py
```

### Example AI Commands

After loading a page, press Ctrl-K and try:

- `summarize this page` - Get a concise summary
- `what are the main points?` - Extract key information
- `translate to spanish` - Translate content
- `explain this like I'm 5` - Simplify complex content
- `find pricing information` - Extract specific data
- `what is this article about?` - General comprehension
- Any natural language question about the page!

### How It Works

1. Load a page by pressing Ctrl-K and entering a URL (e.g., `example.com`)
2. Press Ctrl-K again and enter an AI command (e.g., `summarize this page`)
3. The browser sends the page content to OpenAI's API using **GPT-5 mini** (latest 2025 model)
4. The AI response is displayed in the browser

## What Makes This Special

### The Color Feature That Should Have Existed

In 1997, HTML 3.2 added `<font color="red">` tags. At the same time, every terminal supported ANSI color codes. But **no text browser ever combined them**.

DBBasic TextBrowser is the first to bridge this 28-year gap, creating the colorful text web that could have been.

### Why Text-First Matters

Modern websites load 5-10MB of JavaScript. DBBasic TextBrowser proves content sites work perfectly with:
- Zero JavaScript
- Instant loading
- Keyboard navigation
- Universal accessibility

Sites like Wikipedia, Hacker News, and DuckDuckGo work better here than in Chrome.

### AI Changes Everything

Text browsers were fast but dumb. DBBasic TextBrowser adds intelligence:
- Summarize pages instead of reading them
- Navigate with natural language
- Extract information on demand
- Translate content instantly

It's not just a browser - it's an intelligent agent for the web.

## TextFirst.css Framework

**New!** DBBasic TextBrowser comes with **TextFirst.css** - a semantic CSS framework that works in both text browsers AND graphical browsers.

### Philosophy

- **13 KB total** (vs Bootstrap 200KB, Tailwind 3MB)
- **Zero build process** - Just link the CSS file
- **Works everywhere** - Text browsers, screen readers, curl, graphical browsers
- **Semantic HTML** - Enhances meaning, doesn't hide it
- **Against the Tri-Hard Pattern** - No split across HTML/CSS/JS/build configs

### Quick Example

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="textfirst.css">
</head>
<body>
    <banner type="success">
        Welcome! This works in text browsers AND looks modern in Firefox/Safari.
    </banner>

    <article>
        <h1>My Page</h1>
        <p>Content with <color name="success">semantic colors</color></p>

        <box>
            <h2>Important Info</h2>
            <p>Boxed content with zero JavaScript</p>
        </box>
    </article>
</body>
</html>
```

### Demo

View the complete demo:
```bash
# In DBBasic TextBrowser
python browser.py demo/index.html

# In regular browser
open demo/index.html
```

See it work in **both** text mode and graphical mode!

## Documentation

This project includes comprehensive documentation:

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[PROJECT-STATUS.md](PROJECT-STATUS.md)** - Complete project overview
- **[TEXT-WEB-HTML.md](TEXT-WEB-HTML.md)** - Semantic HTML tag specification
- **[SEMANTIC-CSS-FRAMEWORK.md](SEMANTIC-CSS-FRAMEWORK.md)** - TextFirst.css philosophy
- **[IT-JUST-WORKS.md](IT-JUST-WORKS.md)** - Why basic HTML/CSS is remarkable
- **[USEIT-PARADOX.md](USEIT-PARADOX.md)** - Jakob Nielsen's site case study
- **[WEB-DESIGN-HISTORY.md](WEB-DESIGN-HISTORY.md)** - Web evolution 1995-2025
- **[MOBILE-WEB-HISTORY.md](MOBILE-WEB-HISTORY.md)** - Mobile web complexity cycle

## Testing

Comprehensive test suite with **28 tests, 100% passing**:

```bash
# Run all tests
pytest tests/ -v

# Expected output:
# ======================== 28 passed in 0.57s ========================
```

**Coverage includes:**
- Form submission (GET/POST)
- Link navigation
- AI integration
- Color rendering
- Keyboard controls
- Page parsing

See **[tests/README.md](tests/README.md)** for details.

## Packaging

Ready for distribution:

```bash
# Install from source
pip install -e .

# Build distribution
python setup.py sdist bdist_wheel

# Install dependencies
pip install -r requirements.txt
```

## Roadmap

### Completed ✅
- [x] Numbered link navigation
- [x] Form support
- [x] HTML font color support
- [x] AI integration with function calling
- [x] Curated homepage
- [x] Help system
- [x] Comprehensive test suite (28 tests)
- [x] TextFirst.css framework
- [x] Complete documentation
- [x] Packaging for distribution
- [x] MIT License

### Future Features
- [ ] History and back button
- [ ] Bookmarks manager
- [ ] Search within page (/)
- [ ] Download support
- [ ] Better table rendering
- [ ] Tab support
- [ ] Implement new semantic HTML tags in browser
- [ ] PyPI distribution
- [ ] TextFirst.css as standalone project

## License

MIT License - See [LICENSE](LICENSE) file for details.

Copyright (c) 2025 DBBasic TextBrowser

## Contributing

Contributions welcome! This project demonstrates:
- Text-first web design
- Progressive enhancement
- Accessibility-first development
- Simple over complex
- Fast over fancy

See documentation files for philosophy and design principles.

## Credits

**Philosophy inspired by:**
- Jakob Nielsen's original useit.com (the ugly but perfect one)
- Lynx browser
- The principle that HTML should work everywhere
- The belief that simple is better

**Against:**
- The Tri-Hard Pattern
- Build complexity for static content
- Framework lock-in
- "Modern" over usable

---

*"Somehow you captured modern and classic balance. Looks good, easy to read, lightweight, basic enough to read and edit manually if needed."* - User feedback, 2025

*"The funny thing is nngroup lost what made them special and an example and talking point of the web by 'fixing it'"* - On the importance of differentiation, 2025
