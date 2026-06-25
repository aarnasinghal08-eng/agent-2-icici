#!/usr/bin/env python3
"""
Quick Start Script - Test Agent 2 in 60 seconds
Verifies environment, starts server, and tests the API
"""

import subprocess
import sys
import time
import json
import os
from pathlib import Path

def print_header(text):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_python():
    """Verify Python version"""
    print("✓ Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"  Python {version.major}.{version.minor}.{version.micro} ✅\n")
        return True
    else:
        print(f"  ❌ Python 3.10+ required, found {version.major}.{version.minor}")
        return False

def check_env():
    """Verify .env file and API key"""
    print("✓ Checking environment...")
    env_file = Path(".env")
    
    if not env_file.exists():
        print("  ❌ .env file not found")
        print("  Create it with: cp .env.example .env")
        print("  Then add your GOOGLE_API_KEY\n")
        return False
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("  ⚠️  GOOGLE_API_KEY not loaded")
        print("  Run: source .env (or set manually)\n")
        return False
    
    if api_key:
        print(f"  API Key configured ✅")
        print(f"  Key: {api_key[:20]}...{api_key[-8:]}\n")
        return True
    else:
        print(f"  ❌ Invalid API key format\n")
        return False

def check_dependencies():
    """Verify required packages"""
    print("✓ Checking dependencies...")
    
    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("google.genai", "Google GenAI"),
        ("dotenv", "Python-dotenv"),
    ]
    
    all_installed = True
    for package, name in packages:
        try:
            if package == "google.genai":
                from google import genai
            else:
                __import__(package)
            print(f"  {name:20} ✅")
        except ImportError:
            print(f"  {name:20} ❌")
            all_installed = False
    
    if not all_installed:
        print("\n  Install with: pip install -r requirements.txt\n")
        return False
    
    print()
    return True


def check_files():
    """Verify required files exist"""
    print("✓ Checking project files...")
    
    files = [
        ("app.py", "FastAPI app"),
        ("diagram/agent.py", "Diagram agent"),
        ("diagram/utils.py", "Utilities"),
        ("srs.json", "Sample SRS"),
        ("diagrams_viewer.html", "Frontend"),
    ]
    
    all_exist = True
    for filepath, desc in files:
        if Path(filepath).exists():
            print(f"  {desc:20} ✅")
        else:
            print(f"  {desc:20} ❌ ({filepath})")
            all_exist = False
    
    print()
    return all_exist

def start_server():
    """Start FastAPI server"""
    print("✓ Starting FastAPI server...\n")
    
    print("  Launching: python -m uvicorn app:app --reload --port 8000")
    print("  (This will run in the background)\n")
    
    try:
        # Start server in background
        subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app:app", "--reload", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        print("  Waiting for server to start...")
        for i in range(10):
            time.sleep(1)
            try:
                import requests
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("  ✅ Server is running on http://localhost:8000\n")
                    return True
            except:
                print(f"  Attempt {i+1}/10...", end="\r")
        
        print("  ❌ Server failed to start\n")
        return False
    
    except Exception as e:
        print(f"  ❌ Error starting server: {e}\n")
        return False

def test_api():
    """Test the API endpoint"""
    print("✓ Testing API endpoint...\n")
    
    try:
        import requests
        
        # Load sample SRS
        with open("srs.json") as f:
            srs = json.load(f)
        
        print(f"  System: {srs['system_name']}")
        print(f"  Actors: {len(srs['actors'])}")
        print(f"  Use Cases: {len(srs['use_cases'])}")
        print(f"  Requirements: {len(srs['functional_requirements'])}\n")
        
        # Call API
        print("  Calling: POST /diagrams/generate-srs...")
        response = requests.post(
            "http://localhost:8000/diagrams/generate-srs",
            json=srs,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            diagrams_count = result.get("diagrams_generated", 0)
            print(f"  ✅ Success! Generated {diagrams_count} diagrams\n")
            
            # Show diagram titles
            print("  Diagrams:")
            for i, d in enumerate(result['data']['generated_diagrams'], 1):
                print(f"    {i}. {d['title']}")
            
            print()
            return True
        else:
            print(f"  ❌ API Error: {response.status_code}")
            print(f"  Response: {response.text}\n")
            return False
    
    except requests.exceptions.Timeout:
        print("  ❌ Request timed out\n")
        print("  Claude API took too long to respond")
        print("  This is normal for the first request\n")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}\n")
        return False

def print_next_steps():
    """Print next steps"""
    print("📚 Next Steps:")
    print()
    print("  1. View API documentation:")
    print("     http://localhost:8000/docs\n")
    print("  2. View generated diagrams:")
    print("     open diagrams_viewer.html\n")
    print("  3. Display diagram URLs:")
    print("     python show_diagrams.py\n")
    print("  4. Deploy to Docker:")
    print("     docker compose up --build\n")
    print("  5. Read integration guide:")
    print("     cat INTEGRATION_GUIDE.md\n")

def main():
    """Run all checks"""
    print_header("Agent 2 Quick Start Check")
    
    checks = [
        ("Python Version", check_python),
        ("Environment", check_env),
        ("Dependencies", check_dependencies),
        ("Project Files", check_files),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            if check_func():
                results.append((name, True))
            else:
                results.append((name, False))
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
            results.append((name, False))
    
    # Summary
    print_header("Pre-Deployment Summary")
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:20} {status}")
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print()
        print("All checks passed! 🎉\n")
        
        # Try to start server and test
        if start_server():
            if test_api():
                print_header("✅ Everything is working!")
                print_next_steps()
                return 0
    
    return 1

if __name__ == "__main__":
    sys.exit(main())
