-- ============================================================
-- EduConnect Peer-Group Formation System
-- PostgreSQL Database Schema
-- Step 2: Backend Layer
-- ============================================================

-- ============================================================
-- 1. STUDENTS TABLE
-- Primary entity for Step 2
-- ============================================================

CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,

    student_id VARCHAR(50) UNIQUE NOT NULL,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(150) UNIQUE NOT NULL,

    interests TEXT DEFAULT '',

    skills TEXT DEFAULT '',

    skill_level VARCHAR(30) NOT NULL DEFAULT 'BEGINNER',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_student_name
        CHECK (LENGTH(TRIM(name)) >= 2),

    CONSTRAINT chk_student_email
        CHECK (POSITION('@' IN email) > 1),

    CONSTRAINT chk_skill_level
        CHECK (
            skill_level IN (
                'BEGINNER',
                'INTERMEDIATE',
                'ADVANCED',
                'EXPERT'
            )
        )
);


-- ============================================================
-- 2. PROJECTS TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,

    title VARCHAR(200) NOT NULL,

    description TEXT NOT NULL,

    required_skills TEXT DEFAULT '',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_project_title
        CHECK (LENGTH(TRIM(title)) >= 2)
);


-- ============================================================
-- 3. GROUPS TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,

    project_id INTEGER,

    name VARCHAR(100) NOT NULL,

    status VARCHAR(30) NOT NULL DEFAULT 'FORMING',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_group_project
        FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE SET NULL,

    CONSTRAINT chk_group_status
        CHECK (
            status IN (
                'FORMING',
                'ACTIVE',
                'COMPLETED',
                'CANCELLED'
            )
        )
);


-- ============================================================
-- 4. GROUP MEMBERS TABLE
-- Many-to-Many relationship between Students and Groups
-- ============================================================

CREATE TABLE IF NOT EXISTS group_members (
    id SERIAL PRIMARY KEY,

    group_id INTEGER NOT NULL,

    student_id INTEGER NOT NULL,

    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_group_member_group
        FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_group_member_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE,

    CONSTRAINT unique_group_student
        UNIQUE (group_id, student_id)
);


-- ============================================================
-- 5. GROUP REQUESTS TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS group_requests (
    id SERIAL PRIMARY KEY,

    student_id INTEGER NOT NULL,

    project_id INTEGER NOT NULL,

    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',

    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_request_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_request_project
        FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_request_status
        CHECK (
            status IN (
                'PENDING',
                'APPROVED',
                'REJECTED',
                'CANCELLED'
            )
        )
);


-- ============================================================
-- 6. INDEXES
-- Improve query performance
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_students_email
    ON students(email);

CREATE INDEX IF NOT EXISTS idx_students_student_id
    ON students(student_id);

CREATE INDEX IF NOT EXISTS idx_students_skill_level
    ON students(skill_level);

CREATE INDEX IF NOT EXISTS idx_groups_project_id
    ON groups(project_id);

CREATE INDEX IF NOT EXISTS idx_groups_status
    ON groups(status);

CREATE INDEX IF NOT EXISTS idx_group_members_group_id
    ON group_members(group_id);

CREATE INDEX IF NOT EXISTS idx_group_members_student_id
    ON group_members(student_id);

CREATE INDEX IF NOT EXISTS idx_group_requests_student_id
    ON group_requests(student_id);

CREATE INDEX IF NOT EXISTS idx_group_requests_project_id
    ON group_requests(project_id);

CREATE INDEX IF NOT EXISTS idx_group_requests_status
    ON group_requests(status);


-- ============================================================
-- 7. SAMPLE STUDENT DATA
-- ============================================================

INSERT INTO students (
    student_id,
    name,
    email,
    interests,
    skills,
    skill_level
)
VALUES
(
    'STU001',
    'Arun Kumar',
    'arun@example.com',
    'Artificial Intelligence, Machine Learning',
    'Python, Machine Learning',
    'INTERMEDIATE'
),
(
    'STU002',
    'Priya Sharma',
    'priya@example.com',
    'Web Development, UI Design',
    'React, TypeScript',
    'INTERMEDIATE'
),
(
    'STU003',
    'Rahul Kumar',
    'rahul@example.com',
    'Data Analytics, Machine Learning',
    'Data Science, SQL',
    'ADVANCED'
)
ON CONFLICT (email) DO NOTHING;


-- ============================================================
-- 8. SAMPLE PROJECT DATA
-- ============================================================

INSERT INTO projects (
    title,
    description,
    required_skills
)
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
)
ON CONFLICT DO NOTHING;


-- ============================================================
-- 9. VERIFY STUDENT DATA
-- ============================================================

SELECT
    id,
    student_id,
    name,
    email,
    interests,
    skills,
    skill_level,
    created_at
FROM students
ORDER BY id;


-- ============================================================
-- 10. VERIFY PROJECT DATA
-- ============================================================

SELECT
    id,
    title,
    description,
    required_skills,
    created_at
FROM projects
ORDER BY id;


-- ============================================================
-- 11. VERIFY GROUP DATA
-- ============================================================

SELECT
    id,
    project_id,
    name,
    status,
    created_at
FROM groups
ORDER BY id;


-- ============================================================
-- 12. VERIFY GROUP MEMBERS
-- ============================================================

SELECT
    id,
    group_id,
    student_id,
    joined_at
FROM group_members
ORDER BY id;


-- ============================================================
-- 13. VERIFY GROUP REQUESTS
-- ============================================================

SELECT
    id,
    student_id,
    project_id,
    status,
    requested_at
FROM group_requests
ORDER BY id;
