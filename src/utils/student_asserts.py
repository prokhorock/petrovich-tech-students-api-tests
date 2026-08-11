def assert_student_types(student):
    assert isinstance(student["id"], int), f"id должен быть int, пришло {student.get('id')!r}"
    assert isinstance(student["name"], str), f"name должен быть str, пришло {student.get('name')!r}"
    assert isinstance(student["email"], str), f"email должен быть str, пришло {student.get('email')!r}"
    assert isinstance(student["phone_no"], str), (
        f"phone_no должен быть str, пришло {student.get('phone_no')!r}"
    )
    assert student["gender"] in ("male", "female"), (
        f"gender должен быть male/female, пришло {student.get('gender')!r}"
    )
    assert isinstance(student["status"], int), (
        f"status должен быть int, пришло {student.get('status')!r} ({type(student.get('status')).__name__})"
    )
    assert student["status"] in (0, 1), f"status должен быть 0 или 1, пришло {student.get('status')!r}"
