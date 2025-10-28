# Gateway Architecture: DBBasic TextBrowser as Universal HTML Renderer

**Status:** Architecture pattern documentation (future implementation)
**Date:** 2025-01-28

---

## The Problem

Modern web applications face a dilemma when supporting multiple client types:

**Traditional approach:**
```
Web Users → HTML templates → Browser
BBS/Telnet Users → Separate text templates → Telnet
Screen Reader Users → Hope HTML is accessible
API Users → Yet another format (JSON)
```

**Result:** Multiple template systems, duplicate logic, maintenance nightmare.

---

## The Solution

**DBBasic TextBrowser as a universal HTML renderer:**

```
                    Single HTML Template System
                              ↓
        ┌─────────────────────┴─────────────────────┐
        ↓                                           ↓
  Text Rendering                              Graphical Rendering
  (DBBasic TextBrowser)                       (Web Browser + CSS)
        ↓                                           ↓
  ┌─────────────────┐                     ┌──────────────────┐
  │ Telnet Clients  │                     │  Web Browsers    │
  │ SSH Sessions    │                     │  Mobile Apps     │
  │ Terminal Access │                     │  Desktop Apps    │
  └─────────────────┘                     └──────────────────┘
```

**Result:** Write HTML once. Works everywhere.

---

## Use Case 1: Unified Template System

### The Original Problem

Building a web application that needs to support:
- Modern web browsers (HTML + CSS)
- Telnet/BBS clients (text only)
- Terminal-based access
- Screen readers

**Traditional solution:** Multiple template systems

```python
# templates/web/index.html
<div class="header">Welcome</div>

# templates/telnet/index.txt
=== WELCOME ===

# templates/bbs/index.ans
[ANSI codes] WELCOME [/ANSI codes]
```

**Maintenance nightmare:** 3× templates, 3× logic, 3× bugs

### DBBasic TextBrowser Solution

**One template system:**

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="textfirst.css">
</head>
<body>
    <banner type="success">
        Welcome to the System
    </banner>

    <article>
        <h1>Main Menu</h1>
        <menu type="numbered">
            <li><a href="/messages">Messages</a></li>
            <li><a href="/files">Files</a></li>
            <li><a href="/users">Users</a></li>
        </menu>
    </article>

    <status value="online">System Status: Online</status>
</body>
</html>
```

**How it works:**

**For web users:**
- Browser loads HTML
- TextFirst.css applies styling
- Gets modern, beautiful interface

**For telnet users:**
- DBBasic TextBrowser fetches HTML
- Renders as clean text
- `<font color>` becomes ANSI colors
- Numbered menu becomes interactive
- Works perfectly in terminal

**Result:**
- ✅ One template
- ✅ One codebase
- ✅ Works everywhere
- ✅ Semantic HTML is accessible
- ✅ Progressive enhancement

---

## Use Case 2: Telnet-to-HTTP Gateway

### The Architecture

**DBBasic TextBrowser acts as an HTML rendering engine for telnet sessions:**

```
┌──────────────┐
│ Telnet User  │ Port 23 (telnet)
└──────┬───────┘
       │ Raw text protocol
       ↓
┌─────────────────────────────────────┐
│ Gateway Server                      │
│                                     │
│  ┌───────────────────────────┐     │
│  │ DBBasic TextBrowser       │     │ ← One instance per user
│  │ Instance                  │     │
│  └───────┬───────────────────┘     │
│          │ HTTP                    │
│          ↓                         │
│  ┌───────────────────────────┐     │
│  │ Your Web Application      │     │ ← Outputs HTML
│  └───────────────────────────┘     │
└─────────────────────────────────────┘
```

### How It Works

**Server-side pseudocode:**

```python
import telnetlib3
import subprocess
import asyncio

async def handle_telnet_session(reader, writer):
    """Each telnet connection gets a DBBasic instance"""

    # Spawn DBBasic TextBrowser for this user
    browser = subprocess.Popen(
        ['dbbasic-textbrowser'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Pipe telnet input to browser
    async def send_to_browser():
        async for data in reader:
            browser.stdin.write(data)
            browser.stdin.flush()

    # Pipe browser output to telnet
    async def send_to_telnet():
        while True:
            output = browser.stdout.read(1024)
            if output:
                writer.write(output)
                await writer.drain()

    # Run both pipes concurrently
    await asyncio.gather(
        send_to_browser(),
        send_to_telnet()
    )

# Start telnet server
async def main():
    server = await telnetlib3.create_server(
        port=23,
        shell=handle_telnet_session
    )
    await server.wait_closed()

asyncio.run(main())
```

**What happens:**

1. **User telnets in:** `telnet yourserver.com`
2. **Server spawns browser:** One DBBasic instance per connection
3. **Browser fetches HTML:** From your web app (localhost:8000)
4. **Browser renders:** HTML → beautiful text output
5. **User sees:** Clean terminal interface with colors
6. **User interacts:** Keystrokes sent to browser
7. **Browser navigates:** Makes new HTTP requests
8. **Cycle repeats:** Seamless browsing experience

### Benefits

**For developers:**
- ✅ Write HTML once
- ✅ No telnet-specific code
- ✅ No ANSI code management
- ✅ No special rendering logic
- ✅ Use your existing web framework

**For users:**
- ✅ BBS-like experience via telnet
- ✅ Colors and formatting
- ✅ Interactive navigation
- ✅ Familiar web content
- ✅ Works from any terminal

**For operations:**
- ✅ One web app to maintain
- ✅ No separate BBS software
- ✅ Standard HTTP backend
- ✅ Proxy/cache friendly
- ✅ Standard monitoring tools

---

## Use Case 3: SSH-Based Admin Interface

### The Scenario

You have a server with a web admin panel, but you also want SSH users to access admin functions without leaving the terminal.

**Traditional approach:** Build a curses-based TUI

**DBBasic approach:** Reuse your web admin HTML

```bash
# User SSHs in
ssh admin@server.com

# Server launches DBBasic with admin URL
dbbasic-textbrowser --url http://localhost:8080/admin

# User sees HTML admin panel rendered as text
# Can navigate, fill forms, click links
# All using same backend as web interface
```

**Implementation:**

```bash
# In .ssh/authorized_keys or ssh config
command="dbbasic-textbrowser --url http://localhost:8080/admin" ssh-rsa AAAA...

# Or as login shell
sudo chsh -s /usr/local/bin/dbbasic-admin-shell username
```

---

## Use Case 4: Embedded Systems & IoT

### The Problem

Embedded devices with displays but limited resources:
- Can't run full web browser (too heavy)
- Need to show web content
- Limited RAM/CPU
- Text-based interface is fine

**Solution:** DBBasic TextBrowser as lightweight HTML renderer

```
┌────────────────────┐
│ IoT Device         │
│ (Raspberry Pi)     │
│                    │
│ DBBasic Browser ←──┼─── Fetches HTML from cloud
│       ↓            │
│  Text Display      │
│  (LCD/Terminal)    │
└────────────────────┘
```

**Benefits:**
- Tiny memory footprint vs. Chromium
- Displays HTML content
- Interactive (buttons/forms)
- Updates from cloud
- Same HTML as web version

---

## Implementation Patterns

### Pattern 1: Gateway Mode

**Add `--gateway` mode to DBBasic:**

```bash
dbbasic-textbrowser --gateway --url http://localhost:8000 --stdin --stdout
```

**Features:**
- Reads input from stdin (user keystrokes)
- Writes output to stdout (rendered pages)
- Perfect for piping to/from telnet/ssh

### Pattern 2: Multi-Session Server

```python
class BrowserGateway:
    def __init__(self):
        self.sessions = {}  # session_id -> browser_process

    def new_session(self, session_id):
        """Spawn new browser for this session"""
        browser = subprocess.Popen(
            ['dbbasic-textbrowser', '--gateway', '--url', BASE_URL],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        self.sessions[session_id] = browser
        return browser

    def handle_input(self, session_id, keystroke):
        """Send keystroke to user's browser"""
        browser = self.sessions[session_id]
        browser.stdin.write(keystroke)
        browser.stdin.flush()

    def get_output(self, session_id):
        """Get rendered output from browser"""
        browser = self.sessions[session_id]
        return browser.stdout.read(4096)

    def close_session(self, session_id):
        """Clean up when user disconnects"""
        browser = self.sessions[session_id]
        browser.terminate()
        del self.sessions[session_id]
```

### Pattern 3: Session Persistence

```python
# Store browser state for reconnection
class PersistentSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.current_url = None
        self.history = []
        self.scroll_position = 0

    def save_state(self):
        """Save state to Redis/DB"""
        state = {
            'url': self.current_url,
            'history': self.history,
            'scroll': self.scroll_position
        }
        redis.set(f'session:{self.session_id}', json.dumps(state))

    def restore_state(self):
        """Restore state on reconnect"""
        state = json.loads(redis.get(f'session:{self.session_id}'))
        self.current_url = state['url']
        self.history = state['history']
        self.scroll_position = state['scroll']
        # Navigate browser to saved URL
```

---

## Architecture Benefits

### 1. Single Source of Truth

**One HTML template serves:**
- Web browsers (with CSS)
- Telnet clients (via DBBasic)
- Mobile apps (with CSS)
- Screen readers (semantic HTML)
- API clients (can parse HTML)
- RSS readers (HTML content)

### 2. Progressive Enhancement

**Base layer:** Semantic HTML (works everywhere)
**Enhancement 1:** CSS for graphical browsers
**Enhancement 2:** JavaScript for interactivity
**Enhancement 3:** App-specific features

**DBBasic uses base layer** → always works

### 3. Cost Reduction

**Before:**
- Web frontend team
- BBS/telnet team
- API team
- Mobile team

**After:**
- One web team
- HTML works everywhere
- DBBasic handles text rendering

### 4. Faster Development

**Add a new feature:**
- Write HTML template
- Works on web ✅
- Works on telnet ✅
- Works on mobile ✅
- Works for screen readers ✅

**No separate implementations needed.**

---

## Real-World Examples

### Example 1: Multi-User BBS

**Modern BBS system using web tech:**

```
┌─────────────────────────────────────────┐
│         Your Web Application             │
│                                          │
│  Flask/Django/Node/whatever             │
│  Outputs HTML for all features:         │
│  - Message boards                       │
│  - File areas                           │
│  - User profiles                        │
│  - Games                                │
└───────┬─────────────────────┬───────────┘
        │                     │
        ↓                     ↓
  DBBasic Gateway      Web Browser
  (Telnet users)       (Web users)
        ↓                     ↓
  Text rendering       CSS rendering
```

**Benefits:**
- Write HTML once
- BBS users get telnet experience
- Web users get modern interface
- Share same database
- Share same authentication
- Share same logic

### Example 2: Corporate Intranet

**SSH access to company portal:**

```bash
# Employees SSH to portal
ssh portal@company.com

# DBBasic shows company intranet
# - News feeds
# - HR forms
# - IT tickets
# - Directory

# Same content as web version
# Works from any terminal
# Even over slow connections
```

### Example 3: Remote Admin Dashboard

**Monitor servers via SSH:**

```bash
# SSH to monitoring server
ssh monitor@ops.company.com

# DBBasic displays dashboard
# - Server status (HTML status indicators)
# - Metrics graphs (ASCII art)
# - Alert list (HTML tables)
# - Quick actions (HTML forms)

# Same dashboard as web version
# No VPN needed for web access
# Terminal-native experience
```

### Example 4: Educational Platform

**Terminal-based learning:**

```bash
# Students connect via SSH
ssh learn@university.edu

# DBBasic shows course material
# - Lessons (HTML content)
# - Quizzes (HTML forms)
# - Progress (HTML tables)
# - Resources (HTML links)

# Same content as LMS website
# Works on lab computers
# Works on personal devices
# Accessible for screen readers
```

---

## Technical Requirements

### For Gateway Mode

**DBBasic needs:**
1. `--gateway` mode
   - Read from stdin
   - Write to stdout
   - No TTY required

2. `--url` parameter
   - Start at specific URL
   - Default homepage override

3. Session state
   - Serialize/deserialize state
   - Resume sessions
   - Export/import history

4. Event hooks
   - On page load
   - On navigation
   - On form submit
   - For logging/analytics

### For Server Integration

**Gateway server needs:**
1. Session management
   - Track active sessions
   - Clean up disconnected users
   - Timeout idle sessions

2. Input/output handling
   - Buffer management
   - Character encoding
   - Terminal emulation

3. Process management
   - Spawn browser instances
   - Monitor health
   - Restart on crash
   - Resource limits

4. Authentication
   - User login
   - Session tokens
   - Permission checking

---

## Code Examples

### Minimal Telnet Gateway

```python
#!/usr/bin/env python3
"""
Minimal telnet-to-HTTP gateway using DBBasic TextBrowser
"""

import asyncio
import telnetlib3
import subprocess

async def shell(reader, writer):
    """Handle telnet session with DBBasic browser"""

    # Welcome message
    writer.write('\r\nWelcome to Web Gateway!\r\n')
    writer.write('Powered by DBBasic TextBrowser\r\n\r\n')

    # Spawn browser
    browser = await asyncio.create_subprocess_exec(
        'dbbasic-textbrowser',
        '--gateway',
        '--url', 'http://localhost:8000',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )

    # Forward input to browser
    async def input_loop():
        async for data in reader:
            browser.stdin.write(data.encode())
            await browser.stdin.drain()

    # Forward output to telnet
    async def output_loop():
        while True:
            data = await browser.stdout.read(1024)
            if not data:
                break
            writer.write(data.decode())
            await writer.drain()

    # Run both loops
    await asyncio.gather(input_loop(), output_loop())

    # Cleanup
    browser.terminate()
    await browser.wait()

# Start server
async def main():
    server = await telnetlib3.create_server(
        port=2323,
        shell=shell
    )
    print('Gateway running on port 2323')
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
```

### SSH Force Command

```bash
#!/bin/bash
# /usr/local/bin/web-gateway-shell
# Set as force command for SSH users

exec dbbasic-textbrowser \
    --gateway \
    --url "http://localhost:8000" \
    --stdin \
    --stdout
```

**In `.ssh/authorized_keys`:**
```
command="/usr/local/bin/web-gateway-shell",no-pty ssh-rsa AAAA...
```

---

## Philosophy Connection

This gateway architecture embodies the core TextFirst.css philosophy:

### 1. HTML is Universal

HTML isn't just for web browsers. It's a **semantic markup language** that can be rendered anywhere:
- Graphical browsers → CSS styling
- Text browsers → Clean text
- Screen readers → Semantic meaning
- APIs → Structured data

### 2. Progressive Enhancement

Start with working HTML, enhance upward:
- **Base:** Semantic HTML (works in DBBasic)
- **Layer 1:** CSS (works in graphical browsers)
- **Layer 2:** JavaScript (works for interactivity)

DBBasic uses the base layer → always works.

### 3. Separation of Concerns

- **Content:** HTML (your app)
- **Presentation:** CSS (graphical) or DBBasic (text)
- **Behavior:** JavaScript (optional)

Each layer independent, each layer optional.

### 4. Universal Access

Same content, different rendering:
- Telnet users: text rendering
- Web users: graphical rendering
- Screen reader users: semantic rendering
- API users: structured rendering

**Nobody excluded. Everybody included.**

---

## Future Development

### Phase 1: Gateway Mode (Immediate)
- [ ] Add `--gateway` flag to DBBasic
- [ ] stdin/stdout mode
- [ ] Session state export/import
- [ ] Event hooks

### Phase 2: Reference Implementation
- [ ] Example telnet gateway server
- [ ] Example SSH force command
- [ ] Docker compose example
- [ ] Documentation

### Phase 3: Production Features
- [ ] Multi-session management
- [ ] Session persistence
- [ ] Resource limits
- [ ] Health monitoring
- [ ] Metrics/logging

### Phase 4: Advanced Features
- [ ] Load balancing
- [ ] Horizontal scaling
- [ ] Session migration
- [ ] CDN integration

---

## Comparison with Alternatives

### vs. Separate Telnet Server

**Traditional BBS software:**
- Custom protocol
- Separate codebase
- Different templates
- Different database
- Maintenance overhead

**DBBasic Gateway:**
- Standard HTTP backend
- Shared codebase
- Same templates
- Same database
- Minimal overhead

### vs. Web-Only

**Web browser only:**
- Requires graphical environment
- Heavy resource usage
- Network latency visible
- JavaScript required
- Complex authentication

**DBBasic Gateway:**
- Terminal-native
- Lightweight
- Text is fast
- No JavaScript needed
- SSH authentication

### vs. Curses TUI

**Custom TUI application:**
- Write UI code
- Handle terminal differences
- Manage state
- Separate from web
- Double maintenance

**DBBasic Gateway:**
- Write HTML
- DBBasic handles terminals
- Browser manages state
- Same as web
- Single codebase

---

## Success Metrics

**How to know this works:**

1. **Developer Experience**
   - Can add feature once
   - Works in all clients
   - No telnet-specific code needed

2. **User Experience**
   - Telnet users get rich experience
   - Same features as web users
   - Fast, responsive interface

3. **Operations**
   - One application to deploy
   - Standard monitoring works
   - Logs are unified
   - Scaling is standard

4. **Cost**
   - Reduced development time
   - Reduced maintenance
   - Reduced infrastructure
   - Increased feature velocity

---

## Conclusion

DBBasic TextBrowser isn't just a browser. It's a **universal HTML rendering engine** that enables:

1. **Unified templating** - One HTML template, many renderers
2. **Telnet gateway** - HTTP backend, telnet frontend
3. **SSH admin** - Web panels in terminal
4. **Embedded displays** - Lightweight HTML rendering
5. **Universal access** - Same content, everywhere

**The original problem:**
> "We needed an alternative to telnet that could read HTML, so we could use one template language for both BBS and web."

**The solution:**
> DBBasic TextBrowser as an HTML-to-text rendering engine, acting as a gateway between text-based protocols and HTTP-based applications.

**The result:**
> Write HTML once. Works in telnet, SSH, web, mobile, screen readers, and anywhere else.

**This is the text-first web, realized.**

---

## Related Documents

- **[SEMANTIC-CSS-FRAMEWORK.md](SEMANTIC-CSS-FRAMEWORK.md)** - The Tri-Hard Pattern philosophy
- **[TEXT-WEB-HTML.md](TEXT-WEB-HTML.md)** - Semantic HTML specification
- **[IT-JUST-WORKS.md](IT-JUST-WORKS.md)** - Why basic HTML/CSS works everywhere
- **[USEIT-PARADOX.md](USEIT-PARADOX.md)** - Don't sacrifice simplicity

---

*"We just needed an alternative to telnet that could keep the HTML."* - The insight that unlocked gateway architecture, 2025
