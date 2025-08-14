import pytest
import os
import random

from datetime import datetime, timedelta

from sqlmodel import Session, SQLModel, create_engine, select

from src.models import Task

sqlite_file_name = f"data/{os.getenv("SQLITE_FILENAME", "default.db")}"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

session = Session(engine)


def mock_due_date(days_in_future: int = 1) -> datetime:
  """
    Generates a future mock date that is now plus days_in_future

    Parameters
    ----------
    days_in_future : int
        The number of days to add to now.

    Returns
    -------
    datetime
        The current date time plus days_in_future
  """
  return (datetime.now() + timedelta(days=days_in_future))


def str_format_due_date(date: datetime) -> str:
  """
    Converts the supplied datetime as a string with format '%Y-%m-%dT%H:%M:%S.%f'

    Parameters
    ----------
    date : datetime
        The datetime to convert to a string.

    Returns
    -------
    str
        The supplied datetime as a string.
  """
  return date.strftime('%Y-%m-%dT%H:%M:%S.%f')


seed_tasks = [
  {
    'title': 'foo',
    'description': None,
    'priority': 3,
    'completed': False,
    'due_date': mock_due_date()
  },
  {
    'title': 'bar',
    'description': None,
    'priority': 2,
    'completed': False,
    'due_date': mock_due_date()
  }
]


@pytest.fixture(autouse=True, scope='session')
def seed_db():
  """
    A fixture that handles seeding the test database with data and the teardown
    of the table at the end of the test session.
  """
  SQLModel.metadata.create_all(engine)

  for task in seed_tasks:
    db_task = Task(**task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

  yield

  SQLModel.metadata.drop_all(bind=engine)


def task_to_dict(task: Task) -> dict:
  """
    Converts the supplied Task object to a dictionary with the due_date field
    also converted to a string.

    Parameters
    ----------
    task : Task
        The Task to convert to a dictionary.

    Returns
    -------
    dict
        The supplied Task as a dictionary.
  """
  d = {}
  for column in task.__table__.columns:
    if column.name == 'due_date':
      d[column.name] = str_format_due_date(getattr(task, column.name))
    else:
      d[column.name] = getattr(task, column.name)
  return d


@pytest.fixture()
def all_tasks() -> list[dict]:
  """
    A pytest fixture that looks up all tasks stored in the test database.

    Returns
    -------
    list[dict]
        A list of tasks as dictionaries returned from the test database.
  """
  return [task_to_dict(t) for t in session.exec(select(Task)).all()]


def all_task_ids() -> list[int]:
  """
    Looks up all task ids stored in the test database.

    Returns
    -------
    list[int]
        A list of task ids returned from the test database.
  """
  return session.exec(select(Task.id)).all()


def get_task_by_id(id: int) -> dict:
  """
    Queries the test database for a task where id equals the supplied id int.

    Parameters
    ----------
    id : int
        The task id to look up in the test database.

    Returns
    -------
    dict
        The found task as a dictionary.
  """
  task = session.exec(select(Task).where(Task.id == id)).first()
  return task_to_dict(task)


def random_task_title_description() -> dict:
  """
    A function to get a randomly selected task title and description from a
    predefined list generated using Lumo AI (https://lumo.proton.me). I asked an
    AI to get the titles and description because I didn't want to think of them
    myself.

    Returns
    -------
    dict
        A randomly selected title and description dictionary.
  """
  task_title_descriptions = [
    {
      "title": "Essence of Existence",
      "description": "The essence of existence transcends mere physical manifestation and perception."
    },
    {
      "title": "Quantum Spacetime Dynamics",
      "description": "Quantum fluctuations reveal the underlying fabric of spacetime dynamics."
    },
    {
      "title": "Emergence of Consciousness",
      "description": "Consciousness emerges from intricate neural networks and cognitive processes."
    },
    {
      "title": "Philosophical Inquiry",
      "description": "Philosophical inquiry explores the nature of truth and reality."
    },
    {
      "title": "Abstract Art Challenges",
      "description": "Abstract art challenges conventional perceptions of form and meaning."
    },
    {
      "title": "Cosmic Echoes",
      "description": None
    }
  ]
  return task_title_descriptions[random.randint(0, 4)]


@pytest.fixture()
def task_dictionary() -> dict:
  """
    Generates a semi random Task as a dictionary via a combination of randomly
    generated ints.

    Returns
    -------
    dict
        A dictionary representation of a Task.
  """
  title_desc = random_task_title_description()
  return {
    'title': title_desc["title"],
    'description': title_desc["description"],
    'priority': random.randint(1, 3),
    'completed': False,
    'due_date': str_format_due_date(mock_due_date(random.randint(1, 5)))
  }


@pytest.fixture()
def update_task(task_dictionary):
  task_ids = all_task_ids()
  task_id = random.randint(min(task_ids), max(task_ids))

  update_task = get_task_by_id(task_id)
  update_task["title"] = task_dictionary["title"]
  update_task["description"] = task_dictionary["description"]
  update_task["completed"] = True

  return update_task
