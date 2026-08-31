import os

import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Three Tier Task API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
	"http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskCreate(BaseModel):
    title: str


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "tasks"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
    )


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/tasks")
def get_tasks():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, title, completed
            FROM tasks
            ORDER BY id DESC
            """
        )

        tasks = cursor.fetchall()

        cursor.close()
        connection.close()

        return [
            {
                "id": task[0],
                "title": task[1],
                "completed": task[2],
            }
            for task in tasks
        ]

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/api/tasks")
def create_task(task: TaskCreate):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO tasks (title, completed)
            VALUES (%s, FALSE)
            RETURNING id, title, completed
            """,
            (task.title,),
        )

        new_task = cursor.fetchone()

        connection.commit()

        cursor.close()
        connection.close()

        return {
            "id": new_task[0],
            "title": new_task[1],
            "completed": new_task[2],
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.put("/api/tasks/{task_id}/complete")
def complete_task(task_id: int):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE tasks
            SET completed = TRUE
            WHERE id = %s
            RETURNING id, title, completed
            """,
            (task_id,),
        )

        updated_task = cursor.fetchone()

        if updated_task is None:
            connection.rollback()
            cursor.close()
            connection.close()

            raise HTTPException(
                status_code=404,
                detail="Task not found",
            )

        connection.commit()

        cursor.close()
        connection.close()

        return {
            "id": updated_task[0],
            "title": updated_task[1],
            "completed": updated_task[2],
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM tasks
            WHERE id = %s
            RETURNING id
            """,
            (task_id,),
        )

        deleted_task = cursor.fetchone()

        if deleted_task is None:
            connection.rollback()
            cursor.close()
            connection.close()

            raise HTTPException(
                status_code=404,
                detail="Task not found",
            )

        connection.commit()

        cursor.close()
        connection.close()

        return {"message": "Task deleted"}

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
