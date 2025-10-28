# Semantic CSS Framework: Against the Tri-Hard Pattern

**Date:** 2025-01-28
**Status:** Concept / Design Phase

## The Tri-Hard Pattern Problem

Modern web development has evolved into unnecessary complexity:

```
HTML alone (1990s)
  ↓
HTML + Images (mid 1990s)
  ↓
HTML + CSS + Images (late 1990s)
  ↓
HTML (divs) + CSS + Image Maps + JavaScript (2000s)
  ↓
HTML (divs) + CSS (frameworks) + JavaScript (frameworks) + Build Tools (2010s-2020s)
```

**The Problem:** Instead of making things SIMPLER, each step made them MORE SPREAD OUT.

### Example: Displaying a Red Error Message

**1990s - Simple HTML:**
```html
<font color="red"><b>ERROR:</b> File not found</font>
```
- ✅ Everything in one place
- ✅ Works immediately
- ✅ No external dependencies
- ✅ Semantic meaning clear

**2000s - HTML + CSS:**
```html
<!-- HTML file -->
<span class="error">ERROR: File not found</span>

<!-- CSS file -->
.error {
  color: red;
  font-weight: bold;
}
```
- ⚠️ Split across 2 files
- ⚠️ Need to learn CSS
- ✅ Separation of concerns (supposedly)

**2010s - Bootstrap:**
```html
<!-- HTML file -->
<div class="alert alert-danger">
  <strong>ERROR:</strong> File not found
</div>

<!-- Head tag -->
<link rel="stylesheet" href="bootstrap.min.css">
```
- ⚠️ Requires framework download (200KB+)
- ⚠️ Generic class names
- ⚠️ Lots of markup
- ✅ Consistent styling

**2020s - Tailwind:**
```html
<!-- HTML file -->
<div class="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
  <strong class="font-bold">ERROR:</strong>
  <span class="block sm:inline">File not found</span>
</div>

<!-- Config file, build process, PostCSS, etc. -->
```
- ❌ Requires build process
- ❌ Verbose class soup
- ❌ Presentation in HTML
- ❌ Lost semantic meaning
- ⚠️ 3+ files involved

**2025 - React/TypeScript/Styled Components:**
```tsx
// ErrorMessage.tsx
import styled from 'styled-components';

const ErrorContainer = styled.div`
  background-color: ${props => props.theme.colors.error.light};
  border: 1px solid ${props => props.theme.colors.error.main};
  color: ${props => props.theme.colors.error.dark};
  padding: ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius.sm};
`;

const ErrorTitle = styled.strong`
  font-weight: bold;
`;

export const ErrorMessage: React.FC<{message: string}> = ({message}) => {
  return (
    <ErrorContainer role="alert">
      <ErrorTitle>ERROR:</ErrorTitle> {message}
    </ErrorContainer>
  );
};

// Usage:
<ErrorMessage message="File not found" />

// Plus: theme.ts, package.json, tsconfig.json, webpack.config.js, etc.
```
- ❌ 10+ files involved
- ❌ Build process required
- ❌ Runtime JavaScript needed
- ❌ Learning curve: React, TypeScript, Styled Components, build tools
- ❌ Lost all semantic meaning
- ✅ Type safety (but at what cost?)

## The Tri-Hard Pattern

**Definition:** When a simple task requires coordination across 3+ separate locations:
1. HTML file
2. CSS file
3. JavaScript file
4. Build configuration
5. Package dependencies
6. etc.

**Why it's bad:**
- Mental overhead switching between files
- Harder to debug
- Slower development
- Fragile (breaks if any piece missing)
- Impossible to view source and understand

## The Solution: Semantic CSS Framework

### Philosophy

1. **HTML First** - Semantic HTML should work standalone
2. **CSS Enhances** - CSS makes it prettier, doesn't replace functionality
3. **No JavaScript Required** - Static content needs no JS
4. **Progressive Enhancement** - Works in text browsers, better in graphical
5. **One Source of Truth** - HTML is the truth, everything else enhances it

### Design Principles

```
SEMANTIC HTML (works alone)
    ↓
  + SEMANTIC CSS (optional enhancement)
    ↓
  + JAVASCRIPT (only when truly interactive)
```

Not:
```
DIVS (meaningless)
    ↓
  + CSS CLASSES (presentation in HTML)
    ↓
  + JAVASCRIPT (required to function)
```

## The Framework: TextFirst.css

### Core Idea

**Enhance semantic HTML instead of replacing it.**

```html
<!-- Works in ANY browser, including text browsers -->
<font color="red"><b>ERROR:</b> File not found</font>

<!-- Graphical browsers get enhanced styling automatically -->
<link rel="stylesheet" href="textfirst.css">
```

### Implementation

```css
/* textfirst.css - A semantic CSS framework */

/* ============================================
   1. ENHANCE SEMANTIC TAGS
   ============================================ */

/* Font colors - enhance <font color> tag */
font[color="red"] {
  color: #dc2626;
  background-color: #fef2f2;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-weight: 500;
}

font[color="green"] {
  color: #16a34a;
  background-color: #f0fdf4;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
}

font[color="yellow"] {
  color: #ca8a04;
  background-color: #fefce8;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
}

font[color="blue"] {
  color: #2563eb;
  background-color: #eff6ff;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
}

/* Center tag - works in text, enhanced in graphical */
center {
  text-align: center;
  display: block;
  margin: 1rem 0;
}

/* Menu tag - numbered lists */
menu {
  list-style: none;
  padding: 0;
  counter-reset: menu-counter;
}

menu li {
  counter-increment: menu-counter;
  padding: 0.5rem;
  margin: 0.25rem 0;
  border-left: 3px solid #3b82f6;
  padding-left: 1rem;
}

menu li::before {
  content: "[" counter(menu-counter) "] ";
  font-weight: bold;
  color: #3b82f6;
  margin-right: 0.5rem;
}

/* Details/Summary - enhance collapsible */
details {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 1rem 0;
}

summary {
  cursor: pointer;
  font-weight: 600;
  user-select: none;
  list-style: none;
}

summary::before {
  content: "[+] ";
  color: #3b82f6;
  font-weight: bold;
}

details[open] summary::before {
  content: "[-] ";
}

/* Blockquote - add visual bar */
blockquote {
  border-left: 4px solid #3b82f6;
  padding-left: 1rem;
  margin: 1rem 0;
  color: #6b7280;
  font-style: italic;
}

/* Code and Pre */
code {
  background-color: #f3f4f6;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-family: 'Courier New', monospace;
  font-size: 0.875em;
}

pre {
  background-color: #1f2937;
  color: #f9fafb;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
}

pre code {
  background: none;
  color: inherit;
  padding: 0;
}

/* ============================================
   2. ENHANCE HTML5 SEMANTIC TAGS
   ============================================ */

article {
  max-width: 65ch;
  margin: 2rem auto;
  padding: 0 1rem;
}

article header {
  border-bottom: 2px solid #e5e7eb;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
}

article footer {
  border-top: 1px solid #e5e7eb;
  margin-top: 2rem;
  padding-top: 1rem;
  color: #6b7280;
  font-size: 0.875rem;
}

aside {
  background-color: #f9fafb;
  border-left: 4px solid #fbbf24;
  padding: 1rem;
  margin: 1rem 0;
}

section {
  margin: 2rem 0;
}

/* ============================================
   3. NEW SEMANTIC TAGS (custom elements)
   ============================================ */

/* <color name="error|success|warning|info"> */
color[name="error"] {
  color: #dc2626;
  background-color: #fef2f2;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-weight: 500;
}

color[name="success"] {
  color: #16a34a;
  background-color: #f0fdf4;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-weight: 500;
}

color[name="warning"] {
  color: #ca8a04;
  background-color: #fefce8;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-weight: 500;
}

color[name="info"] {
  color: #2563eb;
  background-color: #eff6ff;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
}

color[name="muted"] {
  color: #6b7280;
}

color[name="highlight"] {
  background-color: #fef08a;
  padding: 0.125rem 0.25rem;
  font-weight: 600;
}

/* <box style="single|double|rounded"> */
box {
  display: block;
  border: 2px solid #3b82f6;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 0.5rem;
}

box[style="double"] {
  border-width: 4px;
}

box[style="rounded"] {
  border-radius: 1rem;
}

box[style="bold"] {
  border-width: 3px;
  border-color: #1e40af;
}

/* <banner type="info|warning|error"> */
banner {
  display: block;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 0.5rem;
  border: 2px solid;
}

banner[type="info"] {
  background-color: #eff6ff;
  border-color: #3b82f6;
  color: #1e40af;
}

banner[type="warning"] {
  background-color: #fefce8;
  border-color: #eab308;
  color: #854d0e;
}

banner[type="error"] {
  background-color: #fef2f2;
  border-color: #ef4444;
  color: #991b1b;
}

banner::before {
  font-weight: bold;
  margin-right: 0.5rem;
}

banner[type="info"]::before {
  content: "ℹ️ ";
}

banner[type="warning"]::before {
  content: "⚠️ ";
}

banner[type="error"]::before {
  content: "❌ ";
}

/* <status value="online|offline|degraded"> */
status::before {
  content: "● ";
  font-size: 1.2em;
  margin-right: 0.25rem;
}

status[value="online"]::before {
  color: #16a34a;
}

status[value="offline"]::before {
  color: #dc2626;
}

status[value="degraded"]::before {
  color: #eab308;
}

status[value="unknown"]::before {
  color: #9ca3af;
}

/* ============================================
   4. TYPOGRAPHY
   ============================================ */

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: #1f2937;
  max-width: 80ch;
  margin: 0 auto;
  padding: 2rem 1rem;
}

h1, h2, h3, h4, h5, h6 {
  line-height: 1.2;
  margin-top: 2rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

h1 { font-size: 2.5rem; color: #111827; }
h2 { font-size: 2rem; color: #1f2937; }
h3 { font-size: 1.5rem; color: #374151; }

p {
  margin: 1rem 0;
}

/* ============================================
   5. FORMS - Enhance semantic form elements
   ============================================ */

input, textarea, select {
  font-family: inherit;
  font-size: 1rem;
  padding: 0.5rem;
  border: 2px solid #d1d5db;
  border-radius: 0.375rem;
  width: 100%;
  max-width: 30rem;
}

input:focus, textarea:focus, select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

button, input[type="submit"] {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  font-weight: 600;
  width: auto;
}

button:hover, input[type="submit"]:hover {
  background-color: #2563eb;
}

/* ============================================
   6. TABLES
   ============================================ */

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

th {
  background-color: #f9fafb;
  font-weight: 600;
  border-bottom: 2px solid #d1d5db;
}

tr:hover {
  background-color: #f9fafb;
}

table[simple] {
  border: 2px solid #d1d5db;
}

table[simple] th {
  background-color: #e5e7eb;
}

/* ============================================
   7. UTILITIES (minimal, semantic)
   ============================================ */

.text-center { text-align: center; }
.text-right { text-align: right; }
.text-left { text-align: left; }

.mb-0 { margin-bottom: 0; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-4 { margin-bottom: 2rem; }

.mt-0 { margin-top: 0; }
.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-4 { margin-top: 2rem; }
```

## Comparison: Same Feature, Different Approaches

### Feature: User Profile Card

**Tailwind (Tri-Hard Pattern):**
```html
<div class="max-w-sm rounded-lg overflow-hidden shadow-lg bg-white p-6">
  <div class="flex items-center mb-4">
    <div class="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold mr-4">
      JD
    </div>
    <div>
      <h2 class="text-xl font-bold text-gray-900">John Doe</h2>
      <p class="text-sm text-gray-600">Software Engineer</p>
    </div>
  </div>
  <div class="border-t border-gray-200 pt-4">
    <div class="flex justify-between items-center mb-2">
      <span class="text-sm text-gray-600">Status:</span>
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
        Online
      </span>
    </div>
  </div>
</div>
```
- ❌ 20+ utility classes
- ❌ No semantic meaning
- ❌ Div soup
- ❌ Invisible in text browsers

**TextFirst.css (Semantic):**
```html
<article>
  <header>
    <h2>John Doe</h2>
    <p><color name="muted">Software Engineer</color></p>
  </header>

  <dl>
    <dt>Status:</dt>
    <dd><status value="online">Online</status></dd>
  </dl>
</article>
```
- ✅ Clean, semantic HTML
- ✅ Works in text browsers
- ✅ Enhanced automatically with CSS
- ✅ Understandable structure

### Feature: Alert Message

**Bootstrap:**
```html
<div class="alert alert-danger" role="alert">
  <h4 class="alert-heading">Error!</h4>
  <p>Something went wrong. Please try again.</p>
  <hr>
  <p class="mb-0">If the problem persists, contact support.</p>
</div>
```

**TextFirst.css:**
```html
<banner type="error">
  <h4>Error!</h4>
  <p>Something went wrong. Please try again.</p>
  <hr>
  <p>If the problem persists, contact support.</p>
</banner>
```

### Feature: Navigation Menu

**Modern React:**
```jsx
<nav className="navbar">
  {menuItems.map((item, index) => (
    <a
      key={item.id}
      href={item.url}
      className="nav-link"
      onClick={(e) => handleClick(e, item)}
    >
      {item.label}
    </a>
  ))}
</nav>
```

**TextFirst.css:**
```html
<menu type="numbered">
  <li><a href="/">Home</a></li>
  <li><a href="/about">About</a></li>
  <li><a href="/contact">Contact</a></li>
</menu>
```

## Building the Framework

### File Structure
```
textfirst/
├── textfirst.css          # Main framework (15KB)
├── textfirst.min.css      # Minified (8KB)
├── demo/
│   ├── index.html         # Kitchen sink demo
│   ├── text-mode.html     # How it looks in text browser
│   ├── comparison.html    # Side-by-side with Tailwind/Bootstrap
│   └── components.html    # All components showcased
├── docs/
│   ├── philosophy.md      # Against the Tri-Hard pattern
│   ├── guide.md          # Usage guide
│   └── components.md     # Component reference
└── README.md
```

### Key Features

1. **Tiny** - 15KB vs Bootstrap 200KB, Tailwind 3MB before purging
2. **Zero Build** - Drop in `<link>`, works immediately
3. **Works Everywhere** - Text browsers to modern browsers
4. **Semantic** - HTML describes content, not layout
5. **Progressive** - Enhance, don't replace

## Demo Page Structure

Create `demo/comparison.html`:

```html
<!DOCTYPE html>
<html>
<head>
  <title>TextFirst.css vs Modern Frameworks</title>
  <link rel="stylesheet" href="../textfirst.css">
  <style>
    /* Demo-specific styling */
    .comparison {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2rem;
      margin: 2rem 0;
    }

    .comparison > div {
      border: 1px solid #e5e7eb;
      padding: 1rem;
    }
  </style>
</head>
<body>

<banner type="info">
  This page demonstrates TextFirst.css - a semantic CSS framework that works in text browsers AND graphical browsers.
</banner>

<article>
  <h1>TextFirst.css: Against the Tri-Hard Pattern</h1>

  <section>
    <h2>What is the Tri-Hard Pattern?</h2>
    <p>
      Modern web development requires splitting simple tasks across
      <color name="error">3+ files</color>:
      HTML, CSS, JavaScript, build configs, etc.
    </p>

    <box>
      <h3>Example: A Simple Error Message</h3>

      <details>
        <summary>The Old Way (1 file, worked everywhere)</summary>
        <pre><code>&lt;font color="red"&gt;&lt;b&gt;ERROR:&lt;/b&gt; File not found&lt;/font&gt;</code></pre>
      </details>

      <details>
        <summary>Tailwind (3+ files, build process required)</summary>
        <pre><code>&lt;div class="bg-red-50 border border-red-400 text-red-700 px-4 py-3"&gt;
  &lt;strong class="font-bold"&gt;ERROR:&lt;/strong&gt; File not found
&lt;/div&gt;</code></pre>
      </details>

      <details>
        <summary>TextFirst.css (1 file, works everywhere)</summary>
        <pre><code>&lt;color name="error"&gt;&lt;b&gt;ERROR:&lt;/b&gt; File not found&lt;/color&gt;</code></pre>
      </details>
    </box>
  </section>

  <section>
    <h2>Live Examples</h2>

    <h3>Status Indicators</h3>
    <dl>
      <dt>Web Server</dt>
      <dd><status value="online">Online</status></dd>

      <dt>Database</dt>
      <dd><status value="online">Online</status></dd>

      <dt>Cache</dt>
      <dd><status value="degraded">Degraded</status></dd>

      <dt>Backup</dt>
      <dd><status value="offline">Offline</status></dd>
    </dl>

    <h3>Banners</h3>
    <banner type="info">
      <strong>Info:</strong> System maintenance tonight at 10 PM
    </banner>

    <banner type="warning">
      <strong>Warning:</strong> Your session will expire in 5 minutes
    </banner>

    <banner type="error">
      <strong>Error:</strong> Connection lost. Attempting to reconnect...
    </banner>

    <h3>Numbered Menu</h3>
    <menu type="numbered">
      <li><a href="#home">Home</a></li>
      <li><a href="#about">About</a></li>
      <li><a href="#services">Services</a></li>
      <li><a href="#contact">Contact</a></li>
    </menu>

    <h3>Collapsible Sections</h3>
    <details>
      <summary>Click to see implementation details</summary>
      <p>This uses the native HTML <code>&lt;details&gt;</code> tag!</p>
      <p>No JavaScript required. Works in text browsers.</p>
      <pre><code>function example() {
  return "Native HTML FTW!";
}</code></pre>
    </details>

    <h3>Boxes</h3>
    <box>
      <h4>Default Box</h4>
      <p>This is a standard box with rounded corners.</p>
    </box>

    <box style="double">
      <h4>Important Notice</h4>
      <p>This uses a double border for emphasis.</p>
    </box>

    <h3>Semantic Colors</h3>
    <p>
      <color name="error">Error message</color> •
      <color name="success">Success message</color> •
      <color name="warning">Warning message</color> •
      <color name="info">Info message</color> •
      <color name="muted">Muted text</color> •
      <color name="highlight">Highlighted text</color>
    </p>

    <h3>Traditional Tags Enhanced</h3>
    <center>
      <font color="blue"><b>Welcome to the Semantic Web!</b></font>
    </center>

    <blockquote>
      The best programs are written so that computing machines can perform them
      quickly and so that human beings can understand them clearly.
      <footer>— Donald Knuth</footer>
    </blockquote>
  </section>

  <section>
    <h2>Why TextFirst.css?</h2>

    <table simple>
      <thead>
        <tr>
          <th>Feature</th>
          <th>TextFirst.css</th>
          <th>Tailwind</th>
          <th>Bootstrap</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Size</td>
          <td><color name="success">15 KB</color></td>
          <td><color name="error">3 MB (before purge)</color></td>
          <td><color name="warning">200 KB</color></td>
        </tr>
        <tr>
          <td>Build Process</td>
          <td><color name="success">None</color></td>
          <td><color name="error">Required</color></td>
          <td><color name="success">Optional</color></td>
        </tr>
        <tr>
          <td>Works in Text Browsers</td>
          <td><color name="success">Yes</color></td>
          <td><color name="error">No</color></td>
          <td><color name="error">No</color></td>
        </tr>
        <tr>
          <td>Semantic HTML</td>
          <td><color name="success">Required</color></td>
          <td><color name="error">Discouraged</color></td>
          <td><color name="warning">Optional</color></td>
        </tr>
        <tr>
          <td>Learning Curve</td>
          <td><color name="success">HTML only</color></td>
          <td><color name="error">High</color></td>
          <td><color name="warning">Medium</color></td>
        </tr>
      </tbody>
    </table>
  </section>

  <footer>
    <center>
      <p><color name="muted">TextFirst.css - Bringing Back Semantic HTML</color></p>
      <p><color name="muted">© 2025 • MIT License</color></p>
    </center>
  </footer>
</article>

</body>
</html>
```

## Next Steps

1. ✅ Document the philosophy (this file)
2. ⬜ Create `textfirst.css` with all semantic enhancements
3. ⬜ Build demo pages showing text mode vs graphical mode
4. ⬜ Create comparison page vs Bootstrap/Tailwind
5. ⬜ Write blog post about the Tri-Hard Pattern
6. ⬜ Release as open source
7. ⬜ Integrate into DBBasic TextBrowser

## The Vision

**A web where:**
- HTML is semantic and self-documenting
- CSS enhances, doesn't define
- JavaScript is optional
- Content works everywhere
- Developers don't need build tools for simple sites
- Text browsers get first-class support

**Against the Tri-Hard Pattern:**
- One HTML file should be complete
- View Source should be understandable
- No frameworks required for basic styling
- Progressive enhancement, not graceful degradation

---

This could be the foundation of a movement: **Text-First Web Development**

The web was supposed to be accessible, fast, and simple. Let's bring that back.
