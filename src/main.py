from typing import Annotated

from fastapi import FastAPI, Query
from sqlmodel import select

from db import setup_db_and_tables, SessionDep
from models import Task

app = FastAPI()

@app.on_event("startup")
def on_startup():
  setup_db_and_tables()

@app.get("/tasks/")
def get_tasks(
  session: SessionDep,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100,
) -> list[Task]:
  tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
  return tasks

@app.post("/tasks/", response_model=Task)
def create_task(task: Task, session: SessionDep) -> Task:
  db_task = Task.model_validate(task)
  session.add(db_task)
  session.commit()
  session.refresh(db_task)
  return db_task
