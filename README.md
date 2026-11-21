# Relay

**Capture. Inspect. Monitor.**

Relay is an open-source, real-time webhook inspection platform for developers.

It provides temporary webhook endpoints that allow developers to capture, inspect, and monitor incoming HTTP requests in real time.

Whether you're integrating Stripe, GitHub, Discord, or building your own webhook-based services, Relay gives you a centralized place to understand exactly what your applications receive.

## Features

### Core capabilities

- **Temporary Webhook Endpoints** — Create dedicated endpoints to receive incoming webhooks.
- **Request Inspection** — Inspect HTTP methods, headers, query parameters, payloads, content types, and metadata.
- **Real-time Updates** — Receive incoming webhook events through WebSockets.
- **Request History** — Persist and retrieve previously captured requests.
- **Request Management** — Browse, retrieve, and delete captured requests.
- **Multi-instance Event Delivery** — Distribute real-time events across multiple backend instances using Redis Pub/Sub.

## Architecture

Relay follows a modular backend architecture designed to support independent components and horizontal scaling.

### Technology Stack

| Component               | Technology      |
| ----------------------- | --------------- |
| Backend                 | Python, FastAPI |
| Database                | PostgreSQL      |
| ORM                     | SQLAlchemy      |
| Migrations              | Alembic         |
| Real-time communication | WebSockets      |
| Event distribution      | Redis Pub/Sub   |
| Infrastructure          | Docker Compose  |
| Testing                 | pytest, HTTPX   |

**Planned frontend:** React, TypeScript, Vite, and Tailwind CSS.

## Project Structure

```text
relay/
├── backend/
│   └── src/relay/
│       ├── api/
│       ├── core/
│       ├── db/
│       ├── models/
│       ├── realtime/
│       ├── schemas/
│       └── services/
├── frontend/
├── infra/
├── docs/
└── README.md
```

## Development Status

Relay is currently under active development.

The backend foundation includes:

- Webhook endpoint management.
- HTTP request capture and PostgreSQL persistence.
- Request retrieval and management.
- WebSocket-based real-time updates.
- Redis Pub/Sub integration.
- Multi-instance real-time event delivery.

### Roadmap

- [ ] User registration and authentication.
- [ ] Endpoint ownership and authorization.
- [ ] Request search, filtering, and pagination.
- [ ] Centralized exception handling and structured logging.
- [ ] Security hardening and rate limiting.
- [ ] Request retention and cleanup.
- [ ] Comprehensive backend testing.
- [ ] Frontend dashboard and request inspector.

## Local Development

### Prerequisites

- Python
- uv
- Docker and Docker Compose
- Git

### Setup

Clone the repository:

```bash
git clone https://github.com/Nilotpal04/relay.git
cd relay
```

Configure your environment variables using the provided environment template.

Start the infrastructure:

```bash
docker compose --env-file .env -f infra/compose.yaml up -d
```

Install backend dependencies:

```bash
cd backend
uv sync
```

Run database migrations:

```bash
uv run alembic upgrade head
```

Start the development server:

```bash
uv run uvicorn relay.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Security

Security is an important part of Relay's development.

- Never commit credentials, API keys, passwords, or production environment files.
- Keep environment variables and secrets outside version control.
- Report security vulnerabilities responsibly.

## Contributing

Relay is being developed as an open-source project.

Contributions, suggestions, bug reports, and discussions are welcome.

## License

License information will be added before the first public release.
