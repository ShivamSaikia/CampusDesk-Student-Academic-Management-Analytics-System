import unittest
from utils.validator import validate_student_id, validate_email, calculate_grade

class TestValidation(unittest.TestCase):
    def test_student_id(self):
        self.assertTrue(validate_student_id("STU001"))
        self.assertFalse(validate_student_id("ABC001"))

    def test_email(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertFalse(validate_email("bad-email"))

    def test_grade(self):
        self.assertEqual(calculate_grade(95), "A+")
        self.assertEqual(calculate_grade(75), "B")
        self.assertEqual(calculate_grade(35), "F")

if __name__ == "__main__":
    unittest.main()
