import { Student } from "./types";

const API_URL = "http://localhost:8000";

export async function getStudents(): Promise<Student[]> {
  const response = await fetch(`${API_URL}/students`);

  if (!response.ok) {
    throw new Error("Failed to fetch students");
  }

  return response.json();
}
