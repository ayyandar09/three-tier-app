import { useEffect, useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);

  const loadTasks = async () => {
    try {
      const response = await fetch(`${API_URL}/api/tasks`);

      if (!response.ok) {
        throw new Error("Failed to load tasks");
      }

      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const createTask = async (event) => {
    event.preventDefault();

    if (!title.trim()) return;

    try {
      const response = await fetch(`${API_URL}/api/tasks`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: title.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to create task");
      }

      setTitle("");
      await loadTasks();
    } catch (error) {
      console.error(error);
    }
  };

  const completeTask = async (id) => {
    try {
      await fetch(`${API_URL}/api/tasks/${id}/complete`, {
        method: "PUT",
      });

      await loadTasks();
    } catch (error) {
      console.error(error);
    }
  };

  const deleteTask = async (id) => {
    try {
      await fetch(`${API_URL}/api/tasks/${id}`, {
        method: "DELETE",
      });

      await loadTasks();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <main className="app">
      <section className="card">
        <h1>DevOps Task Manager</h1>

        <p className="subtitle">
          React + FastAPI + PostgreSQL
        </p>

        <form onSubmit={createTask} className="task-form">
          <input
            type="text"
            placeholder="Enter a task..."
            value={title}
            onChange={(event) => setTitle(event.target.value)}
          />

          <button type="submit">Add Task</button>
        </form>

        {loading ? (
          <p>Loading tasks...</p>
        ) : tasks.length === 0 ? (
          <p>No tasks found.</p>
        ) : (
          <div className="tasks">
            {tasks.map((task) => (
              <div className="task" key={task.id}>
                <span className={task.completed ? "completed" : ""}>
                  {task.title}
                </span>

                <div className="actions">
                  {!task.completed && (
                    <button onClick={() => completeTask(task.id)}>
                      Complete
                    </button>
                  )}

                  <button onClick={() => deleteTask(task.id)}>
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}

export default App;
