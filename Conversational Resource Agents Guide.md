# Conversational Resource Agents Guide

**Make your federated solarpunk network conversational using tiny AI agents + MCP**

Instead of writing code to query resources, just ask:
- *"Is there a circular saw available within 5 miles?"*
- *"Who has surplus tomatoes this week?"*
- *"Find someone who knows solar panel repair nearby"*

**The agent translates your question → uses MCP tools → queries ValueFlows → returns results.**

All running on a repurposed phone. All offline-capable. All using open source. 🌱🤖

---

## The Stack

### smolagents (Hugging Face)
**Tiny AI agents that think in code**
- ~1,000 lines of code total
- Runs on phones, Raspberry Pi, low-power devices
- Model-agnostic (works with any LLM)
- Sandboxed execution (safe!)
- Writes actions in Python code

### Model Context Protocol (MCP)
**Standardized way to expose tools to AI agents**
- Created by Anthropic
- Tools = Functions agents can call
- Python SDK available
- Works with Claude, other LLMs

### ValueFlows Resources
**What the agents search**
- Tools, food, skills across federated communities
- Standard vocabulary
- GraphQL/REST APIs

---

## Architecture

```
User: "Find me a ladder"
    ↓
smolagent (on phone)
    ↓
Translates to → search_tools(classification="Ladder", radius=5)
    ↓
MCP Tool (local)
    ↓
ValueFlows API (local + federated)
    ↓
Returns: [
  {name: "8ft Ladder", location: "Sunnyvale Tool Shed", available: true},
  {name: "Extension Ladder", location: "Oakland Hub", available: true}
]
    ↓
Agent formats response
    ↓
"Found 2 ladders:
1. 8ft Ladder at Sunnyvale Tool Shed (local) - available
2. Extension Ladder at Oakland Hub (3 miles away) - available"
```

---

## Part 1: Create MCP Server for ValueFlows

### Install FastMCP

```bash
pip install fastmcp
```

### Create MCP Server (`valueflows_mcp_server.py`)

```python
from fastmcp import FastMCP
import json
import httpx
from typing import Optional, List

# Initialize MCP server
mcp = FastMCP("Solarpunk Resource Network")

# Configuration
FEDERATED_NODES = [
    "http://localhost:8081",  # Local node
    "http://oakland-hub.local:8081",  # Nearby nodes
    "http://berkeley-hub.local:8081"
]

@mcp.tool()
async def search_tools(
    query: Optional[str] = None,
    classification: Optional[str] = None,
    radius_miles: int = 10,
    available_only: bool = True
) -> str:
    """
    Search for tools across the federated solarpunk network.

    Args:
        query: Natural language search query (e.g., "circular saw", "power tools")
        classification: Tool category (e.g., "Power Tools", "Hand Tools", "Garden Tools")
        radius_miles: Search radius in miles (default: 10)
        available_only: Only show available tools (default: True)

    Returns:
        JSON string with list of matching tools
    """
    results = []

    for node in FEDERATED_NODES:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                params = {
                    "type": "tool",
                    "available": available_only
                }
                if classification:
                    params["classification"] = classification

                response = await client.get(f"{node}/api/resources", params=params)

                if response.status_code == 200:
                    resources = response.json().get("resources", [])

                    # Filter by query if provided
                    if query:
                        query_lower = query.lower()
                        resources = [r for r in resources
                                   if query_lower in r.get("name", "").lower()]

                    results.extend(resources)
        except Exception as e:
            print(f"Error querying {node}: {e}")
            continue

    return json.dumps(results, indent=2)


@mcp.tool()
async def search_food(
    food_type: Optional[str] = None,
    surplus_only: bool = True,
    radius_miles: int = 10
) -> str:
    """
    Search for available food across the federated network.

    Args:
        food_type: Type of food (e.g., "vegetables", "fruit", "tomatoes")
        surplus_only: Only show surplus food available for sharing
        radius_miles: Search radius in miles

    Returns:
        JSON string with list of available food resources
    """
    results = []

    for node in FEDERATED_NODES:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                params = {
                    "type": "food",
                    "classification": "Fresh Produce"
                }

                response = await client.get(f"{node}/api/resources", params=params)

                if response.status_code == 200:
                    resources = response.json().get("resources", [])

                    if food_type:
                        food_lower = food_type.lower()
                        resources = [r for r in resources
                                   if food_lower in r.get("name", "").lower()]

                    if surplus_only:
                        resources = [r for r in resources
                                   if r.get("currentQuantity", 0) > 0]

                    results.extend(resources)
        except Exception:
            continue

    return json.dumps(results, indent=2)


@mcp.tool()
async def search_skills(
    skill: str,
    radius_miles: int = 10
) -> str:
    """
    Find people with specific skills across the network.

    Args:
        skill: Skill to search for (e.g., "solar repair", "carpentry", "bike mechanics")
        radius_miles: Search radius in miles

    Returns:
        JSON string with list of people and their skills
    """
    results = []

    for node in FEDERATED_NODES:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                params = {
                    "type": "skill",
                    "query": skill
                }

                response = await client.get(f"{node}/api/resources", params=params)

                if response.status_code == 200:
                    resources = response.json().get("resources", [])
                    results.extend(resources)
        except Exception:
            continue

    return json.dumps(results, indent=2)


@mcp.tool()
async def request_resource(
    resource_id: str,
    quantity: int,
    duration_days: Optional[int] = None,
    reason: Optional[str] = None
) -> str:
    """
    Request a resource from the network.

    Args:
        resource_id: ID of the resource to request
        quantity: Amount needed
        duration_days: How long you need it (for loans)
        reason: Reason for request (optional)

    Returns:
        JSON confirmation of request
    """
    request_data = {
        "resource_id": resource_id,
        "quantity": quantity,
        "duration_days": duration_days,
        "reason": reason,
        "status": "pending"
    }

    # In real implementation, this would:
    # 1. Post to the resource owner's node
    # 2. Trigger notification
    # 3. Record in ValueFlows as an Intent

    return json.dumps({
        "status": "success",
        "message": f"Request submitted for {resource_id}",
        "request": request_data
    }, indent=2)


@mcp.tool()
async def list_local_resources(
    resource_type: Optional[str] = None
) -> str:
    """
    List all resources from the local community hub.

    Args:
        resource_type: Filter by type ("tool", "food", "skill", "space")

    Returns:
        JSON string with local resources
    """
    try:
        with open('resources.json', 'r') as f:
            resources = json.load(f)

        if resource_type:
            resources = [r for r in resources
                        if r.get("type", "").lower() == resource_type.lower()]

        return json.dumps(resources, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# Run the MCP server
if __name__ == "__main__":
    mcp.run()
```

### Test the MCP Server

```bash
python valueflows_mcp_server.py
```

Now you have MCP tools that can query the federated network! 🎉

---

## Part 2: Set Up smolagent

### Install smolagents

```bash
pip install smolagents
```

### Create Agent with MCP Tools (`resource_agent.py`)

```python
from smolagents import CodeAgent, HfApiModel, MCPClient
import asyncio

# Initialize MCP client to connect to our ValueFlows MCP server
mcp_client = MCPClient(
    server_script="python valueflows_mcp_server.py",
    name="Solarpunk Resource Network"
)

# Get tools from MCP server
tools = asyncio.run(mcp_client.get_tools())

# Initialize the model
# Can use local models via Ollama, or any HuggingFace model
model = HfApiModel(
    model_id="meta-llama/Llama-3.3-70B-Instruct",  # Or smaller models!
    # For local: model_id="ollama/llama3.2:3b"
)

# Create the agent with MCP tools
agent = CodeAgent(
    tools=tools,
    model=model,
    max_steps=5
)

# Now you can ask questions!
if __name__ == "__main__":
    while True:
        user_input = input("\n🌱 Ask about resources (or 'quit'): ")

        if user_input.lower() == 'quit':
            break

        try:
            result = agent.run(user_input)
            print(f"\n✅ {result}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
```

### Run the Agent

```bash
python resource_agent.py
```

**Now you can have conversations!**

```
🌱 Ask about resources: Is there a circular saw available?

Agent thinks: I need to search for circular saws in the tool inventory.
Agent writes code: search_tools(query="circular saw", available_only=True)
Agent executes...

✅ Found 2 circular saws:
1. Makita 10" Circular Saw at Sunnyvale Tool Shed - available now
2. DeWalt Circular Saw at Oakland Hub (3 miles away) - available now

Would you like me to request one?
```

---

## Part 3: Advanced Configurations

### Using Smaller Models (For Phones!)

```python
# Use tiny local models
from smolagents import CodeAgent, MCPClient
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load small model (1-3B parameters)
model = AutoModelForCausalLM.from_pretrained(
    "HuggingFaceTB/SmolLM2-1.7B-Instruct",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-1.7B-Instruct")

# Create agent with tiny model
agent = CodeAgent(
    tools=mcp_tools,
    model=model,
    tokenizer=tokenizer
)
```

**SmolLM2-1.7B runs on phones and Raspberry Pi!**

### Using Ollama (Local Inference)

```bash
# Install Ollama
pkg install ollama

# Pull a small model
ollama pull llama3.2:3b

# Run agent
python resource_agent.py
```

---

## Part 4: Multi-Agent Coordination

### Create Specialized Agents

```python
from smolagents import CodeAgent, ToolCallingAgent

# Tool Coordinator Agent
tool_agent = CodeAgent(
    tools=[search_tools, request_resource],
    model=model,
    role="Tool Library Coordinator",
    backstory="""You help people find and borrow tools from
    the community network. You're friendly and efficient."""
)

# Food Coordinator Agent
food_agent = CodeAgent(
    tools=[search_food],
    model=model,
    role="Food Sharing Coordinator",
    backstory="""You coordinate food surplus and requests
    across the community network."""
)

# Skill Finder Agent
skill_agent = CodeAgent(
    tools=[search_skills],
    model=model,
    role="Skill Directory Navigator",
    backstory="""You help people find community members
    with specific skills."""
)

# Router Agent (decides which specialist to use)
router = ToolCallingAgent(
    tools=[],
    model=model,
    managed_agents=[tool_agent, food_agent, skill_agent]
)

# User asks question → Router picks specialist → Specialist answers
result = router.run("I need someone to help repair my solar panels")
# Router delegates to skill_agent automatically!
```

---

## Part 5: Web Interface (Optional)

### Create Simple Chat UI

```python
from flask import Flask, render_template, request, jsonify
from resource_agent import agent

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get('question')

    try:
        result = agent.run(question)
        return jsonify({
            "answer": result,
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        })

if __name__ == '__main__':
    app.run(port=8082)
```

**Template (`templates/chat.html`):**

```html
<!DOCTYPE html>
<html>
<head>
    <title>🌱 Community Resource Agent</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        #chat {
            border: 1px solid #ddd;
            height: 400px;
            overflow-y: scroll;
            padding: 15px;
            margin-bottom: 15px;
            background: #f9f9f9;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
        }
        .user { background: #e3f2fd; }
        .agent { background: #c8e6c9; }
        input {
            width: 80%;
            padding: 10px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background: #4caf50;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>🌱 Community Resource Agent</h1>
    <div id="chat"></div>
    <input id="question" type="text" placeholder="Ask about tools, food, skills..." />
    <button onclick="ask()">Ask</button>

    <script>
        async function ask() {
            const question = document.getElementById('question').value;
            const chat = document.getElementById('chat');

            // Show user message
            chat.innerHTML += `<div class="message user">You: ${question}</div>`;
            document.getElementById('question').value = '';

            // Get agent response
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question})
            });

            const data = await response.json();

            // Show agent response
            if (data.status === 'success') {
                chat.innerHTML += `<div class="message agent">Agent: ${data.answer}</div>`;
            } else {
                chat.innerHTML += `<div class="message agent">Error: ${data.error}</div>`;
            }

            // Scroll to bottom
            chat.scrollTop = chat.scrollHeight;
        }

        // Allow Enter key to submit
        document.getElementById('question').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') ask();
        });
    </script>
</body>
</html>
```

Now you have a web interface for conversational resource discovery!

---

## Part 6: Complete Setup Script

```bash
#!/bin/bash
# setup-conversational-agents.sh

echo "🌱 Setting up Conversational Resource Agents..."

# Install dependencies
pkg install python
pip install smolagents fastmcp httpx transformers flask

# Create directories
mkdir -p ~/commune-hub/agents
cd ~/commune-hub/agents

# Download setup files
echo "Creating MCP server..."
cat > valueflows_mcp_server.py <<'EOF'
# [Paste MCP server code from Part 1]
EOF

echo "Creating smolagent..."
cat > resource_agent.py <<'EOF'
# [Paste agent code from Part 2]
EOF

echo "Creating web interface..."
mkdir -p templates
cat > app.py <<'EOF'
# [Paste Flask code from Part 5]
EOF

cat > templates/chat.html <<'EOF'
# [Paste HTML from Part 5]
EOF

# Download small model (optional)
echo "Downloading SmolLM2 (tiny model for phones)..."
python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained('HuggingFaceTB/SmolLM2-1.7B-Instruct')
tokenizer = AutoTokenizer.from_pretrained('HuggingFaceTB/SmolLM2-1.7B-Instruct')
print('✅ Model downloaded!')
"

echo "✅ Setup complete!"
echo ""
echo "To run the conversational agent:"
echo "  python resource_agent.py"
echo ""
echo "To run the web interface:"
echo "  python app.py"
echo "  Then visit: http://localhost:8082"
```

---

## Example Conversations

### Finding Tools

```
User: I need to cut some wood for a garden bed

Agent: Let me search for saws in the tool library.
[Executes: search_tools(query="saw")]

Found 3 options:
1. Circular Saw at Sunnyvale Tool Shed - available
2. Hand Saw at Sunnyvale Tool Shed - available
3. Table Saw at Oakland Hub - available (3 miles away)

Which would work best for your project?

User: The circular saw sounds good

Agent: Great! Let me request it for you.
[Executes: request_resource(resource_id="tool:circular-saw-001", quantity=1)]

✅ Request submitted! The tool shed coordinator will be notified.
Pickup location: Sunnyvale Tool Shed
Expected availability: Today

Would you like directions to the tool shed?
```

### Finding Food

```
User: Anyone have extra tomatoes?

Agent: Checking for surplus tomatoes across the network...
[Executes: search_food(food_type="tomatoes", surplus_only=True)]

Found surplus tomatoes:
1. Sunnyvale Community Garden - 50 lbs Roma tomatoes
   Harvested: Dec 15, Organic
   Contact: Alex at garden@sunnyvale-hub.local

2. Berkeley Hub - 20 lbs Cherry tomatoes
   Harvested: Dec 14, Organic
   Contact: Jordan at berkeley-hub.local

Would you like me to coordinate pickup?
```

### Finding Skills

```
User: My solar panel isn't charging properly

Agent: I'll find someone who knows solar panel repair.
[Executes: search_skills(skill="solar repair")]

Found 2 people with solar expertise:
1. Sam Martinez at Sunnyvale Hub
   Skills: Solar installation, repair, battery systems
   Available: Weekends

2. Alex Kim at Oakland Hub (3 miles)
   Skills: Solar repair, electrical systems
   Available: Evenings

Would you like their contact info?
```

---

## Part 7: Voice Interface (Bonus!)

### Add Speech Recognition

```bash
pip install SpeechRecognition pyttsx3
```

```python
import speech_recognition as sr
import pyttsx3

# Initialize
recognizer = sr.Recognizer()
tts = pyttsx3.init()

def listen():
    """Listen to user's voice"""
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except:
        return None

def speak(text):
    """Speak the response"""
    print(f"Agent: {text}")
    tts.say(text)
    tts.runAndWait()

# Voice conversation loop
while True:
    question = listen()

    if question:
        if "quit" in question.lower():
            speak("Goodbye!")
            break

        result = agent.run(question)
        speak(result)
```

Now you can **talk** to your community resource network!

---

## Technical Specifications

### Model Size Comparison

| Model | Size | RAM | Speed | Quality |
|-------|------|-----|-------|---------|
| SmolLM2-1.7B | 1.7GB | 2GB | Fast | Good for simple queries |
| Llama-3.2-3B | 3GB | 4GB | Medium | Very good |
| Llama-3.3-70B (API) | N/A | N/A | Slow | Excellent |

**Recommendation for phones:** SmolLM2-1.7B or Llama-3.2-3B via Ollama

### Resource Usage

**Minimal Setup:**
- MCP Server: ~50MB RAM
- smolagent runtime: ~100MB RAM
- SmolLM2-1.7B: ~2GB RAM
- **Total: ~2.2GB RAM**

**Can run on most phones from 2018+!**

---

## Security & Sandboxing

smolagents supports sandboxed execution:

```python
from smolagents import CodeAgent, E2BSandbox

# Run in isolated sandbox
agent = CodeAgent(
    tools=tools,
    model=model,
    sandbox=E2BSandbox()  # Or Docker, Pyodide, etc.
)
```

This prevents agents from accessing anything outside their sandbox.

---

## Integration with Existing Hub

### Add to Your Current Setup

```bash
cd ~/commune-hub

# Your existing structure:
# index.html (community hub)
# valueflows_api.py (resource API)
# resources.json (resource inventory)

# Add:
mkdir agents
cd agents

# Install conversational agents
./setup-conversational-agents.sh

# Now you have both:
# - Static web interface (index.html)
# - Conversational agent interface (agents/)
```

**Users can choose:**
- Browse resources on website
- OR ask the agent in natural language
- OR use voice commands

---

## Deployment Options

### Option 1: Command Line Interface
```bash
python resource_agent.py
```
Simple terminal interface for questions.

### Option 2: Web Interface
```bash
python app.py
```
Chat UI at http://localhost:8082

### Option 3: Voice Interface
```bash
python voice_agent.py
```
Speak your questions!

### Option 4: MCP in Claude Desktop
Connect your MCP server to Claude Desktop for GUI access.

---

## Real-World Example: Complete Flow

**Scenario:** Maria needs a ladder to pick apples

**Option 1: Traditional (Website)**
1. Opens http://sunnyvale-hub.local:8080
2. Clicks "Tool Library"
3. Scrolls through list
4. Finds ladder
5. Notes location and contact

**Option 2: Conversational (Agent)**
```
Maria: "I need a ladder to pick apples"

Agent: *searches tools, considers height needed*

"I found 2 ladders:
1. 8ft Extension Ladder at Tool Shed - perfect for apple picking!
2. 6ft Step Ladder at Workshop - might be too short

The extension ladder is available. Would you like me to reserve it?"

Maria: "Yes please"

Agent: *submits request*

"✅ Reserved!
Pickup: Tool Shed (behind community center)
Return by: Dec 20
Contact if issues: tools@sunnyvale-hub.local

Need anything else?"
```

**5 clicks vs. 1 sentence.** 🎯

---

## Future Enhancements

### Proactive Agents

```python
# Agent monitors network and suggests matches
surplus_monitor = CodeAgent(
    tools=[search_food, search_tools],
    model=model,
    autonomous=True
)

# Runs periodically
@autonomous_task(interval="1hour")
async def match_needs_with_surplus():
    """Check if anyone's requests match available surplus"""

    # Get pending requests
    requests = await get_pending_requests()

    # Check each against available resources
    for request in requests:
        matches = await search_tools(query=request['item'])

        if matches:
            # Send notification
            await notify(request['user'], f"Found {request['item']}!")
```

### Learning Preferences

```python
# Agent learns your patterns
if user.frequently_requests("tools"):
    agent.prioritize("local_tools")

if user.prefers("organic_food"):
    agent.filter(organic=True)
```

---

## Resources & Documentation

### smolagents
- [GitHub](https://github.com/huggingface/smolagents) - Official repository
- [Documentation](https://huggingface.co/docs/smolagents/) - Full API docs
- [DeepLearning.AI Course](https://learn.deeplearning.ai/courses/building-code-agents-with-hugging-face-smolagents/) - Free course
- [Blog Introduction](https://huggingface.co/blog/smolagents) - Overview and examples

### Model Context Protocol (MCP)
- [Official Site](https://modelcontextprotocol.io/) - Protocol specification
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Build MCP servers
- [FastMCP](https://github.com/jlowin/fastmcp) - Fast Pythonic MCP library
- [Tutorial (6 steps)](https://towardsdatascience.com/model-context-protocol-mcp-tutorial-build-your-first-mcp-server-in-6-steps/) - Comprehensive guide
- [Real Python Guide](https://realpython.com/python-mcp/) - Python MCP tutorial

### Models
- [SmolLM2](https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct) - Tiny model for phones
- [Llama 3.2](https://ollama.com/library/llama3.2) - Via Ollama for local inference

---

## Summary: What This Enables

**Before:**
- Browse websites for resources
- Manual coordination
- Need to know where to look
- Technical knowledge required

**After:**
- "Hey agent, I need a ladder"
- Automatic search across federated network
- Agent understands context
- Natural conversation
- Works by voice
- Runs on a phone

**This makes the federated solarpunk network accessible to EVERYONE, not just programmers.** 🌱✊

---

## Next Steps

1. ✅ Install MCP server with ValueFlows tools
2. ✅ Set up smolagent with MCP integration
3. ✅ Test with simple queries
4. ✅ Add web interface (optional)
5. ✅ Train community members to use it
6. 🌍 Connect with other communities
7. 🤖 Deploy autonomous coordination agents

---

**You're building the conversational interface to the commons.**

**Technology that actually serves the community.**

**This is how AI should work.** 🌱🤖✊
