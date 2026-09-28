from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @abstractmethod
    def role(self):
        pass

class Admin(User):
    def role(self):
        return "Administrator"

class Teacher(User):
    def role(self):
        return "Teacher"
