# Agent 2: SRS → Mermaid Diagrams

**Dynamic diagram generation from SRS documents using Claude AI**

A FastAPI backend that consumes SRS JSON from Agent 1 and generates production-grade Mermaid diagrams.

---

## Features

✅ **Dynamic LLM-based Diagram Generation** - Claude AI creates diagrams from actual SRS content  
✅ **6 Diagram Types** - Use cases, workflows, sequences, state machines, and traceability  
✅ **Auto Image URLs** - Instant visualization via mermaid.ink  
✅ **Docker Ready** - Deploy in seconds  
✅ **API First** - RESTful integration with Agent 1  
✅ **Auto Documentation** - Swagger UI + ReDoc  

---

## Project Structure

```
d:\New folder\
├── app.py                      # FastAPI server with endpoints
├── diagram/
│   ├── __init__.py
│   ├── agent.py               # LLM diagram generation logic
│   └── utils.py               # Mermaid utilities
├── diagrams.json              # (Optional) Template diagrams
├── srs.json                   # Sample SRS for testing
├── diagrams_viewer.html       # Frontend visualization
├── DEPLOYMENT_GUIDE.md        # Complete deployment instructions
├── Dockerfile                 # Docker image configuration
├── docker-compose.yml         # Multi-container orchestration
├── Pipfile                    # Python dependencies
├── .env.example               # Environment variable template
└── README.md                  # This file
```

---

## Quick Start

### 1. Clone & Setup

```bash
cd "d:\New folder"
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 2. Install Dependencies

```bash
# Using pipenv
pipenv install
pipenv shell

# OR using pip
pip install fastapi uvicorn pydantic python-dotenv anthropic
```

### 3. Run Server

```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: **http://localhost:8000**

### 4. Test Integration

```bash
# Check health
curl http://localhost:8000/health

# Generate diagrams from sample SRS
curl -X POST http://localhost:8000/diagrams/generate-srs \
  -H "Content-Type: application/json" \
  -d @srs.json
```

### 5. View Diagrams

Open [diagrams_viewer.html](diagrams_viewer.html) in your browser or run:

```bash
python show_diagrams.py
```

---

## API Reference

### Generate Diagrams from SRS

**Endpoint:** `POST /diagrams/generate-srs`

**Description:** Main integration point that converts SRS JSON to 6 Mermaid diagrams

**Request Body:**

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
    }
  ],
  "functional_requirements": [
    {
      "id": "FR-1",
      "text": "System shall display a paginated list of events with title, date, time, and location",
      "use_cases": ["UC1", "UC2"]
    }
  ]
}
```

**Response (Success):**

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

**Status Codes:**

| Code | Meaning |
|------|---------|
| 200 | ✅ Success - Diagrams generated |
| 400 | ❌ Bad Request - Invalid SRS format |
| 500 | ❌ Server Error - LLM or file system error |

---

### Health Check

**Endpoint:** `GET /health`

**Description:** Check if Agent 2 is running and healthy

**Response:**

```json
{
  "status": "healthy",
  "agent": "Agent-2-DiagramGenerator",
  "endpoints": ["/diagrams/generate-srs (POST)"]
}
```

---

## Integration Workflow (Agent 1 → Agent 2)

### Step 1: Agent 1 Produces SRS JSON

Agent 1 (transcript → SRS) outputs:

```
Transcript Input
    ↓
Agent 1 Processing
    ↓
SRS JSON Output: {system_name, actors[], use_cases[], functional_requirements[]}
```

### Step 2: POST to Agent 2

```bash
curl -X POST http://localhost:8000/diagrams/generate-srs \
  -H "Content-Type: application/json" \
  -d @srs.json
```

### Step 3: Agent 2 Processes with Claude

```python
# diagram/agent.py: generate_diagrams_from_srs()
# 1. Receives SRS JSON from Agent 1
# 2. Creates prompt for Claude
# 3. Calls Claude API (claude-3-5-sonnet-20241022)
# 4. Parses Claude's 6 Mermaid diagrams
# 5. Converts to image URLs via mermaid.ink
# 6. Returns response with diagrams + URLs
```

### Step 4: Response with 6 Diagrams

```json
{
  "status": "success",
  "diagrams_generated": 6,
  "data": {
    "generated_diagrams": [
      { "id": "use-case-diagram", "mermaid": "...", "image_url": "https://..." },
      { "id": "student-journey", "mermaid": "...", "image_url": "https://..." },
      { "id": "organizer-workflow", "mermaid": "...", "image_url": "https://..." },
      { "id": "payment-sequence", "mermaid": "...", "image_url": "https://..." },
      { "id": "state-machine", "mermaid": "...", "image_url": "https://..." },
      { "id": "fr-coverage", "mermaid": "...", "image_url": "https://..." }
    ]
  }
}
```

### Step 5: Agent 1 Displays Diagrams

Use the `image_url` field to display diagrams in your frontend:

```html
<img src="https://mermaid.ink/img/base64code" alt="Use Case Diagram">
```

---

## Deployment

### Local Development

```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker compose up --build
```

### Production

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for:
- Environment configuration
- Docker containerization
- Health monitoring
- Load balancing
- Troubleshooting

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | ✅ Yes | - | Claude API key from console.anthropic.com |
| `FASTAPI_HOST` | ❌ No | `0.0.0.0` | Server bind address |
| `FASTAPI_PORT` | ❌ No | `8000` | Server port |

**Setup:**

```bash
cp .env.example .env
# Edit .env with your values
source .env  # On Unix/macOS
# OR on Windows PowerShell:
Get-Content .env | ForEach-Object { if ($_) { $_ -split '=' | Set-Variable } }
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Agent 1: Transcript → SRS JSON                              │
│ (Runs on another system)                                    │
└──────────────────────┬──────────────────────────────────────┘
                       │ SRS JSON
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ Agent 2: FastAPI Backend (This Project)                     │
├─────────────────────────────────────────────────────────────┤
│ POST /diagrams/generate-srs                                  │
│  ├─ Input: SRS JSON (actors, UCs, FRs)                       │
│  ├─ Processing: Claude LLM Diagram Generation               │
│  │  ├─ Parses SRS structure                                 │
│  │  ├─ Generates 6 Mermaid diagrams                         │
│  │  ├─ Validates syntax                                     │
│  │  └─ Creates image URLs via mermaid.ink                   │
│  └─ Output: Diagrams with URLs                              │
└──────────────────────┬──────────────────────────────────────┘
                       │ JSON Response
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ Frontend / Agent 1: Display Diagrams                        │
│ - Mermaid.js inline rendering                               │
│ - Image links via mermaid.ink                               │
│ - HTML/CSS visualization                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | Latest | REST API framework |
| uvicorn | Latest | ASGI server |
| pydantic | Latest | Data validation |
| python-dotenv | Latest | .env loading |
| anthropic | Latest | Claude API client |

Install with:

```bash
pipenv install
# OR
pip install -r requirements.txt
```

---

## Troubleshooting

### "ANTHROPIC_API_KEY not set"

```bash
# Verify .env exists and has your key
cat .env

# Set environment variable directly
export ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### "Cannot connect to server"

```bash
# Check if server is running
curl http://localhost:8000/health

# Start server if needed
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### "Invalid Mermaid syntax in response"

Claude sometimes includes markdown code fences in responses. This is handled automatically by the parser, but if issues persist:

1. Check Claude's raw response in debug logs
2. Verify SRS format matches schema
3. Try with simplified test SRS

---

## Testing

### Unit Test Example

```python
import json
from diagram.agent import generate_diagrams_from_srs

# Load test SRS
with open("srs.json") as f:
    srs = json.load(f)

# Generate diagrams
result = generate_diagrams_from_srs(srs)

# Verify response
assert result["status"] == "success"
assert result["diagram_count"] == 6
assert len(result["generated_diagrams"]) == 6
```

### Integration Test

```bash
curl -X POST http://localhost:8000/diagrams/generate-srs \
  -H "Content-Type: application/json" \
  -d @srs.json \
  -w "\nStatus: %{http_code}\n"
```

---

## File Reference

| File | Purpose |
|------|---------|
| `app.py` | FastAPI server with `/diagrams/generate-srs` endpoint |
| `diagram/agent.py` | LLM diagram generation using Claude API |
| `diagram/utils.py` | Mermaid utilities (base64 encoding, image URLs) |
| `srs.json` | Sample SRS for testing |
| `diagrams_viewer.html` | Frontend visualization |
| `DEPLOYMENT_GUIDE.md` | Complete deployment instructions |
| `Dockerfile` | Docker image configuration |
| `docker-compose.yml` | Docker Compose orchestration |

---

## API Documentation

Once the server is running, view interactive API docs at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Support

For issues or questions:

1. Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. Review API response status codes
3. Verify ANTHROPIC_API_KEY is set
4. Check server logs: `python -m uvicorn app:app --log-level debug`

---

## Next Steps

- [ ] Integrate Agent 1 to POST SRS to `/diagrams/generate-srs`
- [ ] Deploy using Docker or Docker Compose
- [ ] Set up monitoring and alerting
- [ ] Customize Claude prompt for specific diagram types
- [ ] Add caching layer (Redis) for performance

---

**Version:** 1.0.0  
**Status:** Production Ready  
**Last Updated:** 2024
