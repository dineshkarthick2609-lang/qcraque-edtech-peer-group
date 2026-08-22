-- ============================================================
-- EduConnect Peer-Group Formation System
-- PostgreSQL Database Schema
-- ============================================================

CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    skills TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    required_skills TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    name VARCHAR(100) NOT NULL,
    status VARCHAR(30) DEFAULT 'FORMING'
);

CREATE TABLE IF NOT EXISTS group_members (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    UNIQUE(group_id, student_id)
);

CREATE TABLE IF NOT EXISTS group_requests (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    status VARCHAR(30) DEFAULT 'PENDING'
);

-- ============================================================
-- SAMPLE DATA
-- ============================================================

INSERT INTO students (name, email, skills)
VALUES
    ('Arun Kumar', 'arun@example.com', 'Python, Machine Learning'),
    ('Priya Sharma', 'priya@example.com', 'React, TypeScript'),
    ('Rahul Kumar', 'rahul@example.com', 'Data Science, SQL')
ON CONFLICT (email) DO NOTHING;

INSERT INTO projects (title, description, required_skills)
VALUES
    (
        'AI Study Assistant',
        'Develop an AI-powered assistant for students.',
        'Python, Machine Learning'
    ),
    (
        'Smart Campus Platform',
        'Build a platform for smart campus services.',
        'React, TypeScript, Node.js'
    ),
    (
        'Student Analytics Dashboard',
        'Create an analytics dashboard for student performance.',
        'Python, SQL, Data Science'
    );

-- ============================================================
-- VERIFY DATA
-- ============================================================

SELECT * FROM students;

SELECT * FROM projects;

SELECT * FROM groups;

SELECT * FROM group_members;

SELECT * FROM group_requests;
