"""Utility functions for generating and saving Mermaid diagrams."""
import json
import os
import subprocess
import base64
import urllib.parse
from pathlib import Path


def save_mermaid_code(mermaid_code: str, filename: str = "diagram.mmd") -> str:
    """
    Save Mermaid code to a .mmd file.
    
    Args:
        mermaid_code: The Mermaid syntax code
        filename: Output filename (default: diagram.mmd)
    
    Returns:
        Path to the saved file
    """
    output_dir = Path(__file__).parent
    output_path = output_dir / filename
    
    with open(output_path, 'w') as f:
        f.write(mermaid_code)
    
    print(f"✓ Diagram saved to: {output_path}")
    return str(output_path)


def render_to_image(mermaid_file: str, output_format: str = "png") -> str:
    """
    Convert Mermaid file to PNG/SVG using Mermaid CLI.
    Requires: npm install -g @mermaid-js/mermaid-cli
    
    Args:
        mermaid_file: Path to .mmd file
        output_format: "png" or "svg"
    
    Returns:
        Path to generated image
    """
    try:
        output_image = mermaid_file.replace(".mmd", f".{output_format}")
        subprocess.run([
            "mmdc", "-i", mermaid_file, "-o", output_image
        ], check=True)
        print(f"✓ Image generated: {output_image}")
        return output_image
    except FileNotFoundError:
        print("⚠ Mermaid CLI not found. Install with: npm install -g @mermaid-js/mermaid-cli")
        return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Error rendering diagram: {e}")
        return None


def mermaid_to_image_url(mermaid_code: str) -> str:
    """
    Convert Mermaid code to image URL using mermaid.ink (online rendering).
    No installation required!
    
    Args:
        mermaid_code: The Mermaid syntax code
    
    Returns:
        URL to the rendered diagram image
    """
    encoded = base64.b64encode(mermaid_code.encode()).decode()
    url = f"https://mermaid.ink/img/{encoded}"
    return url


def process_agent_response(response_json: dict, use_online: bool = True) -> dict:
    """
    Process agent response and save all generated diagrams.
    
    Args:
        response_json: Response from agent containing 'generated_diagrams'
        use_online: If True, generate image URLs; if False, render locally
    
    Returns:
        Dictionary with saved file paths and/or image URLs
    """
    results = {}
    
    if "generated_diagrams" in response_json:
        for i, diagram in enumerate(response_json["generated_diagrams"]):
            diagram_type = diagram.get("diagram_type", f"diagram_{i}")
            mermaid_code = diagram.get("mermaid_code", "")
            
            # Save .mmd file
            filename = f"{diagram_type.replace(' ', '_').lower()}.mmd"
            mmd_path = save_mermaid_code(mermaid_code, filename)
            results[diagram_type] = {"mmd": mmd_path}
            
            if use_online:
                # Generate image URL
                img_url = mermaid_to_image_url(mermaid_code)
                results[diagram_type]["image_url"] = img_url
                results[diagram_type]["markdown"] = f"![{diagram_type}]({img_url})"
            else:
                # Try to render to local image
                img_path = render_to_image(mmd_path)
                if img_path:
                    results[diagram_type]["image"] = img_path
    
    return results
