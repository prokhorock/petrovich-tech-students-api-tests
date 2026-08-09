import requests
import allure
from src.config import BASE_URL
from src.utils.allure_logger import attach_http_log


class StudentsClient:
    def __init__(self, timeout: int = 10):
        self.session = requests.Session()
        self.base_url = f"{BASE_URL}/student"
        self.timeout = timeout

    @allure.step("Создать нового студента")
    def create_student(self, payload: dict) -> requests.Response:
        response = self.session.post(self.base_url, json=payload, timeout=self.timeout)
        attach_http_log(response)
        return response

    @allure.step("Получить список студентов")
    def get_students_list(self) -> requests.Response:
        response = self.session.get(self.base_url, timeout=self.timeout)
        attach_http_log(response)
        return response

    @allure.step("Получить студента по ID")
    def get_student(self, student_id) -> requests.Response:
        response = self.session.get(f"{self.base_url}/{student_id}", timeout=self.timeout)
        attach_http_log(response)
        return response

    @allure.step("Обновить данные студента")
    def update_student(self, student_id, payload: dict) -> requests.Response:
        response = self.session.put(f"{self.base_url}/{student_id}", json=payload, timeout=self.timeout)
        attach_http_log(response)
        return response

    @allure.step("Удалить студента")
    def delete_student(self, student_id) -> requests.Response:
        response = self.session.delete(f"{self.base_url}/{student_id}", timeout=self.timeout)
        attach_http_log(response)
        return response




