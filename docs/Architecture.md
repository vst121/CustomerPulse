\# CustomerPulse — Architecture



\*\*Project:\*\* CustomerPulse

\*\*Version:\*\* 1.0

\*\*Status:\*\* Draft / Development Baseline

\*\*Document:\*\* Architecture Specification

\*\*Related Document:\*\* `Requirements.md`



\---



\# 1. Architecture Vision



CustomerPulse is designed as a \*\*modular monolith first\*\*, with a clear path toward an event-driven distributed architecture.



The fundamental architectural principle is:



> \*\*Start simple, establish strong boundaries, measure real requirements, and introduce distributed complexity only when it solves a demonstrated problem.\*\*



The initial architecture is:



```text

┌──────────────────────┐

│      Browser         │

└──────────┬───────────┘

&#x20;          │

&#x20;          │ HTTP / JSON

&#x20;          ▼

┌──────────────────────┐

│       Next.js        │

│ React + TypeScript   │

└──────────┬───────────┘

&#x20;          │

&#x20;          │ REST API

&#x20;          ▼

┌──────────────────────────────────────┐

│              FastAPI                 │

│                                      │

│  API → Application → Domain          │

│                    ↑                 │

│              Infrastructure          │

└───────────────────┬──────────────────┘

&#x20;                   │

&#x20;                   ▼

&#x20;            ┌─────────────┐

&#x20;            │ PostgreSQL  │

&#x20;            └─────────────┘

```



The architecture will evolve incrementally:



```text

Modular Monolith

&#x20;      ↓

PostgreSQL

&#x20;      ↓

Customer 360

&#x20;      ↓

CLM / CVM Decisioning

&#x20;      ↓

Redis / MongoDB where justified

&#x20;      ↓

Kafka + Background Workers

&#x20;      ↓

ML / AI

&#x20;      ↓

Selective Service Extraction

```



\---



\# 2. Architectural Goals



The architecture must support:



\* Clear business boundaries

\* High testability

\* Maintainability

\* API scalability

\* Efficient data access

\* Asynchronous processing

\* Event-driven evolution

\* AI/ML integration

\* Observability

\* Containerization

\* CI/CD

\* Future horizontal scaling



The architecture should also demonstrate senior-level engineering decisions.



\---



\# 3. Architectural Non-Goals



The initial architecture will \*\*not\*\* attempt to provide:



\* Microservices for every domain

\* Kubernetes from day one

\* Multiple databases without a clear reason

\* Kafka before asynchronous events are actually needed

\* Redis before caching requirements are demonstrated

\* ML infrastructure before the business decision model exists

\* Distributed transactions

\* Premature service decomposition



The architecture should avoid technology-driven complexity.



\---



\# 4. High-Level System Architecture



The logical system is divided into:



```text

┌─────────────────────────────────────────────┐

│                  Frontend                   │

│                                             │

│          Next.js / React / TypeScript       │

└──────────────────────┬──────────────────────┘

&#x20;                      │

&#x20;                      │ HTTPS / REST / JSON

&#x20;                      ▼

┌─────────────────────────────────────────────┐

│                  Backend                    │

│                                             │

│                  FastAPI                    │

│                                             │

│ ┌──────────┐ ┌────────────┐ ┌────────────┐ │

│ │   API    │ │ Application│ │   Domain   │ │

│ └──────────┘ └────────────┘ └────────────┘ │

│                         │                   │

│                 ┌───────▼────────┐         │

│                 │ Infrastructure  │         │

│                 └───────┬────────┘         │

└─────────────────────────┼───────────────────┘

&#x20;                         │

&#x20;             ┌───────────┼─────────────┐

&#x20;             ▼           ▼             ▼

&#x20;       PostgreSQL     MongoDB       Redis

```



Later:



```text

&#x20;                        ┌──────────────┐

&#x20;                        │    Kafka     │

&#x20;                        └──────┬───────┘

&#x20;                               │

&#x20;                   ┌───────────┼───────────┐

&#x20;                   ▼           ▼           ▼

&#x20;               Scoring      Lifecycle   Analytics

&#x20;               Worker        Worker      Worker

```



\---



\# 5. Frontend Architecture



The frontend uses:



\* Next.js

\* React

\* TypeScript



The frontend is responsible for:



\* User interface

\* Routing

\* Presentation

\* UI state

\* Form handling

\* Calling backend APIs

\* Displaying customer information

\* Displaying recommendations

\* Dashboard visualization



The frontend should \*\*not own core business rules\*\*.



For example, this should not happen:



```text

Next.js:

if churnProbability > 0.7:

&#x20;   showRetentionOffer()

```



Instead:



```text

Next.js

&#x20;  ↓

GET /customers/{id}/recommendations

&#x20;  ↓

FastAPI

&#x20;  ↓

Decision Engine

&#x20;  ↓

Recommendation

&#x20;  ↓

Next.js displays result

```



This keeps business decisions centralized.



\---



\# 6. Backend Architecture



The backend follows a layered architecture:



```text

┌──────────────────────────────┐

│          API Layer           │

├──────────────────────────────┤

│      Application Layer       │

├──────────────────────────────┤

│         Domain Layer         │

├──────────────────────────────┤

│      Infrastructure Layer    │

└──────────────────────────────┘

```



The layers have different responsibilities.



\---



\# 7. API Layer



The API layer is responsible for:



\* HTTP endpoints

\* Routing

\* Request validation

\* Response serialization

\* Authentication boundary

\* Authorization boundary

\* HTTP status codes

\* API error mapping



Example:



```text

POST /api/v1/customers

```



The API layer should translate:



```text

HTTP Request

&#x20;    ↓

Application Command / Input

&#x20;    ↓

Use Case

```



The API layer should \*\*not contain business logic\*\*.



Bad:



```python

if customer.churn\_probability > 0.7:

&#x20;   recommendation = "RETENTION"

```



Better:



```text

API

&#x20;↓

GenerateRecommendationUseCase

&#x20;↓

DecisionEngine

```



\---



\# 8. Application Layer



The Application layer coordinates use cases.



Examples:



```text

CreateCustomer

GetCustomer

RecordTransaction

CalculateCustomerValue

CalculateCustomerScores

DetermineLifecycle

GenerateRecommendation

ExecuteRecommendation

```



The Application layer is responsible for:



\* Orchestration

\* Use-case execution

\* Transaction boundaries

\* Calling domain services

\* Calling repository abstractions

\* Coordinating infrastructure operations



Example:



```text

GenerateRecommendationUseCase

&#x20;       │

&#x20;       ├── Load Customer

&#x20;       ├── Load Customer Value

&#x20;       ├── Load Customer Scores

&#x20;       ├── Execute Decision Engine

&#x20;       ├── Create Recommendation

&#x20;       └── Persist Recommendation

```



\---



\# 9. Domain Layer



The Domain layer contains the core business logic.



It should have \*\*no dependency on FastAPI, SQLAlchemy, PostgreSQL, MongoDB, Redis, or Kafka\*\*.



Potential domain modules:



```text

domain/

├── customers/

├── transactions/

├── lifecycle/

├── value/

└── recommendations/

```



The domain layer contains:



\* Entities

\* Value objects

\* Business rules

\* Domain services

\* Domain policies

\* Domain events



Examples:



```text

Customer

Transaction

CustomerValue

CustomerScore

Recommendation



LifecyclePolicy

CustomerValueCalculator

RecommendationPolicy

DecisionEngine

```



\---



\# 10. Infrastructure Layer



The Infrastructure layer provides technical implementations.



Examples:



```text

infrastructure/

├── database/

├── mongodb/

├── cache/

├── messaging/

├── external\_services/

└── observability/

```



Responsibilities include:



\* SQLAlchemy implementations

\* PostgreSQL repositories

\* MongoDB repositories

\* Redis cache

\* Kafka producers/consumers

\* External API clients

\* Logging

\* Metrics

\* Tracing



Infrastructure implements contracts required by the Application/Domain layers.



\---



\# 11. Dependency Direction



The dependency direction should be:



```text

&#x20;       API

&#x20;        │

&#x20;        ▼

&#x20;  Application

&#x20;        │

&#x20;        ▼

&#x20;     Domain

&#x20;        ▲

&#x20;        │

&#x20;Infrastructure

```



The important rule is:



> \*\*Business logic must not depend on infrastructure details.\*\*



For example:



```text

Domain

&#x20; ✕ imports SQLAlchemy

&#x20; ✕ imports FastAPI

&#x20; ✕ imports Redis

&#x20; ✕ imports Kafka

```



Instead:



```text

Application

&#x20;    ↓

Repository Interface

&#x20;    ↑

PostgreSQL Repository

```



This makes the business logic testable without a database.



\---



\# 12. Repository Pattern



The application should depend on repository abstractions rather than database implementations.



Conceptually:



```text

CustomerRepository

&#x20;      ▲

&#x20;      │

&#x20;      │ implements

&#x20;      │

PostgresCustomerRepository

```



Example interface:



```python

class CustomerRepository(Protocol):

&#x20;   async def get\_by\_id(

&#x20;       self,

&#x20;       customer\_id: UUID

&#x20;   ) -> Customer | None:

&#x20;       ...

```



The application does not need to know whether the implementation uses:



\* PostgreSQL

\* MongoDB

\* Another database

\* A test double



\---



\# 13. Dependency Injection



FastAPI dependency injection will primarily be used at the application/API boundary.



Conceptually:



```text

HTTP Request

&#x20;    ↓

FastAPI Dependency

&#x20;    ↓

Application Service

&#x20;    ↓

Repository

```



Dependencies should be composed at the application's composition boundary.



This allows:



\* Test substitution

\* Configuration-based implementations

\* Clear lifecycle management

\* Separation of concerns



\---



\# 14. Domain Boundaries



The initial logical domains are:



```text

┌──────────────┐

│  Customers   │

└──────────────┘



┌──────────────┐

│ Transactions │

└──────────────┘



┌──────────────┐

│  Lifecycle   │

└──────────────┘



┌──────────────┐

│     Value    │

└──────────────┘



┌──────────────┐

│Recommendations│

└──────────────┘

```



These are \*\*logical boundaries\*\*, not necessarily separate deployable services.



Initially they live inside one application.



\---



\# 15. Modular Monolith



CustomerPulse starts as a modular monolith.



The runtime may look like:



```text

customerpulse-api

│

├── customers

├── transactions

├── lifecycle

├── value

└── recommendations

```



All modules run in the same process.



However, the code should maintain clear boundaries.



This gives us:



\* Simple deployment

\* Simple debugging

\* Low operational overhead

\* Fast development

\* Strong domain boundaries

\* Easier refactoring



while still preparing for future service extraction.



\---



\# 16. Why Not Microservices First?



The architecture deliberately avoids:



```text

customer-service

transaction-service

lifecycle-service

value-service

recommendation-service

```



as separate deployments during the first phase.



That would introduce:



\* Network communication

\* Service discovery

\* Distributed tracing

\* Multiple deployments

\* Distributed failures

\* Data ownership questions

\* Message brokers

\* Deployment complexity



before those problems actually exist.



The architecture instead creates \*\*service boundaries in code first\*\*.



If later a domain needs independent scaling or deployment, it can be extracted.



\---



\# 17. Database Architecture



PostgreSQL is the initial system of record.



```text

FastAPI

&#x20;  ↓

SQLAlchemy

&#x20;  ↓

PostgreSQL

```



PostgreSQL will initially contain:



```text

customers

transactions

customer\_values

customer\_scores

recommendations

```



Database migrations are managed with:



```text

Alembic

```



\---



\# 18. Relational Data Model



The initial logical relationships are:



```text

Customer

&#x20;  │

&#x20;  ├──────────< Transaction

&#x20;  │

&#x20;  ├────────── CustomerValue

&#x20;  │

&#x20;  ├────────── CustomerScore

&#x20;  │

&#x20;  └──────────< Recommendation

```



A customer can have:



\* Many transactions

\* One current customer-value record

\* One current score set

\* Many recommendations



Historical versions may later be introduced where required.



\---



\# 19. Database Access



The application should use:



\* SQLAlchemy 2.x

\* Async database access where appropriate

\* Connection pooling

\* Parameterized queries

\* Explicit transactions

\* Proper indexes



Large datasets must not be loaded unnecessarily into application memory.



For example, this should be avoided:



```python

transactions = await repository.get\_all()

```



when millions of transactions may exist.



Instead:



```text

Database

&#x20;  ↓

Filtered Query

&#x20;  ↓

Pagination / Streaming

&#x20;  ↓

Application

```



\---



\# 20. MongoDB Architecture



MongoDB will be introduced only when a concrete document-oriented requirement appears.



Potential architecture:



```text

Application

&#x20;   ↓

Mongo Repository

&#x20;   ↓

MongoDB

```



Possible use cases include:



\* Flexible customer interaction history

\* Recommendation explanations

\* Customer 360 projections

\* Event-oriented documents

\* Evolving ML output structures



MongoDB should not become a second copy of PostgreSQL without a clear purpose.



\---



\# 21. Redis Architecture



Redis will be introduced as a cache and fast state store.



Potential architecture:



```text

FastAPI

&#x20;  ↓

Cache

&#x20;  ↓

Redis

```



Example:



```text

GET Customer 360

&#x20;      ↓

&#x20;  Redis Cache

&#x20;      │

&#x20;  ┌───┴───┐

&#x20;  │       │

&#x20;HIT     MISS

&#x20;  │       │

&#x20;  │       ▼

&#x20;  │   PostgreSQL

&#x20;  │       │

&#x20;  └───────┘

&#x20;      ↓

&#x20;   Response

```



Cache behavior must define:



\* TTL

\* Invalidation

\* Consistency expectations

\* Failure behavior

\* Stampede prevention



Redis should not become a mandatory dependency for basic correctness.



\---



\# 22. Customer 360 Architecture



Customer 360 is a \*\*logical read model\*\*.



It combines information from several domains:



```text

&#x20;                 Customer

&#x20;                    │

&#x20;       ┌────────────┼────────────┐

&#x20;       ▼            ▼            ▼

&#x20;  Transactions    Value        Scores

&#x20;       │            │            │

&#x20;       └────────────┼────────────┘

&#x20;                    ▼

&#x20;             Customer 360

&#x20;                    │

&#x20;                    ▼

&#x20;            Recommendation

```



Initially this can be composed synchronously from PostgreSQL.



Later, a denormalized read model may be created:



```text

Domain Events

&#x20;    ↓

Kafka

&#x20;    ↓

Customer360Projector

&#x20;    ↓

MongoDB / Read Store

```



This allows read optimization without changing the source-of-truth domains.



\---



\# 23. CLM Architecture



Customer Lifecycle Management follows:



```text

Customer Data

&#x20;    ↓

Behavior

&#x20;    ↓

Scores

&#x20;    ↓

Lifecycle Rules

&#x20;    ↓

Lifecycle Stage

```



Example:



```text

Churn Probability = 0.82

&#x20;       +

Low Engagement

&#x20;       +

Existing Customer

&#x20;       ↓

RETENTION

```



Lifecycle rules belong to the domain/application logic, not the frontend.



\---



\# 24. CVM Architecture



Customer Value Management follows:



```text

Transactions

&#x20;    ↓

Historical Value

&#x20;    ↓

Future Value Prediction

&#x20;    ↓

Customer Lifetime Value

&#x20;    ↓

Value Segment

```



Example:



```text

Historical Value = €5,200

Future Value     = €3,250



CLV              = €8,450

```



The calculation should be isolated behind a domain service or strategy.



\---



\# 25. Decision Engine



The Decision Engine is one of the most important architectural components.



Its responsibility is to transform predictions and customer context into business decisions.



```text

Customer Context

&#x20;      │

&#x20;      ├── Lifecycle

&#x20;      ├── Value

&#x20;      ├── Scores

&#x20;      ├── Products

&#x20;      └── Behavior

&#x20;             │

&#x20;             ▼

&#x20;       Decision Engine

&#x20;             │

&#x20;             ▼

&#x20;      Next Best Action

```



Example:



```text

IF

&#x20;   churn\_probability > 0.70

AND

&#x20;   customer\_value > 5000

THEN

&#x20;   RETENTION\_OFFER

```



The decision engine should be independent of the ML model implementation.



\---



\# 26. Prediction Architecture



Predictions are treated as inputs to business decisions.



Example:



```text

Transaction History

&#x20;       ↓

Feature Engineering

&#x20;       ↓

Churn Model

&#x20;       ↓

0.82 churn probability

&#x20;       ↓

Decision Engine

&#x20;       ↓

Retention Recommendation

```



The ML model should not directly execute a customer action.



This separation makes it possible to replace:



```text

Rule-based scoring

```



with:



```text

Machine Learning

```



without redesigning the entire decision engine.



\---



\# 27. Recommendation Architecture



The recommendation flow is:



```text

Customer

&#x20;  ↓

Customer Context

&#x20;  ↓

Predictions

&#x20;  ↓

Business Rules

&#x20;  ↓

Decision Engine

&#x20;  ↓

Recommendation

&#x20;  ↓

Explanation

```



The recommendation should contain:



```text

action

product

reason

confidence

status

```



The recommendation becomes a domain object rather than simply an API response.



\---



\# 28. API Versioning



All public APIs will initially use:



```text

/api/v1

```



Example:



```text

GET /api/v1/customers

GET /api/v1/customers/{customer\_id}

GET /api/v1/customers/{customer\_id}/transactions

GET /api/v1/customers/{customer\_id}/recommendations

```



Breaking changes should result in a new API version.



\---



\# 29. API Contract vs Database Model



Database models and API schemas must remain separate.



Conceptually:



```text

HTTP Request

&#x20;    ↓

Pydantic Request Schema

&#x20;    ↓

Application

&#x20;    ↓

Domain Model

&#x20;    ↓

Repository

&#x20;    ↓

SQLAlchemy Model

&#x20;    ↓

PostgreSQL

```



The reverse applies for responses.



This prevents database structure from accidentally becoming the public API contract.



\---



\# 30. Async Architecture



Async programming will be used primarily for I/O-bound workloads.



Good candidates:



```text

Database calls

HTTP calls

Kafka operations

Redis operations

File/network I/O

```



Async does not automatically make CPU-heavy work faster.



CPU-heavy operations such as:



```text

Large-scale feature calculations

ML inference

Large data transformations

```



should eventually be moved to workers or dedicated processing components.



\---



\# 31. Background Worker Architecture



Long-running work should eventually be separated from HTTP requests.



Example:



```text

POST /customers/{id}/scores/calculate

&#x20;             │

&#x20;             ▼

&#x20;       Create Job/Event

&#x20;             │

&#x20;             ▼

&#x20;       Background Worker

&#x20;             │

&#x20;             ▼

&#x20;      Calculate Scores

&#x20;             │

&#x20;             ▼

&#x20;       Store Result

```



The HTTP request should not remain open for a long-running scoring process.



\---



\# 32. Event-Driven Evolution



The architecture will eventually evolve toward:



```text

&#x20;                   ┌──────────────┐

&#x20;                   │   FastAPI    │

&#x20;                   └──────┬───────┘

&#x20;                          │

&#x20;                          ▼

&#x20;                     PostgreSQL

&#x20;                          │

&#x20;                          ▼

&#x20;                 TransactionRecorded

&#x20;                          │

&#x20;                          ▼

&#x20;                    ┌──────────┐

&#x20;                    │  Kafka   │

&#x20;                    └────┬─────┘

&#x20;                         │

&#x20;           ┌─────────────┼──────────────┐

&#x20;           ▼             ▼              ▼

&#x20;      Scoring         Lifecycle      Analytics

&#x20;      Consumer        Consumer       Consumer

&#x20;           │             │              │

&#x20;           └─────────────┼──────────────┘

&#x20;                         ▼

&#x20;                   Recommendation

```



\---



\# 33. Event Delivery Semantics



The initial event architecture assumes:



> \*\*At-least-once delivery\*\*



Therefore consumers must be idempotent.



A consumer may receive:



```text

TransactionRecorded

TransactionRecorded

```



for the same transaction.



The result must still be:



```text

Transaction processed once

```



from a business perspective.



\---



\# 34. Idempotency Architecture



Possible implementation:



```text

Kafka Event

&#x20;    ↓

Check Event / Transaction ID

&#x20;    ↓

Already processed?

&#x20;  ┌───────┴───────┐

&#x20; YES             NO

&#x20;  │               │

Ignore        Process

&#x20;                  │

&#x20;                  ▼

&#x20;            Store Processed ID

```



Database constraints should provide a second layer of protection.



Idempotency must not depend solely on application memory.



\---



\# 35. Retry Architecture



Transient failures should be retried.



Example:



```text

Event

&#x20;↓

Consumer

&#x20;↓

Processing

&#x20;↓

Failure

&#x20;↓

Retry

&#x20;↓

Retry

&#x20;↓

Retry

&#x20;↓

DLQ

```



Retries should distinguish between:



\### Transient failures



Examples:



\* Temporary database outage

\* Network timeout

\* Temporary external API failure



These may be retried.



\### Permanent failures



Examples:



\* Invalid message

\* Invalid schema

\* Impossible business state



These should generally move toward a DLQ rather than retry indefinitely.



\---



\# 36. Dead-Letter Queue



A dead-letter queue provides isolation for messages that cannot be successfully processed.



```text

Kafka Topic

&#x20;    ↓

Consumer

&#x20;    ↓

Processing Failure

&#x20;    ↓

Retry Policy

&#x20;    ↓

DLQ

```



DLQ messages should contain enough metadata to diagnose the failure.



Potential metadata:



```text

event\_id

event\_type

timestamp

correlation\_id

consumer

failure\_reason

retry\_count

original\_payload

```



Sensitive data must be handled carefully.



\---



\# 37. Event Ordering



Ordering requirements must be defined by business semantics.



For example:



```text

TransactionCreated

TransactionReversed

```



may require ordering.



Ordering should not be assumed globally.



Kafka partitioning should eventually be designed around the required ordering key, potentially:



```text

customer\_id

```



where customer-level ordering is required.



\---



\# 38. Correlation and Request IDs



Requests and events should eventually carry correlation information.



Example:



```text

HTTP Request

request\_id = ABC123

&#x20;     ↓

TransactionRecorded

correlation\_id = ABC123

&#x20;     ↓

Kafka Consumer

correlation\_id = ABC123

&#x20;     ↓

RecommendationGenerated

correlation\_id = ABC123

```



This allows a complete business operation to be traced.



\---



\# 39. Observability Architecture



Observability will be implemented across:



```text

Logs

Metrics

Traces

```



Conceptually:



```text

&#x20;                CustomerPulse

&#x20;                     │

&#x20;         ┌───────────┼───────────┐

&#x20;         ▼           ▼           ▼

&#x20;       Logs        Metrics      Traces

&#x20;         │           │           │

&#x20;         └───────────┼───────────┘

&#x20;                     ▼

&#x20;             Observability

&#x20;                Platform

```



\---



\# 40. Logging



Logs should be structured.



Example conceptual log:



```json

{

&#x20; "timestamp": "...",

&#x20; "level": "INFO",

&#x20; "service": "customerpulse-api",

&#x20; "request\_id": "abc123",

&#x20; "operation": "generate\_recommendation",

&#x20; "customer\_id": "...",

&#x20; "duration\_ms": 42

}

```



Sensitive information should not be logged.



\---



\# 41. Metrics



Technical metrics:



```text

HTTP requests

HTTP errors

Latency

Database latency

Kafka lag

Worker throughput

Queue depth

Cache hit ratio

```



Business metrics:



```text

Customers processed

Scores calculated

Recommendations generated

Recommendations executed

Conversion rate

Customer retention

```



\---



\# 42. Security Architecture



The future production architecture is:



```text

User

&#x20;↓

Identity Provider

&#x20;↓

Next.js

&#x20;↓

FastAPI

&#x20;↓

Authentication / Authorization

&#x20;↓

Application

&#x20;↓

Data

```



Potential future components:



\* OAuth2 / OpenID Connect

\* JWT

\* Role-based authorization

\* API scopes

\* Audit logging

\* Secret management



The MVP may postpone authentication but should preserve a clean security boundary.



\---



\# 43. Data Protection



Because the domain is financial, the architecture should assume data is sensitive.



Principles:



\* Minimize stored PII

\* Never use real customer data

\* Avoid sensitive logs

\* Protect secrets

\* Encrypt communication

\* Restrict access

\* Define retention policies

\* Maintain auditability



\---



\# 44. Docker Architecture



Development will use Docker Compose.



Initial:



```text

┌────────────────────┐

│      Next.js       │

└────────────────────┘



┌────────────────────┐

│      FastAPI       │

└────────────────────┘



┌────────────────────┐

│    PostgreSQL      │

└────────────────────┘

```



Later:



```text

Next.js

FastAPI

PostgreSQL

MongoDB

Redis

Kafka

Workers

```



Docker images should use:



\* Multi-stage builds

\* Minimal runtime dependencies

\* Non-root users where practical

\* Reproducible builds

\* Health checks

\* Environment-based configuration



\---



\# 45. Configuration Architecture



Configuration must be externalized.



Conceptually:



```text

Environment

&#x20;    ↓

Configuration Layer

&#x20;    ↓

Application

```



Examples:



```text

DATABASE\_URL

REDIS\_URL

KAFKA\_BOOTSTRAP\_SERVERS

LOG\_LEVEL

ENVIRONMENT

```



Secrets must not be committed to Git.



\---



\# 46. CI/CD Architecture



The target pipeline is:



```text

Developer

&#x20;   │

&#x20;   ▼

&#x20;  Git

&#x20;   │

&#x20;   ▼

CI Pipeline

&#x20;   │

&#x20;   ├── Install

&#x20;   ├── Lint

&#x20;   ├── Type Check

&#x20;   ├── Unit Tests

&#x20;   ├── Integration Tests

&#x20;   ├── Security Checks

&#x20;   ├── Sonar Analysis

&#x20;   │

&#x20;   ▼

Docker Build

&#x20;   │

&#x20;   ▼

Container Registry

&#x20;   │

&#x20;   ▼

Deployment

```



The pipeline should eventually support separate environments:



```text

Development

&#x20;    ↓

Test

&#x20;    ↓

Staging

&#x20;    ↓

Production

```



\---



\# 47. Testing Architecture



Testing follows the architecture.



```text

&#x20;                Tests

&#x20;                  │

&#x20;       ┌──────────┼──────────┐

&#x20;       ▼          ▼          ▼

&#x20;      Unit       API     Integration

&#x20;       │          │          │

&#x20;       ▼          ▼          ▼

&#x20;     Domain     FastAPI   PostgreSQL

&#x20;                          MongoDB

&#x20;                          Redis

&#x20;                          Kafka

```



The majority of business rules should be covered by fast unit tests.



\---



\# 48. Unit Testing Strategy



Domain tests should require no external infrastructure.



Example:



```text

CustomerValueCalculatorTests

LifecyclePolicyTests

RecommendationPolicyTests

DecisionEngineTests

```



Example:



```text

Given:

&#x20;   churn\_probability = 0.82

&#x20;   customer\_value = €8,450



When:

&#x20;   decision engine evaluates customer



Then:

&#x20;   RETENTION\_OFFER is recommended

```



\---



\# 49. Integration Testing Strategy



Integration tests verify infrastructure behavior.



Examples:



```text

CustomerRepository

TransactionRepository

PostgreSQL migrations

MongoDB persistence

Redis caching

Kafka consumers

```



Test environments should be reproducible.



Docker containers may be used for integration testing.



\---



\# 50. Error Handling



The system should provide consistent error responses.



Conceptual format:



```json

{

&#x20; "error": {

&#x20;   "code": "CUSTOMER\_NOT\_FOUND",

&#x20;   "message": "Customer was not found.",

&#x20;   "request\_id": "abc123"

&#x20; }

}

```



Internal implementation details should not be exposed to clients.



\---



\# 51. Performance Architecture



Performance optimization should follow:



```text

Requirement

&#x20;   ↓

Measure

&#x20;   ↓

Profile

&#x20;   ↓

Identify Bottleneck

&#x20;   ↓

Optimize

&#x20;   ↓

Measure Again

```



Potential optimization areas:



```text

Database indexes

Query design

Connection pooling

Caching

Batching

Streaming

Async I/O

Worker concurrency

Kafka partitions

Read models

```



No optimization should be introduced without understanding the bottleneck.



\---



\# 52. Large Dataset Processing



The architecture assumes that transaction volumes may eventually become very large.



For example:



```text

10 million+

transactions

```



The application should avoid:



```text

Database

&#x20;   ↓

Load everything into RAM

&#x20;   ↓

Process

```



Instead:



```text

Database

&#x20;   ↓

Pagination / Cursor / Streaming

&#x20;   ↓

Batch

&#x20;   ↓

Process

&#x20;   ↓

Next Batch

```



For asynchronous large-scale workloads:



```text

Kafka

&#x20; ↓

Worker Pool

&#x20; ↓

Batch Processing

&#x20; ↓

Database

```



\---



\# 53. Scalability



The API layer should be horizontally scalable.



Conceptually:



```text

&#x20;                 Load Balancer

&#x20;                      │

&#x20;         ┌────────────┼────────────┐

&#x20;         ▼            ▼            ▼

&#x20;     FastAPI-1    FastAPI-2    FastAPI-3

&#x20;         │            │            │

&#x20;         └────────────┼────────────┘

&#x20;                      ▼

&#x20;                 PostgreSQL

```



The application should avoid local in-memory state that is required for correctness.



Shared state should be externalized when horizontal scaling requires it.



\---



\# 54. Deployment Architecture



The eventual production architecture may look like:



```text

&#x20;                   Internet

&#x20;                      │

&#x20;                      ▼

&#x20;               Load Balancer

&#x20;                      │

&#x20;            ┌─────────┴─────────┐

&#x20;            ▼                   ▼

&#x20;         Next.js             FastAPI

&#x20;                               │

&#x20;                ┌──────────────┼──────────────┐

&#x20;                ▼              ▼              ▼

&#x20;            PostgreSQL       Redis          Kafka

&#x20;                                               │

&#x20;                                   ┌───────────┼───────────┐

&#x20;                                   ▼           ▼           ▼

&#x20;                                Scoring    Lifecycle   Analytics

&#x20;                                Workers     Workers     Workers

```



Kubernetes may eventually be introduced, but it is not required for the first stages.



\---



\# 55. Architecture Evolution



CustomerPulse evolves through controlled stages.



\## Stage 1 — Simple Backend



```text

Next.js

&#x20;  ↓

FastAPI

&#x20;  ↓

PostgreSQL

```



\## Stage 2 — Modular Monolith



```text

FastAPI

├── Customers

├── Transactions

├── Lifecycle

├── Value

└── Recommendations

```



\## Stage 3 — Decisioning



```text

Customer Data

&#x20;    ↓

Scores

&#x20;    ↓

CLM / CVM

&#x20;    ↓

Decision Engine

&#x20;    ↓

NBA

```



\## Stage 4 — Performance Infrastructure



```text

FastAPI

&#x20;├── PostgreSQL

&#x20;└── Redis

```



\## Stage 5 — Document / Read Models



```text

PostgreSQL

&#x20;    │

&#x20;    ▼

Domain Events

&#x20;    │

&#x20;    ▼

MongoDB Read Model

```



\## Stage 6 — Event-Driven



```text

FastAPI

&#x20;  ↓

Kafka

&#x20;  ↓

Workers

```



\## Stage 7 — AI/ML



```text

Data

&#x20;↓

Features

&#x20;↓

ML Models

&#x20;↓

Predictions

&#x20;↓

Decision Engine

&#x20;↓

NBA

```



\## Stage 8 — Selective Service Extraction



Only if justified:



```text

Customer Service

Transaction Processing

Scoring Service

Recommendation Service

Analytics Service

```



\---



\# 56. Architecture Decision Records



Major architectural decisions should be documented separately under:



```text

docs/ADR/

```



Initial ADRs:



```text

ADR-001 — Modular Monolith First

ADR-002 — FastAPI as Backend Framework

ADR-003 — Next.js as Frontend Framework

ADR-004 — PostgreSQL as Initial Primary Database

ADR-005 — Separate API Schemas from Database Models

ADR-006 — Domain Logic Independent of Infrastructure

ADR-007 — Event-Driven Architecture as Evolution

ADR-008 — Prediction and Decision Separation

```



Each ADR should document:



```text

Context

Decision

Alternatives

Consequences

```



\---



\# 57. Key Architectural Decisions



\## Decision 1 — Modular Monolith First



\*\*Decision:\*\* Start with a modular monolith.



\*\*Reason:\*\* Establish boundaries before introducing distributed-system complexity.



\---



\## Decision 2 — FastAPI



\*\*Decision:\*\* Use FastAPI as the primary business API.



\*\*Reason:\*\* Strong Python typing, API development, validation, asynchronous support, and automatic OpenAPI documentation.



\---



\## Decision 3 — Next.js



\*\*Decision:\*\* Use Next.js for the frontend.



\*\*Reason:\*\* React/TypeScript frontend capabilities, routing, server-side capabilities, and production-oriented application structure.



\---



\## Decision 4 — PostgreSQL First



\*\*Decision:\*\* PostgreSQL is the initial system of record.



\*\*Reason:\*\* Customer, transaction, value, scoring, and recommendation data have strong relational characteristics.



\---



\## Decision 5 — MongoDB Only When Justified



\*\*Decision:\*\* Do not introduce MongoDB until a document-oriented requirement exists.



\*\*Reason:\*\* Avoid polyglot persistence without a business or architectural benefit.



\---



\## Decision 6 — Redis Only When Needed



\*\*Decision:\*\* Introduce Redis when caching or shared low-latency state becomes valuable.



\*\*Reason:\*\* Caching should solve a measured performance or scalability problem.



\---



\## Decision 7 — Kafka Later



\*\*Decision:\*\* Introduce Kafka when asynchronous/event-driven requirements emerge.



\*\*Reason:\*\* Messaging introduces operational and consistency complexity that is unnecessary for the first iteration.



\---



\## Decision 8 — Prediction ≠ Decision



\*\*Decision:\*\* ML predictions remain separate from business decisioning.



\*\*Reason:\*\* Models predict; business policies decide.



\---



\# 58. Architectural Quality Attributes



The architecture prioritizes:



| Attribute       |    Priority | Strategy                       |

| --------------- | ----------: | ------------------------------ |

| Maintainability |        High | Modular architecture           |

| Testability     |        High | Domain isolation               |

| Scalability     |        High | Stateless APIs                 |

| Performance     |        High | Efficient data access          |

| Reliability     |        High | Idempotency, retries           |

| Observability   |        High | Logs, metrics, traces          |

| Security        |        High | Security boundary              |

| Flexibility     |        High | Dependency inversion           |

| Simplicity      |        High | Modular monolith first         |

| AI readiness    | Medium/High | Prediction/decision separation |



\---



\# 59. Architecture Principles



CustomerPulse follows these principles:



\### Principle 1 — Business First



Architecture exists to solve business problems.



\### Principle 2 — Simple Before Distributed



Do not introduce distributed complexity without a reason.



\### Principle 3 — Explicit Boundaries



Modules should have clear responsibilities.



\### Principle 4 — Dependency Inversion



Business logic should not depend on infrastructure.



\### Principle 5 — Measure Before Optimizing



Performance decisions should be evidence-driven.



\### Principle 6 — Async Where Appropriate



Use asynchronous programming for I/O and move CPU-heavy work to appropriate processing mechanisms.



\### Principle 7 — Predict Separately From Decide



Machine learning should provide predictions; business logic determines actions.



\### Principle 8 — Design for Failure



Distributed systems must assume retries, duplicates, timeouts, and partial failures.



\### Principle 9 — Observable by Design



A system that cannot explain what happened cannot be reliably operated.



\### Principle 10 — Evolve, Don't Over-Engineer



Architecture should evolve in response to real requirements.



\---



\# 60. Final Architecture



The target conceptual architecture is:



```text

&#x20;                        ┌───────────────────┐

&#x20;                        │     Browser       │

&#x20;                        └─────────┬─────────┘

&#x20;                                  │

&#x20;                                  ▼

&#x20;                        ┌───────────────────┐

&#x20;                        │     Next.js       │

&#x20;                        │ React + TypeScript│

&#x20;                        └─────────┬─────────┘

&#x20;                                  │

&#x20;                             REST / JSON

&#x20;                                  │

&#x20;                                  ▼

┌─────────────────────────────────────────────────────────────┐

│                         FastAPI                             │

│                                                             │

│  ┌─────────┐     ┌─────────────┐     ┌─────────────────┐  │

│  │   API   │ ──► │ Application │ ──► │     Domain      │  │

│  └─────────┘     └─────────────┘     │                 │  │

│                                      │ Customers       │  │

│                                      │ Transactions    │  │

│                                      │ Lifecycle       │  │

│                                      │ Value           │  │

│                                      │ Recommendations │  │

│                                      └────────┬────────┘  │

│                                               │           │

│                                      ┌────────▼────────┐  │

│                                      │ Infrastructure  │  │

│                                      └────────┬────────┘  │

└──────────────────────────────────────────────┼────────────┘

&#x20;                                              │

&#x20;                    ┌─────────────────────────┼─────────────────────┐

&#x20;                    │                         │                     │

&#x20;                    ▼                         ▼                     ▼

&#x20;             ┌────────────┐            ┌───────────┐        ┌──────────┐

&#x20;             │ PostgreSQL │            │   Redis   │        │ MongoDB  │

&#x20;             └────────────┘            └───────────┘        └──────────┘

&#x20;                    │

&#x20;                    │

&#x20;                    ▼

&#x20;             ┌────────────┐

&#x20;             │   Kafka    │

&#x20;             └─────┬──────┘

&#x20;                   │

&#x20;       ┌───────────┼──────────────┐

&#x20;       ▼           ▼              ▼

&#x20;  ┌─────────┐ ┌───────────┐ ┌───────────┐

&#x20;  │ Scoring │ │ Lifecycle │ │ Analytics │

&#x20;  │ Workers │ │  Workers  │ │  Workers  │

&#x20;  └────┬────┘ └─────┬─────┘ └───────────┘

&#x20;       │             │

&#x20;       └──────┬──────┘

&#x20;              ▼

&#x20;      ┌─────────────────┐

&#x20;      │ Decision Engine │

&#x20;      └────────┬────────┘

&#x20;               ▼

&#x20;      ┌─────────────────┐

&#x20;      │ Next Best Action│

&#x20;      └─────────────────┘

```



\---



\# 61. Final Architectural Objective



CustomerPulse should demonstrate the evolution from a simple backend application into a modern intelligent platform:



```text

&#x20;                DATA

&#x20;                 │

&#x20;                 ▼

&#x20;           CUSTOMER 360

&#x20;                 │

&#x20;                 ▼

&#x20;            ANALYTICS

&#x20;                 │

&#x20;                 ▼

&#x20;            PREDICTION

&#x20;                 │

&#x20;                 ▼

&#x20;         DECISION ENGINE

&#x20;                 │

&#x20;                 ▼

&#x20;         NEXT BEST ACTION

&#x20;                 │

&#x20;                 ▼

&#x20;             ACTION

&#x20;                 │

&#x20;                 ▼

&#x20;            MEASUREMENT

&#x20;                 │

&#x20;                 ▼

&#x20;             FEEDBACK

&#x20;                 │

&#x20;                 └──────────────► DATA

```



The architecture is therefore not simply:



> \*\*"FastAPI + PostgreSQL + Next.js."\*\*



It is designed to demonstrate how a system can progressively evolve from:



> \*\*a clean modular backend\*\*



into:



> \*\*a scalable, event-driven, AI-assisted customer decisioning platform\*\*



without prematurely introducing complexity.



\---



\# 62. Architectural Guiding Principle



The most important rule for the project is:



> \*\*Do not build the final architecture on day one. Build the architecture that today's requirements justify, while keeping tomorrow's evolution possible.\*\*



This principle will guide every major architectural decision in CustomerPulse.



