import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from diagram.agent import add_image_urls_to_response, generate_diagrams_from_srs, run_srs_to_diagrams

# Load environment variables
load_dotenv()

# Initialize FastAPI web engine
app = FastAPI()

# Enable CORS for web frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============= DIAGRAM GENERATION ENDPOINTS =============


@app.post("/diagrams/generate-srs")
async def generate_from_srs(srs: dict):
    """
    Generate diagrams from SRS JSON using Gemini AI.
    
    This is the main Agent 2 endpoint that receives SRS output from Agent 1.
    
    Request body: SRS JSON with:
    - system_name: string
    - actors: [{id, name, description}]
    - use_cases: [{id, name, actors, trigger, outcome, functional_requirements}]
    - functional_requirements: [{id, text, use_cases}]
    
    Response: 6 Mermaid diagrams with image URLs
    """
    try:
        diagrams = await run_srs_to_diagrams(srs)
        response_data = {
            "status": "success",
            "agent": "Agent-2-DiagramGenerator",
            "system_name": srs.get("system_name", "Unknown"),
            "diagrams_generated": diagrams.get("diagram_count", 0),
            "data": diagrams
        }
        
        # Save to latest_diagrams.json for persistence and dynamic frontend viewing
        try:
            with open("latest_diagrams.json", "w", encoding="utf-8") as f:
                json.dump(response_data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
            
        return response_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid SRS format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagram generation failed: {str(e)}")


@app.get("/diagrams/latest")
async def get_latest_diagrams():
    """
    Get the latest generated diagrams from the most recent run.
    """
    try:
        # Check for the latest run
        if os.path.exists("latest_diagrams.json"):
            with open("latest_diagrams.json", "r", encoding="utf-8") as f:
                return json.load(f)
        
        # Fall back to default template diagrams.json if it exists
        elif os.path.exists("diagrams.json"):
            with open("diagrams.json", "r", encoding="utf-8") as f:
                default_diagrams = json.load(f).get("diagrams", [])
                
                # Transform to match the schema expected by the frontend
                for diagram in default_diagrams:
                    if "mermaid" in diagram and "image_url" not in diagram:
                        import base64
                        encoded = base64.b64encode(diagram["mermaid"].encode()).decode()
                        diagram["image_url"] = f"https://mermaid.ink/img/{encoded}"
                        
                return {
                    "status": "success",
                    "agent": "Agent-2-DiagramGenerator",
                    "system_name": "College Event Management Website",
                    "diagrams_generated": len(default_diagrams),
                    "data": {
                        "generated_diagrams": default_diagrams
                    }
                }
        else:
            raise HTTPException(status_code=404, detail="No diagrams found. Please run the generation endpoint first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "agent": "Agent-2-DiagramGenerator",
        "endpoints": [
            "/diagrams/generate-srs (POST)",
            "/diagrams/latest (GET)"
        ]
    }