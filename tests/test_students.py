import allure
import pytest
from src.utils.student_payload import make_student_payload
from src.utils.waits import wait_student_readable
from src.utils.student_asserts import assert_student_types
from src.utils.bug_links import BUG_01, BUG_04, BUG_07


@allure.epic("Студенты")
@allure.story("Позитивные")
class TestStudentsPositive:

    @allure.title("Создать студента")
    def test_create_student(self, client):
        with allure.step("Подготовить данные студента"):
            payload = make_student_payload()

        with allure.step("Отправить запрос на создание"):
            resp = client.create_student(payload)
            body = resp.json()

        with allure.step("Проверить ответ"):
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert body["status"] == 1, f"ожидали status=1, получили {body}"
            student_data = body["student"]
            assert_student_types(student_data)
            assert student_data["name"] == payload["name"], (
                f"name: ожидали {payload['name']!r}, получили {student_data['name']!r}"
            )
            assert student_data["email"] == payload["email"], (
                f"email: ожидали {payload['email']!r}, получили {student_data['email']!r}"
            )
            assert student_data["phone_no"] == payload["phone_no"], (
                f"phone_no: ожидали {payload['phone_no']!r}, получили {student_data['phone_no']!r}"
            )
            assert student_data["gender"] == payload["gender"], (
                f"gender: ожидали {payload['gender']!r}, получили {student_data['gender']!r}"
            )
            assert student_data["status"] == payload["status"], (
                f"status: ожидали {payload['status']!r}, получили {student_data['status']!r}"
            )

        with allure.step("Удалить созданного студента"):
            client.delete_student(student_data["id"])

    @allure.issue(BUG_01, "BUG-01")
    @allure.title("Получить студента по id")
    def test_get_student(self, client, student):
        with allure.step("Запросить студента по id"):
            resp = client.get_student(student["id"])
            body = resp.json()

        with allure.step("Проверить данные студента"):
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert body["status"] == 1, f"ожидали status=1, получили {body}"
            student_data = body["student"]
            assert_student_types(student_data)
            assert student_data["id"] == student["id"], (
                f"id: ожидали {student['id']}, получили {student_data['id']}"
            )
            assert student_data["name"] == student["payload"]["name"], (
                f"name: ожидали {student['payload']['name']!r}, получили {student_data['name']!r}"
            )
            assert student_data["email"] == student["payload"]["email"], (
                f"email: ожидали {student['payload']['email']!r}, получили {student_data['email']!r}"
            )
            assert student_data["phone_no"] == student["payload"]["phone_no"], (
                f"phone_no: ожидали {student['payload']['phone_no']!r}, получили {student_data['phone_no']!r}"
            )
            assert student_data["gender"] == student["payload"]["gender"], (
                f"gender: ожидали {student['payload']['gender']!r}, получили {student_data['gender']!r}"
            )
            assert student_data["status"] == student["payload"]["status"], (
                f"status: ожидали {student['payload']['status']!r}, получили {student_data['status']!r}"
            )

    @allure.title("Найти созданного студента в списке")
    def test_get_students_list(self, client, student):
        with allure.step("Получить список студентов"):
            resp = client.get_students_list()
            body = resp.json()

        with allure.step("Найти созданного студента в списке"):
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert body["status"] == 1, f"ожидали status=1, получили {body}"
            assert "students" in body, f"в ответе нет students: {body}"
            found = None
            for item in body["students"]:
                if item["id"] == student["id"]:
                    found = item
                    break
            assert found is not None, f"студент id={student['id']} не найден в списке"
            assert_student_types(found)
            assert found["name"] == student["payload"]["name"], (
                f"name: ожидали {student['payload']['name']!r}, получили {found['name']!r}"
            )
            assert found["email"] == student["payload"]["email"], (
                f"email: ожидали {student['payload']['email']!r}, получили {found['email']!r}"
            )

    @allure.issue(BUG_04, "BUG-04")
    @pytest.mark.xfail(reason="BUG-04: после PUT student.status приходит строкой")
    @allure.title("Ответ при обновлении студента")
    def test_update_student_response(self, client, student):
        with allure.step("Подготовить данные для обновления"):
            wait_student_readable(client, student["id"])
            payload = make_student_payload(gender="female", status=0)
            payload.pop("phone_no")

        with allure.step("Отправить запрос на обновление"):
            resp = client.update_student(student["id"], payload)
            body = resp.json()

        with allure.step("Проверить тело ответа"):
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert body["status"] == 1, f"ожидали status=1, получили {body}"
            updated = body["student"]
            assert_student_types(updated)
            assert updated["id"] == student["id"], (
                f"id: ожидали {student['id']}, получили {updated['id']}"
            )
            assert updated["name"] == payload["name"], (
                f"name: ожидали {payload['name']!r}, получили {updated['name']!r}"
            )
            assert updated["email"] == payload["email"], (
                f"email: ожидали {payload['email']!r}, получили {updated['email']!r}"
            )
            assert updated["gender"] == payload["gender"], (
                f"gender: ожидали {payload['gender']!r}, получили {updated['gender']!r}"
            )
            assert updated["status"] == payload["status"], (
                f"status: ожидали {payload['status']!r}, получили {updated['status']!r}"
            )

    @allure.issue(BUG_07, "BUG-07")
    @pytest.mark.xfail(reason="BUG-07: gender не сохраняется после PUT")
    @allure.title("Обновление студента сохраняется")
    def test_update_student_persisted(self, client, student):
        with allure.step("Обновить студента"):
            wait_student_readable(client, student["id"])
            payload = make_student_payload(gender="female", status=1)
            payload.pop("phone_no")
            resp = client.update_student(student["id"], payload)
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert resp.json()["status"] == 1, f"ожидали status=1, получили {resp.json()}"

        with allure.step("Проверить данные через GET"):
            after = client.get_student(student["id"]).json()["student"]
            assert after["id"] == student["id"], (
                f"id: ожидали {student['id']}, получили {after['id']}"
            )
            assert after["name"] == payload["name"], (
                f"name не сохранился: ожидали {payload['name']!r}, получили {after['name']!r}"
            )
            assert after["email"] == payload["email"], (
                f"email не сохранился: ожидали {payload['email']!r}, получили {after['email']!r}"
            )
            assert after["gender"] == payload["gender"], (
                f"gender не сохранился: ожидали {payload['gender']!r}, получили {after['gender']!r}"
            )
            assert after["phone_no"] == student["payload"]["phone_no"], (
                f"phone_no изменился: ожидали {student['payload']['phone_no']!r}, получили {after['phone_no']!r}"
            )

    @allure.title("Удалить студента")
    def test_delete_student(self, client, student):
        with allure.step("Удалить студента"):
            resp = client.delete_student(student["id"])
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert resp.json()["status"] == 1, f"ожидали status=1 при delete, получили {resp.json()}"

        with allure.step("Проверить, что студент не найден"):
            get_resp = client.get_student(student["id"])
            get_body = get_resp.json()
            assert get_resp.status_code == 200, f"ожидали 200, получили {get_resp.status_code}"
            assert get_body["status"] == 0, f"после delete ожидали status=0, получили {get_body}"
            assert "not found" in get_body.get("message", "").lower(), (
                f"ожидали message с not found, получили {get_body.get('message')!r}"
            )
