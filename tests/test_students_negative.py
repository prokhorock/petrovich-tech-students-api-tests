import allure
import pytest
from src.utils.student_payload import make_student_payload
from src.utils.bug_links import BUG_02, BUG_03, BUG_05, BUG_06


@allure.epic("Студенты")
@allure.story("Негативные")
class TestStudentsNegative:

    @pytest.mark.parametrize("field", ["email", "name", "phone_no", "gender", "status"])
    def test_create_student_without_required_field(self, client, field):
        allure.dynamic.title(f"Создать студента без {field}")
        with allure.step(f"Собрать payload без поля {field}"):
            payload = make_student_payload()
            payload.pop(field)

        with allure.step("Отправить запрос на создание"):
            resp = client.create_student(payload)
            body = resp.json()

        with allure.step("Проверить, что создание отклонено"):
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert body["status"] == 0, (
                f"без поля {field} ожидали status=0, получили {body}"
            )
            assert body.get("message"), f"ожидали message об ошибке, получили {body}"

    @pytest.mark.parametrize(
        "field, value",
        [
            ("gender", "unknown"),
            ("status", 2),
        ],
    )
    def test_create_student_invalid_field(self, client, field, value):
        allure.dynamic.title(f"Создать студента с невалидным {field}")
        with allure.step(f"Собрать payload с невалидным {field}"):
            payload = make_student_payload(**{field: value})

        with allure.step("Отправить запрос на создание"):
            resp = client.create_student(payload)
            body = resp.json()

        with allure.step("Проверить, что создание отклонено"):
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert body["status"] == 0, (
                f"невалидный {field}={value!r}: ожидали status=0, получили {body}"
            )
            assert body.get("message"), f"ожидали message об ошибке, получили {body}"

    @allure.title("Создать студента с пустым телом")
    def test_create_student_empty_body(self, client):
        with allure.step("Отправить пустой payload"):
            resp = client.create_student({})
            body = resp.json()

        with allure.step("Проверить, что создание отклонено"):
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert body["status"] == 0, f"пустой body: ожидали status=0, получили {body}"
            assert body.get("message"), f"ожидали message об ошибке, получили {body}"

    @allure.issue(BUG_05, "BUG-05")
    @pytest.mark.parametrize("field", ["email", "phone_no"])
    @pytest.mark.xfail(reason="BUG-05: API принимает дубликаты email/phone_no")
    def test_create_duplicate_field(self, client, field):
        allure.dynamic.title(f"Создать студента с дубликатом {field}")
        with allure.step("Создать первого студента"):
            payload = make_student_payload()
            first = client.create_student(payload).json()
            assert first["status"] == 1, f"не удалось создать первого студента: {first}"
            student_id = first["student"]["id"]

        dup_id = None
        try:
            with allure.step(f"Попытаться создать второго с тем же {field}"):
                dup_payload = make_student_payload()
                dup_payload[field] = payload[field]
                resp = client.create_student(dup_payload)
                body = resp.json()
                if body.get("status") == 1 and body.get("student"):
                    dup_id = body["student"]["id"]

            with allure.step("Проверить, что дубликат отклонён"):
                assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
                assert body["status"] == 0, (
                    f"дубликат {field}: ожидали status=0, получили {body}"
                )
                assert body.get("message"), f"ожидали message об ошибке, получили {body}"
        finally:
            with allure.step("Удалить тестовые данные"):
                client.delete_student(student_id)
                if dup_id:
                    client.delete_student(dup_id)

    @pytest.mark.parametrize(
        "field",
        [
            "name",
            pytest.param(
                "email",
                marks=pytest.mark.xfail(reason="BUG-06: API принимает пустой email"),
            ),
            "phone_no",
        ],
    )
    def test_create_empty_required_field(self, client, field):
        allure.dynamic.title(f"Создать студента с пустым {field}")
        if field == "email":
            allure.dynamic.issue(BUG_06, "BUG-06")
        with allure.step(f"Собрать payload с пустым {field}"):
            payload = make_student_payload()
            payload[field] = ""

        with allure.step("Отправить запрос на создание"):
            resp = client.create_student(payload)
            body = resp.json()
            created_id = None
            if body.get("status") == 1 and body.get("student"):
                created_id = body["student"]["id"]

        try:
            with allure.step("Проверить, что создание отклонено"):
                assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
                assert body["status"] == 0, (
                    f"пустой {field}: ожидали status=0, получили {body}"
                )
                assert body.get("message"), f"ожидали message об ошибке, получили {body}"
        finally:
            if created_id:
                client.delete_student(created_id)

    @allure.issue(BUG_06, "BUG-06")
    @pytest.mark.xfail(reason="BUG-06: API принимает невалидный email")
    @allure.title("Создать студента с невалидным email")
    def test_create_invalid_email(self, client):
        with allure.step("Собрать payload с невалидным email"):
            payload = make_student_payload(email="not-email")

        with allure.step("Отправить запрос на создание"):
            resp = client.create_student(payload)
            body = resp.json()
            created_id = None
            if body.get("status") == 1 and body.get("student"):
                created_id = body["student"]["id"]

        try:
            with allure.step("Проверить, что создание отклонено"):
                assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
                assert body["status"] == 0, (
                    f"невалидный email: ожидали status=0, получили {body}"
                )
                assert body.get("message"), f"ожидали message об ошибке, получили {body}"
        finally:
            if created_id:
                client.delete_student(created_id)

    @allure.issue(BUG_02, "BUG-02")
    @allure.title("Получить несуществующего студента")
    def test_get_student_not_found(self, client):
        with allure.step("Запросить несуществующего студента"):
            resp = client.get_student(99999999)
            body = resp.json()

        with allure.step("Проверить ответ not found"):
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert body["status"] == 0, f"ожидали status=0, получили {body}"
            assert "not found" in body["message"].lower(), (
                f"ожидали message с not found, получили {body.get('message')!r}"
            )

    @allure.title("Получить студента с невалидным id")
    def test_get_student_invalid_id(self, client):
        with allure.step("Запросить студента с id=abc"):
            resp = client.get_student("abc")

        with allure.step("Проверить, что нет 500 и ошибка в теле"):
            assert resp.status_code != 500, f"не ожидали 500, получили {resp.status_code}"
            if resp.headers.get("content-type", "").startswith("application/json"):
                body = resp.json()
                assert body["status"] == 0, f"ожидали status=0, получили {body}"

    @allure.title("Обновить несуществующего студента")
    def test_update_student_not_found(self, client):
        student_id = 99999999

        with allure.step("Убедиться, что студента нет"):
            get_resp = client.get_student(student_id)
            get_body = get_resp.json()
            assert get_resp.status_code == 200, f"ожидали 200, получили {get_resp.status_code}"
            assert get_body["status"] == 0, f"ожидали status=0, получили {get_body}"

        with allure.step("Попытаться обновить несуществующего студента"):
            payload = make_student_payload()
            payload.pop("phone_no")
            resp = client.update_student(student_id, payload)
            body = resp.json()

        with allure.step("Проверить, что обновление отклонено"):
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert body["status"] == 0, f"ожидали status=0, получили {body}"
            assert body.get("message"), f"ожидали message об ошибке, получили {body}"

    @allure.title("Обновить студента с неполным телом")
    def test_update_student_partial_body(self, client, student):
        with allure.step("Отправить неполное тело обновления"):
            resp = client.update_student(student["id"], {"name": "Only Name"})
            body = resp.json()

        with allure.step("Проверить, что обновление отклонено"):
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert body["status"] == 0, f"неполное тело: ожидали status=0, получили {body}"
            assert body.get("message"), f"ожидали message об ошибке, получили {body}"

    @allure.title("Обновить студента с phone_no в теле")
    def test_update_student_with_phone_no(self, client, student):
        old_phone = student["payload"]["phone_no"]
        old_gender = student["payload"]["gender"]

        with allure.step("Обновить студента, передав phone_no"):
            payload = make_student_payload(gender=old_gender, status=1)
            resp = client.update_student(student["id"], payload)
            body = resp.json()
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert body["status"] == 1, f"ожидали status=1, получили {body}"
            assert body["student"]["phone_no"] == old_phone, (
                f"phone_no в ответе PUT изменился: был {old_phone!r}, стал {body['student']['phone_no']!r}"
            )
            assert body["student"]["name"] == payload["name"], (
                f"name: ожидали {payload['name']!r}, получили {body['student']['name']!r}"
            )
            assert body["student"]["email"] == payload["email"], (
                f"email: ожидали {payload['email']!r}, получили {body['student']['email']!r}"
            )

        with allure.step("Проверить, что телефон не изменился"):
            after = client.get_student(student["id"]).json()["student"]
            assert after["phone_no"] == old_phone, (
                f"phone_no после GET изменился: был {old_phone!r}, стал {after['phone_no']!r}"
            )
            assert after["name"] == payload["name"], (
                f"name: ожидали {payload['name']!r}, получили {after['name']!r}"
            )
            assert after["gender"] == old_gender, (
                f"gender изменился: был {old_gender!r}, стал {after['gender']!r}"
            )

    @pytest.mark.parametrize(
        "field, value",
        [
            ("gender", "unknown"),
            ("status", 2),
        ],
    )
    def test_update_student_invalid_field(self, client, student, field, value):
        allure.dynamic.title(f"Обновить студента с невалидным {field}")
        with allure.step(f"Собрать payload с невалидным {field}"):
            payload = make_student_payload(**{field: value})
            payload.pop("phone_no")

        with allure.step("Отправить запрос на обновление"):
            resp = client.update_student(student["id"], payload)
            body = resp.json()

        with allure.step("Проверить, что обновление отклонено"):
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert body["status"] == 0, (
                f"невалидный {field}={value!r}: ожидали status=0, получили {body}"
            )

    @allure.issue(BUG_03, "BUG-03")
    @pytest.mark.xfail(reason="BUG-03: DELETE несуществующего возвращает success")
    @allure.title("Удалить несуществующего студента")
    def test_delete_student_not_found(self, client):
        student_id = 99999999

        with allure.step("Убедиться, что студента нет"):
            get_resp = client.get_student(student_id)
            get_body = get_resp.json()
            assert get_resp.status_code == 200, f"ожидали 200, получили {get_resp.status_code}"
            assert get_body["status"] == 0, f"ожидали status=0, получили {get_body}"

        with allure.step("Попытаться удалить несуществующего студента"):
            resp = client.delete_student(student_id)
            body = resp.json()

        with allure.step("Проверить, что удаление отклонено"):
            assert resp.status_code == 200, f"ожидали 200, получили {resp.status_code}"
            assert body["status"] == 0, (
                f"delete несуществующего: ожидали status=0, получили {body}"
            )
