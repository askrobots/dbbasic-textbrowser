# DBBasic TextBrowser - Quick Start Guide

**Welcome!** Get started in under 5 minutes.

---

## What is This?

**DBBasic TextBrowser** is a terminal-based web browser with AI assistance that demonstrates the "text-first web" philosophy.

**TextFirst.css** is a 13 KB CSS framework that makes semantic HTML beautiful without build processes or JavaScript dependencies.

---

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- requests
- beautifulsoup4
- html2text
- openai (optional, for AI features)
- pytest (for running tests)

### 2. Run the Browser

```bash
python browser.py
```

Or open a specific page:

```bash
python browser.py homepage.html
```

---

## Basic Controls

| Key | Action |
|-----|--------|
| `Number` | Click numbered link |
| `Up/Down` | Scroll page |
| `PgUp/PgDn` | Scroll page faster |
| `Home/End` | Jump to top/bottom |
| `Ctrl-K` | Enter URL |
| `Ctrl-B` | Go back |
| `Ctrl-F` | Submit form |
| `Ctrl-A` | AI assistant (if enabled) |
| `H` | Show help |
| `Q` | Quit |

---

## Features

### ✨ Text Browser Features
- ✅ Numbered link navigation
- ✅ Form support (GET/POST)
- ✅ Color support (16 colors)
- ✅ Local and remote pages
- ✅ Clean, readable output

### 🤖 AI Integration (Optional)
- ✅ ChatGPT integration
- ✅ Natural language commands
- ✅ Function calling for navigation
- ✅ Page summarization

### 🎨 TextFirst.css Features
- ✅ Works in text browsers
- ✅ Enhanced in graphical browsers
- ✅ Zero build process
- ✅ 13 KB total size
- ✅ Mobile-first responsive

---

## Quick Examples

### 1. View the Demo Page

**In DBBasic TextBrowser:**
```bash
python browser.py
# Press Ctrl-K
# Type: demo/index.html
```

**In Regular Browser:**
```bash
open demo/index.html
```

### 2. Browse a Website

```bash
python browser.py
# Press Ctrl-K
# Type: example.com
```

### 3. Use AI Assistant

```bash
python browser.py
# Navigate to any page
# Press Ctrl-A
# Type: "summarize this page"
# Or: "click the login link"
```

---

## Using TextFirst.css in Your Project

### Step 1: Add the CSS File

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Page</title>
    <link rel="stylesheet" href="textfirst.css">
</head>
```

### Step 2: Write Semantic HTML

```html
<body>
    <banner type="success">
        Welcome to my site!
    </banner>

    <article>
        <h1>My Article</h1>
        <p>
            This is <color name="success">good content</color>
            that works everywhere.
        </p>

        <box>
            <h2>Important Information</h2>
            <p>This box highlights key content.</p>
        </box>

        <menu type="numbered">
            <li><a href="/home">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/contact">Contact</a></li>
        </menu>
    </article>
</body>
</html>
```

### Step 3: That's It!

No build process. No webpack. No babel. No npm.

**Just works.**

---

## Supported HTML Tags

### New Semantic Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `<color name="...">` | Semantic colors | `<color name="error">Error</color>` |
| `<banner type="...">` | Alert banners | `<banner type="warning">Warning</banner>` |
| `<box style="...">` | Content boxes | `<box>Important info</box>` |
| `<status value="...">` | Status indicators | `<status value="online">Online</status>` |

### Enhanced Old Tags

| Tag | Example |
|-----|---------|
| `<font color="...">` | `<font color="red">Red text</font>` |
| `<center>` | `<center>Centered content</center>` |
| `<menu type="numbered">` | `<menu type="numbered"><li>Item</li></menu>` |

### Standard HTML5

All standard HTML5 tags work: `<article>`, `<section>`, `<aside>`, `<nav>`, `<header>`, `<footer>`, `<details>`, `<summary>`, etc.

---

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

**Expected output:**
```
======================== 28 passed in 0.57s ========================
```

### Run Specific Test

```bash
pytest tests/test_browser.py -v
pytest tests/test_integration.py -v
```

---

## Configuration

### Enable AI Features

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or in Python:

```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

### Customize Colors

Edit the `color_map` in `browser.py`:

```python
self.color_map = {
    'red': curses.COLOR_RED,
    'green': curses.COLOR_GREEN,
    # Add your custom colors
}
```

---

## Project Structure

```
dbbasic-textbrowser/
├── browser.py              # Main application
├── textfirst.css           # CSS framework (13 KB)
├── demo/
│   └── index.html          # Complete demo
├── tests/
│   ├── test_browser.py     # Unit tests (11)
│   └── test_integration.py # Integration tests (17)
└── docs/
    ├── TEXT-WEB-HTML.md    # HTML specification
    └── SEMANTIC-CSS-FRAMEWORK.md  # Philosophy
```

---

## Common Use Cases

### 1. SSH/Remote Terminal
Browse documentation from a remote server without leaving the terminal.

### 2. Accessibility Testing
Test your website in a text browser to ensure it's accessible.

### 3. Minimalist Browsing
Fast, distraction-free web browsing for reading articles.

### 4. Static Site Development
Build sites with TextFirst.css - no build process needed.

### 5. Learning Web Development
Teach HTML fundamentals without overwhelming with frameworks.

---

## Troubleshooting

### "Module not found: curses"

On Windows, install windows-curses:
```bash
pip install windows-curses
```

### "OpenAI API key not found"

AI features are optional. Either:
- Set `OPENAI_API_KEY` environment variable
- Or use browser without AI features (everything else works)

### "Tests failing"

Ensure all dependencies installed:
```bash
pip install -r requirements.txt
```

### "Page not rendering"

- Check file path is correct
- Try absolute path: `file:///full/path/to/file.html`
- For remote URLs, include `http://` or `https://`

---

## Philosophy in 3 Sentences

1. **HTML should work everywhere** - Text browsers, screen readers, curl, graphical browsers.
2. **CSS should enhance, not define** - Content first, styling second.
3. **JavaScript should be optional** - Static content doesn't need JS.

This is progressive enhancement done right.

---

## Learn More

- **[TEXT-WEB-HTML.md](TEXT-WEB-HTML.md)** - Semantic HTML tag specification
- **[SEMANTIC-CSS-FRAMEWORK.md](SEMANTIC-CSS-FRAMEWORK.md)** - Framework philosophy
- **[IT-JUST-WORKS.md](IT-JUST-WORKS.md)** - Why basic HTML/CSS is amazing
- **[USEIT-PARADOX.md](USEIT-PARADOX.md)** - Jakob Nielsen case study
- **[WEB-DESIGN-HISTORY.md](WEB-DESIGN-HISTORY.md)** - Web evolution 1995-2025
- **[PROJECT-STATUS.md](PROJECT-STATUS.md)** - Complete project status

---

## Real-World Example

Here's a complete working page using TextFirst.css:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server Status</title>
    <link rel="stylesheet" href="textfirst.css">
</head>
<body>

<article>
    <header>
        <center>
            <h1>Server Status Dashboard</h1>
            <p><color name="muted">Last updated: 2 minutes ago</color></p>
        </center>
    </header>

    <banner type="success">
        All systems operational
    </banner>

    <section>
        <h2>Services</h2>
        <dl>
            <dt>Web Server</dt>
            <dd><status value="online">Online</status> - 99.9% uptime</dd>

            <dt>Database</dt>
            <dd><status value="online">Online</status> - 50ms latency</dd>

            <dt>Cache</dt>
            <dd><status value="degraded">Degraded</status> - High memory usage</dd>
        </dl>
    </section>

    <box>
        <h3>Quick Links</h3>
        <menu type="numbered">
            <li><a href="/metrics">View Metrics</a></li>
            <li><a href="/logs">Check Logs</a></li>
            <li><a href="/alerts">Manage Alerts</a></li>
        </menu>
    </box>

    <footer>
        <hr>
        <center>
            <p><color name="muted">© 2025 Your Company</color></p>
        </center>
    </footer>
</article>

</body>
</html>
```

**Copy this, save as `status.html`, open in any browser. It just works.**

---

## Get Started Now

```bash
# Clone or download the project
cd dbbasic-textbrowser

# Install dependencies
pip install -r requirements.txt

# Run the browser
python browser.py

# Or run tests
pytest tests/ -v

# Or view demo
open demo/index.html
```

---

## Questions?

Check the documentation files for detailed information:

- New to text browsers? Read **IT-JUST-WORKS.md**
- Want to understand the philosophy? Read **SEMANTIC-CSS-FRAMEWORK.md**
- Need HTML tag reference? Read **TEXT-WEB-HTML.md**
- Curious about web history? Read **WEB-DESIGN-HISTORY.md**

---

**Welcome to the text-first web!**

*"Somehow you captured modern and classic balance. Looks good, easy to read, lightweight, basic enough to read and edit manually if needed."* - User feedback, 2025
