# Codebase Onboarding Agent

A web app that takes a public GitHub repository URL and automatically generates a comprehensive onboarding document for new developers, powered by a multi-agent AI pipeline.

## Architecture

```
GitHub URL → Orchestrator → Architecture Agent → Setup Agent → Code Flow Agent → Writer Agent → Markdown
```

Each agent analyzes a different aspect of the repository using LLM calls via OpenRouter, and the Writer agent synthesizes everything into a clean onboarding guide.

## Prerequisites

- Python 3.11+
- Node.js 18+
- Redis server running locally
- OpenRouter API key ([get one here](https://openrouter.ai/keys))

## Quick Start

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env from example and add your OpenRouter key
cp .env.example .env

# Start the server
uvicorn main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 and paste a GitHub repo URL.

## Project Structure

```
├── backend/
│   ├── main.py                 # FastAPI app with API endpoints
│   ├── agents/
│   │   ├── orchestrator.py     # Coordinates the pipeline
│   │   ├── architecture.py     # Analyzes project structure & tech stack
│   │   ├── setup.py            # Extracts setup instructions
│   │   ├── code_flow.py        # Traces entry points & data flow
│   │   └── writer.py           # Synthesizes final markdown document
│   ├── services/
│   │   ├── github.py           # GitHub API client
│   │   ├── redis.py            # Redis caching & job tracking
│   │   └── llm.py              # OpenRouter LLM client
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── components/         # UrlInput, AgentProgressTracker, MarkdownResult
    │   ├── pages/              # Home, Processing, Result
    │   ├── api/client.js       # API client
    │   └── App.jsx             # Main app with view routing
    ├── package.json
    └── vite.config.js
```
