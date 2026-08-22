# EduConnect Data Flow Description

## 1. Overview

The EduConnect peer-group formation system uses a full-stack architecture consisting of React, FastAPI, PostgreSQL, Redis, Kafka, and WebSocket communication.

The architecture is designed to support scalable peer-group formation for students working on collaborative academic projects.

---

# 2. Core Data Entities

## Student

Stores student profile information.

Attributes:

- Student ID
- Name
- Email
- Skills

---

## Project

Stores information about collaborative projects.

Attributes:

- Project ID
- Title
- Description
- Required Skills

---

## Group

Represents a peer group created for a project.

Attributes:

- Group ID
- Project ID
- Group Name
- Status

---

## Group Member

Maintains the relationship between students and groups.

Attributes:

- Membership ID
- Group ID
- Student ID

---

## Group Request

Represents a student's request to join a project group.

Attributes:

- Request ID
- Student ID
- Project ID
- Status

---

# 3. Frontend Layer

The React frontend provides the student-facing interface.

Students can:

1. View available projects.
2. View project requirements.
3. Submit a peer-group formation request.
4. View group status.

The frontend communicates with FastAPI using HTTP REST APIs.

---

# 4. FastAPI Backend

FastAPI acts as the main application and API layer.

It performs:

- Request validation
- Business logic
- Database operations
- Cache access
- Event publishing
- API response generation

The main API endpoints are documented in:

`api/endpoints.md`

---

# 5. PostgreSQL Database

PostgreSQL is the primary persistent storage layer.

It stores:

- Students
- Projects
- Groups
- Group members
- Group requests

The database schema is available in:

`backend/schema.sql`

---

# 6. Redis Cache

Redis is used as a high-speed caching layer.

For frequently accessed project information:

```text
React
  ↓
FastAPI
  ↓
Redis
  ↓
Cache Hit → Return Data
