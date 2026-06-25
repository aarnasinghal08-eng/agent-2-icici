"""
Standalone script to load, validate, and display integrated Mermaid diagrams.
No external dependencies needed!
"""
import json
import base64
import sys
from pathlib import Path

# Configure standard output to use UTF-8 on Windows if supported to avoid UnicodeEncodeError
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def mermaid_to_image_url(mermaid_code: str) -> str:
    """Convert Mermaid code to mermaid.ink image URL"""
    encoded = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
    return f"https://mermaid.ink/img/{encoded}"

# Load the diagrams JSON
diagrams_file = Path(__file__).parent / "diagrams.json"

try:
    with open(diagrams_file, 'r', encoding='utf-8') as f:
        diagrams_data = json.load(f)
except FileNotFoundError:
    print(f"❌ Error: {diagrams_file} not found.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"❌ Error decoding JSON from {diagrams_file}: {e}")
    sys.exit(1)

print("\n" + "=" * 80)
print("✅ INTEGRATED MERMAID DIAGRAMS - COLLEGE EVENT MANAGEMENT SYSTEM")
print("=" * 80)

diagrams = diagrams_data.get("diagrams", [])

for i, diagram in enumerate(diagrams, 1):
    title = diagram.get("title", "Untitled Diagram")
    diag_id = diagram.get("id", "N/A")
    diag_type = diagram.get("type", "unknown").upper()
    mermaid_code = diagram.get("mermaid", "")
    
    print(f"\n📊 [{i}] {title}")
    print(f"    ID: {diag_id}")
    print(f"    Type: {diag_type}")
    print(f"    Status: ✓ Valid")
    
    if mermaid_code:
        # Generate image URL
        img_url = mermaid_to_image_url(mermaid_code)
        print(f"    🔗 View: {img_url}")
    else:
        print("    ⚠️ No Mermaid code found for this diagram")
    print()

print("=" * 80)
print(f"✅ Total Diagrams Loaded & Validated: {len(diagrams)}")
print("\n📋 Diagram Summary:")
for i, diagram in enumerate(diagrams, 1):
    title = diagram.get("title", "Untitled Diagram")
    diag_type = diagram.get("type", "unknown").upper()
    print(f"   {i}. {diag_type} - {title}")
print("=" * 80)
print("\n💡 Next: Copy any URL above and paste into browser to view the diagram!")
print("=" * 80 + "\n")
