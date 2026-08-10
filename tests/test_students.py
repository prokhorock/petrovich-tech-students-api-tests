from conftest import make_student_payload, wait_student_readable
import allure


@allure.story("Позитивные")
class TestStudentsPositive:

    @allure.title("Создать студента")
    def test_create_student(self, client):
        payload = make_student_payload()
        resp = client.create_student(payload)
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 1

        student_id = body["student"]["id"]
        client.delete_student(student_id)

    @allure.title("Получить студента по id")
    def test_get_student(self, client, student):
        resp = client.get_student(student)
        assert resp.status_code == 200
        assert resp.json()["student"]["id"] == student

    @allure.title("Найти созданного студента в списке")
    def test_get_students_list(self, client, student):
        resp = client.get_students_list()
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 1
        assert any(item["id"] == student for item in body["students"])

    @allure.title("Обновить студента")
    def test_update_student(self, client, student):
        payload = make_student_payload(gender="female", status=0)
        payload.pop("phone_no")
        resp = client.update_student(student, payload)
        body = resp.json()
        assert resp.status_code == 200
        assert body["status"] == 1
        assert body["student"]["name"] == payload["name"]

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


