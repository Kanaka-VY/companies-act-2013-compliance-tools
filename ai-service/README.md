# AI Service

Flask-based AI microservice for Describe, Recommend, and Generate Report flows.

## Setup

1. Copy env file:
   - `cp .env.example .env` (Linux/macOS) or `copy .env.example .env` (Windows)
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run:
   - `python app.py`

## Environment Variables

- `GROQ_API_KEY`: Groq API key (required for live AI)
- `GROQ_MODEL`: model name used by all endpoints
- `REDIS_URL`: Redis connection string for AI cache
- `CACHE_TTL_SECONDS`: cache TTL in seconds (default 900)
- `CHROMA_PERSIST_DIR`: ChromaDB persistence directory
- `EMBEDDING_MODEL`: sentence-transformers model preloaded at startup

## API Reference

### POST `/describe`

Request:
```json
{"record":"Vendor onboarding missed risk sign-off and evidence tracking."}
```

Response:
```json
{
  "description":"Vendor onboarding has missing risk sign-off and weak evidence trail.",
  "risk_level":"high",
  "is_fallback":false,
  "generated_at":"2026-05-06T00:00:00+00:00"
}
```

### POST `/recommend`

Request:
```json
{"record":"Access review was delayed for privileged users."}
```

Response:
```json
{
  "recommendations":[
    {"action_type":"review","description":"Run an immediate privileged access review.","priority":"high"},
    {"action_type":"implement","description":"Automate access certification reminders.","priority":"medium"},
    {"action_type":"monitor","description":"Track monthly completion KPIs.","priority":"low"}
  ],
  "is_fallback":false,
  "generated_at":"2026-05-06T00:00:00+00:00"
}
```

### POST `/generate-report`

Request:
```json
{"record":"Data retention policy does not cover archived partner exports."}
```

Response:
```json
{
  "title":"Data Retention Compliance Review",
  "summary":"Retention scope gap detected for archived partner exports.",
  "overview":"Current policy omits archived datasets handled by partner integrations.",
  "key_items":["Scope mismatch","Control ownership unclear","Audit trail incomplete"],
  "recommendations":[{"action_type":"implement","description":"Extend retention controls to archives.","priority":"high"}],
  "is_fallback":false,
  "generated_at":"2026-05-06T00:00:00+00:00"
}
```

### GET `/health`

Response includes:
- model
- average response time
- uptime
- cache status
- seeded domain knowledge doc count

## Docker

Build:
- `docker build -t ai-service .`

Run:
- `docker run --env-file .env -p 8000:8000 ai-service`
