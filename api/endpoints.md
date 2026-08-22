# Peer-Group Formation API Endpoints

## Student APIs

### GET /api/students/{student_id}

Retrieves student profile information.

### GET /api/students/{student_id}/groups

Retrieves the groups associated with a student.

---

## Project APIs

### GET /api/projects

Retrieves available projects.

### GET /api/projects/{project_id}

Retrieves details of a specific project.

---

## Group APIs

### GET /api/groups

Retrieves available peer groups.

### GET /api/groups/{group_id}

Retrieves details of a specific group.

### POST /api/groups

Creates a new peer group.

### POST /api/groups/{group_id}/members

Adds a student to a peer group.

### DELETE /api/groups/{group_id}/members/{student_id}

Removes a student from a peer group.

---

## Group Formation APIs

### POST /api/group-requests

Creates a request for peer-group formation.

### GET /api/group-requests/{request_id}

Retrieves the status of a group formation request.

---

## Real-Time API

### WebSocket /ws/groups/{student_id}

Provides real-time updates about group formation and group assignment.
