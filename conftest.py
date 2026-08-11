import pytest
import allure
from src.clients.students_client import StudentsClient
from src.utils.allure_logger import http_logs
from src.utils.student_payload import make_student_payload
from src.utils.waits import wait_student_readable


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

