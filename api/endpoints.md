# EduConnect Peer-Group Formation API

## API Overview

The EduConnect backend uses FastAPI to provide REST APIs for students, projects, peer groups, and group formation requests.

Base URL:

http://localhost:8000

---

## 1. Health Check

### GET /health

Checks whether the backend service is running.

### Response

```json
{
  "status": "healthy",
  "service": "peer-group-formation-api"
}
