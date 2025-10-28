# Text Web HTML: A Better HTML for Terminal Browsers

**Date:** 2025-01-28
**Status:** Proposed / Future Implementation

## The Problem

Modern HTML moved from semantic markup to generic containers styled by CSS. This makes content invisible to text browsers.

**Before (worked in text browsers):**
```html
<center>
  <font color="red" size="+2">
    <b>DANGER</b>
  </font>
</center>
```

**After (requires CSS, invisible in text):**
```html
<div class="alert alert-danger text-center">
  <span class="text-large font-weight-bold">DANGER</span>
</div>
```

The old way was immediately renderable. The new way is meaningless without CSS.

## Historical Tags That Were Great for Text Mode

### `<center>` - Simple Centering
```html
<center>Welcome to My Site</center>
```
- **Why it was great:** No CSS needed, perfect for centering ASCII art and headers
- **Modern replacement:** `<div style="text-align: center">` (requires CSS knowledge)
- **Text browser impact:** Could center text in terminal width

### `<font color>` - Direct Color Control
```html
<font color="red">ERROR:</font> File not found
<font color="green">SUCCESS:</font> Operation complete
```
- **Why it was great:** Mapped perfectly to terminal colors
- **Modern replacement:** `<span style="color: red">` (requires CSS)
- **DBBasic TextBrowser:** Already implements this! First text browser to do so since 1997

### `<menu>` - Semantic Menus
```html
<menu>
  <li>Option 1</li>
  <li>Option 2</li>
  <li>Option 3</li>
</menu>
```
- **Why it was great:** Clearly indicated navigation options
- **Could have been:** Auto-numbered for keyboard navigation
- **Modern replacement:** Generic `<ul>` or `<nav><ul>`

### `<blink>` and `<marquee>` - Animation
```html
<blink>IMPORTANT!</blink>
<marquee>Scrolling text</marquee>
```
- **Why they were terrible:** Annoying in graphical browsers
- **Text browser potential:** Could use ANSI escape codes for blinking/scrolling
- **Modern replacement:** CSS animations (doesn't work in text mode)

## Tags That Work Great in Text Mode Today

### Semantic HTML5 Tags
```html
<article>
  <header>
    <h1>Article Title</h1>
    <time>2025-01-28</time>
  </header>

  <section>
    <h2>Section 1</h2>
    <p>Content...</p>
  </section>

  <aside>
    Note: Related information
  </aside>

  <footer>
    Author: John Doe
  </footer>
</article>
```
**Benefits for text browsers:**
- Provides structure for formatting (indentation, spacing)
- Can add visual separators between sections
- `<aside>` can be indented or marked with `│` characters
- `<footer>` can be visually separated with lines

### `<details>` and `<summary>` - Collapsible Content
```html
<details>
  <summary>Click to expand technical details</summary>
  <p>Hidden content here that can be shown on demand</p>
  <pre><code>
    Code examples
    More details
  </code></pre>
</details>
```
**Text browser rendering:**
```
[+] Click to expand technical details

# When expanded:
[-] Click to expand technical details
    Hidden content here that can be shown on demand

    Code examples
    More details
```
**Implementation:** Press number or key to toggle expansion

### `<dl>`, `<dt>`, `<dd>` - Definition Lists
```html
<dl>
  <dt>API Key</dt>
  <dd>A unique identifier for authentication</dd>

  <dt>Endpoint</dt>
  <dd>A specific URL that accepts requests</dd>
</dl>
```
**Text browser rendering:**
```
API Key
    A unique identifier for authentication

Endpoint
    A specific URL that accepts requests
```
**Benefits:** Natural indentation, clear structure

### `<pre>` and `<code>` - Preformatted Content
```html
<pre>
  ┌─────────────┐
  │  ASCII Art  │
  └─────────────┘
</pre>

<code>function example() { return 42; }</code>
```
**Benefits:**
- Preserves spacing and formatting
- Perfect for terminal output, code, ASCII art
- Could apply syntax highlighting via colors

### `<blockquote>` - Quotations
```html
<blockquote>
  The best way to predict the future is to invent it.
  <footer>— Alan Kay</footer>
</blockquote>
```
**Text browser rendering:**
```
│ The best way to predict the future is to invent it.
│ — Alan Kay
```
**Benefits:** Visual indication via `│` characters or indentation

## Tags That DON'T Work in Text Mode

### Generic Containers: `<div>` and `<span>`
```html
<div class="error-message">Error occurred</div>
<span class="badge badge-danger">ALERT</span>
```
**Problem:** Zero semantic meaning without CSS classes
**Solution:** Use semantic tags or proposed `<color>` tag

### CSS Grid/Flexbox Layouts
```html
<div class="container">
  <div class="row">
    <div class="col-md-4">Column 1</div>
    <div class="col-md-4">Column 2</div>
    <div class="col-md-4">Column 3</div>
  </div>
</div>
```
**Problem:** Entire layout disappears in text mode
**Solution:** Use semantic HTML5 sections instead

### `<canvas>` and SVG Graphics
```html
<canvas id="chart"></canvas>
<svg>...</svg>
```
**Problem:** Cannot render graphics in text mode
**Possible solution:** Provide text fallback or ASCII art representation

## Proposed New Tags for Text-First HTML

### 1. `<box>` - ASCII Box Drawing
```html
<box style="single">Content in a single-line box</box>
<box style="double">Content in a double-line box</box>
<box style="rounded">Content in a rounded box</box>
<box style="bold">Content in a bold box</box>
```

**Rendering:**
```
Single:
┌─────────────────────────┐
│ Content in a box        │
└─────────────────────────┘

Double:
╔═════════════════════════╗
║ Content in a box        ║
╚═════════════════════════╝

Rounded:
╭─────────────────────────╮
│ Content in a box        │
╰─────────────────────────╯

Bold:
┏━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Content in a box        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Use cases:**
- Important notices
- Menu boxes
- Code output
- ASCII art containers

### 2. `<color>` - Semantic Color Names
```html
<color name="error">Critical failure</color>
<color name="success">Operation successful</color>
<color name="warning">Proceed with caution</color>
<color name="info">For your information</color>
<color name="muted">Less important text</color>
<color name="highlight">Important highlight</color>
```

**Benefits:**
- Semantic meaning (error/success/warning/info)
- Terminal can map to appropriate colors automatically
- Better than `<font color="red">` because it's meaningful
- Different terminals can use different color schemes

**Color mapping:**
```
error    → red (or user's error color preference)
success  → green
warning  → yellow
info     → cyan/blue
muted    → gray/dim
highlight→ bright white or inverse
```

### 3. `<menu type="numbered">` - Interactive Menus
```html
<menu type="numbered">
  <li><a href="/home">Home</a></li>
  <li><a href="/about">About</a></li>
  <li><a href="/contact">Contact</a></li>
  <li><a href="/help">Help</a></li>
</menu>
```

**Rendering:**
```
[0] Home
[1] About
[2] Contact
[3] Help
```

**Benefits:**
- Automatic numbering for keyboard navigation
- Browser knows these are navigation options
- Perfect for text browser numbered link system
- Could also support `type="lettered"` for A, B, C...

### 4. `<tree>` - Hierarchical Tree Structures
```html
<tree>
  <branch>Root Directory
    <branch>Documents
      <branch>2025
        <branch>January</branch>
        <branch>February</branch>
      </branch>
    </branch>
    <branch>Pictures
      <branch>Vacation</branch>
      <branch>Family</branch>
    </branch>
  </branch>
</tree>
```

**Rendering:**
```
└─ Root Directory
   ├─ Documents
   │  └─ 2025
   │     ├─ January
   │     └─ February
   └─ Pictures
      ├─ Vacation
      └─ Family
```

**Use cases:**
- File system hierarchies
- Organization charts
- Navigation structures
- Dependency trees

### 5. Enhanced `<progress>` - Better Text Fallback
```html
<progress value="70" max="100" label="Download">70%</progress>
<progress value="30" max="100" style="bar">30%</progress>
<progress value="90" max="100" style="dots">90%</progress>
```

**Rendering:**
```
Download: [████████████████░░░░] 70%

[██████░░░░░░░░░░░░░░] 30%

[●●●●●●●●●●●●●●●●●●○○] 90%
```

**Benefits:**
- Visual progress indication in text
- Multiple styles (bar, dots, blocks)
- Works without JavaScript

### 6. `<banner>` - Important Announcements
```html
<banner type="info">
  System maintenance scheduled for tonight at 10 PM
</banner>

<banner type="warning">
  Your session will expire in 5 minutes
</banner>

<banner type="error">
  Connection lost. Attempting to reconnect...
</banner>
```

**Rendering:**
```
╔════════════════════════════════════════════╗
║ ℹ System maintenance scheduled for tonight  ║
║   at 10 PM                                  ║
╚════════════════════════════════════════════╝

╔════════════════════════════════════════════╗
║ ⚠ Your session will expire in 5 minutes    ║
╚════════════════════════════════════════════╝

╔════════════════════════════════════════════╗
║ ✗ Connection lost. Attempting to reconnect ║
╚════════════════════════════════════════════╝
```

**Benefits:**
- Highly visible notifications
- Semantic types (info/warning/error/success)
- Could use colors + borders + icons

### 7. `<table simple>` - Text-Optimized Tables
```html
<table simple>
  <thead>
    <tr>
      <th>Name</th>
      <th>Status</th>
      <th>Progress</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Task 1</td>
      <td>Complete</td>
      <td>100%</td>
    </tr>
    <tr>
      <td>Task 2</td>
      <td>In Progress</td>
      <td>45%</td>
    </tr>
  </tbody>
</table>
```

**Rendering:**
```
┌─────────┬─────────────┬──────────┐
│ Name    │ Status      │ Progress │
├─────────┼─────────────┼──────────┤
│ Task 1  │ Complete    │ 100%     │
│ Task 2  │ In Progress │ 45%      │
└─────────┴─────────────┴──────────┘
```

**Benefits:**
- Uses box-drawing characters
- Properly aligned columns
- Better than trying to parse complex HTML tables

### 8. `<panel>` - Collapsible Panels with Icons
```html
<panel icon="📁" title="Files">
  <ul>
    <li>document.txt</li>
    <li>image.png</li>
    <li>data.csv</li>
  </ul>
</panel>

<panel icon="⚙️" title="Settings" collapsed>
  <p>Configuration options here</p>
</panel>
```

**Rendering:**
```
┌─ 📁 Files ────────────────┐
│ • document.txt            │
│ • image.png               │
│ • data.csv                │
└───────────────────────────┘

[+] ⚙️ Settings
```

**Benefits:**
- Organizes content into collapsible sections
- Visual hierarchy with icons
- Press key to expand/collapse

### 9. `<status>` - Status Indicators
```html
<status value="online">Server</status>
<status value="offline">Database</status>
<status value="degraded">Cache</status>
<status value="unknown">API</status>
```

**Rendering:**
```
● Server      [online]
● Database    [offline]
● Cache       [degraded]
● API         [unknown]
```

**Color mapping:**
```
online   → green ●
offline  → red ●
degraded → yellow ●
unknown  → gray ●
```

### 10. `<kbd>` and `<samp>` Enhanced
```html
<p>Press <kbd>Ctrl+K</kbd> to open command palette</p>
<p>Output: <samp>Process completed successfully</samp></p>
```

**Rendering:**
```
Press [Ctrl+K] to open command palette

Output: │ Process completed successfully
```

**Benefits:**
- Already exist in HTML but underused
- Can be styled distinctively in text mode
- `<kbd>` in brackets, `<samp>` with prefix marker

## Example: Complete Text-First HTML Page

```html
<!DOCTYPE html>
<html>
<head>
  <title>Text-First Example</title>
  <meta charset="utf-8">
</head>
<body>

  <!-- Banner for important announcements -->
  <banner type="info">
    Welcome to the Text-First Web! This page is optimized for terminal browsers.
  </banner>

  <!-- Main header in a box -->
  <box style="double">
    <center>
      <color name="highlight">MAIN MENU</color>
    </center>
  </box>

  <!-- Numbered navigation menu -->
  <menu type="numbered">
    <li><a href="/news">Latest News</a></li>
    <li><a href="/docs">Documentation</a></li>
    <li><a href="/api">API Reference</a></li>
    <li><a href="/help">Help & Support</a></li>
  </menu>

  <!-- Main content article -->
  <article>
    <header>
      <h1>Getting Started with Text Browsing</h1>
      <p>
        <color name="muted">Published: 2025-01-28 by Admin</color>
      </p>
    </header>

    <section>
      <h2>Introduction</h2>
      <p>
        Text-first browsing is <color name="success">fast</color>,
        <color name="success">accessible</color>, and
        <color name="success">efficient</color>.
      </p>

      <box style="single">
        <color name="info">💡 Tip:</color> Use keyboard shortcuts for faster navigation!
      </box>

      <p>Common shortcuts:</p>
      <dl>
        <dt><kbd>0-9</kbd></dt>
        <dd>Jump to numbered links</dd>

        <dt><kbd>Ctrl+K</kbd></dt>
        <dd>Open command/address bar</dd>

        <dt><kbd>H</kbd></dt>
        <dd>Show help</dd>
      </dl>
    </section>

    <section>
      <h2>System Status</h2>
      <table simple>
        <thead>
          <tr>
            <th>Service</th>
            <th>Status</th>
            <th>Uptime</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Web Server</td>
            <td><status value="online">Online</status></td>
            <td>99.9%</td>
          </tr>
          <tr>
            <td>Database</td>
            <td><status value="online">Online</status></td>
            <td>99.8%</td>
          </tr>
          <tr>
            <td>Cache</td>
            <td><status value="degraded">Degraded</status></td>
            <td>95.2%</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section>
      <h2>Technical Details</h2>

      <!-- Collapsible technical info -->
      <details>
        <summary>View implementation details</summary>

        <h3>Architecture</h3>
        <tree>
          <branch>System
            <branch>Frontend
              <branch>Text Browser</branch>
              <branch>Terminal UI</branch>
            </branch>
            <branch>Backend
              <branch>API Server</branch>
              <branch>Database</branch>
              <branch>Cache Layer</branch>
            </branch>
          </branch>
        </tree>

        <h3>Code Example</h3>
        <pre><code>
def fetch_page(url):
    response = requests.get(url)
    return parse_html(response.text)
        </code></pre>
      </details>
    </section>

    <section>
      <h2>Download Progress</h2>
      <p>Current operations:</p>
      <progress value="100" max="100" label="Package 1">100%</progress>
      <progress value="75" max="100" label="Package 2">75%</progress>
      <progress value="30" max="100" label="Package 3">30%</progress>
    </section>

    <aside>
      <box style="rounded">
        <h3>Related Resources</h3>
        <ul>
          <li><a href="/tutorial">Complete Tutorial</a></li>
          <li><a href="/faq">Frequently Asked Questions</a></li>
          <li><a href="/community">Join the Community</a></li>
        </ul>
      </box>
    </aside>

    <footer>
      <center>
        <color name="muted">© 2025 Text-First Web Initiative</color>
      </center>
    </footer>
  </article>

</body>
</html>
```

## Implementation Plan for DBBasic TextBrowser

### Phase 1: Enhanced Existing Tags
1. ✅ `<font color>` - Already implemented!
2. ⬜ `<center>` - Center text within terminal width
3. ⬜ `<details>`/`<summary>` - Collapsible sections with `[+]`/`[-]`
4. ⬜ `<blockquote>` - Indent and add `│` prefix
5. ⬜ `<aside>` - Visual separator or box

### Phase 2: New Semantic Tags
1. ⬜ `<color name="...">` - Semantic color names
2. ⬜ `<menu type="numbered">` - Auto-numbered menus
3. ⬜ `<status>` - Status indicators with colored dots

### Phase 3: Advanced Layout Tags
1. ⬜ `<box>` - ASCII box drawing
2. ⬜ `<banner>` - Important announcements with borders
3. ⬜ `<table simple>` - Better table rendering
4. ⬜ `<tree>` - Hierarchical tree structures
5. ⬜ `<panel>` - Collapsible panels with icons

### Phase 4: Interactive Elements
1. ⬜ Enhanced `<progress>` - Visual progress bars
2. ⬜ `<kbd>` and `<samp>` - Better keyboard/output display
3. ⬜ Interactive tree navigation
4. ⬜ Panel expand/collapse

## Implementation Approach

All of these can be implemented in `browser.py` by preprocessing HTML before passing to `html2text`:

```python
def preprocess_html_for_text(soup):
    """Convert text-friendly HTML tags to marked text"""

    # 1. Handle <color name="..."> tags
    for color_tag in soup.find_all('color'):
        name = color_tag.get('name')
        color_map = {
            'error': 'red',
            'success': 'green',
            'warning': 'yellow',
            'info': 'cyan',
            'muted': 'white',  # Could use dim/gray
            'highlight': 'white'  # Could use bold/bright
        }
        color = color_map.get(name, 'white')
        text = color_tag.get_text()
        color_tag.string = f"«{color}»{text}«/{color}»"

    # 2. Handle <box> tags
    for box in soup.find_all('box'):
        style = box.get('style', 'single')
        content = box.get_text()
        box.string = render_box(content, style, terminal_width)

    # 3. Handle <banner> tags
    for banner in soup.find_all('banner'):
        banner_type = banner.get('type', 'info')
        content = banner.get_text()
        banner.string = render_banner(content, banner_type, terminal_width)

    # 4. Handle <center> tags
    for center in soup.find_all('center'):
        text = center.get_text()
        center.string = center_text(text, terminal_width)

    # 5. Handle <details>/<summary>
    for details in soup.find_all('details'):
        summary = details.find('summary')
        if summary:
            # Mark as collapsible
            summary.string = f"[+] {summary.get_text()}"

    # 6. Handle <menu type="numbered">
    for menu in soup.find_all('menu'):
        if menu.get('type') == 'numbered':
            # Links will be numbered by existing link system
            # Just mark it for special handling
            pass

    # 7. Handle <tree> structures
    for tree in soup.find_all('tree'):
        tree.string = render_tree(tree)

    # 8. Handle <status> indicators
    for status in soup.find_all('status'):
        value = status.get('value', 'unknown')
        text = status.get_text()
        status.string = render_status(value, text)

    # 9. Handle <progress> bars
    for progress in soup.find_all('progress'):
        value = int(progress.get('value', 0))
        max_val = int(progress.get('max', 100))
        label = progress.get('label', '')
        progress.string = render_progress_bar(value, max_val, label)

    return soup

def render_box(content, style, width):
    """Render content in an ASCII box"""
    styles = {
        'single': ('┌', '─', '┐', '│', '└', '┘'),
        'double': ('╔', '═', '╗', '║', '╚', '╝'),
        'rounded': ('╭', '─', '╮', '│', '╰', '╯'),
        'bold': ('┏', '━', '┓', '┃', '┗', '┛')
    }
    tl, h, tr, v, bl, br = styles.get(style, styles['single'])

    lines = content.split('\n')
    max_len = min(max(len(line) for line in lines), width - 4)

    result = [tl + h * (max_len + 2) + tr]
    for line in lines:
        padded = line.ljust(max_len)
        result.append(f"{v} {padded} {v}")
    result.append(bl + h * (max_len + 2) + br)

    return '\n'.join(result)

def render_progress_bar(value, max_val, label, width=20):
    """Render a progress bar"""
    percentage = int((value / max_val) * 100)
    filled = int((value / max_val) * width)
    bar = '█' * filled + '░' * (width - filled)

    if label:
        return f"{label}: [{bar}] {percentage}%"
    return f"[{bar}] {percentage}%"

def render_status(value, text):
    """Render a status indicator"""
    icons = {
        'online': '●',
        'offline': '●',
        'degraded': '●',
        'unknown': '●'
    }
    colors = {
        'online': 'green',
        'offline': 'red',
        'degraded': 'yellow',
        'unknown': 'white'
    }

    icon = icons.get(value, '●')
    color = colors.get(value, 'white')

    return f"«{color}»{icon}«/{color}» {text}"

def render_tree(tree_element):
    """Render a tree structure with box-drawing characters"""
    def render_branch(branch, prefix='', is_last=True):
        lines = []

        # Get text content (first text node)
        text = next(branch.stripped_strings, '')

        # Current item
        connector = '└─ ' if is_last else '├─ '
        lines.append(prefix + connector + text)

        # Get sub-branches
        sub_branches = branch.find_all('branch', recursive=False)

        for i, sub_branch in enumerate(sub_branches):
            is_last_sub = (i == len(sub_branches) - 1)
            extension = '   ' if is_last else '│  '
            lines.extend(render_branch(sub_branch, prefix + extension, is_last_sub))

        return lines

    root = tree_element.find('branch')
    if root:
        return '\n'.join(render_branch(root, '', True))
    return ''
```

## Benefits of This Approach

1. **Backward compatible** - Regular HTML still works
2. **Progressive enhancement** - Graphical browsers can style with CSS
3. **Semantic meaning** - Tags describe content, not just presentation
4. **Fast rendering** - No CSS parsing, immediate display
5. **Accessible** - Screen readers can understand semantic tags
6. **Keyboard-first** - Designed for keyboard navigation
7. **Low bandwidth** - No CSS/JS downloads needed

## Next Steps

1. Create test HTML pages with proposed tags
2. Implement Phase 1 (enhanced existing tags)
3. Test rendering in DBBasic TextBrowser
4. Iterate on design based on real usage
5. Create a "Text-First HTML" specification
6. Build a validator for text-friendly HTML

## Related Files

- `browser.py` - Main implementation
- `demo.html` - Color demo (could add new tag demos)
- `IDEAS.md` - Additional design ideas
- This file - Specification and examples

---

**Remember:** The goal is to make the web accessible, fast, and keyboard-driven while maintaining semantic meaning. Text-first HTML brings us back to the original vision of the web as a document system, enhanced with modern ideas.
