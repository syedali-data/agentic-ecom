# Agentic-Ecom

A multi-agent AI system that automates the day-to-day work of an online store: product research and listings, ad campaigns, order support and fraud checks. Risky actions wait for human approval.

> **Status:** Prototype built in August 2025. The fulfillment, tracking and support services are mocked so the whole system runs locally without live store accounts.

## The agents

| Agent | Model | Job |
|---|---|---|
| **SalesGenie** | GPT-4o | Product research, listing copy, ad creatives, campaign launch and optimization |
| **LogiBot** | Claude | Fulfillment, order tracking, returns, customer support, fraud checks |
| **BuyBot** | GPT-4o | Customer-facing product Q&A and recommendations |

## What it does

- **REST API (FastAPI):** endpoints for products, orders, customers, support chat, analytics and agent triggers, with JWT sign-in.
- **Human-in-the-loop:** risky actions go to an approval queue. Budget limits, rate limiting and an emergency stop keep spending under control.
- **Integrations:** Shopify, Meta Ads, Pinterest Ads and CJ Dropshipping, each behind its own client in `services/`.
- **Event bus:** the agents hand tasks to each other through shared events.
- **Monitoring dashboard (Dash + Plotly):** revenue, products, customers and system health.
- **Scheduling:** an n8n workflow triggers the agents on a schedule.

## How it works

```
n8n schedule ──► FastAPI ──► SalesGenie / LogiBot / BuyBot
                     │              │
                     │              ▼
                     │     services: Shopify, Meta Ads, Pinterest, CJ
                     ▼
     HITL approval queue · budget guard · rate limits
                     │
                     ▼
   Database (SQLAlchemy: SQLite or PostgreSQL) ──► Dash dashboard
```

## Tech stack

Python, FastAPI, Pydantic, SQLAlchemy, OpenAI and Anthropic APIs, Dash and Plotly, n8n, pytest

## Project structure

```
agents/            SalesGenie, LogiBot, BuyBot
api/               FastAPI app, auth, analytics, approval and safety endpoints
services/          Shopify, Meta Ads, Pinterest, CJ clients, ad optimizer, budget guard
db/                Models, database setup, sample data
dashboard/         Dash monitoring app
config/            Agent, budget, compliance and rate-limit settings
prompts/           Prompt templates
n8n/workflows/     Scheduling workflow
tests/             Unit, integration and performance tests
docs/              Design notes and feature guides
```

## Run locally

```bash
pip install -r requirements.txt
# add your OpenAI and Anthropic keys to config/api_keys.yaml (or environment variables)
python db/init_database.py --action full-setup   # create tables and sample data
python api/fastapi_api.py       # API on http://localhost:8000
python dashboard/app.py         # dashboard on http://localhost:8050
pytest tests
```

## How it was built

I designed the agent roles and the safety controls (approval queue, budgets, emergency stop) and built the system with the help of AI coding assistants.
