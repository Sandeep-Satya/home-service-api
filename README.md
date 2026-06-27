# Home Services API

A REST API for connecting homeowners with local service professionals — plumbers, electricians, painters, AC technicians, and more. Built to solve a real gap in my hometown where no easy way existed to find and book trusted local workers.

Built and deployed end-to-end in under two weeks as both a learning project and a foundation for a real local startup.

**Live URL:** http://34.234.44.64/docs

---

## What It Does

- Homeowners can browse available services and book appointments
- Service providers are easy to discover and contact
- Bookings are tracked with status and timestamps
- Simple, fast API that can power a mobile or web frontend

---

## Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI (Python) |
| Database | PostgreSQL on AWS RDS |
| Containerization | Docker + Docker Compose |
| Web Server | Nginx (reverse proxy) |
| Cloud | AWS EC2, RDS, Secrets Manager, CloudWatch |
| CI/CD | GitHub Actions |
| Secret Management | AWS Secrets Manager |
| Logging | AWS CloudWatch |

---

## Architecture

```
Internet
    │
    ▼
Nginx (port 80)          ← EC2, public facing
    │
    ▼
FastAPI (port 8000)      ← Docker container, internal only
    │
    ▼
PostgreSQL               ← AWS RDS, private subnet
    │
AWS Secrets Manager      ← DB credentials, fetched at startup
AWS CloudWatch           ← Container logs, streamed in real time
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/services` | List all available services |
| GET | `/bookings` | List all bookings |
| GET | `/bookings/{id}` | Get a specific booking |
| POST | `/bookings` | Create a new booking |

### Example: Create a Booking

```bash
curl -X POST http://34.234.44.64/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Satya",
    "phone_number": "9999999999",
    "address": "123 Main Street",
    "service_id": 1,
    "preferred_time": "10am"
  }'
```

### Example Response

```json
{
  "id": 1,
  "customer_name": "Satya",
  "phone_number": "9999999999",
  "address": "123 Main Street",
  "service_id": 1,
  "preferred_time": "10am",
  "status": "pending",
  "created_at": "2026-06-27T10:00:00"
}
```

---

## Local Development Setup

### Prerequisites
- Python 3.12+
- Docker + Docker Compose
- PostgreSQL (or use the Docker Compose db service)

### Run Locally

```bash
# Clone the repo
git clone https://github.com/Sandeep-Satya/home-service-api.git
cd home-service-api

# Create .env file
echo "DATABASE_URL=postgresql://user:password@localhost:5432/home_services_db" > .env

# Start with Docker Compose
docker compose up -d --build

# API is now running at http://localhost:8000/docs
```

---

## Deployment

The app is deployed on AWS with a fully automated CI/CD pipeline.

### Infrastructure
- **EC2** — Ubuntu t3.micro instance with Docker installed
- **RDS** — Managed PostgreSQL 16, private subnet
- **Elastic IP** — Static public IP, survives instance restarts
- **Nginx** — Reverse proxy, port 80 → 8000
- **Secrets Manager** — DB credentials stored encrypted, fetched at startup via boto3
- **CloudWatch** — Container logs streamed in real time

### CI/CD Pipeline

Every push to `main` triggers an automatic deployment:

1. GitHub Actions runner spins up
2. Runner's IP is temporarily added to EC2 security group (SSH access)
3. SSH into EC2, `git pull`, `docker compose down`, `docker compose up --build`
4. SSH rule is revoked immediately after (self-revoking for security)

This means: `git push` → live in under 60 seconds, no manual SSH needed.

---

## Security Decisions

| Decision | Reason |
|---|---|
| Port 8000 closed externally | Only Nginx talks to the app, not the public internet |
| RDS in private subnet | Database not reachable from outside AWS |
| Secrets Manager for DB credentials | No plaintext passwords on the server |
| SSH restricted to deployer IP only | Temporary, self-revoking rule per deploy |
| IAM role on EC2 | No hardcoded AWS credentials anywhere |

---

## Real Problems Solved During Build

**1. Docker container couldn't connect to Postgres**
The API container used `localhost` to connect to the database, which inside Docker refers to the container itself, not the db container. Fixed by using the Docker Compose service name (`db`) as the hostname instead.

**2. Healthcheck race condition**
The API container started before Postgres was ready, causing startup failures. Fixed with a `depends_on` condition tied to the Postgres healthcheck (`pg_isready`), ensuring the database is fully ready before the API starts.

**3. RDS connection refused**
After migrating to RDS, the API couldn't reach the database. Root cause: the RDS security group only allowed connections from specific IPs, not from the EC2 security group. Fixed by adding an inbound rule on the RDS security group allowing port 5432 from the EC2 security group ID.

**4. GitHub Actions SSH timeout**
The CI/CD pipeline couldn't SSH into EC2 because port 22 was restricted to a static IP. Fixed by adding a deploy step that dynamically fetches the GitHub Actions runner IP, temporarily opens SSH, deploys, then immediately revokes the rule.

**5. git pull not updating files on server**
The server had local uncommitted changes to `docker-compose.yml` and `requirements.txt`, which blocked `git pull` silently. Fixed by running `git checkout -- .` before pulling to discard server-side manual edits and let the repo stay as the single source of truth.

---

## Project Structure

```
home-service-api/
├── main.py              # FastAPI app, routes, startup seed
├── models.py            # SQLAlchemy models (Service, Booking)
├── database.py          # DB connection, Secrets Manager integration
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build
├── docker-compose.yml   # Service orchestration
└── .github/
    └── workflows/
        └── deploy.yml   # CI/CD pipeline
```

---

## Author

**Sandeep Satya**
GitHub: [@Sandeep-Satya](https://github.com/Sandeep-Satya)

Built in Hyderabad, India. Inspired by the real need to connect local service workers with homeowners in smaller towns where no such platform exists.
