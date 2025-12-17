# Community Hub Website Template

**Easy-to-edit website for your community information node**

This template is designed for people who are NOT comfortable with HTML. You can edit it in any simple text editor!

---

## What's Included

**Website Files:**
- `index.html` - Homepage (START HERE)
- `emergency.html` - Emergency contacts and procedures
- `skills.html` - Community skills directory
- `tools.html` - Tool library and resources
- `maps.html` - Local maps and wayfinding
- `mutual-aid.html` - Mutual aid protocols
- `style.css` - Colors and design (optional to edit)

**Federation & API Tools:**
- `valueflows_api.py` - REST API server exposing your resources (ValueFlows protocol)
- `search_network.py` - Search tools/food/skills across federated communities
- `resources.json` - Your community's resource inventory (tools, food, skills)
- `federation.json` - List of connected community hubs in your network

**Guides:**
- `README.md` - This file (editing guide)
- `Solarpunk Node Content Ideas.md` - Comprehensive list of what to include
- `Open Source Community Tools Guide.md` - ⭐ **Advanced tools for expanding your hub**
- `Federated Solarpunk Networks Guide.md` - 🌐 **Connect with other communities using open protocols**
- `Conversational Resource Agents Guide.md` - 🤖 **Make your network conversational with AI agents + MCP**

---

## How to Use This Template

### Step 1: Copy All Files

Copy all these files to your phone's web directory:
- **Android:** `~/commune-hub/`
- **iOS:** Your designated folder in Files app

### Step 2: Edit in a Simple Text Editor

**On Android (Termux):**
```bash
cd ~/commune-hub
nano index.html
```

**On Computer (then transfer to phone):**
- **Windows:** Use Notepad
- **Mac:** Use TextEdit (Format → Make Plain Text first!)
- **Any OS:** VS Code, Sublime Text, or any text editor

**On iOS:**
- Use the "Files" app
- Or edit on computer and sync via iCloud/Dropbox

### Step 3: Find and Replace

Look for text in `[BRACKETS]` - that's what you replace!

Example:
```html
<h1>[YOUR COMMUNITY NAME]</h1>
```

Change to:
```html
<h1>Sunset Eco-Village</h1>
```

### Step 4: Save and Reload

After editing:
1. Save the file
2. Reload your browser (if server is running)
3. See your changes!

---

## Quick Editing Guide

### To Change Your Community Name

Find this in `index.html`:
```html
<h1>[YOUR COMMUNITY NAME]</h1>
```

Replace with:
```html
<h1>Your Actual Community Name</h1>
```

### To Add Emergency Contacts

Find this in `emergency.html`:
```html
<li><strong>Fire/Medical Emergency:</strong> 911</li>
<li><strong>Community Medic:</strong> [NAME] - [PHONE]</li>
```

Replace with real info:
```html
<li><strong>Fire/Medical Emergency:</strong> 911</li>
<li><strong>Community Medic:</strong> Alex Rivera - (555) 123-4567</li>
```

### To Add Skills

Find this in `skills.html`:
```html
<li><strong>[NAME]</strong> - [SKILLS]</li>
```

Add as many as you want:
```html
<li><strong>Jordan Chen</strong> - Solar panel repair, bike mechanics</li>
<li><strong>Sam Martinez</strong> - Foraging expert, mushroom cultivation</li>
<li><strong>Alex Kim</strong> - Welding, metalwork, tool repair</li>
```

### To Change Colors

Open `style.css` and find:
```css
--primary-color: #2c5f2d; /* Main green color */
```

Change the `#2c5f2d` to any color you want!

**Common colors:**
- Green: `#2c5f2d`
- Blue: `#2c5f9d`
- Purple: `#5f2c9d`
- Orange: `#d97706`
- Red: `#dc2626`

---

## Common Mistakes (And How to Fix)

### Mistake 1: Forgetting to Close Tags

❌ **Wrong:**
```html
<li>Solar panel repair
<li>Bike mechanics
```

✅ **Right:**
```html
<li>Solar panel repair</li>
<li>Bike mechanics</li>
```

Every `<tag>` needs a `</tag>` to close it!

### Mistake 2: Breaking the Quotes

❌ **Wrong:**
```html
<a href="emergency.html>Emergency</a>
```

✅ **Right:**
```html
<a href="emergency.html">Emergency</a>
```

Make sure quotes are closed: `" "` not `" >`

### Mistake 3: Deleting Important Structural Stuff

Only edit the text BETWEEN tags, not the tags themselves!

❌ **Don't delete:**
```html
<!DOCTYPE html>
<html>
<head>
```

✅ **Do edit:**
```html
<h1>[YOUR TEXT HERE]</h1>
```

---

## Don't Know HTML? No Problem!

### Use Claude to Help You Edit

**Prompt for Claude:**
```
I have this HTML file for my community hub. I want to:
- [Describe what you want to change]

Here's the current code:
[Paste the relevant section]

Can you show me exactly what to change it to?
```

**Example:**
```
I have this HTML file for my community hub. I want to add a section about our tool library with these tools:
- Circular saw (Alex has it)
- Cordless drill (Available in shed)
- Ladder (Jordan borrowed it)

Here's the current code:
<ul>
  <li>[TOOL NAME] - [STATUS]</li>
</ul>

Can you show me exactly what to change it to?
```

Claude will give you the exact code to use!

---

## File Descriptions

### index.html (Homepage)
**What it is:** The first page people see
**What to edit:**
- Community name
- Welcome message
- Quick links to other pages
- Important announcements

**Don't touch:**
- The `<head>` section
- The `<link>` to style.css
- The closing `</html>` tag

---

### emergency.html (Emergency Info)
**What it is:** Emergency contacts and procedures
**What to edit:**
- Emergency contact names and numbers
- Community-specific emergency procedures
- Rally point locations
- Medical supply locations

**Suggested content:**
- 911 or local emergency number
- Community medic/first aider
- Fire safety procedures
- Evacuation routes
- Severe weather protocols
- Emergency meeting locations

---

### skills.html (Skills Directory)
**What it is:** Who knows what in your community
**What to edit:**
- Names of community members
- Their skills and expertise
- How to contact them (optional)

**Example skills:**
- Repair: bike repair, phone repair, appliance repair
- Building: carpentry, welding, electrical, plumbing
- Growing: gardening, seed saving, permaculture
- Healing: first aid, herbalism, massage
- Teaching: any subject area expertise
- Making: sewing, knitting, crafts

---

### tools.html (Tool Library)
**What it is:** Shared community tools and resources
**What to edit:**
- List of available tools
- Where they're located
- Who has them checked out
- How to borrow them

**Example tools:**
- Hand tools: hammers, saws, screwdrivers
- Power tools: drill, circular saw, sander
- Garden tools: shovels, rakes, wheelbarrow
- Specialized: ladder, chainsaw, generator
- Other: camping gear, party supplies, tables

---

### maps.html (Local Maps)
**What it is:** Offline maps of your area
**What to edit:**
- Description of your area
- Links to map images
- Important landmarks
- Instructions for using maps

**How to add actual maps:**
1. Download map images (OpenStreetMap, Google Maps screenshot, hand-drawn)
2. Save as `map-overview.jpg`, `map-trails.jpg`, etc.
3. Reference in HTML:
   ```html
   <img src="map-overview.jpg" alt="Community overview map">
   ```

---

### mutual-aid.html (Mutual Aid Protocols)
**What it is:** How community members help each other
**What to edit:**
- Types of aid offered
- How to request help
- How to offer help
- Community agreements

**Suggested content:**
- Food sharing
- Childcare cooperation
- Ride sharing
- Tool/resource lending
- Skill exchanges
- Time banking
- Emergency support

---

## Advanced Customization (Optional)

### Add a New Page

1. **Copy an existing page:**
   ```bash
   cp emergency.html garden.html
   ```

2. **Edit the content** in your new page

3. **Add link from homepage:**
   ```html
   <li><a href="garden.html">Garden Info</a></li>
   ```

### Add Images

1. **Add image file** to your commune-hub folder

2. **Reference in HTML:**
   ```html
   <img src="photo.jpg" alt="Description of photo">
   ```

3. **Keep images small** (phone storage is limited!)
   - Use JPEG for photos
   - Keep under 500KB each if possible

### Add a Section

Copy this block and paste it where you want a new section:
```html
<div class="card">
    <h2>Your Section Title</h2>
    <p>Your content here</p>
</div>
```

---

## Testing Your Changes

1. **Save your edited file**
2. **Make sure server is running:**
   ```bash
   python -m http.server 8080
   ```
3. **Open browser on phone:** http://localhost:8080
4. **See your changes!**
5. **Not seeing changes?** Refresh the page (pull down or F5)

---

## Getting Help

**If you get stuck:**

1. **Check your changes** - Did you break a tag? Miss a quote?
2. **Look at the original template** - Compare to what you changed
3. **Ask Claude:**
   ```
   I'm editing my community hub website and something broke.

   Here's what I changed:
   [Paste your edited section]

   Now the page shows [describe problem].

   Can you help me fix it?
   ```
4. **Ask facilitator** or post in community Matrix space

---

## Tips for Non-Technical Editors

### Start Small
- Edit one page at a time
- Change small bits of text first
- Test after each change
- Build confidence gradually

### Use Find-and-Replace
Most text editors have Find-and-Replace:
- Find: `[YOUR COMMUNITY NAME]`
- Replace: `Sunset Eco-Village`
- Replace All!

### Make a Backup
Before big changes:
```bash
cp index.html index-backup.html
```

If you break something, restore:
```bash
cp index-backup.html index.html
```

### Don't Panic!
- HTML files are just text
- You can always undo changes
- We have the original template
- Mistakes are how you learn!

---

## Checklist: Customizing Your Hub

- [ ] Change community name on all pages
- [ ] Add real emergency contacts (emergency.html)
- [ ] List at least 5 community skills (skills.html)
- [ ] Add available tools/resources (tools.html)
- [ ] Add map info or images (maps.html)
- [ ] Document mutual aid practices (mutual-aid.html)
- [ ] Test all pages load correctly
- [ ] Check all links work
- [ ] Show to someone for feedback
- [ ] Celebrate! You customized a website!

---

## Using the Federation Tools

Once you've customized your hub, you can connect with other communities!

### 1. Edit Your Resource Inventory

Edit `resources.json` with your actual tools, food, and skills:

```bash
nano resources.json
```

Example:
```json
{
  "id": "tool:ladder-001",
  "name": "8ft Extension Ladder",
  "type": "tool",
  "classification": "Tools",
  "currentLocation": "Tool Shed",
  "status": "available",
  "currentQuantity": 1
}
```

### 2. Start the API Server

```bash
# Install Flask first
pip install flask

# Run the API
python valueflows_api.py
```

Your resources are now available at: `http://your-ip:8081/api/resources`

### 3. Add Other Communities to Federation

Edit `federation.json` with hubs you want to connect with:

```json
{
  "nodes": [
    {
      "name": "Your Community Hub",
      "url": "http://localhost:8081"
    },
    {
      "name": "Friend's Hub",
      "url": "http://192.168.1.100:8081"
    }
  ]
}
```

### 4. Search the Network

```bash
# Search all resources
python search_network.py

# Search only tools
python search_network.py --type tool

# Search for specific item
python search_network.py --query ladder
```

**That's it! You're now part of a federated solarpunk network!** 🌱🌐

---

## Ready to Go Beyond the Basics?

### Expand Your Single Hub

Check out **[Open Source Community Tools Guide.md](Open%20Source%20Community%20Tools%20Guide.md)** for:

**Advanced Features:**
- 📚 **TiddlyWiki** - Entire wiki in a single HTML file
- 📝 **Bulletin boards** - Simple message boards with Python
- 📅 **Interactive calendars** - Event scheduling with JavaScript
- 🗺️ **Maps** - Offline mapping with Leaflet.js
- 🔧 **Tool checkout systems** - Track community resources

**All recommendations are:**
- ✅ Free and open source
- ✅ Lightweight (work on phones!)
- ✅ Offline-capable
- ✅ No heavy dependencies (no PHP, no databases)
- ✅ Easy to install in Termux

### Connect with Other Communities 🌐

Check out **[Federated Solarpunk Networks Guide.md](Federated%20Solarpunk%20Networks%20Guide.md)** to:

**Build the Network:**
- 🤝 **Share resources** between communities (tools, food, skills)
- 🔍 **Auto-discover** nearby nodes on local networks
- 🌍 **Federate** with remote communities using open protocols
- 🤖 **AI agents** coordinate resource allocation automatically
- 📡 **Open standards** - ValueFlows, ActivityPub, mDNS

### Make It Conversational 🤖

Check out **[Conversational Resource Agents Guide.md](Conversational%20Resource%20Agents%20Guide.md)** to:

**Add Natural Language Interface:**
- 💬 **"Find me a ladder"** - No browsing needed!
- 🗣️ **Voice interface** - Talk to your community network
- 🤏 **Tiny agents** - smolagents runs on phones (1.7B-3B models)
- 🔧 **MCP integration** - Standard tools that agents can use
- 🌐 **Federated queries** - Search across all connected communities

**Make the network accessible to everyone, not just programmers!**

Start simple with this template, then expand when you're ready!

---

## You've Got This!

**Remember:**
- You don't need to be a programmer
- Just change the text in [brackets]
- Test often to catch mistakes early
- Use Claude when you're stuck
- Ask for help when you need it

**This template is designed to be edited by humans, not just coders.**

You're building community infrastructure. That's amazing.

Now go make it yours! 🌱
