import time
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
    def test_get_student(self, client, student):
        resp = client.get_student(student["id"])
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 1
        student_data = body["student"]
        assert_student_types(student_data)
        assert student_data["id"] == student["id"]
        assert student_data["name"] == student["payload"]["name"]
        assert student_data["email"] == student["payload"]["email"]
        assert student_data["phone_no"] == student["payload"]["phone_no"]
        assert student_data["gender"] == student["payload"]["gender"]
        assert student_data["status"] == student["payload"]["status"]

    @allure.title("Найти созданного студента в списке")
    def test_get_students_list(self, client, student):
        resp = client.get_students_list()
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 1
        assert "students" in body

        found = None
        for item in body["students"]:
            if item["id"] == student["id"]:
                found = item
                break
        assert found is not None
        assert_student_types(found)
        assert found["name"] == student["payload"]["name"]
        assert found["email"] == student["payload"]["email"]

    @pytest.mark.xfail(reason="BUG-04: после PUT student.status приходит строкой")
    @allure.title("Ответ при обновлении студента")
    def test_update_student_response(self, client, student):
        wait_student_readable(client, student["id"])
        payload = make_student_payload(gender="female", status=0)
        payload.pop("phone_no")
        resp = client.update_student(student["id"], payload)
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 1

        updated = body["student"]
        assert_student_types(updated)
        assert updated["id"] == student["id"]
        assert updated["name"] == payload["name"]
        assert updated["email"] == payload["email"]
        assert updated["gender"] == payload["gender"]
        assert updated["status"] == payload["status"]

    @pytest.mark.xfail(reason="BUG-07: gender не сохраняется после PUT")
    @allure.title("Обновление студента сохраняется")
    def test_update_student_persisted(self, client, student):
        wait_student_readable(client, student["id"])
        payload = make_student_payload(gender="female", status=1)
        payload.pop("phone_no")
        resp = client.update_student(student["id"], payload)
        assert resp.status_code == 200
        assert resp.json()["status"] == 1
        # time.sleep(10)
        after = client.get_student(student["id"]).json()["student"]
        assert after["id"] == student["id"]
        assert after["name"] == payload["name"]
        assert after["email"] == payload["email"]
        assert after["gender"] == payload["gender"]
        assert after["phone_no"] == student["payload"]["phone_no"]

    @allure.title("Удалить студента")
    def test_delete_student(self, client, student):
        resp = client.delete_student(student["id"])
        assert resp.status_code == 200
        assert resp.json()["status"] == 1

        get_resp = client.get_student(student["id"])
        get_body = get_resp.json()
        assert get_resp.status_code == 200
        assert get_body["status"] == 0
        assert "not found" in get_body.get("message", "").lower()
