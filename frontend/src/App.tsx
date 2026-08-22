import { useEffect, useState } from "react";

interface Project {
  id: number;
  title: string;
  description: string;
  required_skills: string;
}

interface Student {
  id: number;
  name: string;
  email: string;
  skills: string;
}

interface Group {
  id: number;
  project_id: number | null;
  name: string;
  status: string;
}

const API_URL = "http://localhost:8000";

function App() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [groups, setGroups] = useState<Group[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const [projectsResponse, studentsResponse, groupsResponse] =
        await Promise.all([
          fetch(`${API_URL}/api/projects`),
          fetch(`${API_URL}/api/students`),
          fetch(`${API_URL}/api/groups`),
        ]);

      if (!projectsResponse.ok || !studentsResponse.ok || !groupsResponse.ok) {
        throw new Error("Unable to load data");
      }

      setProjects(await projectsResponse.json());
      setStudents(await studentsResponse.json());
      setGroups(await groupsResponse.json());
    } catch (error) {
      setMessage(
        "Backend is not running. Start the FastAPI server on port 8000."
      );
    } finally {
      setLoading(false);
    }
  }

  async function requestGroup(projectId: number) {
    if (students.length === 0) {
      setMessage("No students are available.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/api/group-requests`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          student_id: students[0].id,
          project_id: projectId,
        }),
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      setMessage("Group formation request submitted successfully.");
    } catch {
      setMessage("Unable to submit group request.");
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>EduConnect</h1>
          <p>Scalable Peer-Group Formation System</p>
        </div>

        <div className="status">
          ● Real-Time Learning Platform
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <h2>Find Your Perfect Peer Group</h2>
          <p>
            Explore collaborative projects and submit a request to join a
            suitable peer group.
          </p>
        </section>

        {message && <div className="message">{message}</div>}

        {loading ? (
          <div className="loading">Loading EduConnect data...</div>
        ) : (
          <>
            <section className="stats">
              <div className="stat-card">
                <strong>{students.length}</strong>
                <span>Students</span>
              </div>

              <div className="stat-card">
                <strong>{projects.length}</strong>
                <span>Projects</span>
              </div>

              <div className="stat-card">
                <strong>{groups.length}</strong>
                <span>Active Groups</span>
              </div>
            </section>

            <section>
              <div className="section-title">
                <h2>Available Projects</h2>
                <span>{projects.length} projects</span>
              </div>

              <div className="project-grid">
                {projects.map((project) => (
                  <article className="project-card" key={project.id}>
                    <div className="project-icon">🚀</div>

                    <h3>{project.title}</h3>

                    <p>{project.description}</p>

                    <div className="skills">
                      {project.required_skills
                        .split(",")
                        .filter(Boolean)
                        .map((skill) => (
                          <span key={skill}>{skill.trim()}</span>
                        ))}
                    </div>

                    <button onClick={() => requestGroup(project.id)}>
                      Request Peer Group
                    </button>
                  </article>
                ))}
              </div>
            </section>

            <section className="groups-section">
              <div className="section-title">
                <h2>Group Status</h2>
                <span>Live updates</span>
              </div>

              {groups.length === 0 ? (
                <div className="empty">
                  No groups have been formed yet.
                </div>
              ) : (
                <div className="group-grid">
                  {groups.map((group) => (
                    <div className="group-card" key={group.id}>
                      <h3>{group.name}</h3>
                      <p>Project ID: {group.project_id ?? "N/A"}</p>
                      <span className="group-status">
                        {group.status}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </section>
          </>
        )}
      </main>

      <footer>
        EduConnect • Phase 1 Vertical Slice
      </footer>
    </div>
  );
}

export default App;
