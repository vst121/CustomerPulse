# CustomerPulse

**AI-powered Customer Lifecycle & Value Management Platform**

CustomerPulse is a realistic Customer Lifecycle Management (CLM) and Customer Value Management (CVM) platform built as a practical backend engineering project.

The project is designed to explore how a modern customer intelligence platform can evolve from a **well-structured modular monolith** into an **event-driven, scalable and AI-powered architecture**.

The primary focus is not simply building CRUD APIs, but designing the foundations required for:

- Customer lifecycle management
- Customer value calculation
- Customer scoring
- Next Best Action (NBA)
- Customer 360
- Asynchronous processing
- Event-driven architecture
- AI/ML-powered customer intelligence
- Production-grade reliability and scalability

---

# Project Vision

CustomerPulse follows this conceptual flow:

```text
                    ┌──────────────────┐
                    │     Customer     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Transactions   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Customer Value  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Customer Scoring │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Decision / NBA   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Personalization  │
                    │   & Campaigns    │
                    └──────────────────┘
```

The long-term goal is to evolve this into:

```text
Customer Data
      │
      ▼
Prediction
      │
      ▼
Decision Engine
      │
      ▼
Next Best Action
      │
      ▼
Personalization / Campaign
      │
      ▼
Measurement & Feedback
      │
      └──────────────► ML / AI improvement
```

---

# Architecture Philosophy

CustomerPulse starts deliberately as a **modular monolith**.

The reason is simple:

> Build strong domain boundaries first. Distribute the system only when there is a real architectural reason to do so.

The initial architecture follows:

```text
API
 │
 ▼
Application
 │
 ▼
Domain

Infrastructure
 │
 └── implements persistence / messaging / external integrations
```

Dependency direction:

```text
API
 │
 ▼
Application
 │
 ▼
Domain
```

Infrastructure implements the contracts required by the application/domain layers.

This allows the system to evolve toward event-driven microservices without prematurely introducing distributed-system complexity.

---

# Technology Stack

## Backend

- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy 2.x (async)
- asyncpg
- PostgreSQL 17
- Alembic
- asyncio
- pytest
- HTTPX / FastAPI TestClient

## Frontend

- Next.js 16 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- Recharts (charts and visualizations)
- ESLint

## Deployment & Infrastructure

- Docker Compose

## Planned / Future

- Apache Kafka
- MongoDB
- ML/model-serving infrastructure
- Linux
- Jenkins
- SonarQube
- Nexus
- Observability stack

Redis is intentionally **not part of the current architecture**.

---

# Project Structure

```text
CustomerPulse/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── customer_360.py
│   │   │       ├── customers.py
│   │   │       ├── health.py
│   │   │       ├── recommendations.py
│   │   │       ├── router.py
│   │   │       ├── scoring.py
│   │   │       └── transactions.py
│   │   ├── application/
│   │   │   ├── common/
│   │   │   ├── customers/
│   │   │   ├── recommendations/
│   │   │   ├── scoring/
│   │   │   ├── transactions/
│   │   │   └── exceptions.py
│   │   ├── config/
│   │   │   └── settings.py
│   │   ├── domain/
│   │   │   ├── customers/
│   │   │   ├── recommendations/
│   │   │   ├── scoring/
│   │   │   ├── transactions/
│   │   │   └── value/
│   │   ├── infrastructure/
│   │   │   └── database/
│   │   │       ├── repositories/
│   │   │       ├── database.py
│   │   │       ├── models.py
│   │   │       └── unit_of_work.py
│   │   ├── schemas/
│   │   │   ├── customer_360.py
│   │   │   ├── customer_intelligence.py
│   │   │   ├── customers.py
│   │   │   └── transactions.py
│   │   └── main.py
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── alembic.ini
│   ├── tests/
│   │   ├── api/
│   │   ├── integration/
│   │   └── unit/
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── customers/
│   │   │   │   ├── [customerId]/
│   │   │   │   │   ├── 360/page.tsx
│   │   │   │   │   ├── intelligence/page.tsx
│   │   │   │   │   ├── recommendations/page.tsx
│   │   │   │   │   ├── page.tsx
│   │   │   │   │   └── transactions/
│   │   │   │   ├── new/page.tsx
│   │   │   │   └── page.tsx
│   │   │   ├── favicon.ico
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── intelligence/
│   │   │   ├── layout/
│   │   │   ├── transactions/
│   │   │   └── ui/
│   │   ├── services/
│   │   │   └── api/
│   │   └── types/
│   ├── .gitignore
│   ├── eslint.config.mjs
│   ├── next.config.ts
│   ├── package.json
│   ├── postcss.config.mjs
│   ├── pnpm-lock.yaml
│   ├── tsconfig.json
│   └── README.md
│
├── docs/
│   ├── Architecture.md
│   └── Requirements.md
│
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

# Getting Started

## Prerequisites

- Python 3.12+
- Node.js 20+
- pnpm 9+
- Docker & Docker Compose (for PostgreSQL)
- PostgreSQL 17 (or use the provided docker-compose)

## Setup — Backend

```bash
# Start PostgreSQL
docker-compose up -d

# Install dependencies
pip install -e ".[dev]"

# Run database migrations
alembic upgrade head

# Run tests
pytest
```

## Setup — Frontend

```bash
cd frontend

# Install dependencies
pnpm install

# Run the development server
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

The frontend proxies API requests to `http://localhost:8000` by default (configurable via `NEXT_PUBLIC_API_BASE_URL`).

## Running the Backend

```bash
# Development server (API docs at http://localhost:8000/docs)
uvicorn backend.app.main:app --reload
```

The API documentation is available at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

# Phase 1 — Core Customer Intelligence Platform

**Status: ✅ COMPLETE**

Phase 1 establishes the complete functional and architectural foundation of CustomerPulse.

## 1. FastAPI Foundation

Implemented:

- FastAPI application
- API versioning
- Application lifecycle
- Health endpoint
- Test infrastructure

Example:

```text
GET /api/v1/health
```

---

## 2. Customer Domain

Implemented:

- Customer domain entity
- Customer creation
- Customer retrieval
- Customer listing
- Pagination
- Search
- Lifecycle filtering
- Duplicate email handling
- Pydantic request/response models

---

## 3. PostgreSQL & Alembic

Implemented:

- PostgreSQL persistence
- SQLAlchemy 2.x
- Async database access
- Alembic migrations
- Database constraints
- Repository abstraction

---

## 4. Customer Lifecycle Management

Implemented lifecycle stages:

```text
ACQUISITION
     ↓
ONBOARDING
     ↓
ACTIVATION
     ↓
ENGAGEMENT
     ↓
GROWTH
     ↓
RETENTION
     ↓
WIN_BACK
```

Lifecycle stages are represented as domain concepts rather than arbitrary strings throughout the business logic.

---

## 5. Transaction Domain

Implemented:

- Transaction entity
- Transaction status
- Transaction categories
- Customer transactions
- Pagination
- Idempotency keys
- Database uniqueness constraints

Supported transaction statuses:

```text
PENDING
COMPLETED
FAILED
REVERSED
```

---

## 6. Error Handling

Implemented API-level handling for important domain conditions:

```text
400 / 422 → Invalid input
404       → Resource not found
409       → Duplicate resource
```

Business logic remains outside the API layer.

---

# 7. Unit of Work

Implemented a Unit of Work abstraction:

```text
UnitOfWork
    │
    ├── CustomerRepository
    ├── TransactionRepository
    ├── CustomerValueRepository
    ├── CustomerScoreRepository
    └── RecommendationRepository
```

This allows multiple changes to participate in one database transaction.

---

# 8. Concurrency & Idempotency

CustomerPulse explicitly addresses concurrent transaction requests.

Transaction creation uses an idempotency key:

```text
(customer_id, idempotency_key)
```

The database enforces uniqueness.

The system was also tested with concurrent requests to ensure that multiple requests with the same idempotency key result in a single transaction.

---

# 9. Customer Value

Implemented Customer Value:

```text
CustomerValue
 ├── total_spend
 └── transaction_count
```

Completed transactions update the customer's value.

Example:

```text
Transaction: €250
Transactions: 1

Customer Value:
total_spend      = €250
transaction_count = 1
```

---

# 10. Customer Scoring

Implemented the first rule-based scoring model.

Current formula:

```text
score =
    min(
        100,
        total_spend × 0.5
        +
        transaction_count × 5
    )
```

Example:

```text
€120 spend
1 transaction

120 × 0.5 + 1 × 5
= 65
```

The scoring domain is deliberately separated from the recommendation/decision logic.

This allows the future scoring implementation to evolve from:

```text
Rules
  ↓
Statistical Model
  ↓
ML Model
  ↓
AI / Predictive Model
```

without redesigning the entire platform.

---

# 11. Recommendation / Next Best Action

Implemented the first rule-based Next Best Action engine.

Current rules:

```text
WIN_BACK
    → REACTIVATION

Score >= 80
    → LOYALTY_REWARD

RETENTION
    → RETENTION_OFFER

Score >= 60
    → UPSELL

Score >= 40
    → CROSS_SELL

Otherwise
    → NO_ACTION
```

Each recommendation also contains an explanation/reason.

Example:

```text
Recommendation:
    type   = UPSELL
    reason = Customer has a strong value score.
```

---

# 12. Customer 360

Implemented:

```text
GET /api/v1/customers/{customer_id}/360
```

The Customer 360 view combines:

```text
Customer
   │
   ├── Lifecycle
   ├── Customer Value
   ├── Customer Score
   ├── Transactions
   └── Recommendations
```

This creates the foundation for a unified customer intelligence view.

---

# 13. Search & Filtering

Implemented:

- Customer search
- Lifecycle filtering
- Pagination
- Combined search + filtering
- Input validation

Example:

```text
GET /api/v1/customers?page=1&page_size=20
```

---

# 14. Integration Testing

Implemented API and integration tests covering:

- Customer creation
- Customer retrieval
- Customer search
- Transaction creation
- Transaction idempotency
- Customer value
- Customer scoring
- Recommendations
- Customer 360
- Background scoring
- Concurrent requests

Current test status:

```text
32 passed
0 failed
```

---

# 15. Background Processing

Implemented an in-process asynchronous background worker.

Current architecture:

```text
TransactionService
       │
       ▼
Transaction committed
       │
       ▼
Scoring Scheduler
       │
       ▼
BackgroundWorker
       │
       ▼
CustomerScoringJob
       │
       ▼
Fresh DB Session
       │
       ▼
CustomerScoringService
```

The background job deliberately creates its own database session rather than reusing the request-scoped session.

The scoring repository also uses an atomic PostgreSQL UPSERT to make concurrent scoring operations safe:

```text
Request A ──► UPSERT ──► INSERT

Request B ──► UPSERT ──► UPDATE
```

This prevents the classic:

```text
SELECT
   ↓
not found
   ↓
INSERT
```

race condition.

---

# 16. Frontend

A Next.js + TypeScript frontend provides the user interface for the platform.

## Pages

### Dashboard

```text
GET /  (static)
```

Displays the customer count and an overview of the customer lifecycle stages.

### Customer List

```text
GET /customers
```

Lists customers with:
- Search by name/email
- Filtering by lifecycle stage
- Pagination

### Customer Profile

```text
GET /customers/{customerId}
```

Shows customer details, lifecycle stage, and links to transactions, 360 view, intelligence, and recommendations.

### Customer 360

```text
GET /customers/{customerId}/360
```

A unified read model combining customer profile, value, score, transactions, and recommendations. Includes:
- KPI cards (total spend, transaction count, customer score)
- Transaction trend chart (recharts)
- Spending by category chart (recharts)
- Recent transactions table

### Customer Intelligence

```text
GET /customers/{customerId}/intelligence
```

Displays customer health, behavioral signals, risk assessment (churn probability), and the decision/next-best-action flow.

### Recommendations

```text
GET  /customers/{customerId}/recommendations
POST /customers/{customerId}/recommendations/generate
```

Lists existing recommendations and allows on-demand generation of Next Best Action recommendations.

### Transactions

```text
GET  /customers/{customerId}/transactions
POST /customers/{customerId}/transactions/new
```

Lists customer transactions with pagination and provides a form to record new transactions (with idempotency keys).

### Create Customer

```text
POST /customers/new
```

Form to create a new customer.

## Frontend Architecture

- **Next.js App Router** for file-based routing
- **React Server/Client component split** for optimal data fetching
- **apiClient** wrapper using the native `fetch` API with centralized error handling
- **TypeScript types** mirroring backend schemas (`@/types/`)
- **Tailwind CSS** with dark mode support via `ThemeProvider`
- **Component library** with reusable UI primitives (`Card`, `Badge`, `MetricCard`, `LoadingState`, `ErrorState`)
- Theme-aware styling throughout (light/dark mode toggle)

The frontend consumes the versioned FastAPI APIs under `/api/v1/`.

---

# Phase 1 Result

At the end of Phase 1, CustomerPulse is a functional customer intelligence backend.

The platform can:

```text
Create Customer
      ↓
Record Transaction
      ↓
Calculate Customer Value
      ↓
Calculate Customer Score
      ↓
Generate Next Best Action
      ↓
Expose Customer 360
```

with asynchronous background scoring, an interactive Next.js frontend, and automated tests.

**Phase 1: 🟢 COMPLETE**

---

# Phase 2 — Event-Driven & Production Architecture

**Status: 🔵 PLANNED / NEXT**

Phase 2 moves CustomerPulse from a functional modular monolith toward a production-oriented, event-driven architecture.

The main objective is:

> Introduce distributed-system capabilities only where they provide real business or operational value.

---

# Phase 2 Roadmap

## 1. Domain Events

First, introduce domain events.

Example:

```text
TransactionCompleted
        │
        ├── Update Customer Value
        │
        ├── Trigger Scoring
        │
        └── Trigger other interested processes
```

Instead of directly coupling transaction processing to every downstream operation:

```text
TransactionService
      │
      ├── Scoring
      ├── Recommendation
      ├── Analytics
      └── Campaign
```

we move toward:

```text
TransactionService
      │
      ▼
TransactionCompleted
      │
      ├── Scoring Handler
      ├── Analytics Handler
      ├── Recommendation Handler
      └── Campaign Handler
```

This is the first major step toward event-driven architecture.

---

# 2. Kafka

After establishing domain events, introduce Kafka.

Target architecture:

```text
                    ┌───────────────┐
                    │ Transaction   │
                    │    Service    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │     Kafka     │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
          Scoring       Analytics     Recommendation
          Consumer       Consumer        Consumer
```

Topics, consumer groups, partitioning, ordering, retries and dead-letter handling will be introduced progressively.

---

# 3. Reliable Event Processing

Phase 2 will address:

- At-least-once delivery
- Idempotent consumers
- Retry policies
- Dead Letter Queue
- Poison messages
- Event ordering
- Correlation IDs
- Message tracing
- Consumer failures

The goal is to understand the difference between:

```text
Message delivered
```

and:

```text
Business operation successfully processed
```

---

# 4. Customer Value Concurrency

The current CustomerValue implementation uses a read-modify-write pattern.

Under heavy concurrent transaction processing, this can potentially cause lost updates.

Phase 2 will introduce a stronger approach, such as:

```text
Atomic SQL update
```

or appropriate row-level concurrency control.

The objective is to guarantee correct customer value even under high transaction concurrency.

---

# 5. Prediction Layer

Introduce a dedicated prediction abstraction.

Architecture:

```text
Customer Data
     │
     ▼
Feature Preparation
     │
     ▼
Prediction Model
     │
     ▼
Prediction Result
```

Prediction remains separate from business decisions.

For example:

```text
Prediction:
    churn_probability = 0.87
```

does not automatically mean:

```text
Decision:
    send_discount
```

The Decision Engine remains responsible for turning predictions into actions.

---

# 6. Decision Engine

Introduce an explicit decision layer:

```text
Customer Data
     │
     ▼
Predictions
     │
     ▼
Business Rules
     │
     ▼
Constraints
     │
     ▼
Decision
```

Example:

```text
Churn probability = 0.87
Customer value     = HIGH
Lifecycle          = RETENTION
Campaign eligibility = TRUE

                ↓

Decision:
RETENTION_OFFER
```

This separation is particularly important for explainability and enterprise systems.

---

# 7. Next Best Action Evolution

The current NBA engine is rule-based.

It will evolve toward:

```text
Rule-based NBA
      ↓
Scored candidates
      ↓
Prediction-assisted NBA
      ↓
Optimization
      ↓
AI-assisted decisioning
```

Potential inputs:

- Customer value
- Lifecycle stage
- Churn probability
- Purchase history
- Product affinity
- Customer behavior
- Campaign history
- Business constraints

---

# 8. MongoDB

MongoDB will be introduced where document-oriented data provides a genuine advantage.

Potential use cases:

- Customer behavioral profiles
- Flexible customer attributes
- Model/prediction metadata
- Recommendation context
- Event-derived customer views

PostgreSQL remains the source of truth for transactional relational data.

---

# 9. Observability

Introduce production-grade observability:

```text
Logs
Metrics
Traces
Health Checks
Correlation IDs
```

Important metrics include:

```text
TPS
P95 latency
P99 latency
Error rate
Queue depth
Consumer lag
Job processing time
Database latency
```

This allows architecture decisions to be based on measurable system behavior rather than assumptions.

---

# 10. Reliability & Resilience

Phase 2 will address:

- Timeouts
- Retries
- Backoff
- Circuit breakers where appropriate
- Idempotency
- Failure isolation
- Graceful shutdown
- Background worker draining
- Database failure scenarios
- Kafka failure scenarios

---

# 11. Security

Introduce:

- Authentication
- Authorization
- Role-based access
- API security
- Input validation
- Secrets management
- Secure configuration
- Audit logging

---

# 12. Advanced Python / Async Architecture

The project will also be used to deeply explore modern Python backend engineering.

Topics include:

```text
async / await
asyncio
Tasks
Queues
I/O concurrency
Cancellation
Timeouts
Context management
Generators
Async generators
Dependency injection
Typing
Protocols
Generics
Performance optimization
```

The goal is not learning Python syntax in isolation.

The goal is understanding how Python is used to build **high-performance asynchronous backend systems**.

---

# 13. Production Docker & Linux

CustomerPulse will eventually run as containerized services:

```text
Frontend
   │
Backend API
   │
 ┌─┴───────────────┐
 │                 │
PostgreSQL       Kafka
 │                 │
 └───────┬─────────┘
         │
    Background
     Consumers
```

Topics include:

- Multi-stage Docker builds
- Container security
- Linux runtime behavior
- Resource limits
- Health checks
- Networking
- Production configuration

---

# 14. CI/CD

Planned pipeline:

```text
Git Push
   │
   ▼
Build
   │
   ▼
Unit Tests
   │
   ▼
Integration Tests
   │
   ▼
Static Analysis
   │
   ▼
Security Checks
   │
   ▼
Docker Build
   │
   ▼
Artifact Repository
   │
   ▼
Deployment
```

Potential tooling:

- Jenkins
- SonarQube
- Nexus
- Docker
- Kubernetes

---

# 15. Frontend

A Next.js + TypeScript frontend provides the user interface:

```text
Customer Dashboard
       │
       ├── Customer 360
       ├── Lifecycle
       ├── Transactions
       ├── Customer Value
       ├── Score
       ├── Intelligence
       ├── Recommendations
       └── Next Best Actions
```

The frontend consumes the versioned FastAPI APIs under `/api/v1/`.

---

# Architecture Evolution

The overall evolution of CustomerPulse is intentional:

```text
PHASE 1

Modular Monolith
       │
       ├── PostgreSQL
       ├── REST API
       ├── Domain Layer
       ├── Application Layer
       └── Background Worker


                ↓


PHASE 2

Event-Driven Modular System
       │
       ├── REST API
       ├── Domain Events
       ├── Kafka
       ├── Consumers
       ├── PostgreSQL
       ├── MongoDB
       ├── Prediction
       ├── Decision Engine
       └── Observability


                ↓


FUTURE

Distributed Customer Intelligence Platform
       │
       ├── Customer Data
       ├── Event Streaming
       ├── ML / AI
       ├── Prediction
       ├── Decisioning
       ├── Next Best Action
       ├── Personalization
       ├── Experimentation
       └── Continuous Feedback
```

---

# Engineering Principles

CustomerPulse follows several principles throughout its evolution.

### 1. Domain first

Business concepts should not depend on infrastructure.

### 2. Explicit boundaries

Customer, transaction, scoring, recommendation and prediction responsibilities should remain clearly separated.

### 3. Database as concurrency authority

Database constraints and atomic operations are used where correctness depends on concurrent access.

### 4. Async where it provides value

Asynchronous programming is used for I/O-bound and background workloads rather than simply making everything async.

### 5. Events for decoupling

Events should be introduced when multiple independent consumers need to react to business events.

### 6. Distributed systems only when justified

Do not introduce Kafka, microservices or other distributed infrastructure simply because they are fashionable.

### 7. Measure before optimizing

Performance decisions should be based on:

```text
TPS
P95
P99
CPU
Memory
Database latency
Queue depth
Consumer lag
```

---

# Current Status

```text
Phase 1 — Core Customer Intelligence
████████████████████████████████ 100%

Phase 2 — Event-Driven & Production Architecture
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0%
```

Current test status:

```text
32 passed
0 failed
```

---

# API Overview

Current APIs include:

```text
GET    /api/v1/health

GET    /api/v1/customers
POST   /api/v1/customers
GET    /api/v1/customers/{customer_id}
GET    /api/v1/customers/{customer_id}/intelligence

GET    /api/v1/transactions/customers/{customer_id}
POST   /api/v1/transactions/customers/{customer_id}
GET    /api/v1/transactions/{transaction_id}

GET    /api/v1/customers/{customer_id}/scores

GET    /api/v1/customers/{customer_id}/recommendations
POST   /api/v1/customers/{customer_id}/recommendations/generate

GET    /api/v1/customers/{customer_id}/360
```

---

# Project Objective

CustomerPulse is also an engineering learning project.

The objective is to practice the complete lifecycle of a modern backend platform:

```text
Requirements
     ↓
Domain Modeling
     ↓
Architecture
     ↓
Implementation
     ↓
Testing
     ↓
Concurrency
     ↓
Async Processing
     ↓
Event-Driven Architecture
     ↓
Distributed Systems
     ↓
AI / ML
     ↓
Observability
     ↓
CI/CD
     ↓
Production
```

The final system should demonstrate not only that the application works, but **why the architecture works, where it can fail, how it scales, and how it should evolve**.

---

# Phase Completion Criteria

A phase is considered complete when:

- The required functionality is implemented.
- Domain boundaries are respected.
- Tests cover the important behavior.
- Concurrency implications are understood.
- Architecture decisions are documented.
- Known technical debt is explicitly identified rather than hidden.

---

# License

This project is currently a personal engineering and learning project.
