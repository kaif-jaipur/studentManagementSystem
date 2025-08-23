# student.py
class student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def display(self):
        print(f"name:{self.name},age:{self.age}")
    def __eq__(self, other):
        if not isinstance(other, student):
            return False
        return self.name == other.name and self.age == other.age