# Federated Solarpunk Networks Guide

**Building interoperable resource-sharing networks between community nodes**

When solarpunk communities discover each other, they should be able to **automatically share resources** - tools, food, skills, spaces - using open, standardized protocols. This guide shows you how.

---

## Vision: The Network of Nodes

Imagine:
- **Your tool library** automatically shows available tools from 5 nearby communities
- **Food surplus** in one community triggers alerts to communities with requests
- **Skill directories** federate - "Who knows solar repair within 10 miles?"
- **AI agents** coordinate resource allocation without central control
- **All offline-capable** - works on local mesh networks when internet is down

**This isn't science fiction. The protocols exist. Let's build it.** 🌱

---

## The Open Standards Stack

### Layer 1: Discovery (Who's out there?)
**Protocol:** mDNS/Avahi
**What:** Automatically discover nearby community nodes on local networks

### Layer 2: Communication (How do we talk?)
**Protocol:** ActivityPub
**What:** Send messages and updates between federated communities

### Layer 3: Resource Sharing (What do we have?)
**Protocol:** ValueFlows ⭐ **This is the key!**
**What:** Describe and share economic resources (tools, food, skills, time)

### Layer 4: Coordination (Who gets what?)
**AI Agents:** AutoGen, CrewAI, or custom agents
**What:** Autonomous allocation and coordination without central authority

---

## ValueFlows: The Perfect Protocol ⭐

### What is ValueFlows?

**ValueFlows is a vocabulary for describing economic resource flows in distributed networks.**

It's specifically designed for commons-based, peer-to-peer, and solidarity economy networks. **This is EXACTLY what solarpunk communities need!**

### What You Can Track

ValueFlows can describe:
- 🔧 **Tools** - circular saw, ladder, generator
- 🌾 **Food** - surplus vegetables, bulk grains, seeds
- 💡 **Skills** - solar installation, bike repair, foraging
- ⚡ **Energy** - solar production, battery capacity
- 💧 **Water** - rainwater, well access
- 🏠 **Spaces** - workshop time, event space, kitchen use
- ⏰ **Time** - volunteer hours, skill exchanges
- 🌱 **Everything else** - literally any resource!

### ValueFlows Data Model

```json
{
  "@context": "https://w3id.org/valueflows/ont/vf#",
  "resource": {
    "id": "tool:circular-saw-001",
    "name": "Makita 10\" Circular Saw",
    "resourceClassification": "Power Tool",
    "currentLocation": "Sunnyvale Tool Shed",
    "unit": "item",
    "currentQuantity": 1,
    "accountedFor": "Sunnyvale Solarpunk Hub"
  },
  "availability": {
    "status": "available",
    "availableFrom": "2025-12-16",
    "availableUntil": "2025-12-31",
    "conditions": "Free loan for community members"
  }
}
```

### Real Implementation: Bonfire

**Bonfire** is a federated social network that implements ValueFlows + ActivityPub!

- Federates resources across communities
- Uses same GraphQL API as hREA (Holochain ValueFlows implementation)
- Already working in 2025!

**Website:** https://bonfirenetworks.org/

---

## Discovery: Finding Nearby Nodes

### mDNS/Avahi (Local Network Discovery)

**What it does:** Automatically announces your community node to nearby networks

**How it works:**
1. Your node broadcasts "I'm here!" to local network
2. Other nodes hear it and respond
3. Services are discovered without manual configuration
4. Works on mesh networks!

**Installation on Termux:**
```bash
pkg install avahi

# Configure service
nano ~/.config/avahi/services/solarpunk-node.service
```

**Service Definition:**
```xml
<?xml version="1.0" standalone='no'?>
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name replace-wildcards="yes">Sunnyvale Solarpunk Hub</name>
  <service>
    <type>_solarpunk._tcp</type>
    <port>8080</port>
    <txt-record>version=1.0</txt-record>
    <txt-record>resources=tools,food,skills</txt-record>
    <txt-record>protocol=valueflows</txt-record>
  </service>
</service-group>
```

**Start service:**
```bash
avahi-daemon
```

Now other nodes on your local network will auto-discover you!

**Learn more:** https://avahi.org/

---

## Communication: ActivityPub Federation

### What is ActivityPub?

**The protocol behind Mastodon, used by 1.75M+ users across 6,000+ federated servers in 2025.**

It's how independent servers talk to each other while staying independent.

### How It Works for Solarpunk Nodes

```
[Sunnyvale Hub] ---> ActivityPub ---> [Oakland Hub]
      |                                      |
      v                                      v
 "We have surplus     -->          "We need tomatoes!"
   tomatoes!"
```

**Messages automatically federate** between communities using the same protocol as Mastodon/Fediverse.

### Simple ActivityPub Implementation

You can use existing libraries:

**Python (ActivityPub):**
```bash
pip install activitypub
```

**Example - Announce Surplus Food:**
```python
from activitypub import ActivityPubClient

client = ActivityPubClient("https://sunnyvale-hub.local")

# Announce surplus
activity = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Offer",
    "actor": "https://sunnyvale-hub.local/actor",
    "object": {
        "type": "Note",
        "content": "50 lbs of tomatoes available for pickup",
        "tags": ["#food", "#surplus", "#tomatoes"]
    },
    "to": ["https://oakland-hub.local/followers"]
}

client.post_activity(activity)
```

### Or Use Existing Platforms

**Bonfire** - Already implements ActivityPub + ValueFlows
- Install on your node
- Auto-federates with other Bonfire instances
- Built for commons-based communities

**Learn more:**
- [ActivityPub Spec](https://www.w3.org/TR/activitypub/)
- [ActivityPub Rocks!](https://activitypub.rocks/)
- [Awesome ActivityPub Projects](https://github.com/BasixKOR/awesome-activitypub)

---

## Resource Sharing: ValueFlows API

### GraphQL API for Resource Queries

**Query available tools across federated nodes:**

```graphql
query FindTools {
  economicResources(
    classification: "Power Tools",
    status: "available",
    location: {
      withinRadius: {
        center: {lat: 37.7749, lng: -122.4194},
        distance: 10,
        unit: "miles"
      }
    }
  ) {
    id
    name
    currentLocation
    accountedFor
    availableQuantity
  }
}
```

**Response:**
```json
{
  "data": {
    "economicResources": [
      {
        "id": "sunnyvale:tool:001",
        "name": "Circular Saw",
        "currentLocation": "Sunnyvale Tool Shed",
        "accountedFor": "Sunnyvale Hub",
        "availableQuantity": 1
      },
      {
        "id": "oakland:tool:042",
        "name": "Table Saw",
        "currentLocation": "Oakland Maker Space",
        "accountedFor": "Oakland Hub",
        "availableQuantity": 1
      }
    ]
  }
}
```

### Simple ValueFlows Server (Python)

```python
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load local resources
with open('resources.json', 'r') as f:
    resources = json.load(f)

@app.route('/api/valueflows/resources', methods=['GET'])
def get_resources():
    """Return all available resources in ValueFlows format"""
    classification = request.args.get('classification')

    filtered = resources
    if classification:
        filtered = [r for r in resources
                   if r['resourceClassification'] == classification]

    return jsonify({
        "@context": "https://w3id.org/valueflows/ont/vf#",
        "resources": filtered
    })

@app.route('/api/valueflows/resources/<resource_id>', methods=['GET'])
def get_resource(resource_id):
    """Get specific resource details"""
    resource = next((r for r in resources if r['id'] == resource_id), None)

    if resource:
        return jsonify({
            "@context": "https://w3id.org/valueflows/ont/vf#",
            **resource
        })
    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    app.run(port=8080)
```

**Resources file (resources.json):**
```json
[
  {
    "id": "tool:circular-saw-001",
    "name": "Makita 10\" Circular Saw",
    "resourceClassification": "Power Tools",
    "currentLocation": "Tool Shed",
    "accountedFor": "Sunnyvale Hub",
    "currentQuantity": 1,
    "unit": "item",
    "metadata": {
      "condition": "good",
      "lastMaintenance": "2025-11-01"
    }
  },
  {
    "id": "food:tomatoes-winter",
    "name": "Roma Tomatoes",
    "resourceClassification": "Fresh Produce",
    "currentLocation": "Community Garden",
    "accountedFor": "Sunnyvale Hub",
    "currentQuantity": 50,
    "unit": "lbs",
    "metadata": {
      "harvestDate": "2025-12-15",
      "organic": true
    }
  }
]
```

**Learn more:** https://www.valueflo.ws/

---

## AI Agents: Autonomous Coordination

### Why AI Agents?

Instead of manually coordinating resource sharing:
- **Agents monitor** resource availability across network
- **Agents match** requests with availability
- **Agents negotiate** fair exchanges
- **Agents learn** community patterns and preferences

**No central control. Distributed intelligence.**

### Example: Tool Sharing Agent

```python
from crewai import Agent, Task, Crew

# Define agent
tool_coordinator = Agent(
    role="Tool Library Coordinator",
    goal="Match tool requests with available tools across federated network",
    backstory="""You manage tool sharing across a network of solarpunk
    communities. You know what tools each community has, what's available,
    and who needs what. You optimize for community benefit, not profit.""",
    tools=[
        query_valueflows_api,
        send_activitypub_notification,
        calculate_distance
    ]
)

# Define task
match_request = Task(
    description="""Someone in Oakland needs a circular saw for 3 days.
    Find available circular saws within 10 miles, considering:
    - Distance
    - Current availability
    - Maintenance status
    - Fair distribution (has this community shared recently?)

    Send notification to both communities if match found.""",
    agent=tool_coordinator
)

# Execute
crew = Crew(agents=[tool_coordinator], tasks=[match_request])
result = crew.kickoff()
```

### Multi-Agent Food Network

```python
# Agent 1: Surplus Monitor
surplus_monitor = Agent(
    role="Surplus Food Monitor",
    goal="Track food surplus across all federated gardens",
    tools=[monitor_valueflows_food, check_harvest_calendars]
)

# Agent 2: Need Matcher
need_matcher = Agent(
    role="Food Need Matcher",
    goal="Match surplus with communities that need food",
    tools=[query_food_requests, calculate_nutrition]
)

# Agent 3: Logistics Coordinator
logistics = Agent(
    role="Logistics Coordinator",
    goal="Arrange pickup/delivery between communities",
    tools=[check_transport_availability, optimize_routes]
)

# They work together
food_network = Crew(
    agents=[surplus_monitor, need_matcher, logistics],
    tasks=[monitor_task, match_task, coordinate_task]
)
```

### AI Agent Frameworks

**Best for Solarpunk Networks:**

1. **CrewAI** - Multi-agent collaboration
   - Easy to define roles and goals
   - Agents work together on complex tasks
   - Good for resource coordination

2. **AutoGen** - Conversational agents
   - Agents negotiate with each other
   - Good for complex decision-making

3. **Microsoft Agent Framework** - Enterprise-ready
   - Combines Semantic Kernel + AutoGen
   - Production-ready

**Installation:**
```bash
pip install crewai
# or
pip install autogen
```

**Learn more:**
- [CrewAI Docs](https://docs.crewai.com/)
- [AutoGen](https://microsoft.github.io/autogen/)
- [Top AI Agent Frameworks 2025](https://www.shakudo.io/blog/top-9-ai-agent-frameworks)

---

## Food Sharing Platforms

### Shareish - Open Source Mutual Aid Platform ⭐

**What it is:** Map-based web platform for fostering mutual aid through gift economy

**Features:**
- 🗺️ **Map display** of community resources
- 📍 **Free amenities** - community fridges, food banks, soup kitchens
- 🌳 **Falling fruit** locations
- 🎁 **Gift economy** - donations, free loans
- 📢 **Requests** for goods and services

**Perfect for:** Mapping food sources and mutual aid across federated communities

**Learn more:** https://dl.acm.org/doi/fullHtml/10.1145/3593743.3593790

### Open Food Network

**What it is:** Full-featured online marketplace for farmers and food hubs

**Features:**
- 🌾 Farm-to-community distribution
- 📦 Order management
- 🗓️ Delivery scheduling
- 💰 Payment processing (optional)

**Used by:** 2,500+ enterprises in 15+ countries

**Great for:** Larger-scale food coordination between communities

**Learn more:** https://openfoodnetwork.org/

### Lanka Kitchen API

**What it is:** GraphQL API for community kitchens and ration groups

**Features:**
- 📊 Kitchen operations management
- 🍽️ Meal tracking
- 👥 Community support coordination

**Code:** https://github.com/team-watchdog/lanka-kitchen-api

---

## Complete Architecture Example

### Scenario: Three Federated Communities

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  Sunnyvale Hub      │────▶│   Oakland Hub       │────▶│  Berkeley Hub       │
│                     │◀────│                     │◀────│                     │
│ Tools: 50 items     │     │ Tools: 30 items     │     │ Tools: 40 items     │
│ Food: Tomatoes++    │     │ Food: Greens++      │     │ Food: Apples++      │
│ Skills: Solar, Bikes│     │ Skills: Carpentry   │     │ Skills: Permaculture│
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
         │                            │                            │
         └────────────────────────────┴────────────────────────────┘
                                      │
                              ┌───────▼────────┐
                              │  Shared Index  │
                              │  (ValueFlows)  │
                              │                │
                              │  AI Agents     │
                              │  - Tool Match  │
                              │  - Food Coord  │
                              │  - Skill Find  │
                              └────────────────┘
```

### Technical Stack

**Each Community Hub Runs:**
1. **Web Server** - Python http.server (already have!)
2. **ValueFlows API** - Flask app exposing resources
3. **ActivityPub Server** - For federation messages
4. **mDNS Service** - Auto-discovery on local network
5. **AI Agent** - Coordinating with other communities

**Total Additional Footprint:** ~100-150MB

### Data Flow Example

**1. Sunnyvale has surplus tomatoes:**
```python
# Add to resources.json
{
  "id": "food:tomatoes-2025-12",
  "name": "Roma Tomatoes",
  "currentQuantity": 50,
  "classification": "Fresh Produce",
  "availableFrom": "2025-12-16"
}
```

**2. AI Agent announces via ActivityPub:**
```python
announce_to_federation({
  "type": "Offer",
  "resource": "food:tomatoes-2025-12",
  "quantity": 50,
  "location": "Sunnyvale Hub"
})
```

**3. Oakland's agent sees it, checks needs:**
```python
# Oakland's AI agent
if community_needs("tomatoes") and within_range("Sunnyvale Hub", 10):
    request_resource("food:tomatoes-2025-12", quantity=20)
```

**4. Agents coordinate pickup:**
```python
logistics_agent.coordinate({
  "from": "Sunnyvale Hub",
  "to": "Oakland Hub",
  "resource": "tomatoes",
  "quantity": 20,
  "method": "community_van"  # Someone driving to Oakland anyway
})
```

**5. Transaction recorded in ValueFlows:**
```json
{
  "type": "Transfer",
  "resource": "food:tomatoes-2025-12",
  "quantity": 20,
  "from": "Sunnyvale Hub",
  "to": "Oakland Hub",
  "date": "2025-12-16",
  "reciprocity": "gift"  # or "trade", "loan", etc.
}
```

---

## Implementation Roadmap

### Phase 1: Single Node (Current)
- ✅ Static HTML community hub
- ✅ Local tool library (HTML pages)
- ✅ Food surplus announcements (manual)

### Phase 2: ValueFlows API (Next)
- 📝 Create resources.json
- 🔧 Flask API exposing ValueFlows endpoints
- 📊 Track tools, food, skills in standard format

### Phase 3: Local Discovery
- 📡 Install Avahi/mDNS
- 🔍 Auto-discover nearby nodes
- 🤝 Manual federation with nearby communities

### Phase 4: ActivityPub Federation
- 💬 Implement ActivityPub server
- 🌐 Federate with remote communities
- 📢 Broadcast announcements across network

### Phase 5: AI Coordination
- 🤖 Deploy basic matching agents
- 🧠 Learn community patterns
- ⚖️ Optimize resource allocation

### Phase 6: Full Network
- 🌍 Federation with national/global solarpunk network
- 🔄 Reciprocity tracking and time banking
- 📈 Collective intelligence and learning

---

## Quick Start: Add ValueFlows to Your Hub

### 1. Create Resource Inventory

```bash
cd ~/commune-hub
nano resources.json
```

**Add your resources in ValueFlows format:**
```json
[
  {
    "id": "tool:ladder-001",
    "name": "8ft Extension Ladder",
    "resourceClassification": "Tools",
    "currentLocation": "Tool Shed",
    "currentQuantity": 1,
    "unit": "item",
    "status": "available"
  }
]
```

### 2. Create Simple API

```bash
nano valueflows_api.py
```

```python
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/resources')
def get_resources():
    with open('resources.json', 'r') as f:
        resources = json.load(f)
    return jsonify({
        "@context": "https://w3id.org/valueflows/ont/vf#",
        "resources": resources
    })

if __name__ == '__main__':
    app.run(port=8081)
```

### 3. Install and Run

```bash
pkg install python
pip install flask

# Run API
python valueflows_api.py &

# Now accessible at http://your-ip:8081/api/resources
```

### 4. Test It

```bash
curl http://localhost:8081/api/resources
```

**Congratulations!** Your community hub now speaks ValueFlows! 🎉

Other communities can now query your resources programmatically.

---

## Resources & Further Reading

### Protocols & Standards
- [ValueFlows Specification](https://www.valueflo.ws/specification/spec-overview/) - REA-based economic resource protocol
- [ActivityPub W3C Spec](https://www.w3.org/TR/activitypub/) - Decentralized social networking protocol
- [Avahi mDNS](https://avahi.org/) - Local network service discovery
- [Awesome ActivityPub](https://github.com/BasixKOR/awesome-activitypub) - Projects using ActivityPub

### Implementations
- [Bonfire Networks](https://bonfirenetworks.org/) - Federated app with ValueFlows
- [hREA](https://github.com/h-rea/hrea) - ValueFlows on Holochain
- [Open Food Network](https://openfoodnetwork.org/) - Food distribution platform
- [Shareish](https://dl.acm.org/doi/fullHtml/10.1145/3593743.3593790) - Mutual aid mapping platform

### AI Agents
- [Top 9 AI Agent Frameworks](https://www.shakudo.io/blog/top-9-ai-agent-frameworks) - Comparison guide
- [CrewAI Documentation](https://docs.crewai.com/) - Multi-agent collaboration
- [Microsoft Agent Framework](https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/) - Production-ready framework
- [Multi-Agent Resource Allocation](https://arxiv.org/html/2504.02051v1) - Research paper

### Community Projects
- [P2P Foundation: Value Flows](https://wiki.p2pfoundation.net/Value_Flows_Vocabulary) - Background and philosophy
- [ReflowOS ValueFlows Docs](https://reflowos.dyne.org/docs/valueflows/) - Implementation guide
- [Lanka Kitchen API](https://github.com/team-watchdog/lanka-kitchen-api) - Community kitchen coordination

---

## Example: Complete Federated Setup

### Directory Structure
```
~/commune-hub/
├── index.html                 # Main hub page
├── resources.json            # ValueFlows resource inventory
├── valueflows_api.py         # Resource API
├── activitypub_server.py     # Federation server
├── ai_agents/
│   ├── tool_coordinator.py   # Tool matching agent
│   ├── food_coordinator.py   # Food sharing agent
│   └── skill_finder.py       # Skill directory agent
└── config/
    └── avahi/
        └── solarpunk-node.service  # mDNS announcement
```

### Automated Setup Script

```bash
#!/bin/bash
# setup-federated-node.sh

echo "Setting up federated solarpunk node..."

# Install dependencies
pkg install python avahi
pip install flask activitypub crewai

# Create directory structure
mkdir -p ~/commune-hub/ai_agents
mkdir -p ~/commune-hub/config/avahi

# Create initial resources
cat > ~/commune-hub/resources.json <<EOF
[
  {
    "id": "node:info",
    "name": "Community Hub Info",
    "type": "CommunityNode",
    "location": "Update with your location",
    "contact": "Update with contact info"
  }
]
EOF

# Create ValueFlows API
cat > ~/commune-hub/valueflows_api.py <<'EOF'
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/api/resources')
def get_resources():
    with open('resources.json', 'r') as f:
        return jsonify({
            "@context": "https://w3id.org/valueflows/ont/vf#",
            "resources": json.load(f)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
EOF

# Create mDNS service
cat > ~/commune-hub/config/avahi/solarpunk-node.service <<EOF
<?xml version="1.0" standalone='no'?>
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
  <name replace-wildcards="yes">Solarpunk Node %h</name>
  <service>
    <type>_solarpunk._tcp</type>
    <port>8081</port>
    <txt-record>protocol=valueflows</txt-record>
  </service>
</service-group>
EOF

echo "✅ Setup complete!"
echo "Edit resources.json to add your community's resources"
echo "Run: python valueflows_api.py to start the API"
```

**Run it:**
```bash
chmod +x setup-federated-node.sh
./setup-federated-node.sh
```

---

## The Future: Global Solarpunk Network

Imagine a world where:

- 🌍 **Thousands of community hubs** federated worldwide
- 🤝 **Resources flow** where they're needed most
- 🧠 **AI agents coordinate** without central control
- 💚 **Gift economy** replaces extractive capitalism
- 🔧 **Tools travel** through community networks
- 🌱 **Food abundance** is shared, not wasted
- 🎓 **Skills and knowledge** flow freely
- 🌐 **No corporations** - just communities helping communities

**This is what open protocols enable.**

**This is what decentralized technology makes possible.**

**This is the solarpunk future we're building.** ✊🌱

---

## Start Small, Dream Big

**You don't need to implement everything at once:**

1. ✅ **Start:** Static HTML hub (you have this!)
2. 📊 **Add:** Resources inventory (resources.json)
3. 🔌 **Expose:** ValueFlows API (simple Flask app)
4. 🤝 **Connect:** One neighboring community
5. 🤖 **Automate:** Basic AI agent for one use case
6. 🌐 **Expand:** Join the federated network

**Each step makes your community more resilient, more connected, more powerful.**

---

## Questions to Guide Your Implementation

**Ask your community:**
- What resources do we have to share?
- What do we need from other communities?
- Who are our nearest neighbor communities?
- What would make our lives easier?
- What would make us more resilient?

**The answers will tell you where to start.**

---

## Remember

**Technology is just a tool. Community is the foundation.**

Build what serves your people. Share what helps others. Connect when it makes sense. Stay local, think global.

**Together, we're building the infrastructure for a better world.** 🌱✊

---

*This guide is a living document. As you implement these technologies, please share what you learn. Let's build this network together.*
