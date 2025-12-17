#!/usr/bin/env python3
"""
ValueFlows API Server for Community Hubs

Exposes community resources via REST API using ValueFlows vocabulary.

Usage:
    python valueflows_api.py

Then access at: http://localhost:8081/api/resources

Based on: https://w3id.org/valueflows/ont/vf
"""

from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

# Configuration
RESOURCES_FILE = 'resources.json'
PORT = 8081


def load_resources():
    """Load resources from JSON file"""
    if not os.path.exists(RESOURCES_FILE):
        # Create empty resources file if it doesn't exist
        default_resources = [
            {
                "id": "example:tool-001",
                "name": "Example Tool",
                "type": "tool",
                "classification": "Hand Tools",
                "currentLocation": "Community Hub",
                "status": "available",
                "currentQuantity": 1,
                "unit": "item",
                "note": "Replace this with real resources!"
            }
        ]
        save_resources(default_resources)
        return default_resources

    try:
        with open(RESOURCES_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"⚠️  Warning: {RESOURCES_FILE} is invalid JSON, using empty list")
        return []


def save_resources(resources):
    """Save resources to JSON file"""
    with open(RESOURCES_FILE, 'w') as f:
        json.dump(resources, f, indent=2)


@app.route('/')
def home():
    """API home page with documentation"""
    return jsonify({
        "message": "Solarpunk Community Hub - ValueFlows API",
        "version": "1.0",
        "endpoints": {
            "/api/resources": "GET - List all resources",
            "/api/resources?type=tool": "GET - Filter by type",
            "/api/resources?available=true": "GET - Filter by availability",
            "/api/health": "GET - Health check"
        },
        "documentation": "https://w3id.org/valueflows/ont/vf",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "resources_count": len(load_resources())
    })


@app.route('/api/resources', methods=['GET'])
def get_resources():
    """
    Get all resources or filter by parameters

    Query parameters:
        type: Filter by resource type (tool, food, skill, etc.)
        available: Filter by availability (true/false)
        classification: Filter by classification
    """
    resources = load_resources()

    # Apply filters
    resource_type = request.args.get('type')
    available_only = request.args.get('available')
    classification = request.args.get('classification')

    if resource_type:
        resources = [r for r in resources if r.get('type') == resource_type]

    if available_only == 'true':
        resources = [r for r in resources if r.get('status') == 'available']

    if classification:
        resources = [r for r in resources
                    if r.get('classification', '').lower() == classification.lower()]

    # Return in ValueFlows format
    return jsonify({
        "@context": "https://w3id.org/valueflows/ont/vf#",
        "timestamp": datetime.now().isoformat(),
        "resources": resources
    })


@app.route('/api/resources/<resource_id>', methods=['GET'])
def get_resource(resource_id):
    """Get a specific resource by ID"""
    resources = load_resources()

    for resource in resources:
        if resource.get('id') == resource_id:
            return jsonify({
                "@context": "https://w3id.org/valueflows/ont/vf#",
                "resource": resource
            })

    return jsonify({"error": "Resource not found"}), 404


# Optional: POST endpoint for updating resources (workshop extension)
@app.route('/api/resources', methods=['POST'])
def add_resource():
    """
    Add a new resource (optional - for advanced participants)

    Requires JSON body with resource data
    """
    if not request.json:
        return jsonify({"error": "JSON body required"}), 400

    resources = load_resources()

    # Validate required fields
    required_fields = ['id', 'name', 'type']
    for field in required_fields:
        if field not in request.json:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Add resource
    new_resource = request.json
    resources.append(new_resource)
    save_resources(resources)

    return jsonify({
        "message": "Resource added successfully",
        "resource": new_resource
    }), 201


if __name__ == '__main__':
    print("🌱 Starting Solarpunk Community Hub API...")
    print(f"📡 Serving resources from: {RESOURCES_FILE}")
    print(f"🌐 API available at: http://0.0.0.0:{PORT}")
    print(f"📖 Documentation: http://0.0.0.0:{PORT}/")
    print("\n✨ Press Ctrl+C to stop\n")

    app.run(host='0.0.0.0', port=PORT, debug=False)
