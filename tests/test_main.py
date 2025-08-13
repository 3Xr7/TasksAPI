import random

from fastapi.testclient import TestClient
from src.main import app
from tests.conftest import all_task_ids, get_task_by_id

client = TestClient(app)


def test_get_tasks(all_tasks):
  resp = client.get("/tasks/")
  assert resp.status_code == 200
  assert resp.json() == all_tasks


def test_create_task(task_dictionary):
  new_task = {
    "title": task_dictionary["title"],
    "description": task_dictionary["description"],
    "priority": task_dictionary["priority"],
    "due_date": task_dictionary["due_date"]
  }

  resp = client.post("/tasks/", json=new_task)
  task_created = resp.json()
  task_ids = all_task_ids()

  assert task_created["id"] == max(task_ids)
  assert task_created["title"] == task_dictionary["title"]
  assert task_created["description"] == task_dictionary["description"]
  assert task_created["priority"] == task_dictionary["priority"]
  assert task_created["due_date"] == task_dictionary["due_date"]
  assert not task_created["completed"]


def test_update_task(task_dictionary):
  task_ids = all_task_ids()
  task_id = random.randint(min(task_ids), max(task_ids))

  update_task = get_task_by_id(task_id)
  update_task["title"] = task_dictionary["title"]
  update_task["description"] = task_dictionary["description"]
  update_task["completed"] = True

  resp = client.put(f"/tasks/{task_id}", json=update_task)
  task_updated = resp.json()

  assert task_updated["title"] == task_dictionary["title"]
  assert task_updated["description"] == task_dictionary["description"]
  assert task_updated["completed"]


def test_delete_task():
  task_id = max(all_task_ids())

  resp = client.delete(f"/tasks/{task_id}")

  assert "message" in resp.json().keys()
  assert resp.json()["message"] == "Task deleted successfully."
