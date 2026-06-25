# Agent 2: System Architecture

**Complete technical architecture for the SRS → Mermaid Diagrams pipeline**

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ Agent 2: SRS to Mermaid Diagrams Generator                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐         ┌──────────────┐     ┌────────────┐  │
│  │   FastAPI    │         │  Claude AI   │     │ Mermaid.ink│  │
│  │   Backend    │────────>│  (LLM API)   │────>│  (Image    │  │
│  │              │         │              │     │   URLs)    │  │
│  └──────────────┘         └──────────────┘     └────────────┘  │
│        ▲                                              │          │
│        │ HTTP POST                                   │          │
│        │ (SRS JSON)                    Image URLs    │          │
│        │                               (base64)      ▼          │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  Agent 1  (Transcript → SRS)                             │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. FastAPI Backend (`app.py`)

**Purpose:** RESTful API server that orchestrates diagram generation

**Stack:**
- Framework: FastAPI v0.104.1
- Server: Uvicorn ASGI (0.24.0)
- Validation: Pydantic v2.5.0
- Environment: python-dotenv v1.0.0

**Endpoints:**

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/diagrams/generate-srs` | Generate 6 diagrams from SRS JSON |
| GET | `/health` | Health check for monitoring |

**Features:**
- CORS enabled (all origins for frontend access)
- Async/await for concurrent requests
- Error handling with HTTP status codes
- Type hints with Pydantic validation

**Request/Response:**
```python
POST /diagrams/generate-srs
├─ Input: SRS JSON (dict)
│  └─ system_name, actors[], use_cases[], functional_requirements[]
└─ Output: 200 OK
   └─ JSON with 6 diagrams + metadata + image URLs
```

---

### 2. LLM Diagram Generator (`diagram/agent.py`)

**Purpose:** Core logic for Claude AI-based diagram generation

**Components:**

#### A. `generate_diagrams_from_srs(srs_data)`

**Function:** Convert SRS to 6 Mermaid diagrams using Claude AI

**Flow:**
1. Load environment variables (ANTHROPIC_API_KEY)
2. Initialize Anthropic client
3. Create comprehensive prompt with SRS data
4. Call Claude API (claude-3-5-sonnet-20241022)
5. Parse JSON response (handles markdown code blocks)
6. Return diagrams with metadata

**Diagram Types Generated:**
1. **Use Case Diagram** - Actors and all use cases with relationships
2. **Student Journey** - Primary workflow (registration, browsing, payment)
3. **Organizer Workflow** - Event management and analytics
4. **Payment Sequence** - Integration with payment systems
5. **State Machine** - Registration state transitions
6. **Requirements Traceability** - FR to UC mapping

**Error Handling:**
- ValueError if API key not set
- JSONDecodeError if Claude response invalid
- KeyError if diagram structure wrong

#### B. `add_image_urls_to_response(response_data)`

**Function:** Convert Mermaid code to displayable image URLs

**Process:**
1. Iterate through generated_diagrams array
2. Extract mermaid code from "mermaid" field
3. Base64 encode the code
4. Generate mermaid.ink URL: `https://mermaid.ink/img/{base64}`
5. Add image_url field to each diagram

**Example:**
```
Input:  {"id": "use-case", "mermaid": "graph TB\nA1[Student]"}
Output: {"id": "use-case", "mermaid": "...", 
         "image_url": "https://mermaid.ink/img/Z3JhcGggVEI..."}
```

#### C. `run_srs_to_diagrams(srs_json)`

**Function:** Async wrapper for diagram generation

**Flow:**
1. Call `generate_diagrams_from_srs()`
2. Enhance response with `add_image_urls_to_response()`
3. Return complete result

---

### 3. Utilities Module (`diagram/utils.py`)

**Purpose:** Helper functions for Mermaid diagram processing

**Functions:**
- `mermaid_to_image_url()` - Create mermaid.ink URLs
- `save_mermaid_code()` - Save diagrams to `.mmd` files
- `render_to_image()` - Optional CLI rendering

---

### 4. Frontend Viewer (`diagrams_viewer.html`)

**Purpose:** Display all 6 diagrams in browser

**Technology:**
- HTML5 semantic markup
- CSS3 responsive grid layout
- Mermaid.js v11.15.0 (CDN)
- Bootstrap 5 styling

**Features:**
- 6 diagram cards with titles and descriptions
- Inline Mermaid.js rendering
- Responsive design (mobile, tablet, desktop)
- Gradient header with system name
- Copy-to-clipboard diagram code

**Rendering:**
```html
<div class="mermaid">
  {{mermaid_code}}
</div>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>mermaid.initialize({ theme: 'default' }); mermaid.contentLoaded();</script>
```

---

## Data Flow Architecture

### Request-Response Cycle

```
Agent 1 System
     │
     │ POST /diagrams/generate-srs
     │ Content-Type: application/json
     │ {system_name, actors[], use_cases[], functional_requirements[]}
     │
     ▼
┌─────────────────────────┐
│  FastAPI: app.generate_ │
│          from_srs()     │
└─────────────────────────┘
     │
     │ await run_srs_to_diagrams()
     │
     ▼
┌──────────────────────────────┐
│ diagram.agent:               │
│ - Validate ANTHROPIC_API_KEY │
│ - Initialize Anthropic()     │
└──────────────────────────────┘
     │
     │ Claude API Call
     │
     ▼
┌─────────────────────────────────────────┐
│ Claude AI (claude-3-5-sonnet-20241022) │
│                                         │
│ Process: Generate 6 Mermaid diagrams   │
│ from SRS structure                     │
│ Response: JSON with diagrams[]         │
└─────────────────────────────────────────┘
     │
     │ Diagram JSON response
     │
     ▼
┌──────────────────────────────┐
│ add_image_urls_to_response() │
│ - Iterate diagrams[]         │
│ - Base64 encode mermaid code │
│ - Create mermaid.ink URLs    │
└──────────────────────────────┘
     │
     │ HTTP 200 OK + JSON response
     │
     ▼
Agent 1 / Frontend
     │
     │ Display:
     │ - 6 diagrams with titles
     │ - Image URLs via mermaid.ink
     │ - System metadata
     │
     ▼
User Browser
```

---

## API Contract

### Input Schema (SRS JSON)

```typescript
interface SRS {
  system_name: string;
  actors: Actor[];
  use_cases: UseCase[];
  functional_requirements: FunctionalRequirement[];
}

interface Actor {
  id: string;          // e.g., "A1"
  name: string;        // e.g., "Student"
  description: string;
}

interface UseCase {
  id: string;                          // e.g., "UC1"
  name: string;
  actors: string[];                    // Actor IDs
  trigger: string;
  outcome: string;
  includes: string[];                  // UC IDs
  extends: string[];                   // UC IDs
  functional_requirements: string[];   // FR IDs
}

interface FunctionalRequirement {
  id: string;           // e.g., "FR-1"
  text: string;
  use_cases: string[];  // UC IDs
}
```

### Output Schema (Diagram Response)

```typescript
interface DiagramResponse {
  status: "success" | "error";
  agent: "Agent-2-DiagramGenerator";
  system_name: string;
  diagrams_generated: number;
  data: {
    status: "success" | "error";
    generated_diagrams: Diagram[];
    srs_metadata: SRS;
    diagram_count: number;
  };
}

interface Diagram {
  id: string;           // e.g., "use-case-diagram"
  title: string;
  type: "flowchart" | "stateDiagram";
  mermaid: string;      // Raw Mermaid code
  image_url: string;    // https://mermaid.ink/img/{base64}
}
```

---

## Technology Stack

### Runtime
- **Python:** 3.13+
- **OS:** Windows, macOS, Linux (Docker for consistency)

### Web Framework
- **FastAPI:** 0.104.1 (REST API)
- **Uvicorn:** 0.24.0 (ASGI server)
- **Pydantic:** 2.5.0 (data validation)

### AI/ML
- **Anthropic SDK:** 0.25.0
- **Model:** claude-3-5-sonnet-20241022
- **Token budget:** 8000 tokens per request

### Frontend
- **Mermaid.js:** 11.15.0 (diagram rendering)
- **HTML5:** Semantic markup
- **CSS3:** Responsive design

### Deployment
- **Docker:** Container orchestration
- **Docker Compose:** Multi-container setup

### Development
- **Python:** 3.13.14
- **Virtual Environment:** Pipenv or venv
- **Package Manager:** pip or Pipenv

---

## Deployment Architecture

### Local Development

```
Developer Machine
├─ Python 3.13
├─ .env (with ANTHROPIC_API_KEY)
├─ FastAPI Server (port 8000)
├─ diagrams_viewer.html (browser)
└─ Test scripts (test_agent2.py, etc)
```

### Docker Deployment

```
Docker Host
├─ Image: diagram-generator:latest
├─ Container: diagram-generator
│  ├─ Python 3.13-slim
│  ├─ FastAPI server (port 8000)
│  ├─ Healthcheck: /health
│  └─ Environment: .env passed
└─ Network: diagram-network
```

### Production Deployment

```
Production Environment
├─ Docker Registry
│  └─ diagram-generator:v1.0.0
├─ Orchestrator (Kubernetes or Docker Compose)
│  ├─ Load Balancer (nginx)
│  │  └─ Port 443 (HTTPS)
│  ├─ Agent 2 Container (3 replicas)
│  │  ├─ Liveness probe: /health
│  │  ├─ Readiness probe: /health
│  │  └─ Resource limits: 2GB RAM, 1 CPU
│  ├─ Monitoring (Prometheus + Grafana)
│  └─ Logging (ELK Stack or CloudWatch)
├─ Secrets Manager
│  └─ ANTHROPIC_API_KEY (encrypted)
└─ CI/CD Pipeline
   ├─ GitHub/GitLab webhook
   ├─ Automated tests
   ├─ Docker build
   ├─ Registry push
   └─ Deployment trigger
```

---

## Performance Characteristics

### Response Times

| Operation | Time | Notes |
|-----------|------|-------|
| Health check | < 100ms | Simple JSON response |
| SRS validation | < 50ms | Pydantic validation |
| Claude API call | 5-30s | Depends on SRS size |
| Image URL generation | < 100ms | Base64 encoding |
| **Total request** | **6-31s** | Dominated by Claude API |

### Throughput

| Metric | Value |
|--------|-------|
| Concurrent requests | Limited by Claude API quota |
| Requests per second | ~1 (serialized) |
| Diagrams per minute | ~6 (one SRS per request) |

### Resource Usage

| Resource | Typical | Peak |
|----------|---------|------|
| Memory | 150 MB | 250 MB |
| CPU | 5% | 20% |
| Network | 50 KB/s | 200 KB/s |

---

## Security Architecture

### Authentication & Authorization

**Current:** None (public API for development)

**Production Requirements:**
- API Key authentication
- OAuth 2.0 for multi-user
- Role-based access control

### Data Security

- **In Transit:** HTTPS/TLS (via nginx reverse proxy)
- **At Rest:** No persistent data stored
- **Encryption:** API key in secrets manager

### Network Security

```
Internet
   │ HTTPS (TLS 1.3)
   ▼
┌──────────────────────────┐
│ Reverse Proxy (nginx)    │
│ - Rate limiting          │
│ - Request validation     │
│ - CORS headers           │
└──────────────────────────┘
   │ HTTP (internal network)
   ▼
┌──────────────────────────┐
│ Agent 2 FastAPI          │
│ - Pydantic validation    │
│ - Error handling         │
│ - Audit logging          │
└──────────────────────────┘
   │ HTTPS (TLS 1.3)
   ▼
┌──────────────────────────┐
│ Anthropic API            │
│ - Bearer token auth      │
│ - Rate limited           │
│ - Encrypted              │
└──────────────────────────┘
```

---

## Scalability Strategy

### Horizontal Scaling

```
Load Balancer
├─ Agent 2 Instance 1
├─ Agent 2 Instance 2
├─ Agent 2 Instance 3
└─ Agent 2 Instance N
   (Each handles independent requests)
```

### Bottlenecks & Solutions

| Bottleneck | Current | Solution |
|-----------|---------|----------|
| Claude API rate limit | ~5 req/min | Queue system + backoff |
| Response time | 6-31s | Async processing + caching |
| Memory per request | 100 MB | Streaming responses |
| Concurrent SRS size | Large (20+ UCs) | Simplified prompt |

### Caching Strategy (Optional)

```python
cache = Redis()

@app.post("/diagrams/generate-srs")
async def generate_from_srs(srs: dict):
    # Hash SRS for cache key
    key = hashlib.sha256(json.dumps(srs, sort_keys=True)).hexdigest()
    
    # Check cache
    if cache.exists(key):
        return cache.get(key)
    
    # Generate if not cached
    result = await generate_diagrams(srs)
    
    # Cache for 1 hour
    cache.setex(key, 3600, json.dumps(result))
    
    return result
```

---

## Monitoring & Observability

### Metrics

```
Prometheus endpoints (future):
- Request count: total_requests_count
- Request duration: request_duration_seconds
- Error rate: request_errors_total
- API quota: anthropic_api_quota_used
```

### Logging

```python
logging.config.dictConfig({
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/agent2.log',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 5
        }
    },
    'loggers': {
        'fastapi': {'handlers': ['file'], 'level': 'INFO'},
        'uvicorn': {'handlers': ['file'], 'level': 'INFO'},
        'agent': {'handlers': ['file'], 'level': 'DEBUG'}
    }
})
```

### Health Checks

```
GET /health
├─ Server: Running ✓
├─ Anthropic API: Accessible ✓
├─ Response time: 95ms ✓
└─ Uptime: 24h 15m 30s ✓
```

---

## Disaster Recovery

### Backup Strategy

- **Source code:** Git repository with tags
- **Configuration:** Environment variables in secrets manager
- **Diagrams:** Generated on-demand (no storage needed)

### Recovery Procedures

| Scenario | RTO | RPO | Procedure |
|----------|-----|-----|-----------|
| Container crash | 1 min | 0 | Auto-restart via orchestrator |
| API key compromise | 5 min | 0 | Rotate key in secrets manager |
| Deployment failure | 10 min | 0 | Rollback to previous image |
| Region outage | 30 min | 0 | Failover to backup region |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024 | Initial release with Claude AI integration |

---

**Architecture Owner:** DevOps Team  
**Last Updated:** 2024  
**Next Review:** Q2 2025
