import allure
import pytest
from src.utils.student_payload import make_student_payload


@allure.story("Негативные")
class TestStudentsNegative:

    @pytest.mark.parametrize("field", ["email", "name", "phone_no", "gender", "status"])
    def test_create_student_without_required_field(self, client, field):
        allure.dynamic.title(f"Создать студента без {field}")
        payload = make_student_payload()
        payload.pop(field)
        resp = client.create_student(payload)
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 0
        assert body.get("message")

    @pytest.mark.parametrize(
        "field, value",
        [
            ("gender", "unknown"),
            ("status", 2),
        ],
    )
    def test_create_student_invalid_field(self, client, field, value):
        allure.dynamic.title(f"Создать студента с невалидным {field}")
        payload = make_student_payload(**{field: value})
        resp = client.create_student(payload)
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 0
        assert body.get("message")

    @allure.title("Создать студента с пустым телом")
    def test_create_student_empty_body(self, client):
        resp = client.create_student({})
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 0
        assert body.get("message")

    @allure.title("Получить несуществующего студента")
    def test_get_student_not_found(self, client):
        resp = client.get_student(99999999)
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 0
        assert "not found" in body["message"].lower()

    @allure.title("Получить студента с невалидным id")
    def test_get_student_invalid_id(self, client):
        resp = client.get_student("abc")
        assert resp.status_code != 500
        if resp.headers.get("content-type", "").startswith("application/json"):
            body = resp.json()
            assert body["status"] == 0

    @allure.title("Обновить несуществующего студента")
    def test_update_student_not_found(self, client):
        student_id = 99999999

        get_resp = client.get_student(student_id)
        get_body = get_resp.json()
        assert get_resp.status_code == 200
        assert get_body["status"] == 0

        payload = make_student_payload()
        payload.pop("phone_no")
        resp = client.update_student(student_id, payload)
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 0
        assert body.get("message")

    @allure.title("Обновить студента с неполным телом")
    def test_update_student_partial_body(self, client, student):
        resp = client.update_student(student, {"name": "Only Name"})
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 0
        assert body.get("message")

    @allure.title("Обновить студента с phone_no в теле")
    def test_update_student_with_phone_no(self, client, student):
        before = client.get_student(student).json()
        assert before["status"] == 1
        old_phone = before["student"]["phone_no"]

        payload = make_student_payload(gender="female", status=1)
        resp = client.update_student(student, payload)
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 1
        assert body["student"]["phone_no"] == old_phone
        assert body["student"]["name"] == payload["name"]
        assert body["student"]["email"] == payload["email"]

        after = client.get_student(student).json()["student"]
        assert after["phone_no"] == old_phone
        assert after["name"] == payload["name"]
        assert after["gender"] == payload["gender"]

    @pytest.mark.parametrize(
        "field, value",
        [
            ("gender", "unknown"),
            ("status", 2),
        ],
    )
    def test_update_student_invalid_field(self, client, student, field, value):
        allure.dynamic.title(f"Обновить студента с невалидным {field}")
        payload = make_student_payload(**{field: value})
        payload.pop("phone_no")
        resp = client.update_student(student, payload)
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 0

    @pytest.mark.xfail(reason="BUG-03")
    @allure.title("Удалить несуществующего студента")
    def test_delete_student_not_found(self, client):
        student_id = 99999999

        get_resp = client.get_student(student_id)
        get_body = get_resp.json()
        assert get_resp.status_code == 200
        assert get_body["status"] == 0

        resp = client.delete_student(student_id)
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 0



