import random
import uuid
import pytest
from src.clients.students_client import StudentsClient


def make_student_payload(**overrides):
    suffix = uuid.uuid4().hex[:10]
    payload = {
        "name": f"Student {suffix}",
        "email": f"student_{suffix}@test.com",
        "phone_no": f"+7{random.randint(9000000000, 9999999999)}",
        "gender": "male",
        "status": 1,
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def client():
    return StudentsClient()


@pytest.fixture
def student(client):
    payload = make_student_payload()
    resp = client.create_student(payload)
    body = resp.json()
    assert resp.status_code == 200
    assert body["status"] == 1
    student_id = body["student"]["id"]
    yield student_id
    client.delete_student(student_id)


