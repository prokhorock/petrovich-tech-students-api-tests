import random
import uuid


def make_student_payload(**overrides):
    suffix = uuid.uuid4().hex[:10]
    payload = {
        "name": f"Student {suffix}",
        "email": f"student_{suffix}@test.com",
        "phone_no": f"+7{random.randint(9000000000, 9999999999)}",
        "gender": "male",
        "status": 1,
    }
    payload.update(overrides)
    return payload

