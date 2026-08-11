import random
import uuid
import pytest
import allure
from src.clients.students_client import StudentsClient
from src.utils.allure_logger import http_logs
import time


@pytest.fixture(autouse=True)
def attach_test_http_log():
    http_logs.clear()
    yield
    if http_logs:
        allure.attach(
            "\n\n---\n\n".join(http_logs),
            name="http log",
            attachment_type=allure.attachment_type.TEXT,
        )
    http_logs.clear()


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


def wait_student_readable(client, student_id, attempts=15, delay=0.3):
    for attempt in range(attempts):
        resp = client.get_student(student_id)
        body = resp.json()
        if resp.status_code == 200 and body.get("status") == 1:
            return body
        time.sleep(delay)
    raise AssertionError(f"Student {student_id} not readable after create")


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
    wait_student_readable(client, student_id)
    yield student_id
    client.delete_student(student_id)

