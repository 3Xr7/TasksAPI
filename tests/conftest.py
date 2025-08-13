import pytest
import os

from datetime import datetime, timedelta

from sqlmodel import Session, SQLModel, create_engine, select

from src.models import Task

sqlite_file_name = f"data/{os.getenv("SQLITE_FILENAME", "default.db")}"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

mock_due_data = (datetime.now() + timedelta(days=1))

def str_format_due_date(date: datetime):
  return date.strftime('%Y-%m-%dT%H:%M:%S.%f')

seed_tasks = [
  {
    'title': 'foo',
    'description': None,
    'priority': 3,
    'completed': False,
    'due_date': mock_due_data
  },
  {
    'title': 'bar',
    'description': None,
    'priority': 2,
    'completed': False,
    'due_date': mock_due_data
  }
]

@pytest.fixture(scope='session')
def session():
  return Session(engine)


@pytest.fixture(autouse=True, scope='session')
def seed_db(session):
  SQLModel.metadata.create_all(engine)

  for task in seed_tasks:
    db_task = Task(**task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

  yield

  SQLModel.metadata.drop_all(bind=engine)


def task_to_dict(task):
  d = {}
  for column in task.__table__.columns:
    if column.name == 'due_date':
      d[column.name] = str_format_due_date(getattr(task, column.name))
    else:
      d[column.name] = getattr(task, column.name)
  return d


@pytest.fixture(scope='session')
def all_tasks(session):
  return [task_to_dict(t) for t in session.exec(select(Task)).all()]

