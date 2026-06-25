#!/usr/bin/env python3
"""
Agent 1 Integration Test Script
Tests the Agent 2 API with sample SRS data
"""

import json
import requests
import sys
from pathlib import Path

# Configure standard output to use UTF-8 on Windows if supported to avoid UnicodeEncodeError
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Configuration
API_URL = "http://localhost:8000/diagrams/generate-srs"
HEALTH_URL = "http://localhost:8000/health"


def check_health():
    """Verify Agent 2 is running"""
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Agent 2 is healthy")
            return True
        else:
            print(f"❌ Agent 2 health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Agent 2. Is it running on localhost:8000?")
        print("   Start it with: python -m uvicorn app:app --reload")
        return False

def load_srs(filepath):
    """Load SRS JSON file"""
    if not Path(filepath).exists():
        print(f"❌ SRS file not found: {filepath}")
        return None
    
    try:
        with open(filepath) as f:
            srs = json.load(f)
        print(f"✅ Loaded SRS: {srs.get('system_name', 'Unknown')}")
        return srs
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {filepath}: {e}")
        return None

def generate_diagrams(srs_data):
    """Call Agent 2 API to generate diagrams"""
    try:
        print("\n📊 Calling Agent 2: /diagrams/generate-srs")
        response = requests.post(
            API_URL,
            json=srs_data,
            timeout=60  # Allow up to 60 seconds for Claude API
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Generated {result['data']['diagram_count']} diagrams")
            return result
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Claude API is taking too long.")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Agent 2")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def save_diagrams(diagrams, filepath):
    """Save diagrams to file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(diagrams, f, indent=2)
        print(f"✅ Diagrams saved to {filepath}")
        return True
    except Exception as e:
        print(f"❌ Failed to save diagrams: {e}")
        return False

def display_diagrams(diagrams):
    """Display diagram information"""
    if not diagrams or diagrams.get("status") != "success":
        return
    
    data = diagrams.get("data", {})
    generated = data.get("generated_diagrams", [])
    
    print(f"\n📈 Generated Diagrams:")
    for i, diagram in enumerate(generated, 1):
        print(f"\n  {i}. {diagram.get('title', 'Unknown')}")
        print(f"     ID: {diagram.get('id')}")
        print(f"     Type: {diagram.get('type')}")
        if diagram.get('image_url'):
            print(f"     Image: {diagram['image_url'][:80]}...")

def main():
    """Main integration test workflow"""
    print("=" * 60)
    print("Agent 2 Integration Test - SRS → Diagrams")
    print("=" * 60)
    
    # Check if custom SRS file path was passed as CLI argument, otherwise default to srs.json
    srs_file = sys.argv[1] if len(sys.argv) > 1 else "srs.json"
    
    # Step 1: Health check
    print("\n1️⃣  Checking if Agent 2 is running...")
    if not check_health():
        return 1
    
    # Step 2: Load SRS
    print("\n2️⃣  Loading SRS data...")
    srs_data = load_srs(srs_file)
    if not srs_data:
        return 1
    
    # Step 3: Generate diagrams
    print("\n3️⃣  Generating diagrams...")
    diagrams = generate_diagrams(srs_data)
    if not diagrams:
        return 1
    
    # Derive dynamic output file name from system name
    system_name = srs_data.get("system_name", "diagrams").replace(" ", "_").lower()
    output_file = f"{system_name}_output.json"
    
    # Step 4: Save results
    print("\n4️⃣  Saving results...")
    if not save_diagrams(diagrams, output_file):
        return 1
    
    # Step 5: Display summary
    print("\n5️⃣  Diagram Summary:")
    display_diagrams(diagrams)
    
    print("\n" + "=" * 60)
    print("✅ Integration Test Complete!")
    print("=" * 60)
    print(f"\nNext Steps:")
    print(f"1. View full diagrams in browser: open diagrams_viewer.html")
    print(f"2. Check generated diagrams: cat {output_file}")
    print(f"3. Display diagram URLs: python show_diagrams.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
