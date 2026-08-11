def assert_student_types(student):
    assert isinstance(student["id"], int)
    assert isinstance(student["name"], str)
    assert isinstance(student["email"], str)
    assert isinstance(student["phone_no"], str)
    assert student["gender"] in ("male", "female")
    assert isinstance(student["status"], int)
    assert student["status"] in (0, 1)
