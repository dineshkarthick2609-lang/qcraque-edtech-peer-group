# Data Flow Design

## Overview

The Scalable Peer-Group Formation System uses React, FastAPI, PostgreSQL, Redis, Apache Kafka, and WebSocket to provide an efficient and real-time group formation process.

## Data Flow

1. Students interact with the React frontend.
2. React sends requests to the FastAPI backend.
3. FastAPI validates and processes the request.
4. Redis is checked for frequently accessed student and group data.
5. PostgreSQL stores persistent student, project, group, and assignment data.
6. Group formation requests are published to Apache Kafka.
7. The group formation service processes these requests.
8. Group assignments are stored in PostgreSQL.
9. WebSocket sends real-time updates to the React frontend.

## Main Components

### React
Provides the user interface for students.

### FastAPI
Handles API requests and business logic.

### PostgreSQL
Stores persistent application data.

### Redis
Provides fast caching for frequently accessed data.

### Apache Kafka
Handles asynchronous group formation requests and events.

### WebSocket
Provides real-time group status updates.

## Main Entities

- Student
- Project
- Group
- Group Member
- Group Request
