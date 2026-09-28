import re

EMAIL_RE = r"^[\w\.-]+@[\w\.-]+\.\w+$"
PHONE_RE = r"^[6-9]\d{9}$"
STUDENT_RE = r"^STU\d{3}$"

def validate_student_id(value):
    return bool(re.fullmatch(STUDENT_RE, value.strip().upper()))

def validate_email(value):
    return bool(re.fullmatch(EMAIL_RE, value.strip()))

def validate_phone(value):
    return not value.strip() or bool(re.fullmatch(PHONE_RE, value.strip()))

def validate_marks(*values):
    try:
        nums = [float(v) for v in values]
        return all(0 <= n <= 100 for n in nums)
    except ValueError:
        return False

def calculate_grade(total):
    if total >= 90:
        return "A+"
    if total >= 80:
        return "A"
    if total >= 70:
        return "B"
    if total >= 60:
        return "C"
    if total >= 50:
        return "D"
    if total >= 40:
        return "E"
    return "F"
