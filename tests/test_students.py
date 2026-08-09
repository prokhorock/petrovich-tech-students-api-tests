import uuid


def test_create_student(client):
    payload = {
        "name": "Create Test",
        "email": f"create_{uuid.uuid4().hex}@test.com",
        "phone_no": "+79990001122",
        "gender": "male",
        "status": 1,
    }
    resp = client.create_student(payload)
    assert resp.status_code == 200

    student_id = resp.json()["student"]["id"]
    client.delete_student(student_id)


def test_get_student(client, student):
    resp = client.get_student(student)
    assert resp.status_code == 200
    assert resp.json()["student"]["id"] == student


def test_get_students_list(client):
    resp = client.get_students_list()
    assert resp.status_code == 200
    assert "students" in resp.json()


def test_update_student(client, student):
    payload = {
        "name": "Updated Name",
        "email": f"upd_{uuid.uuid4().hex}@test.com",
        "gender": "female",
        "status": 0,
    }
    resp = client.update_student(student, payload)
    assert resp.status_code == 200
    assert resp.json()["student"]["name"] == "Updated Name"


def test_delete_student(client):
    payload = {
        "name": "Delete Test",
        "email": f"del_{uuid.uuid4().hex}@test.com",
        "phone_no": "+79990001122",
        "gender": "male",
        "status": 1,
    }
    create_resp = client.create_student(payload)
    student_id = create_resp.json()["student"]["id"]

    resp = client.delete_student(student_id)
    assert resp.status_code == 200
