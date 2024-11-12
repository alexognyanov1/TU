# Description: This script defines two classes, Person and Student, where Student inherits from Person. It initializes instances of both classes and uses the print methods to display information about them.
# Tags: Object-Oriented Programming, Inheritance, Class Definition

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


student1 = Student('Георги', 'Георгиев', 20,
                   'Българин', 'Софийски университет', 2)
student1.print()
