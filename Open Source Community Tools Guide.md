# Open Source Community Tools Guide

**Lightweight, offline-capable tools for your community information hub**

This guide recommends free, open-source tools that work well on low-power devices (like repurposed phones) with minimal memory footprint. All recommendations avoid heavy dependencies and work offline.

---

## Philosophy: Keep It Simple

Following the decentralized, open-source spirit of the early internet:
- ✅ **No PHP** - Too heavy for phone-based servers
- ✅ **No databases** - Use flat files instead (JSON, Markdown, text)
- ✅ **Offline-first** - Everything works without internet
- ✅ **Minimal dependencies** - Easy to install and maintain
- ✅ **Static when possible** - Fast, secure, simple

---

## Quick Reference by Use Case

| Need | Tool | Why It's Great |
|------|------|----------------|
| Wiki/Knowledge Base | **TiddlyWiki** | Single HTML file, works anywhere |
| Documentation Site | **MkDocs** | Python-based, builds static sites |
| Bulletin Board | **Custom Flask App** | Python, no database needed |
| Calendar | **FullCalendar.js** | JavaScript, works offline with local storage |
| File Sharing | **Python http.server** | Already using it! |

---

## 1. Wiki & Knowledge Base

### TiddlyWiki ⭐ Top Pick

**What it is:** An entire wiki in a single HTML file

**Perfect for:**
- Community manuals and guides
- Skill documentation
- Maintenance logs
- Policy documentation
- Meeting notes

**Why it's amazing:**
- 🎯 Literally one HTML file - the whole wiki!
- 📱 Works on any device with a browser
- 💾 No server needed (but can use one)
- 🔌 100% offline capable
- 📧 Can email the entire wiki as an attachment
- 💪 Powerful linking and tagging
- 🎨 Highly customizable

**Installation:**
```bash
# Download the empty TiddlyWiki file
cd ~/commune-hub
wget https://tiddlywiki.com/empty.html -O wiki.html

# Or create via npm if you want the full version
pkg install nodejs
npm install -g tiddlywiki
tiddlywiki mynewwiki --init server
tiddlywiki mynewwiki --listen port=8081
```

**Use it for:**
- "How to repair the water pump"
- "Emergency procedures"
- "Garden planting calendar"
- "Tool maintenance logs"

**Learn more:** https://tiddlywiki.com/

---

### MkDocs (Python-based documentation)

**What it is:** Static site generator for beautiful documentation

**Perfect for:**
- Technical documentation
- Project documentation
- Structured knowledge bases

**Why it's good:**
- 🐍 Python-based (already installed!)
- 📝 Write in Markdown
- 🚀 Builds fast static sites
- 📱 Mobile-friendly by default
- 🔍 Built-in search

**Installation:**
```bash
pkg install python
pip install mkdocs

# Create new docs site
mkdocs new my-community-docs
cd my-community-docs

# Edit docs/index.md with your content
# Build static site
mkdocs build

# Site is in site/ directory - copy to commune-hub
```

**Learn more:** https://www.mkdocs.org/

---

## 2. Bulletin Boards & Forums

### Custom Flask App (DIY Approach)

**What it is:** Simple Python web app - you build exactly what you need

**Perfect for:**
- Community announcements
- Message boards
- Simple bulletin board
- Request/offer board

**Why build your own:**
- 🎯 Only features you need
- 🐍 Python (same as your web server)
- 📦 No database required (use JSON files)
- 🔧 Full control
- 📚 Learning opportunity

**Simple Example:**
```python
# bulletin_board.py - Store posts in JSON file
from flask import Flask, render_template, request
import json
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    posts = load_posts()
    return render_template('board.html', posts=posts)

@app.route('/post', methods=['POST'])
def add_post():
    posts = load_posts()
    new_post = {
        'author': request.form['author'],
        'message': request.form['message'],
        'date': str(datetime.datetime.now())
    }
    posts.append(new_post)
    save_posts(posts)
    return redirect('/')

def load_posts():
    try:
        with open('posts.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_posts(posts):
    with open('posts.json', 'w') as f:
        json.dump(posts, f)

if __name__ == '__main__':
    app.run(port=8080)
```

**Installation:**
```bash
pkg install python
pip install flask

# Create your app
nano bulletin_board.py
# Paste code above

# Run it
python bulletin_board.py
```

**Tutorials:**
- [Flask with no database](https://iq.opengenus.org/static-webpage-flask-no-database/)
- [Building a message board](https://joalon.se/blog/Building-a-message-board.html)

---

## 3. Calendars & Scheduling

### FullCalendar.js + LocalStorage

**What it is:** JavaScript calendar that saves to browser

**Perfect for:**
- Community event calendar
- Workshop schedules
- Meeting calendars
- Work party schedules

**Why it works:**
- 📅 Beautiful calendar UI
- 💾 Saves to browser's local storage
- 🔌 Fully offline
- 📱 Mobile responsive

**Simple Implementation:**
```html
<!DOCTYPE html>
<html>
<head>
    <script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.10/index.global.min.js'></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
                initialView: 'dayGridMonth',
                events: loadEvents(),
                editable: true,
                eventAdd: function(info) { saveEvent(info.event); },
                eventChange: function(info) { saveEvent(info.event); }
            });
            calendar.render();
        });

        function saveEvent(event) {
            // Save to localStorage
            var events = JSON.parse(localStorage.getItem('events') || '[]');
            events.push({
                title: event.title,
                start: event.start,
                end: event.end
            });
            localStorage.setItem('events', JSON.stringify(events));
        }

        function loadEvents() {
            return JSON.parse(localStorage.getItem('events') || '[]');
        }
    </script>
</head>
<body>
    <div id='calendar'></div>
</body>
</html>
```

**Note:** For offline use, download FullCalendar.js locally instead of using CDN.

**Learn more:** https://fullcalendar.io/

---

## 4. Static Site Generators

### Hugo (Ultra-fast)

**What it is:** Fastest static site generator, written in Go

**Perfect for:**
- Large documentation sites
- Complex community sites
- Multi-language content

**Why it's fast:**
- ⚡ Builds sites in milliseconds
- 📦 Single binary (easy install)
- 🎨 Beautiful themes
- 📚 Great for large sites

**Installation:**
```bash
# Download Hugo binary for Android
pkg install wget
wget https://github.com/gohugoio/hugo/releases/download/v0.122.0/hugo_0.122.0_linux-arm64.tar.gz
tar -xzf hugo_0.122.0_linux-arm64.tar.gz
mv hugo ~/bin/

# Create new site
hugo new site my-community-site
cd my-community-site

# Build
hugo

# Output is in public/ directory
```

**Learn more:** https://gohugo.io/

---

## 5. File Sharing & Management

### Python http.server (You're already using it!)

**What it is:** Simple file server built into Python

**Perfect for:**
- Sharing PDFs, images, documents
- File downloads
- Media library

**Already installed!** Just create directories for organization:

```bash
cd ~/commune-hub
mkdir -p files/{manuals,forms,maps,photos}

# Put files in those folders
# They'll be browseable at http://your-ip:8080/files/
```

---

## 6. Tool Library & Checkout Systems

### Simple JSON-based System

**What it is:** Custom tool tracking with JSON files

**Perfect for:**
- Tool checkout
- Resource lending
- Equipment status

**Simple Example:**
```python
# tools.py - Simple tool library tracker
import json
from datetime import datetime

def load_tools():
    try:
        with open('tools.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def checkout_tool(tool_name, person_name):
    tools = load_tools()
    tools[tool_name] = {
        'checked_out_by': person_name,
        'date': str(datetime.now()),
        'status': 'out'
    }
    with open('tools.json', 'w') as f:
        json.dump(tools, f, indent=2)

def checkin_tool(tool_name):
    tools = load_tools()
    tools[tool_name]['status'] = 'available'
    tools[tool_name]['returned'] = str(datetime.now())
    with open('tools.json', 'w') as f:
        json.dump(tools, f, indent=2)

def list_tools():
    tools = load_tools()
    print("\nTool Status:")
    for tool, info in tools.items():
        print(f"{tool}: {info['status']}")
        if info['status'] == 'out':
            print(f"  → Checked out by: {info['checked_out_by']}")
```

**Make it a web interface** by wrapping in Flask (see bulletin board example above).

---

## 7. Maps & Wayfinding

### Leaflet.js with Offline Tiles

**What it is:** JavaScript map library with offline support

**Perfect for:**
- Community site maps
- Trail maps
- Garden plot maps
- Resource locations

**Why it's good:**
- 🗺️ Powerful mapping
- 📱 Mobile-friendly
- 💾 Works with pre-downloaded tiles
- 🎨 Customizable markers

**Basic Setup:**
```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="leaflet.css" />
    <script src="leaflet.js"></script>
</head>
<body>
    <div id="map" style="height: 500px;"></div>
    <script>
        var map = L.map('map').setView([45.5231, -122.6765], 13);

        // Use offline tiles (pre-downloaded)
        L.tileLayer('tiles/{z}/{x}/{y}.png', {
            maxZoom: 18,
        }).addTo(map);

        // Add markers
        L.marker([45.5231, -122.6765])
            .addTo(map)
            .bindPopup('Tool Shed');
    </script>
</body>
</html>
```

**Download tiles beforehand** using tools like [MapTiler](https://www.maptiler.com/) or Mobile Atlas Creator.

**Learn more:** https://leafletjs.com/

---

## Recommended Combinations

### Minimal Setup (Easiest)
- **TiddlyWiki** for all documentation
- **Static HTML** for announcements (like current template)
- **Python http.server** for file sharing

**Total footprint:** ~10MB

---

### Medium Setup (More Features)
- **MkDocs** for structured docs
- **Simple Flask app** for bulletin board
- **FullCalendar.js** for calendar
- **TiddlyWiki** for personal/working notes

**Total footprint:** ~50MB

---

### Full-Featured Setup (Community Hub)
- **Hugo** for main site
- **TiddlyWiki** for community wiki
- **Custom Flask apps** for:
  - Tool checkout
  - Bulletin board
  - Request/offer board
- **Leaflet maps** for navigation
- **FullCalendar** for scheduling

**Total footprint:** ~100MB

---

## Installation Helpers

### Quick Install Script for Termux

```bash
#!/bin/bash
# install-community-tools.sh

echo "Installing community hub tools..."

# Update packages
pkg update && pkg upgrade -y

# Core tools
pkg install -y python nodejs git wget

# Python tools
pip install flask mkdocs

# Create directories
mkdir -p ~/commune-hub/{wiki,docs,files,apps}

# Download TiddlyWiki
cd ~/commune-hub/wiki
wget https://tiddlywiki.com/empty.html -O community-wiki.html

# Create MkDocs site
cd ~/commune-hub/docs
mkdocs new community-docs

echo "✅ Tools installed!"
echo "📂 Your hub is in ~/commune-hub/"
```

**Save and run:**
```bash
nano install-community-tools.sh
chmod +x install-community-tools.sh
./install-community-tools.sh
```

---

## Resources & Further Reading

### Documentation
- [TiddlyWiki](https://tiddlywiki.com/) - Single-file wiki
- [MkDocs](https://www.mkdocs.org/) - Python documentation generator
- [Hugo](https://gohugo.io/) - Fast static site generator
- [Flask](https://flask.palletsprojects.com/) - Python web framework

### Tutorials
- [Building static sites with Flask (no database)](https://iq.opengenus.org/static-webpage-flask-no-database/)
- [Flask Message Board Tutorial](https://joalon.se/blog/Building-a-message-board.html)
- [FullCalendar Documentation](https://fullcalendar.io/docs)
- [Leaflet.js Tutorials](https://leafletjs.com/examples.html)

### Community
- [Termux Community](https://termux.dev/en/)
- [TiddlyWiki Community](https://talk.tiddlywiki.org/)
- [Self-Hosted Subreddit](https://www.reddit.com/r/selfhosted/)

---

## Next Steps

1. **Start simple** - Pick one tool from the "Minimal Setup"
2. **Test it out** - Make sure it works on your device
3. **Add features gradually** - Only add what you actually need
4. **Document your setup** - Help others replicate it
5. **Share back** - Contribute improvements to the community

---

## Questions to Guide Your Choices

**Ask yourself:**
- What do we use most often? (Start there)
- What causes the most confusion? (Solve that first)
- What would help in an emergency? (Prioritize safety)
- What can we maintain? (Don't over-engineer)
- What matches our skills? (Build on what you know)

---

## Remember

**The best tool is the one you'll actually use and maintain.**

Don't feel pressured to implement everything. Start with static HTML (like the provided template) and add features only when you have a real need.

Community infrastructure should be:
- ✅ Simple enough to maintain
- ✅ Useful enough to use
- ✅ Resilient enough to trust
- ✅ Open enough to adapt

Build what serves your people. 🌱
