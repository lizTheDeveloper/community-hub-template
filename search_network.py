#!/usr/bin/env python3
"""
Solarpunk Network Search Tool

Searches across federated community hubs for resources (tools, food, skills)

Usage:
    python search_network.py               # Search all resources
    python search_network.py --type tool   # Search only tools
    python search_network.py --query saw   # Search for "saw"
"""

import requests
import json
import argparse
from typing import List, Dict, Optional


def load_federation_nodes(federation_file: str = 'federation.json') -> List[Dict]:
    """Load list of federated nodes from JSON file"""
    try:
        with open(federation_file, 'r') as f:
            data = json.load(f)
            return data.get('nodes', [])
    except FileNotFoundError:
        print(f"❌ Error: {federation_file} not found!")
        print("Create federation.json with at least one node.")
        return []
    except json.JSONDecodeError:
        print(f"❌ Error: {federation_file} is not valid JSON")
        return []


def query_node(node: Dict, resource_type: Optional[str] = None,
               query: Optional[str] = None) -> List[Dict]:
    """Query a single node for resources"""
    url = node['url']
    name = node['name']

    try:
        response = requests.get(f"{url}/api/resources", timeout=5)

        if response.status_code != 200:
            print(f"⚠️  {name} - HTTP {response.status_code}")
            return []

        data = response.json()
        resources = data.get('resources', [])

        # Filter by type if specified
        if resource_type:
            resources = [r for r in resources if r.get('type') == resource_type]

        # Filter by query string if specified
        if query:
            query_lower = query.lower()
            resources = [r for r in resources
                        if query_lower in r.get('name', '').lower()
                        or query_lower in r.get('classification', '').lower()]

        return resources

    except requests.exceptions.Timeout:
        print(f"⏱️  {name} - Timeout (offline?)")
        return []
    except requests.exceptions.ConnectionError:
        print(f"❌ {name} - Connection failed (offline)")
        return []
    except Exception as e:
        print(f"❌ {name} - Error: {e}")
        return []


def format_resource(resource: Dict, node_name: str) -> str:
    """Format a resource for display"""
    name = resource.get('name', 'Unknown')
    rtype = resource.get('type', 'unknown')
    status = resource.get('status', 'unknown')
    location = resource.get('currentLocation', 'Unknown')
    quantity = resource.get('currentQuantity', '?')
    unit = resource.get('unit', 'item')

    # Emoji by type
    type_emoji = {
        'tool': '🔧',
        'food': '🍅',
        'skill': '🎓',
        'energy': '⚡',
        'water': '💧',
        'space': '🏠',
        'knowledge': '📚'
    }
    emoji = type_emoji.get(rtype, '📦')

    # Status indicator
    status_emoji = {
        'available': '✅',
        'in_use': '🔄',
        'unavailable': '❌',
        'reserved': '🔒'
    }
    status_indicator = status_emoji.get(status, '❓')

    if unit != 'item':
        quantity_str = f"{quantity} {unit}"
    else:
        quantity_str = f"qty: {quantity}" if quantity != 1 else ""

    return f"  {emoji} {status_indicator} {name} - {location} ({node_name}) {quantity_str}"


def main():
    parser = argparse.ArgumentParser(
        description='Search federated solarpunk community hubs for resources'
    )
    parser.add_argument(
        '--type',
        choices=['tool', 'food', 'skill', 'energy', 'water', 'space', 'knowledge'],
        help='Filter by resource type'
    )
    parser.add_argument(
        '--query',
        type=str,
        help='Search query (matches name or classification)'
    )
    parser.add_argument(
        '--federation-file',
        type=str,
        default='federation.json',
        help='Path to federation.json file'
    )

    args = parser.parse_args()

    # Load nodes
    nodes = load_federation_nodes(args.federation_file)

    if not nodes:
        print("\n💡 Tip: Create federation.json like this:")
        print("""
{
  "nodes": [
    {
      "name": "Oakland Hub",
      "url": "http://192.168.1.100:8081",
      "location": "Oakland, CA"
    },
    {
      "name": "Berkeley Hub",
      "url": "http://192.168.1.101:8081",
      "location": "Berkeley, CA"
    }
  ]
}
        """)
        return

    # Build search description
    search_desc = "all resources"
    if args.type:
        search_desc = f"{args.type}s"
    if args.query:
        search_desc += f" matching '{args.query}'"

    print(f"\n🌐 Searching federated network for {search_desc}...\n")

    # Query all nodes
    all_results = {}
    for node in nodes:
        resources = query_node(node, args.type, args.query)
        if resources:
            all_results[node['name']] = resources

    # Display results
    if not all_results:
        print("❌ No resources found matching your criteria.\n")
        return

    total_count = 0
    for node_name, resources in all_results.items():
        print(f"📍 {node_name}:")
        for resource in resources:
            print(format_resource(resource, node_name))
            total_count += 1
        print()

    print(f"✅ Found {total_count} resource(s) across {len(all_results)} hub(s)\n")

    # Show communication info if available
    for node in nodes:
        if node['name'] in all_results:
            comm = node.get('communication', {})
            if comm:
                print(f"📡 {node['name']} communication:")
                if 'meshtastic_channel' in comm:
                    print(f"   Meshtastic: {comm['meshtastic_channel']}")
                if 'briar_group' in comm:
                    print(f"   Briar: {comm['briar_group']}")
                print()


if __name__ == '__main__':
    main()
