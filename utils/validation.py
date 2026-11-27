import re

def validate_student_id(student_id: str) -> bool:
    """Accept formats like 2026-001, 2026001, or any non-empty alphanumeric ID."""
    if not student_id or not student_id.strip():
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9\-]+", student_id.strip()))

def validate_course_code(code: str) -> bool:
    """Accept e.g. CS101, IT-201, MATH101."""
    if not code or not code.strip():
        return False
    return bool(re.fullmatch(r"[A-Za-z]{2,5}[-]?\d{3,4}", code.strip().upper()))

def validate_name(name: str) -> bool:
    return bool(name and name.strip() and len(name.strip()) >= 2)

def validate_capacity(capacity) -> bool:
    try:
        return int(capacity) > 0
    except (TypeError, ValueError):
        return False
