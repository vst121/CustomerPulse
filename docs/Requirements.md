\# CustomerPulse — Requirements



\*\*Project:\*\* CustomerPulse

\*\*Version:\*\* 1.0

\*\*Status:\*\* Draft / Development Baseline

\*\*Document:\*\* Requirements Specification

\*\*Primary Domain:\*\* Customer Lifecycle Management (CLM) \& Customer Value Management (CVM)



\---



\## 1. Purpose



CustomerPulse is a learning-oriented but production-inspired platform for \*\*Customer Lifecycle Management (CLM)\*\* and \*\*Customer Value Management (CVM)\*\*.



The system models how a modern financial institution can transform customer data into actionable decisions:



```text

Customer Data

&#x20;     ↓

Customer 360

&#x20;     ↓

Analytics \& Features

&#x20;     ↓

Predictions

&#x20;     ↓

Decision Engine

&#x20;     ↓

Next Best Action

&#x20;     ↓

Personalized Customer Interaction

&#x20;     ↓

Measurement \& Feedback

```



The project is intentionally designed to demonstrate modern backend engineering, data processing, distributed systems, AI/ML integration, and software architecture.



The system should evolve incrementally rather than starting with unnecessary complexity.



\---



\# 2. Business Problem



A financial institution may have large amounts of customer data distributed across:



\* Core banking systems

\* CRM systems

\* Card systems

\* Transaction databases

\* Data warehouses

\* Marketing platforms

\* Customer interaction systems

\* External data sources



Raw data alone does not answer the most important business question:



> \*\*"What should we do with this customer next?"\*\*



CustomerPulse aims to answer this question by combining:



\* Customer information

\* Transaction behavior

\* Customer lifecycle state

\* Customer value

\* Predictive scores

\* Business rules

\* Recommendation logic

\* Personalized actions



For example:



```text

Customer:

Anna Müller



Current products:

\- Current Account

\- Credit Card



Behavior:

\- €1,850 monthly card spending

\- Increasing transaction frequency

\- Reduced recent engagement



Predictions:

\- Churn probability: 72%

\- Premium-card propensity: 81%

\- Customer lifetime value: €8,450



Decision:

High-value customer with elevated churn risk



Next Best Action:

Offer premium-card retention package



Confidence:

84%

```



\---



\# 3. Project Goals



The project has two goals.



\## 3.1 Business Goal



Demonstrate a simplified CLM/CVM platform capable of:



1\. Creating and managing customers.

2\. Recording customer transactions.

3\. Building a customer 360 view.

4\. Determining customer lifecycle stages.

5\. Calculating customer value.

6\. Calculating customer scores.

7\. Generating Next Best Actions.

8\. Explaining why an action was recommended.

9\. Tracking recommendations and outcomes.



\## 3.2 Engineering Goal



Use the project to demonstrate modern engineering practices including:



\* Python

\* FastAPI

\* Type hints

\* Pydantic

\* Async programming

\* SQL

\* NoSQL

\* REST APIs

\* Clean architecture

\* Domain-driven design concepts

\* Docker

\* CI/CD

\* Testing

\* PostgreSQL

\* MongoDB

\* Redis

\* Kafka

\* Event-driven architecture

\* Background processing

\* Observability

\* AI/ML integration

\* Performance optimization



Complexity should be introduced only when there is a demonstrated reason for it.



\---



\# 4. Non-Goals



The first version is \*\*not\*\* intended to be:



\* A real banking system

\* A real payment-processing system

\* A production financial product

\* A complete CRM

\* A real customer communication platform

\* A production fraud-detection system

\* A production-grade ML platform

\* A replacement for a core banking system

\* A fully distributed microservice architecture from day one



The project will use synthetic data.



No real customer PII or financial information should be used.



\---



\# 5. Target Users



\## 5.1 Relationship Manager



A bank employee who needs to understand:



\* Who is the customer?

\* What products do they use?

\* How valuable are they?

\* Are they likely to leave?

\* What should I offer them?



\## 5.2 Marketing / CRM User



A user who needs to:



\* Identify customer segments.

\* Find high-value customers.

\* Identify churn risks.

\* Generate customer recommendations.

\* Understand campaign opportunities.

\* Measure campaign results.



\---



\# 6. Core Domain Concepts



CustomerPulse contains five primary business concepts.



\## 6.1 Customer



Represents a bank customer.



Initial attributes:



```text

Customer

\---------

id

first\_name

last\_name

email

lifecycle\_stage

segment

created\_at

```



Future attributes may include:



\* Date of birth

\* Customer since

\* Location

\* Preferred channel

\* Risk profile

\* Consent information

\* Products

\* Communication preferences



Sensitive attributes should not be introduced unless there is a clear architectural or business reason.



\---



\## 6.2 Transaction



Represents a financial transaction associated with a customer.



Initial attributes:



```text

Transaction

\-----------

id

customer\_id

amount

currency

category

status

timestamp

```



Possible categories:



```text

GROCERY

TRAVEL

RESTAURANT

SHOPPING

RENT

UTILITIES

ENTERTAINMENT

OTHER

```



Possible statuses:



```text

PENDING

COMPLETED

FAILED

REVERSED

```



Transactions will initially be stored in PostgreSQL.



\---



\## 6.3 Customer Value



Represents the economic value associated with a customer.



Initial attributes:



```text

CustomerValue

\-------------

customer\_id

current\_value

lifetime\_value

predicted\_future\_value

calculated\_at

```



The implementation should eventually distinguish between:



\* Historical value

\* Current value

\* Predicted future value

\* Customer Lifetime Value (CLV)

\* Cost to serve

\* Product profitability



The first implementation may use a simplified model.



Example:



```text

Historical value:

€5,200



Predicted future value:

€3,250



Customer Lifetime Value:

€8,450

```



\---



\# 7. Customer Lifecycle Management (CLM)



CustomerPulse shall model the customer lifecycle.



Initial lifecycle stages:



```text

ACQUISITION

&#x20;   ↓

ONBOARDING

&#x20;   ↓

ACTIVATION

&#x20;   ↓

ENGAGEMENT

&#x20;   ↓

GROWTH

&#x20;   ↓

RETENTION

&#x20;   ↓

WIN\_BACK

```



A customer may transition between lifecycle stages based on:



\* Customer age

\* Product ownership

\* Transaction behavior

\* Engagement

\* Churn probability

\* Business rules

\* Recommendations

\* Campaign interactions



The lifecycle engine should eventually make lifecycle transitions explainable.



Example:



```text

Previous:

ENGAGEMENT



New:

RETENTION



Reason:

Churn probability exceeded 70%.

```



\---



\# 8. Customer Value Management (CVM)



CustomerPulse shall calculate and manage customer economic value.



The initial implementation may use a simplified model:



```text

CLV ≈ Expected Monthly Margin × Expected Customer Lifetime

```



This is intentionally simplified.



Future versions may incorporate:



```text

Historical Revenue

&#x20;       +

Expected Future Revenue

&#x20;       -

Cost to Serve

&#x20;       -

Expected Loss

&#x20;       =

Customer Value

```



The system should allow the value-calculation strategy to evolve without requiring changes to the API layer.



\---



\# 9. Customer Scoring



CustomerPulse shall support predictive and behavioral scores.



Initial scores:



```text

Churn Probability

Engagement Score

Purchase Propensity

```



Example:



```text

Customer:

Anna Müller



Churn Probability:

0.72



Engagement:

0.61



Premium Card Propensity:

0.81

```



Scores must contain:



\* Customer identifier

\* Score

\* Calculation timestamp



Future versions may contain:



\* Model version

\* Feature version

\* Prediction explanation

\* Confidence

\* Data freshness

\* Model metadata



\---



\# 10. Prediction vs Decision



A fundamental architectural requirement is to keep \*\*prediction\*\* separate from \*\*decision\*\*.



Prediction answers:



> "What is likely to happen?"



Example:



```text

Churn probability = 0.82

```



Decision answers:



> "What should the business do?"



Example:



```text

Decision = RETENTION\_CAMPAIGN

```



Therefore:



```text

Customer Data

&#x20;    ↓

Feature Calculation

&#x20;    ↓

Prediction

&#x20;    ↓

Decision Engine

&#x20;    ↓

Next Best Action

```



The prediction model must not directly determine the final business action.



This separation will allow different decision strategies to use the same predictive models.



\---



\# 11. Next Best Action (NBA)



CustomerPulse shall generate recommendations for customers.



Examples:



```text

RETENTION\_OFFER

PREMIUM\_CARD\_OFFER

SAVINGS\_ACCOUNT\_OFFER

INVESTMENT\_OFFER

PERSONAL\_LOAN\_OFFER

RE\_ENGAGEMENT\_CAMPAIGN

NO\_ACTION

```



Each recommendation should contain:



```text

Recommendation

\--------------

id

customer\_id

action

product

reason

confidence\_score

status

created\_at

```



Possible statuses:



```text

GENERATED

APPROVED

EXECUTED

REJECTED

EXPIRED

```



\---



\# 12. Recommendation Explainability



Every recommendation should have a human-readable explanation.



Example:



```text

Recommendation:

Premium Card Retention Offer



Reason:

Customer has high card usage, high customer value,

and increasing churn probability.



Confidence:

84%

```



The system should avoid generating unexplained recommendations.



Future versions may provide structured explanations:



```json

{

&#x20; "factors": \[

&#x20;   {

&#x20;     "feature": "monthly\_card\_spend",

&#x20;     "impact": "positive"

&#x20;   },

&#x20;   {

&#x20;     "feature": "churn\_probability",

&#x20;     "impact": "high"

&#x20;   }

&#x20; ]

}

```



\---



\# 13. Customer 360



The system shall provide a consolidated customer view.



A Customer 360 response should eventually combine:



```text

Customer

&#x20;  +

Products

&#x20;  +

Transactions

&#x20;  +

Lifecycle

&#x20;  +

Customer Value

&#x20;  +

Scores

&#x20;  +

Recommendations

```



Example conceptual response:



```text

Customer

&#x20;├── Profile

&#x20;├── Lifecycle

&#x20;├── Products

&#x20;├── Recent Transactions

&#x20;├── Customer Value

&#x20;├── Scores

&#x20;└── Recommendations

```



Customer 360 is primarily a \*\*read-oriented business concept\*\*.



It does not require all information to be stored in one physical database table.



\---



\# 14. API Requirements



FastAPI shall expose the primary business API.



All APIs shall use versioning.



Initial API prefix:



```text

/api/v1

```



\## 14.1 Health



```http

GET /api/v1/health

```



Returns service health information.



\---



\## 14.2 Customers



```http

GET /api/v1/customers

GET /api/v1/customers/{customer\_id}

POST /api/v1/customers

```



Future operations:



```http

PUT /api/v1/customers/{customer\_id}

DELETE /api/v1/customers/{customer\_id}

```



The list endpoint should eventually support:



\* Pagination

\* Filtering

\* Searching

\* Sorting



\---



\## 14.3 Transactions



```http

GET /api/v1/customers/{customer\_id}/transactions

POST /api/v1/customers/{customer\_id}/transactions

```



The API should support pagination for large transaction sets.



\---



\## 14.4 Scores



```http

GET /api/v1/customers/{customer\_id}/scores

```



Future:



```http

POST /api/v1/customers/{customer\_id}/scores/calculate

```



\---



\## 14.5 Customer Value



```http

GET /api/v1/customers/{customer\_id}/value

```



Future:



```http

POST /api/v1/customers/{customer\_id}/value/calculate

```



\---



\## 14.6 Recommendations



```http

GET /api/v1/customers/{customer\_id}/recommendations

POST /api/v1/customers/{customer\_id}/recommendations/generate

```



Future:



```http

POST /api/v1/recommendations/{recommendation\_id}/execute

```



\---



\# 15. Data Architecture Requirements



\## 15.1 PostgreSQL



PostgreSQL shall be the initial primary database.



It will contain structured transactional data such as:



\* Customers

\* Transactions

\* Lifecycle state

\* Customer values

\* Scores

\* Recommendations



The project should use:



\* SQLAlchemy 2.x

\* Alembic

\* Explicit database migrations

\* Connection pooling



\---



\# 16. MongoDB



MongoDB shall \*\*not\*\* be introduced merely because the project uses both SQL and NoSQL.



It will be introduced when the system has a clear use case.



Potential use cases:



\* Flexible customer interaction documents

\* Customer 360 read models

\* Event/document history

\* Model outputs with evolving schemas

\* Analytics-oriented documents



The architecture should demonstrate the ability to choose the correct persistence technology based on data characteristics rather than technology preference.



\---



\# 17. Redis



Redis will be introduced later.



Potential use cases:



\* Customer 360 caching

\* Recommendation caching

\* Frequently accessed reference data

\* Distributed locks where justified

\* Rate limiting

\* Short-lived processing state



Caching must explicitly consider:



\* TTL

\* Invalidation

\* Stale data

\* Cache stampede

\* Consistency



\---



\# 18. Event-Driven Architecture



The initial application will be a \*\*modular monolith\*\*.



Event-driven architecture will be introduced incrementally.



Potential events:



```text

CustomerCreated

TransactionRecorded

CustomerScoreUpdated

CustomerValueCalculated

LifecycleStageChanged

RecommendationGenerated

RecommendationExecuted

CampaignExecuted

```



Potential future flow:



```text

Transaction API

&#x20;     ↓

PostgreSQL

&#x20;     ↓

TransactionRecorded

&#x20;     ↓

Kafka

&#x20;     ↓

&#x20;┌───────────────┬────────────────┬─────────────────┐

&#x20;↓               ↓                ↓

Scoring       Lifecycle       Analytics

Service       Engine          Pipeline

&#x20;↓               ↓                ↓

&#x20;└───────────────┴────────────────┘

&#x20;                ↓

&#x20;         Recommendation

```



The event-driven implementation must address:



\* At-least-once delivery

\* Idempotency

\* Retries

\* Dead-letter queues

\* Correlation IDs

\* Event ordering where required

\* Observability



\---



\# 19. Performance Requirements



CustomerPulse should be designed with the assumption that the underlying business may eventually contain:



```text

Millions of customers

Hundreds of millions of transactions

Large numbers of concurrent API requests

Large scoring workloads

```



The system should therefore use:



\* Pagination

\* Efficient SQL queries

\* Database indexes

\* Connection pooling

\* Async I/O where appropriate

\* Streaming for large datasets

\* Batch processing

\* Background processing

\* Caching where justified



Performance optimization should be evidence-driven.



The project should follow:



```text

Measure

&#x20;  ↓

Identify Bottleneck

&#x20;  ↓

Optimize

&#x20;  ↓

Measure Again

```



\---



\# 20. Asynchronous Processing



The application should distinguish between:



\### I/O-bound work



Examples:



\* Database calls

\* HTTP requests

\* Message broker operations

\* File/network operations



These may use asynchronous APIs.



\### CPU-bound work



Examples:



\* Large-scale scoring

\* ML inference

\* Complex data transformations



These should not simply be placed inside an async web request.



Potential approaches include:



\* Background workers

\* Process pools

\* Dedicated scoring services

\* Batch jobs

\* Kafka consumers



\---



\# 21. Background Processing



Long-running operations should not block HTTP requests.



Potential background operations:



```text

Calculate customer scores

Calculate customer value

Generate recommendations

Process transaction batches

Build Customer 360 projections

Run campaigns

```



The architecture should eventually support:



```text

API

&#x20;↓

Command/Event

&#x20;↓

Background Worker

&#x20;↓

Processing

&#x20;↓

Result

```



\---



\# 22. Reliability Requirements



The system shall provide:



\* Request validation

\* Structured error responses

\* Exception handling

\* Database transaction management

\* Retry mechanisms where appropriate

\* Idempotent processing where required

\* Health checks

\* Readiness checks

\* Graceful shutdown

\* Structured logging



Failures should be observable and diagnosable.



\---



\# 23. Idempotency



Operations that may be retried must be designed for idempotency.



For example:



```text

TransactionRecorded

```



may be delivered more than once.



Processing the same transaction event twice must not create duplicate business effects.



Potential mechanisms include:



\* Unique constraints

\* Idempotency keys

\* Processed-event tables

\* Deduplication

\* Consumer-side state



The final implementation should demonstrate at least one robust idempotency strategy.



\---



\# 24. Testing Requirements



The project shall include multiple testing levels.



\## 24.1 Unit Tests



Business logic should be testable without:



\* PostgreSQL

\* MongoDB

\* Kafka

\* Redis

\* HTTP



Examples:



```text

Lifecycle rules

CLV calculation

Recommendation rules

Decision engine

Score interpretation

```



\---



\## 24.2 API Tests



Test:



\* HTTP status codes

\* Request validation

\* Response schemas

\* Error handling

\* API behavior



\---



\## 24.3 Integration Tests



Test interactions with:



\* PostgreSQL

\* MongoDB

\* Redis

\* Kafka



These should be introduced as those technologies enter the project.



\---



\## 24.4 Event Tests



Future event-driven tests should verify:



\* Event publication

\* Event consumption

\* Idempotency

\* Retry behavior

\* Dead-letter behavior



\---



\# 25. Security Requirements



Security is initially simplified but the architecture must leave room for production security.



Future requirements include:



\* Authentication

\* Authorization

\* Role-based access control

\* Secure secret management

\* Encryption in transit

\* Encryption at rest

\* Audit logging

\* PII minimization

\* Data retention

\* Consent management



Sensitive information must not be written to application logs.



\---



\# 26. Frontend Requirements



The frontend will use:



\* Next.js

\* React

\* TypeScript



Next.js will be responsible primarily for:



\* UI

\* Routing

\* Presentation

\* Server-side rendering where useful

\* Frontend composition



FastAPI remains the primary business API.



The architecture should avoid duplicating business logic between Next.js and FastAPI.



\---



\# 27. Dashboard



The application should eventually provide a dashboard containing:



```text

CustomerPulse Dashboard

────────────────────────────────────



Customers             125,430



High Value Customers   12,420



High Churn Risk         8,240



Recommendations        34,210



Campaign Conversion       14.8%

```



Additional views:



\### Customer List



Search and filter customers.



\### Customer Profile



Display:



\* Customer information

\* Lifecycle stage

\* Products

\* Transaction summary

\* Customer value

\* Scores

\* Recommendations



\### Recommendation View



Display:



\* Recommended action

\* Reason

\* Confidence

\* Status

\* Creation time



\---



\# 28. CI/CD Requirements



The project shall eventually implement a complete CI/CD pipeline.



Target flow:



```text

Git Push

&#x20;  ↓

Build

&#x20;  ↓

Unit Tests

&#x20;  ↓

Integration Tests

&#x20;  ↓

Static Analysis

&#x20;  ↓

Security Checks

&#x20;  ↓

Docker Build

&#x20;  ↓

Container Registry

&#x20;  ↓

Deployment

```



Technologies may include:



\* Git

\* GitHub

\* Jenkins

\* SonarQube

\* Nexus

\* Docker



The exact CI/CD tooling may evolve.



\---



\# 29. Docker Requirements



All major runtime components should eventually be containerized.



Initial components:



```text

frontend

backend

postgresql

```



Later:



```text

mongodb

redis

kafka

workers

scoring services

```



Docker images should be:



\* Small

\* Reproducible

\* Secure

\* Efficiently cached

\* Suitable for production deployment



The project should demonstrate multi-stage Docker builds where appropriate.



\---



\# 30. Linux Requirements



The backend and containers should be designed to run in a Linux environment.



The project should demonstrate practical knowledge of:



\* Processes

\* Environment variables

\* File permissions

\* Networking

\* Container processes

\* Logs

\* Signals

\* Resource usage



\---



\# 31. Observability



The application shall eventually provide:



\### Logging



Structured JSON logs containing information such as:



```text

timestamp

level

service

request\_id

correlation\_id

operation

duration

result

```



Sensitive data must not be logged.



\### Metrics



Technical metrics:



```text

Request rate

Latency

Error rate

Database latency

Queue depth

Worker throughput

```



Business metrics:



```text

Churn rate

Customer lifetime value

Recommendation rate

Recommendation conversion

Campaign conversion

```



\### Tracing



Distributed tracing should eventually allow:



```text

HTTP Request

&#x20;   ↓

FastAPI

&#x20;   ↓

Database

&#x20;   ↓

Kafka

&#x20;   ↓

Worker

&#x20;   ↓

Recommendation Engine

```



to be followed through the system.



\---



\# 32. API Design Principles



APIs shall follow:



\* REST principles

\* Consistent resource naming

\* Versioning

\* HTTP semantics

\* Explicit request/response schemas

\* Pagination

\* Filtering

\* Validation

\* Structured errors



Database models must not automatically become public API contracts.



The system should use dedicated DTO/schema models.



\---



\# 33. Domain Independence



Business rules must remain independent of infrastructure technologies.



The domain layer should not depend directly on:



```text

FastAPI

SQLAlchemy

PostgreSQL

MongoDB

Redis

Kafka

Docker

```



This allows business logic to be tested and evolved independently.



\---



\# 34. Initial Project Structure



The expected structure is:



```text

CustomerPulse/

│

├── backend/

│   ├── app/

│   │   ├── main.py

│   │   │

│   │   ├── api/

│   │   │   └── v1/

│   │   │       ├── router.py

│   │   │       ├── health.py

│   │   │       ├── customers.py

│   │   │       ├── transactions.py

│   │   │       └── recommendations.py

│   │   │

│   │   ├── domain/

│   │   │   ├── customers/

│   │   │   ├── transactions/

│   │   │   ├── lifecycle/

│   │   │   ├── value/

│   │   │   └── recommendations/

│   │   │

│   │   ├── application/

│   │   │   ├── customers/

│   │   │   ├── scoring/

│   │   │   ├── value/

│   │   │   └── recommendations/

│   │   │

│   │   ├── infrastructure/

│   │   │   ├── database/

│   │   │   ├── mongodb/

│   │   │   ├── messaging/

│   │   │   └── cache/

│   │   │

│   │   └── config/

│   │

│   └── tests/

│       ├── unit/

│       ├── api/

│       └── integration/

│

├── frontend/

│

├── infrastructure/

│   └── docker-compose.yml

│

├── docs/

│   ├── Requirements.md

│   ├── Architecture.md

│   └── ADR/

│

└── README.md

```



The structure may evolve as implementation experience reveals better boundaries.



\---



\# 35. Development Phases



The project will be developed incrementally.



\## Phase 1 — Backend Foundation



Implement:



\* Python project

\* FastAPI

\* Configuration

\* Health endpoint

\* API versioning

\* Basic testing

\* Development tooling



\---



\## Phase 2 — Customer Domain



Implement:



\* Customer domain model

\* PostgreSQL

\* SQLAlchemy

\* Alembic

\* Customer APIs

\* Repository abstraction

\* Unit and integration tests



\---



\## Phase 3 — Transactions



Implement:



\* Transaction domain

\* Transaction APIs

\* Pagination

\* Database indexes

\* Efficient queries

\* Transaction validation



\---



\## Phase 4 — Customer 360



Implement:



\* Customer profile

\* Transaction summaries

\* Product information

\* Lifecycle state

\* Customer value

\* Customer scores



\---



\## Phase 5 — CLM



Implement:



\* Lifecycle stages

\* Lifecycle rules

\* Lifecycle transitions

\* Explainable lifecycle decisions



\---



\## Phase 6 — CVM



Implement:



\* Historical value

\* Customer Lifetime Value

\* Predicted future value

\* Value segmentation



\---



\## Phase 7 — Decision Engine / NBA



Implement:



```text

Prediction

&#x20;   ↓

Decision

&#x20;   ↓

Recommendation

```



with explainable business rules.



\---



\## Phase 8 — Redis / MongoDB



Introduce additional infrastructure only when justified by concrete requirements.



\---



\## Phase 9 — Event-Driven Processing



Introduce:



\* Kafka

\* Events

\* Consumers

\* Background workers

\* Idempotency

\* Retry

\* DLQ

\* Correlation IDs



\---



\## Phase 10 — AI/ML



Introduce:



\* ML models

\* Feature engineering

\* Model inference

\* Churn prediction

\* Propensity prediction

\* CLV prediction

\* Model versioning

\* Explainability



\---



\# 36. Future AI/ML Requirements



The final system should demonstrate a realistic separation between:



```text

Data

&#x20;↓

Feature Engineering

&#x20;↓

Model

&#x20;↓

Prediction

&#x20;↓

Decision Engine

&#x20;↓

Recommendation

```



Potential models:



```text

Churn Prediction

Purchase Propensity

Next Best Category

Customer Lifetime Value

Revenue Forecast

```



The ML layer should not directly own business policy.



For example:



```text

ML:

churn\_probability = 0.82



Decision Engine:

customer\_value > €5,000

AND churn\_probability > 0.70



Decision:

RETENTION\_REQUIRED

```



\---



\# 37. Business Metrics



The platform should eventually measure:



\### Customer Metrics



\* Customer count

\* Active customers

\* Churn rate

\* Customer lifetime value

\* Customer engagement



\### Recommendation Metrics



\* Recommendations generated

\* Recommendations accepted

\* Recommendations executed

\* Conversion rate

\* Revenue generated



\### Campaign Metrics



\* Reach

\* Conversion

\* Revenue

\* Retention

\* ROI



\---



\# 38. Technical Acceptance Criteria



The initial system is considered successful when it can:



\* Start locally with documented commands.

\* Expose a working FastAPI application.

\* Expose `/api/v1/health`.

\* Create customers.

\* Retrieve customers.

\* Search and paginate customers.

\* Record transactions.

\* Retrieve transactions.

\* Calculate customer value.

\* Determine lifecycle stage.

\* Calculate customer scores.

\* Generate recommendations.

\* Explain recommendations.

\* Expose the functionality through REST APIs.

\* Provide automated tests.

\* Run inside Docker.

\* Provide useful logs and health information.



\---



\# 39. Architecture Evolution Principle



CustomerPulse must not begin as an unnecessarily complex distributed system.



The initial architecture should be:



```text

Next.js

&#x20;  ↓

FastAPI

&#x20;  ↓

Modular Monolith

&#x20;  ↓

PostgreSQL

```



As real requirements appear:



```text

&#x20;                   ┌── Redis

&#x20;                   │

Next.js → FastAPI → PostgreSQL

&#x20;                   │

&#x20;                   ├── MongoDB

&#x20;                   │

&#x20;                   └── Kafka → Workers

&#x20;                                 ↓

&#x20;                             ML / Scoring

```



Later, individual modules may become services if there is a measurable reason.



Possible reasons include:



\* Independent scaling

\* Independent deployment

\* Different runtime requirements

\* Isolation of failure

\* Independent ownership

\* High processing volume



\---



\# 40. Interview Learning Objectives



CustomerPulse is also intended to demonstrate senior-level engineering decision making.



The project should allow discussion of questions such as:



\### Architecture



\* Why modular monolith first?

\* When should a service be extracted?

\* Where are the domain boundaries?

\* Why SQL first?

\* When does MongoDB make sense?



\### Backend



\* Why FastAPI?

\* When should an endpoint be async?

\* How should dependency injection work?

\* How should API contracts be separated from persistence models?



\### Data



\* How do we handle millions of transactions?

\* What indexes are required?

\* How do we paginate efficiently?

\* When should data be denormalized?



\### Distributed Systems



\* How do we guarantee idempotency?

\* What happens when Kafka delivers the same event twice?

\* How should retries work?

\* What belongs in a DLQ?

\* How do we handle ordering?



\### Performance



\* Where is the bottleneck?

\* When should caching be introduced?

\* How do we process large datasets?

\* When should work leave the HTTP request?



\### AI



\* What is the difference between prediction and decision?

\* How do we explain recommendations?

\* How do we monitor model performance?

\* How do we prevent an ML model from directly controlling business policy?



\### DevOps



\* How do we build an optimized Docker image?

\* How should CI/CD work?

\* How do we deploy safely?

\* How do we observe the system in production?



\---



\# 41. Guiding Engineering Principle



CustomerPulse follows one central principle:



> \*\*Business Need → Simple Solution → Measure → Identify Bottleneck → Architectural Change → Measure Again\*\*



The goal is not to demonstrate how many technologies can be placed into one application.



The goal is to demonstrate the ability to make \*\*good engineering decisions at the right time\*\*.



\---



\# 42. Definition of Done



A feature is considered complete when:



1\. The business requirement is clearly understood.

2\. The domain behavior is defined.

3\. The API contract is defined where applicable.

4\. The implementation is tested.

5\. Error cases are handled.

6\. Persistence behavior is tested where applicable.

7\. Logging/observability is considered.

8\. The implementation follows the established architecture.

9\. Documentation is updated when the design changes.

10\. The feature can be explained in an engineering interview.



\---



\# 43. Final Product Vision



The final CustomerPulse platform should demonstrate the complete journey:



```text

&#x20;                CUSTOMER DATA

&#x20;                      │

&#x20;                      ▼

&#x20;               CUSTOMER 360

&#x20;                      │

&#x20;                      ▼

&#x20;             FEATURE ENGINEERING

&#x20;                      │

&#x20;                      ▼

&#x20;                AI / PREDICTION

&#x20;                      │

&#x20;         ┌────────────┴────────────┐

&#x20;         ▼                         ▼

&#x20;    Churn Risk                Customer Value

&#x20;         │                         │

&#x20;         └────────────┬────────────┘

&#x20;                      ▼

&#x20;               DECISION ENGINE

&#x20;                      │

&#x20;                      ▼

&#x20;              NEXT BEST ACTION

&#x20;                      │

&#x20;                      ▼

&#x20;            PERSONALIZED ACTION

&#x20;                      │

&#x20;                      ▼

&#x20;               CUSTOMER RESULT

&#x20;                      │

&#x20;                      ▼

&#x20;                MEASUREMENT

&#x20;                      │

&#x20;                      └──────────────► Feedback

```



CustomerPulse should ultimately demonstrate how a modern financial institution can move from:



> \*\*"We have customer data."\*\*



to:



> \*\*"We understand the customer, predict what may happen, decide what should happen next, take action, and measure the result."\*\*



That is the core business and engineering objective of the project.



