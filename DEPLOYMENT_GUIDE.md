# Agent 2: Diagram Generator - Deployment Guide

**Complete guide for deploying the SRS → Mermaid Diagrams pipeline**

---

## Architecture Overview

```
Agent 1 (Transcript → SRS JSON)
         ↓
  POST http://localhost:8000/diagrams/generate-srs
         ↓
   Agent 2 (FastAPI Backend)
         ↓
   Claude AI (LLM Diagram Generation)
         ↓
   Response: 6 Mermaid Diagrams + Image URLs
         ↓
   Frontend Viewer (HTML + Mermaid.js)
```

---

## Quick Start (Local Development)

### 1. Environment Setup

**Create `.env` file in workspace root:**

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
```

**Get your Anthropic API key:**
1. Go to https://console.anthropic.com/
2. Create account or login
3. Navigate to "API Keys"
4. Create new key
5. Copy to `.env`

### 2. Install Dependencies

```bash
# Using pip
pip install fastapi uvicorn pydantic python-dotenv anthropic

# OR using Pipfile (already configured)
pipenv install
pipenv shell
```

### 3. Run Development Server

```bash
# Start FastAPI server with auto-reload
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: `http://localhost:8000`

**API Documentation (auto-generated):**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 4. Test the API

**Using curl:**

```bash
curl -X POST http://localhost:8000/diagrams/generate-srs \
  -H "Content-Type: application/json" \
  -d @srs.json
```

**Using Python requests:**

```python
import requests
import json

with open("srs.json") as f:
    srs_data = json.load(f)

response = requests.post(
    "http://localhost:8000/diagrams/generate-srs",
    json=srs_data
)

print(response.json())
```

### 5. View Diagrams

**Option A: Frontend Viewer**
```bash
# Open in browser
start diagrams_viewer.html
# OR on macOS/Linux:
open diagrams_viewer.html
```

**Option B: Terminal Display**
```bash
python show_diagrams.py
```

---

## Docker Deployment

### 1. Dockerfile Configuration

**Create `Dockerfile` in workspace root:**

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Alternative with requirements.txt:**

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Docker Compose (Recommended)

**Create `docker-compose.yml`:**

```yaml
version: '3.8'

services:
  diagram-generator:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - FASTAPI_HOST=0.0.0.0
      - FASTAPI_PORT=8000
    volumes:
      - ./srs.json:/app/srs.json
      - ./diagrams_viewer.html:/app/diagrams_viewer.html
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 3. Build and Run

```bash
# Build image
docker build -t diagram-generator:latest .

# Run container
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=sk-ant-xxxxx \
  diagram-generator:latest

# OR using Docker Compose (recommended)
docker compose up --build
```

---

## Integration with Agent 1

### API Contract

**Endpoint:** `POST /diagrams/generate-srs`

**Request:**
```json
{
  "system_name": "College Event Management Website",
  "actors": [
    {
      "id": "A1",
      "name": "Student",
      "description": "Regular user browsing and registering for events"
    }
  ],
  "use_cases": [
    {
      "id": "UC1",
      "name": "Browse Events",
      "actors": ["A1"],
      "trigger": "Student opens platform",
      "outcome": "List of events displayed",
      "includes": [],
      "extends": [],
      "functional_requirements": ["FR-1", "FR-2"]
    }
  ],
  "functional_requirements": [
    {
      "id": "FR-1",
      "text": "System must display event list with pagination",
      "use_cases": ["UC1"]
    }
  ]
}
```

**Response:**
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
        "id": "use-case",
        "title": "Use Case Diagram",
        "type": "flowchart",
        "mermaid": "graph TB\nA1[Student]\nA1 -->|Browse Events| UC1[UC1]\n...",
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

### Health Check

**Endpoint:** `GET /health`

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "agent": "Agent-2-DiagramGenerator",
  "endpoints": ["/diagrams/generate-srs (POST)"]
}
```

---

## Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `ANTHROPIC_API_KEY` | Claude AI API key | ✅ Yes | `sk-ant-xxxxx` |
| `FASTAPI_HOST` | Server bind address | ❌ No | `0.0.0.0` |
| `FASTAPI_PORT` | Server port | ❌ No | `8000` |

**Load from `.env`:**
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Monitoring & Logging

### Enable Debug Logging

**In `app.py` add:**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### Monitor API Response Times

```bash
# Using Apache Bench
ab -c 10 -n 100 http://localhost:8000/health

# Using curl with timing
curl -w "Time: %{time_total}s\n" \
  http://localhost:8000/health
```

### View Logs

**Docker logs:**
```bash
docker logs -f diagram-generator
# OR with docker compose:
docker compose logs -f diagram-generator
```

---

## Troubleshooting

### Issue: API Key Error

```
ValueError: ANTHROPIC_API_KEY environment variable not set
```

**Solution:**
```bash
# Verify .env file exists in workspace root
cat .env

# Or set directly
export ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### Issue: Connection Refused

```
ConnectionError: Cannot connect to localhost:8000
```

**Solution:**
```bash
# Check if server is running
curl http://localhost:8000/health

# If not, start the server
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Issue: Invalid Mermaid Syntax

```
ValueError: Failed to parse Claude's diagram response
```

**Solution:**
- Claude sometimes returns code blocks with markdown fences
- This is handled by the parser in `generate_diagrams_from_srs()`
- If issue persists, check Claude response in debug logs

### Issue: Timeout from Claude

```
Timeout waiting for Claude API response
```

**Solution:**
- Increase Claude timeout: adjust `max_tokens` in prompt
- Reduce SRS complexity for testing
- Check API rate limits: https://console.anthropic.com/

---

## Performance Optimization

### Caching Diagrams

Add Redis caching for frequently requested SRS:

```python
import redis

cache = redis.Redis(host='localhost', port=6379)

@app.post("/diagrams/generate-srs")
async def generate_from_srs(srs: dict):
    srs_hash = hash(json.dumps(srs, sort_keys=True))
    
    # Check cache
    cached = cache.get(f"diagrams:{srs_hash}")
    if cached:
        return json.loads(cached)
    
    # Generate if not cached
    diagrams = await run_srs_to_diagrams(srs)
    cache.setex(f"diagrams:{srs_hash}", 3600, json.dumps(diagrams))
    
    return {"status": "success", "data": diagrams}
```

### Batch Processing

Process multiple SRS documents:

```bash
# Create batch_srs.json with array of SRS objects
python batch_generate.py < batch_srs.json > batch_diagrams.json
```

---

## Production Checklist

- [ ] ANTHROPIC_API_KEY configured securely (use secrets manager)
- [ ] `.env` file in `.gitignore`
- [ ] Docker image built and tested
- [ ] Health check endpoint responding (GET /health)
- [ ] API documentation accessible (GET /docs)
- [ ] CORS settings reviewed (currently allows all origins)
- [ ] Error handling verified (500, 400, etc.)
- [ ] Logging configured and monitored
- [ ] Load tested with expected SRS complexity
- [ ] Backup & disaster recovery plan documented

---

## Next Steps

1. **Integrate with Agent 1**: Configure Agent 1 to POST to Agent 2's `/diagrams/generate-srs` endpoint
2. **Add Frontend**: Deploy `diagrams_viewer.html` as web interface
3. **Monitor Production**: Set up alerting for API failures
4. **Scale**: Use load balancer (nginx) if handling many concurrent requests

---

## Support & Debugging

**Check API Status:**
```bash
curl -v http://localhost:8000/health
```

**View Full Request/Response:**
```bash
curl -v -X POST http://localhost:8000/diagrams/generate-srs \
  -H "Content-Type: application/json" \
  -d @srs.json
```

**Test with Example SRS:**
```bash
python -c "import json; from srs import sample_srs; print(json.dumps(sample_srs))" | \
  curl -X POST http://localhost:8000/diagrams/generate-srs \
    -H "Content-Type: application/json" \
    -d @-
```

---

**Last Updated:** 2024
**Version:** Agent 2 v1.0
**Status:** Production Ready
