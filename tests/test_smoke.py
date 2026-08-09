from src.clients.students_client import StudentsClient


def test_smoke_client_check():
    client = StudentsClient()
    response = client.get_students_list()
    print("Данные от сервера:", response.text)
    assert response.status_code == 200, f"Сервер вернул ошибку: {response.status_code}"





