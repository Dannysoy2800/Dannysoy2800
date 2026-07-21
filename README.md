# OmniRouter AI

OmniRouter AI is a production-ready FastAPI starter for routing chat requests across multiple AI providers. It starts with Gemini, Groq, and OpenRouter support and includes automatic fallback when a provider is unavailable, unconfigured, or returns an upstream error.

## Features

- FastAPI application skeleton with health and chat endpoints.
- Provider framework for Gemini, Groq, and OpenRouter.
- Automatic fallback based on configurable provider order.
- Environment-based configuration with no secrets committed to source control.
- Docker, Docker Compose, and Railway deployment files.
- Tests for API health and fallback behavior.

## Project structure

```text
.
├── omnirouter_ai/
│   ├── app.py                  # FastAPI app factory and HTTP routes
│   ├── config.py               # Environment-driven settings
│   ├── router.py               # Provider selection and fallback logic
│   ├── schemas.py              # Pydantic request/response schemas
│   └── providers/              # Gemini, Groq, and OpenRouter adapters
├── tests/                      # Automated tests
├── .env.example                # Safe configuration template
├── Dockerfile                  # Container image definition
├── docker-compose.yml          # Local container orchestration
├── railway.json                # Railway deployment configuration
├── main.py                     # Local development runner
├── pyproject.toml              # Package metadata
└── requirements.txt            # Runtime and test dependencies
```

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 3. Configure providers

```bash
cp .env.example .env
```

Add API keys for the providers you want to enable. At least one provider key is required for `/v1/chat` to return model output.

| Variable | Purpose | Default |
| --- | --- | --- |
| `OMNI_PROVIDER_ORDER` | Fallback order used by the router. | `["gemini","groq","openrouter"]` |
| `OMNI_GEMINI_API_KEY` | Enables Gemini routing. | Not set |
| `OMNI_GEMINI_MODEL` | Gemini model name. | `gemini-1.5-flash` |
| `OMNI_GROQ_API_KEY` | Enables Groq routing. | Not set |
| `OMNI_GROQ_MODEL` | Groq model name. | `llama-3.1-8b-instant` |
| `OMNI_OPENROUTER_API_KEY` | Enables OpenRouter routing. | Not set |
| `OMNI_OPENROUTER_MODEL` | OpenRouter model identifier. | `openai/gpt-4o-mini` |
| `OMNI_REQUEST_TIMEOUT_SECONDS` | Upstream HTTP timeout. | `30` |

### 4. Run locally

```bash
uvicorn omnirouter_ai.app:app --reload
```

Or:

```bash
python main.py
```

Open the interactive API docs at <http://localhost:8000/docs>.

## API usage

### Health check

```bash
curl http://localhost:8000/health
```

### Routed chat request

```bash
curl -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a concise assistant."},
      {"role": "user", "content": "Write a one-line launch tagline."}
    ]
  }'
```

To force a provider for one request, include `"provider": "groq"`, `"provider": "gemini"`, or `"provider": "openrouter"` in the JSON body.

## Deployment

### Docker Compose

```bash
docker compose up --build
```

### Railway

1. Create a Railway service from this repository.
2. Add the provider environment variables from `.env.example`.
3. Deploy with the included `railway.json` configuration.

## Development

Run tests:

```bash
python -m pytest
```

## Security notes

- Keep real API keys in `.env`, Railway variables, or another secret manager.
- Do not commit credentials, private keys, or provider secrets.
- Configure only providers you intend to use.
