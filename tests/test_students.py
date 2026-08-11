import allure
import pytest
from src.utils.student_payload import make_student_payload
from src.utils.waits import wait_student_readable
from src.utils.student_asserts import assert_student_types


@allure.story("Позитивные")
class TestStudentsPositive:

    @allure.title("Создать студента")
    def test_create_student(self, client):
        payload = make_student_payload()
        resp = client.create_student(payload)
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 1

        student_data = body["student"]
        assert_student_types(student_data)
        assert student_data["name"] == payload["name"]
        assert student_data["email"] == payload["email"]
        assert student_data["phone_no"] == payload["phone_no"]
        assert student_data["gender"] == payload["gender"]
        assert student_data["status"] == payload["status"]

        client.delete_student(student_data["id"])

    @allure.title("Получить студента по id")
    def test_get_student(self, client):
        payload = make_student_payload()
        create_resp = client.create_student(payload)
        create_body = create_resp.json()
        assert create_resp.status_code == 200
        assert create_body["status"] == 1
        student_id = create_body["student"]["id"]
        wait_student_readable(client, student_id)

        resp = client.get_student(student_id)
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 1
        student_data = body["student"]
        assert_student_types(student_data)
        assert student_data["id"] == student_id
        assert student_data["name"] == payload["name"]
        assert student_data["email"] == payload["email"]
        assert student_data["phone_no"] == payload["phone_no"]
        assert student_data["gender"] == payload["gender"]
        assert student_data["status"] == payload["status"]

        client.delete_student(student_id)

    @allure.title("Найти созданного студента в списке")
    def test_get_students_list(self, client, student):
        resp = client.get_students_list()
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 1
        assert "students" in body

        found = None
        for item in body["students"]:
            if item["id"] == student:
                found = item
                break
        assert found is not None
        assert_student_types(found)

    @pytest.mark.xfail(reason="BUG-04: после PUT student.status приходит строкой")
    @allure.title("Обновить студента")
    def test_update_student(self, client, student):
        wait_student_readable(client, student)
        payload = make_student_payload(gender="female", status=0)
        payload.pop("phone_no")
        resp = client.update_student(student, payload)
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 1

        updated = body["student"]
        assert_student_types(updated)
        assert updated["id"] == student
        assert updated["name"] == payload["name"]
        assert updated["email"] == payload["email"]
        assert updated["gender"] == payload["gender"]
        assert updated["status"] == payload["status"]

    @allure.title("Удалить студента")
    def test_delete_student(self, client):
        payload = make_student_payload()
        create_resp = client.create_student(payload)
        create_body = create_resp.json()
        assert create_resp.status_code == 200
        assert create_body["status"] == 1
        student_id = create_body["student"]["id"]
        wait_student_readable(client, student_id)

        resp = client.delete_student(student_id)
        assert resp.status_code == 200
        assert resp.json()["status"] == 1

        get_resp = client.get_student(student_id)
        get_body = get_resp.json()
        assert get_resp.status_code == 200
        assert get_body["status"] == 0
        assert "not found" in get_body.get("message", "").lower()
