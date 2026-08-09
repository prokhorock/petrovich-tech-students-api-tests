import pytest
from src.clients.students_client import StudentsClient
import uuid


@pytest.fixture
def client():
    return StudentsClient()

@pytest.fixture
def student(client):
    payload = {
        "name": "Ivan Test",
        "email": f"ivan_{uuid.uuid4().hex}@test.com",
        "phone_no": "+79990001122",
        "gender": "male",
        "status": 1,
    }
    resp = client.create_student(payload)
    assert resp.status_code == 200
    student_id = resp.json()["student"]["id"]
    yield student_id
    client.delete_student(student_id)
