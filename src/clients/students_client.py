import requests
import allure
from src.config import BASE_URL


class StudentsClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = f"{BASE_URL}/student"

    @allure.step("Создать нового студента")
    def create_student(self, payload: dict) -> requests.Response:
        response = self.session.post(self.base_url, json=payload, timeout=10)
        return response

    @allure.step("Получить список студентов")
    def get_students_list(self) -> requests.Response:
        response = self.session.get(self.base_url, timeout=10)
        return response




