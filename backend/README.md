# EduConnect Backend

The EduConnect backend provides REST APIs for the Peer-Group Formation System.

## Technology Stack

- FastAPI
- Python
- PostgreSQL
- SQLAlchemy
- Pydantic
- Docker

## Primary Entity

The primary entity implemented in this phase is Student.

## Student API

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/students` | Create student |
| GET | `/students` | Get all students |
| GET | `/students/{id}` | Get student |
| PUT | `/students/{id}` | Update student |
| DELETE | `/students/{id}` | Delete student |

## Database

PostgreSQL is used as the primary relational database.

The database schema is available in:

```text
schema.sql
