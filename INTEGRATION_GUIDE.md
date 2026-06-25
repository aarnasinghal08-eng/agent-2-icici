# Agent 1 ↔ Agent 2 Integration Guide

**Complete guide for integrating the two-agent pipeline: Transcript → SRS → Diagrams**

---

## Overview

The 2-agent pipeline works as follows:

```
AGENT 1: Transcript Processor         AGENT 2: Diagram Generator
┌─────────────────────────┐          ┌──────────────────────────┐
│ Input: Transcript text  │          │ Input: SRS JSON          │
│ Process: NLP + LLM      │          │ Process: Claude AI       │
│ Output: SRS JSON        │ ────────>│ Output: 6 Mermaid        │
└─────────────────────────┘          │         Diagrams + URLs  │
                                     └──────────────────────────┘
```

---

## Agent 1: Transcript → SRS Output

Agent 1 should produce JSON with this exact structure:

```json
{
  "system_name": "College Event Management Website",
  "actors": [
    {
      "id": "A1",
      "name": "Student",
      "description": "Regular user browsing and registering for events"
    },
    {
      "id": "A2",
      "name": "Organizer",
      "description": "Admin managing events and viewing analytics"
    }
  ],
  "use_cases": [
    {
      "id": "UC1",
      "name": "Browse Events",
      "actors": ["A1"],
      "trigger": "Student opens the platform",
      "outcome": "List of all upcoming events is displayed",
      "includes": [],
      "extends": [],
      "functional_requirements": ["FR-1", "FR-2", "FR-3"]
    },
    {
      "id": "UC2",
      "name": "Register for Event",
      "actors": ["A1"],
      "trigger": "Student clicks 'Register' on an event",
      "outcome": "Student registration is recorded and ticket is generated",
      "includes": ["UC-Payment"],
      "extends": [],
      "functional_requirements": ["FR-4", "FR-5"]
    }
  ],
  "functional_requirements": [
    {
      "id": "FR-1",
      "text": "System shall display a paginated list of events with title, date, time, and location",
      "use_cases": ["UC1"]
    },
    {
      "id": "FR-2",
      "text": "System shall allow filtering events by category, date range, and location",
      "use_cases": ["UC1"]
    }
  ]
}
```

### Agent 1 Output Schema Details

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `system_name` | string | ✅ | Name of the system (e.g., "College Event Management") |
| `actors` | array | ✅ | List of actors interacting with the system |
| `actors[].id` | string | ✅ | Unique actor ID (e.g., "A1", "A2") |
| `actors[].name` | string | ✅ | Actor name (e.g., "Student", "Organizer") |
| `actors[].description` | string | ✅ | What the actor does |
| `use_cases` | array | ✅ | List of system use cases |
| `use_cases[].id` | string | ✅ | Unique use case ID (e.g., "UC1") |
| `use_cases[].name` | string | ✅ | Use case name |
| `use_cases[].actors` | array | ✅ | List of actor IDs involved |
| `use_cases[].trigger` | string | ✅ | What triggers this use case |
| `use_cases[].outcome` | string | ✅ | Desired outcome |
| `use_cases[].includes` | array | ❌ | Use case IDs this includes (usually empty) |
| `use_cases[].extends` | array | ❌ | Use case IDs this extends (usually empty) |
| `use_cases[].functional_requirements` | array | ✅ | List of FR IDs |
| `functional_requirements` | array | ✅ | List of functional requirements |
| `functional_requirements[].id` | string | ✅ | Unique FR ID (e.g., "FR-1") |
| `functional_requirements[].text` | string | ✅ | Requirement description |
| `functional_requirements[].use_cases` | array | ✅ | List of UC IDs implementing this FR |

---

## Agent 2: SRS → Diagrams Integration

### Endpoint

**URL:** `POST http://agent2-server:8000/diagrams/generate-srs`

(Replace `agent2-server` with the actual Agent 2 host)

### Request

Agent 1 sends the SRS JSON as the request body:

```bash
curl -X POST http://localhost:8000/diagrams/generate-srs \
  -H "Content-Type: application/json" \
  -d @srs.json
```

**Python Example:**

```python
import requests
import json

# Load SRS from Agent 1
with open("srs.json") as f:
    srs_data = json.load(f)

# Call Agent 2
response = requests.post(
    "http://localhost:8000/diagrams/generate-srs",
    json=srs_data,
    timeout=60
)

if response.status_code == 200:
    diagrams = response.json()
    print(f"✅ Generated {diagrams['diagrams_generated']} diagrams")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
```

### Response

Agent 2 returns 6 diagrams with metadata:

```json
{
  "status": "success",
  "agent": "Agent-2-DiagramGenerator",
  "system_name": "College Event Management Website",
  "diagrams_generated": 6,
  "data": {
    "status": "success",
    "generated_diagrams": [
      {
        "id": "use-case-diagram",
        "title": "Use Case Diagram - College Event Management",
        "type": "flowchart",
        "mermaid": "graph TB\n    A1[Student]\n    A2[Organizer]\n    ...",
        "image_url": "https://mermaid.ink/img/base64encodedcode"
      },
      {
        "id": "student-journey",
        "title": "Student Journey - Registration Workflow",
        "type": "flowchart",
        "mermaid": "flowchart TD\n    Start[Open Platform]\n    ...",
        "image_url": "https://mermaid.ink/img/base64encodedcode"
      },
      {
        "id": "organizer-workflow",
        "title": "Organizer Workflow - Event Management",
        "type": "flowchart",
        "mermaid": "flowchart TD\n    Start[Login as Organizer]\n    ...",
        "image_url": "https://mermaid.ink/img/base64encodedcode"
      },
      {
        "id": "payment-sequence",
        "title": "Payment Processing - Sequence Diagram",
        "type": "flowchart",
        "mermaid": "sequenceDiagram\n    Student->>System: Initiate Payment\n    ...",
        "image_url": "https://mermaid.ink/img/base64encodedcode"
      },
      {
        "id": "state-machine",
        "title": "Registration Flow - State Machine",
        "type": "stateDiagram",
        "mermaid": "stateDiagram-v2\n    [*] --> Registration\n    ...",
        "image_url": "https://mermaid.ink/img/base64encodedcode"
      },
      {
        "id": "fr-coverage",
        "title": "Requirements Traceability - FR to UC Mapping",
        "type": "flowchart",
        "mermaid": "graph LR\n    FR-1 --> UC1\n    ...",
        "image_url": "https://mermaid.ink/img/base64encodedcode"
      }
    ],
    "srs_metadata": {
      "system_name": "College Event Management Website",
      "actors": [...],
      "use_cases": [...],
      "functional_requirements": [...]
    },
    "diagram_count": 6
  }
}
```

### Response Fields

| Field | Description |
|-------|-------------|
| `status` | "success" or "error" |
| `agent` | Always "Agent-2-DiagramGenerator" |
| `system_name` | System name from input SRS |
| `diagrams_generated` | Number of diagrams created (should be 6) |
| `data.generated_diagrams[]` | Array of 6 diagram objects |
| `data.generated_diagrams[].id` | Unique diagram identifier |
| `data.generated_diagrams[].title` | Human-readable diagram title |
| `data.generated_diagrams[].type` | "flowchart" or "stateDiagram" |
| `data.generated_diagrams[].mermaid` | Raw Mermaid diagram code |
| `data.generated_diagrams[].image_url` | HTTP URL for viewing the diagram |

---

## Integration Patterns

### Pattern 1: Synchronous Integration

Agent 1 waits for Agent 2 to complete:

```python
def agent1_complete_pipeline(transcript):
    """
    Agent 1: Convert transcript to SRS
    Agent 2: Convert SRS to diagrams
    Return: Complete output with diagrams
    """
    # Step 1: Agent 1 processes transcript
    srs = agent1_transcript_to_srs(transcript)
    
    # Step 2: Agent 2 processes SRS
    response = requests.post(
        "http://localhost:8000/diagrams/generate-srs",
        json=srs,
        timeout=60
    )
    
    # Step 3: Return combined result
    if response.status_code == 200:
        diagrams = response.json()
        return {
            "srs": srs,
            "diagrams": diagrams["data"]["generated_diagrams"],
            "image_urls": [d["image_url"] for d in diagrams["data"]["generated_diagrams"]]
        }
    else:
        raise Exception(f"Agent 2 failed: {response.text}")
```

### Pattern 2: Asynchronous Integration

Agent 1 doesn't wait for Agent 2:

```python
import asyncio
import aiohttp

async def agent1_async_pipeline(transcript):
    """
    Agent 1: Convert transcript to SRS (fast)
    Agent 2: Convert SRS to diagrams (async, may take time)
    """
    # Step 1: Agent 1 processes transcript
    srs = agent1_transcript_to_srs(transcript)
    
    # Step 2: Send to Agent 2 without waiting
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:8000/diagrams/generate-srs",
            json=srs
        ) as response:
            diagrams = await response.json()
    
    # Step 3: Return immediately
    return {
        "srs": srs,
        "diagrams_request_id": diagrams.get("request_id")
    }
```

### Pattern 3: Polling for Completion

Check diagram generation status:

```python
def poll_diagram_generation(request_id, max_attempts=30):
    """Poll Agent 2 for completion"""
    for attempt in range(max_attempts):
        response = requests.get(
            f"http://localhost:8000/diagrams/status/{request_id}"
        )
        
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "complete":
                return data["diagrams"]
        
        time.sleep(2)  # Wait 2 seconds before retrying
    
    raise TimeoutError("Diagram generation took too long")
```

---

## Error Handling

### Common Error Responses

**400 - Bad Request (Invalid SRS Format)**

```json
{
  "status": "error",
  "detail": "Invalid SRS format: Missing required field 'actors'"
}
```

**Handling in Agent 1:**

```python
try:
    response = requests.post(
        "http://localhost:8000/diagrams/generate-srs",
        json=srs,
        timeout=60
    )
    
    if response.status_code == 400:
        # Validate SRS format
        print(f"❌ SRS validation failed: {response.json()['detail']}")
        # Fix and retry
        srs = validate_and_fix_srs(srs)
        response = requests.post(...)
    
    elif response.status_code == 500:
        # Agent 2 error
        print(f"❌ Agent 2 error: {response.json()['detail']}")
        # Maybe Claude API failed - retry with exponential backoff
        
except requests.exceptions.Timeout:
    print("❌ Agent 2 took too long to respond")
    
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to Agent 2 at http://localhost:8000")
```

### Retry Strategy

```python
import time
from typing import Optional

def call_agent2_with_retry(srs: dict, max_retries: int = 3) -> Optional[dict]:
    """Call Agent 2 with exponential backoff retry"""
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "http://localhost:8000/diagrams/generate-srs",
                json=srs,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code >= 500:
                # Server error - retry
                wait_time = 2 ** attempt
                print(f"⏳ Agent 2 error, retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                # Client error - don't retry
                raise Exception(f"Agent 2 error: {response.text}")
        
        except requests.exceptions.Timeout:
            wait_time = 2 ** attempt
            print(f"⏳ Timeout, retrying in {wait_time}s...")
            time.sleep(wait_time)
            continue
    
    raise Exception("Failed to generate diagrams after retries")
```

---

## Health Monitoring

### Check Agent 2 Status

```bash
# Health check endpoint
curl http://localhost:8000/health

# Response:
{
  "status": "healthy",
  "agent": "Agent-2-DiagramGenerator",
  "endpoints": ["/diagrams/generate-srs (POST)"]
}
```

**Agent 1 Health Check Logic:**

```python
def wait_for_agent2(timeout_seconds: int = 30):
    """Wait for Agent 2 to become available"""
    start_time = time.time()
    
    while time.time() - start_time < timeout_seconds:
        try:
            response = requests.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✅ Agent 2 is ready")
                return True
        except requests.exceptions.ConnectionError:
            pass
        
        time.sleep(1)
    
    raise TimeoutError("Agent 2 did not start within timeout period")
```

---

## Configuration

### Agent 2 Server Address

If Agent 2 is running on a different machine:

```python
AGENT2_URL = "http://192.168.1.100:8000"  # Remote server
# OR
AGENT2_URL = "http://localhost:8000"      # Local development
# OR
AGENT2_URL = "http://diagram-generator:8000"  # Docker network
```

### Timeout Configuration

Adjust based on SRS complexity:

```python
# For small SRS (5-10 UCs):
timeout = 30  # seconds

# For medium SRS (10-20 UCs):
timeout = 60  # seconds

# For large SRS (20+ UCs):
timeout = 120  # seconds
```

---

## Example: Complete Integration

**Agent 1 → Agent 2 Complete Workflow:**

```python
import requests
import json
from datetime import datetime

def complete_srs_to_diagrams_pipeline(transcript: str) -> dict:
    """
    Complete 2-agent pipeline:
    1. Agent 1: Transcript → SRS
    2. Agent 2: SRS → Diagrams
    """
    
    print("=" * 60)
    print("Starting 2-Agent Pipeline")
    print("=" * 60)
    
    # Step 1: Check Agent 2 is available
    print("\n1️⃣  Checking Agent 2 availability...")
    try:
        health = requests.get("http://localhost:8000/health", timeout=5)
        assert health.status_code == 200
        print("   ✅ Agent 2 is healthy")
    except:
        print("   ❌ Agent 2 is not available at http://localhost:8000")
        return None
    
    # Step 2: Agent 1 processes transcript
    print("\n2️⃣  Agent 1: Converting transcript to SRS...")
    start_time = datetime.now()
    
    # This would be your actual Agent 1 function
    srs = {
        "system_name": "Example System",
        "actors": [{"id": "A1", "name": "User", "description": "System user"}],
        "use_cases": [{"id": "UC1", "name": "Test", "actors": ["A1"], 
                      "trigger": "Test", "outcome": "Test", 
                      "includes": [], "extends": [],
                      "functional_requirements": ["FR-1"]}],
        "functional_requirements": [{"id": "FR-1", "text": "Test FR", 
                                     "use_cases": ["UC1"]}]
    }
    
    agent1_time = (datetime.now() - start_time).total_seconds()
    print(f"   ✅ SRS generated in {agent1_time:.2f}s")
    print(f"      - System: {srs['system_name']}")
    print(f"      - Actors: {len(srs['actors'])}")
    print(f"      - Use Cases: {len(srs['use_cases'])}")
    print(f"      - Requirements: {len(srs['functional_requirements'])}")
    
    # Step 3: Agent 2 generates diagrams
    print("\n3️⃣  Agent 2: Generating diagrams from SRS...")
    start_time = datetime.now()
    
    try:
        response = requests.post(
            "http://localhost:8000/diagrams/generate-srs",
            json=srs,
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"   ❌ Agent 2 failed: {response.status_code}")
            print(f"      {response.text}")
            return None
        
        result = response.json()
        agent2_time = (datetime.now() - start_time).total_seconds()
        
        print(f"   ✅ Diagrams generated in {agent2_time:.2f}s")
        print(f"      - Diagrams: {result['diagrams_generated']}")
        print(f"      - Status: {result['status']}")
        
    except requests.exceptions.Timeout:
        print("   ❌ Agent 2 request timed out")
        return None
    
    # Step 4: Summary
    print("\n" + "=" * 60)
    print("Pipeline Complete!")
    print("=" * 60)
    print(f"Total time: {agent1_time + agent2_time:.2f}s")
    print(f"\nGenerated Diagrams:")
    
    for i, diagram in enumerate(result['data']['generated_diagrams'], 1):
        print(f"\n{i}. {diagram['title']}")
        print(f"   ID: {diagram['id']}")
        print(f"   Image: {diagram['image_url'][:50]}...")
    
    return result

# Run the pipeline
if __name__ == "__main__":
    transcript = "Sample transcript text..."
    result = complete_srs_to_diagrams_pipeline(transcript)
```

---

## Deployment Setup

### Local Development

```bash
# Terminal 1: Start Agent 2
cd "d:\New folder"
python -m uvicorn app:app --reload --port 8000

# Terminal 2: Run Agent 1
python agent1.py
```

### Docker Deployment

```bash
# Start Agent 2
docker compose up --build

# Run Agent 1 (from different machine)
python agent1.py --agent2-url http://192.168.1.100:8000
```

---

## Next Steps

1. **Implement Agent 1** to output the exact SRS JSON schema
2. **Test Integration** using `test_agent2.py` script
3. **Deploy Agent 2** using Docker Compose
4. **Configure Agent 1** to call Agent 2's `/diagrams/generate-srs` endpoint
5. **Monitor** both agents in production

---

**Last Updated:** 2024  
**Version:** Integration v1.0  
**Status:** Production Ready
