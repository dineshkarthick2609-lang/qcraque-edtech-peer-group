import { useEffect, useState } from "react";
import "./PeerGroupDisplay.css";

interface Student {
  id: number;
  student_id: string;
  name: string;
  email: string;
  interests: string;
  skills: string;
  skill_level: string;
}

const API_URL = "http://localhost:8000";

function PeerGroupDisplay() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(`${API_URL}/students`);

        if (!response.ok) {
          throw new Error("Failed to fetch student data");
        }

        const data: Student[] = await response.json();

        setStudents(data);
      } catch (err) {
        setError("Unable to load student data. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  if (loading) {
    return (
      <section className="peer-group-section">
        <div className="status-card">
          <div className="loader"></div>
          <p>Loading student data...</p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="peer-group-section">
        <div className="status-card error-card">
          <h3>Unable to Load Data</h3>
          <p>{error}</p>
        </div>
      </section>
    );
  }

  return (
    <section className="peer-group-section">
      <div className="section-header">
        <div>
          <p className="section-label">EDUCONNECT</p>
          <h2>Peer Group Formation</h2>
          <p className="section-description">
            Students available for peer-group formation.
          </p>
        </div>

        <div className="student-count">
          <span>{students.length}</span>
          <small>Students</small>
        </div>
      </div>

      {students.length === 0 ? (
        <div className="status-card">
          <h3>No Students Found</h3>
          <p>There are currently no students available.</p>
        </div>
      ) : (
        <div className="student-grid">
          {students.map((student) => (
            <article className="student-card" key={student.id}>
              <div className="student-header">
                <div className="avatar">
                  {student.name.charAt(0).toUpperCase()}
                </div>

                <div>
                  <h3>{student.name}</h3>
                  <span>{student.student_id}</span>
                </div>
              </div>

              <div className="student-info">
                <div className="info-item">
                  <strong>Email</strong>
                  <p>{student.email}</p>
                </div>

                <div className="info-item">
                  <strong>Skills</strong>
                  <p>{student.skills || "Not specified"}</p>
                </div>

                <div className="info-item">
                  <strong>Interests</strong>
                  <p>{student.interests || "Not specified"}</p>
                </div>
              </div>

              <div className="skill-level">
                <span>Skill Level</span>
                <strong>{student.skill_level}</strong>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

export default PeerGroupDisplay;
