from datetime import datetime

from fastapi import FastAPI, HTTPException
from sqlmodel import select

from src.db import setup_db_and_tables, SessionDep
from src.models import Task

app = FastAPI()


@app.on_event("startup")
def on_startup():
  setup_db_and_tables()


@app.get("/tasks/")
def get_tasks(session: SessionDep) -> list[Task]:
  """
    Get all tasks returning them to the client.

    Parameters
    ----------

    Returns
    -------
    list[Task]
        List of all tasks.
  """
  tasks = session.exec(select(Task)).all()
  return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int, session: SessionDep) -> Task:
  """
    Get a task by ID returning it to the client.

    Parameters
    ----------
    task_id : int
        The ID of the tasks to look up.

    Returns
    -------
    Task
        Task record found.

    Raises
    ------
    HTTPException
        If the task ID can't be found.
  """
  task = session.get(Task, task_id)
  if not task:
      raise HTTPException(status_code=404, detail="Task not found")
  return task


@app.post("/tasks/", response_model=Task)
def create_task(task: Task, session: SessionDep) -> Task:
  """
    Creates a tasks sent by the client.

    Parameters
    ----------
    task : Task
        The task to create.

    Returns
    -------
    Task
        Task record created.

    Raises
    ------
    ValidationError
        If the recieved task data doesn't match the Task model.
  """
  db_task = Task.model_validate(task)
  session.add(db_task)
  session.commit()
  session.refresh(db_task)
  return db_task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task, session: SessionDep):
  """
    Updates the task with task_id with the data sent by the client.

    Parameters
    ----------
    task_id : int
        The ID of the tasks to look up.
    task : Task
        The task data to update.

    Returns
    -------
    Task
        Task record created.

    Raises
    ------
    HTTPException
        404 If the recieved task id can't be found.
        400 If the recieved task due_date isn't ISO format.
  """
  task_db = session.get(Task, task_id)
  if not task_db:
    raise HTTPException(status_code=404, detail="Task not found")

  task_data = task.model_dump(exclude_unset=True)
  try:
    task_data["due_date"] = datetime.fromisoformat(task_data["due_date"])
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))

  task_db.sqlmodel_update(task_data)
  session.add(task_db)
  session.commit()
  session.refresh(task_db)
  return task_db


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: SessionDep):
  """
    Deletes the task with the task_id sent by the client.

    Parameters
    ----------
    task_id : int
        The ID of the tasks to delete.

    Returns
    -------
    dict
        A dictionary response with a message confirming the task was deleted.

    Raises
    ------
    HTTPException
        404 If the recieved task id can't be found.
  """
  task = session.get(Task, task_id)
  if not task:
    raise HTTPException(status_code=404, detail="Task not found")
  session.delete(task)
  session.commit()
  return {"message": "Task deleted successfully."}
