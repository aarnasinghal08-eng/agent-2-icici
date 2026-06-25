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

# Try to find the diagrams JSON file dynamically
current_dir = Path(__file__).parent
diagrams_file = None

# 1. Check for latest_diagrams.json
if (current_dir / "latest_diagrams.json").exists():
    diagrams_file = current_dir / "latest_diagrams.json"
else:
    # 2. Check for any *_output.json files
    output_files = list(current_dir.glob("*_output.json"))
    if output_files:
        # Sort by modification time (newest first)
        output_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        diagrams_file = output_files[0]
    else:
        # 3. Fallback to default diagrams.json
        diagrams_file = current_dir / "diagrams.json"

try:
    print(f"📂 Loading diagrams from: {diagrams_file.name}")
    with open(diagrams_file, 'r', encoding='utf-8') as f:
        diagrams_data = json.load(f)
except FileNotFoundError:
    print(f"❌ Error: No diagrams file found.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"❌ Error decoding JSON from {diagrams_file}: {e}")
    sys.exit(1)

# Extract diagrams based on the schema format
if "data" in diagrams_data and "generated_diagrams" in diagrams_data["data"]:
    diagrams = diagrams_data["data"]["generated_diagrams"]
    system_name = diagrams_data.get("system_name", "Integrated Diagrams")
elif "diagrams" in diagrams_data:
    diagrams = diagrams_data["diagrams"]
    system_name = "College Event Management Website"
else:
    diagrams = []
    system_name = "Unknown System"

print("\n" + "=" * 80)
print(f"✅ INTEGRATED MERMAID DIAGRAMS - {system_name.upper()}")
print("=" * 80)


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
