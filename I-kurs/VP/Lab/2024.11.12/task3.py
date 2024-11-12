# Description: This script defines classes for Person, Student, and Lecturer, inheriting from Person. It creates an instance of the Lecturer class and prints its information.
# Tags: Object-Oriented Programming, Inheritance, Class Definition, Instance Creation

class Person:
    def __init__(self, first_name, last_name, age, nationality):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.nationality = nationality

    def print(self):
        print(f'{self.first_name} {self.last_name}, {self.nationality}')


class Student(Person):
    def __init__(self, first_name, last_name, age, nationality, university, year):
        super().__init__(first_name, last_name, age, nationality)
        self.university = university
        self.year = year

    def print(self):
        print(f'{self.first_name} {self.last_name}, {self.nationality}, {self.university}, Year: {self.year}')


class Lecturer(Person):
    def __init__(self, first_name, last_name, age, nationality, university, experience):
        super().__init__(first_name, last_name, age, nationality)
        self.university = university
        self.experience = experience

    def print(self):
        print(f'{self.first_name} {self.last_name}, {self.nationality}, {self.university}, Experience: {self.experience} years')


lecturer1 = Lecturer('Иван', 'Иванов', 30, 'Българин',
                     'Софийски университет', 5)
lecturer1.print()
