# DBBasic TextBrowser: Ideas & Insights

## Core Concept

A text-mode web browser with AI assistance that demonstrates how keyboard-first, intentional navigation can be superior to mouse-driven browsing.

## Key Innovations

### 1. AI Integration in a Text Browser

**Game Changer**: While Lynx is lightweight and fast, it has no intelligence. Adding GPT-5 gives you:

- **Natural language navigation**: "go to wikipedia for WebDAV"
- **Content extraction**: "find the pricing information"
- **Summarization**: "what are the main points?"
- **Translation**: "translate this to Spanish"
- **Q&A**: "what does this article say about security?"
- **Function calling**: AI can actually navigate the browser, not just suggest URLs

**Why it works in text mode**:
- Clean, structured content (no CSS/JS soup)
- AI gets exactly what the user sees
- Natural fit with command-driven interface
- Faster than most modern websites render

### 2. Numbered Links

**The Insight**: Every clickable element should be numbered and accessible via keyboard.

**Current Implementation**:
- Links numbered inline: `[0] Main page`, `[1] Talk`, etc.
- Press 0-9 for instant access to first 10 links
- Press G + number for any link
- Link list at bottom of page

**Why this matters**: No mouse hunting, no accidental clicks, deliberate navigation.

### 3. Form Support

**Features**:
- Automatic form detection
- Press F to fill out forms
- Interactive field-by-field input
- Supports GET and POST methods
- Works with search engines (DuckDuckGo, etc.)

### 4. Text-First Design Philosophy

**Core Principle**: Build for text/keyboard first, add GUI as progressive enhancement.

**Advantages**:
- Forces you to think about information hierarchy
- Accessibility built in from day one
- No accidental interactions
- Fast and intentional
- Works over SSH, slow connections, screen readers

**Modern web dev typically goes**:
1. Design visual layout
2. Add interactions
3. Try to make it accessible
4. Try to make it fast

**We went**:
1. What's the actual content/function?
2. How do I navigate with keyboard?
3. How do I make it smart with AI?

## The Big Idea: Numbered Navigation in Modern Browsers

### The Problem

Firefox, Chrome, Safari all assume mouse-first navigation. Keyboard users are second-class citizens.

### The Solution

**What if Firefox had native numbered navigation?**

1. Press a key (like `/` or `F`)
2. Every clickable element gets a number overlay
3. Type the number, hit Enter
4. Element is clicked

### Benefits

- **Accessibility**: Motor disabilities, screen readers
- **Power users**: Way faster than mouse
- **Remote desktop**: Mouse over RDP is painful
- **Laptop trackpads**: Trackpads are terrible
- **Gaming/streaming**: Keep hands on keyboard
- **Efficiency**: No visual hunting

### Existing Attempts (All Extensions)

- **Vimium** / **Vimium-C**: Press `f`, links get letter combos
- **Tridactyl**: Vim-like navigation
- **SurfingKeys**: Chrome equivalent

**Problem**: They're extensions, not core browser features.

### Why Browsers Don't Do This

1. Mouse-first mindset
2. Fear of complexity ("normal users won't use it")
3. Design language assumes hover states
4. "Someone will make an extension"

**But**: This should be core browser functionality, just like Ctrl+T, Ctrl+L, Ctrl+F.

## Future Features to Add

### High Priority

- [ ] **History/Back button**: Navigate backward through visited pages
- [ ] **Bookmarks**: Save and manage favorite pages
- [ ] **Search within page**: `/` to search like vim
- [ ] **Better table rendering**: Parse HTML tables into ASCII tables

### AI Enhancements

- [ ] **Web search function**: Give AI ability to search the web
- [ ] **Extract to file**: "save this table as CSV"
- [ ] **Page comparison**: "compare these two product pages"
- [ ] **Multi-page chains**: AI visits multiple pages to gather info
- [ ] **Content filtering**: "show only the article, hide everything else"

### Navigation Improvements

- [ ] **Tab support**: Multiple pages open at once
- [ ] **Session restore**: Reopen tabs from last session
- [ ] **Link previews**: Hover (or key) to see URL before visiting
- [ ] **Smart back**: Remember scroll position

### Downloads

- [ ] **File download detection**: Detect and save binary files
- [ ] **Download manager**: Track download progress
- [ ] **Auto-open**: Open downloaded files in appropriate apps

### Performance

- [ ] **Caching**: Cache pages locally
- [ ] **Prefetch**: Preload likely next pages
- [ ] **Compression**: Support gzip/brotli

## Technical Insights

### What We Learned

1. **Text wrapping is critical**: Setting `body_width=0` broke everything
2. **GPT-5 API changes**: New models need `max_completion_tokens` instead of `max_tokens`, and don't support custom `temperature`
3. **Form handling is complex**: Need to handle relative URLs, GET vs POST, field types
4. **Link extraction requires filtering**: Skip `#`, `javascript:`, `mailto:` links
5. **Color makes a huge difference**: Even in a text browser, syntax highlighting helps

### Architecture Decisions

- **BeautifulSoup** for HTML parsing (could switch to lxml for speed)
- **html2text** for HTML→markdown conversion (works well but could be customized)
- **curses** for terminal UI (standard but limiting on Windows)
- **requests** for HTTP (simple but no async support)

### Performance Characteristics

- **Faster than graphical browsers** for simple pages
- **AI calls are the bottleneck**: GPT-5-nano is slower than expected
- **No JS execution**: Some sites won't work (SPAs, etc.)
- **Text rendering is instant**: No layout engine, no reflows

## Potential Projects

### 1. Firefox Extension: Native Numbered Links

Build a better Vimium that:
- Uses actual numbers (not letter combos)
- Integrates with browser UI
- Has better visual design
- Supports forms, buttons, all clickables

### 2. Text-First Web Framework

A web framework that generates both:
- Text-mode interface (for this browser)
- GUI interface (progressive enhancement)

Like how GraphQL has one schema, multiple clients.

### 3. AI-Enhanced Bookmarklet

A bookmarklet that adds AI to any browser:
- Summarize page
- Extract data
- Answer questions
- Navigate intelligently

### 4. Terminal Browser as Developer Tool

Use this as a debugging tool:
- See what screen readers see
- Test keyboard navigation
- Validate content hierarchy
- Check accessibility

## Philosophy

### Text-Only Forces Good Design

When you can't hide behind visual design:
- Information hierarchy must be clear
- Navigation must be intuitive
- Content must be well-structured
- Every interaction must be intentional

### Keyboard-First is Faster

Once you learn the keys:
- No visual hunting for clickable areas
- No mouse precision required
- No accidental clicks
- Muscle memory develops

### AI Changes Everything

AI in a browser isn't just a chatbot:
- It can navigate for you
- It can extract information
- It can answer questions about what you're viewing
- It can chain actions together

**The browser becomes an agent, not just a viewer.**

## Success Metrics

How do we know this approach works?

1. **Speed**: From thought to action is faster than mouse
2. **Intentionality**: Every action is deliberate
3. **Accessibility**: Works for everyone, not just mouse users
4. **Intelligence**: AI makes browsing smarter, not just automated
5. **Simplicity**: Core functionality is obvious and learnable

## Related Work

- **Lynx**: The original text browser (no AI)
- **w3m**: Another text browser (better table support)
- **elinks**: Feature-rich text browser
- **Vimium**: Vim keybindings for browsers
- **qutebrowser**: Keyboard-focused browser
- **surf**: Minimalist browser
- **Browserless**: Headless browser automation

## Questions to Explore

1. Could this approach work for mobile?
2. What about voice navigation with numbers?
3. How would numbered navigation work with dynamic content?
4. Could AI predict which link you want?
5. What if every app had a text-mode interface?

## Contact & Contributions

This is an exploration of what browsers could be. Ideas, code, and discussion welcome.

**Core insight**: Text-first, keyboard-first, AI-enhanced browsing might actually be the future, not the past.
