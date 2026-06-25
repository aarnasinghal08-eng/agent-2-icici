import json
import os
from pathlib import Path
import base64
from google import genai
from google.genai import types



def add_image_urls_to_response(response_data):
    """
    Convert mermaid code in agent response to displayable image URLs.
    Uses mermaid.ink for online rendering - no installation needed!
    
    Args:
        response_data: Agent's JSON response containing generated_diagrams
        
    Returns:
        Enhanced response with image_url field for each diagram
    """
    if isinstance(response_data, str):
        response_data = json.loads(response_data)
    
    if "generated_diagrams" in response_data:
        for diagram in response_data["generated_diagrams"]:
            # Get mermaid code from either "mermaid" or "mermaid_code" field
            mermaid_code = diagram.get("mermaid") or diagram.get("mermaid_code", "")
            if mermaid_code:
                # Encode to base64 for mermaid.ink
                encoded = base64.b64encode(mermaid_code.encode()).decode()
                img_url = f"https://mermaid.ink/img/{encoded}"
                diagram["image_url"] = img_url
    
    return response_data

def generate_diagrams_from_srs(srs_data):
    """
    Convert SRS to Mermaid diagrams using Google Gemini AI.
    Dynamically generates diagrams based on the actual SRS content.
    
    Args:
        srs_data: Structured JSON with actors, use_cases, functional_requirements
        
    Returns:
        JSON with 6 production-grade Mermaid diagrams
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    client = genai.Client(api_key=api_key)
    
    # Create prompt for Gemini to generate diagrams
    srs_json = json.dumps(srs_data, indent=2)
    
    # Dynamically extract actors and system name to make the prompt generic
    system_name = srs_data.get("system_name", "the system")
    actors = srs_data.get("actors", [])
    primary_actor = actors[0].get("name", "Primary Actor") if len(actors) > 0 else "Primary Actor"
    secondary_actor = actors[1].get("name", "Secondary Actor") if len(actors) > 1 else "Secondary Actor"
    
    prompt = f"""You are a Diagram Generation Expert specializing in UML and Mermaid visualization.

Given this SRS JSON for the system '{system_name}', generate exactly 6 production-grade Mermaid diagrams in valid JSON format.

SRS INPUT:
{srs_json}

TASK: Generate exactly 6 diagrams matching this schema:
{{
  "diagrams": [
    {{
      "id": "diagram-id",
      "title": "Diagram Title",
      "type": "flowchart|state",
      "mermaid": "graph TB\\nA[Node A]\\nA --> B[Node B]"
    }}
  ]
}}

DIAGRAMS TO GENERATE:
1. Use Case Diagram - All actors and use cases with relationships for {system_name}
2. Primary Actor Journey - Main workflow sequence for {primary_actor}
3. Secondary Workflow - Alternative processes or workflow sequence for {secondary_actor}
4. System Integration & Flow - Flow involving external systems, APIs, or database integrations
5. State Machine - Key entity or process state transitions in the system
6. Requirements Traceability - Functional requirements (FR) mapped to use cases (UC)

CRITICAL RULES:
✓ Generate VALID Mermaid syntax
✓ Use "\\n" for newlines in JSON strings (NOT actual newlines)
✓ Preserve all IDs (e.g., A1, UC1, FR-1) in diagram labels
✓ Use flowchart for workflows, stateDiagram-v2 for states
✓ Return ONLY valid JSON, no markdown, no code fences
✓ Each diagram type MUST match the schema exactly

Return valid JSON only."""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    
    # Parse response
    response_text = response.text
    
    # Try to extract JSON from response
    try:
        # Handle markdown code blocks if present
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0]
        else:
            json_str = response_text
        
        diagrams_json = json.loads(json_str.strip())
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Gemini's diagram response: {str(e)}")

    
    return {
        "status": "success",
        "generated_diagrams": diagrams_json.get("diagrams", []),
        "srs_metadata": {
            "system_name": srs_data.get("system_name", "Unknown System"),
            "actors": srs_data.get("actors", []),
            "use_cases": srs_data.get("use_cases", []),
            "functional_requirements": srs_data.get("functional_requirements", [])
        },
        "diagram_count": len(diagrams_json.get("diagrams", []))
    }

async def run_srs_to_diagrams(srs_json):
    """
    Async wrapper to generate diagrams from SRS JSON.
    Uses Claude AI for dynamic diagram generation.
    """
    diagrams = generate_diagrams_from_srs(srs_json)
    response = add_image_urls_to_response(diagrams)
    return response