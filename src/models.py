
# id (int): Primary key.
# title (string): Task title (required).
# description (string): Task description (optional).
# priority (int): Task priority (1 = High, 2 = Medium, 3 = Low).
# due_date (datetime): Due date for the task.
# completed (bool): Completion status (default: False).

from datetime import datetime, timedelta

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True)
  title: str = Field(index=True)
  description: str | None = Field(default=None)
  priority: int = Field(default=3, index=True)
  due_date: datetime = Field(default=datetime.now() + timedelta(days=1), index=True)
  completed: bool = Field(default=False)
