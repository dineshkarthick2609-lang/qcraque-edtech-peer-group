import { useEffect, useState } from "react";
import { getStudents } from "./api";
import { Student } from "./types";
import "./App.css";

function App() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getStudents()
      .then((data) => {
        setStudents(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Unable to load students");
        setLoading(false);
      });
  }, []);

  return (
    <div className="app">
      <header>
        <h1>EduConnect</h1>
        <p>Peer-Group Formation System</p>
      </header>

      <main>
        <h2>Students</h2>

        {loading && <p>Loading students...</p>}

        {error && <p className="error">{error}</p>}

        {!loading && !error && (
          <div className="student-grid">
            {students.map((student) => (
              <div className="student-card" key={student.id}>
                <h3>{student.name}</h3>

                <p>
                  <strong>ID:</strong> {student.student_id}
                </p>

                <p>
                  <strong>Email:</strong> {student.email}
                </p>

                <p>
                  <strong>Skills:</strong> {student.skills}
                </p>

                <p>
                  <strong>Level:</strong> {student.skill_level}
                </p>

                <p>
                  <strong>Interests:</strong> {student.interests}
                </p>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
