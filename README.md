# EduConnect – Scalable Peer-Group Formation System

## Phase 1: Understand & Explore

EduConnect is a scalable EdTech platform designed to improve peer-group formation for collaborative academic projects.

The system uses React, FastAPI, PostgreSQL, Redis, Kafka, WebSocket, and Docker to provide a scalable full-stack architecture.

---

## Business Problem

EduConnect needs an efficient way to form suitable peer groups for students working on collaborative projects.

The system considers student profiles, skills, project requirements, and group requests while providing a scalable architecture for group formation.

---

# Architecture

```text
                         React Frontend
                               |
                               v
                         FastAPI Backend
                               |
              +----------------+----------------+
              |                |                |
              v                v                v
         PostgreSQL          Redis            Kafka
              |                |                |
              |                |                v
              |                |        Group Formation
              |                |            Events
              |                |
              +----------------+
                       |
                       v
                Group Formation
                   Processing
                       |
                       v
                  WebSocket
                       |
                       v
                  React UI
