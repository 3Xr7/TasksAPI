from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_get_tasks(all_tasks):
  resp = client.get("/tasks/")
  print(resp.json())
  assert resp.status_code == 200
  assert resp.json() == all_tasks
