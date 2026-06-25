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
    Generate diagrams from SRS JSON using Claude AI.
    
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
        return {
            "status": "success",
            "agent": "Agent-2-DiagramGenerator",
            "system_name": srs.get("system_name", "Unknown"),
            "diagrams_generated": diagrams.get("diagram_count", 0),
            "data": diagrams
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid SRS format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagram generation failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "agent": "Agent-2-DiagramGenerator",
        "endpoints": [
            "/diagrams/generate-srs (POST)"
        ]
    }