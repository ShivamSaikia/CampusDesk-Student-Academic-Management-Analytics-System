class Student:
    def __init__(self, student_id, name, email, course, semester, phone=""):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.course = course
        self.semester = semester
        self.phone = phone

    def __str__(self):
        return f"{self.student_id} - {self.name}"

    def to_dict(self):
        return self.__dict__.copy()
