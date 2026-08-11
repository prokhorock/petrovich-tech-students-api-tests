import time


def wait_student_readable(client, student_id, attempts=15, delay=0.3):
    for _ in range(attempts):
        resp = client.get_student(student_id)
        body = resp.json()
        if resp.status_code == 200 and body.get("status") == 1:
            return body
        time.sleep(delay)
    raise AssertionError(
        f"студент id={student_id} не стал читаемым после create"
    )


