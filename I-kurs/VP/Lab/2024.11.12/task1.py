class Person:
    def __init__(self, first_name, last_name, age, nationality):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.nationality = nationality

    def print(self):
        print(f'{self.first_name} {self.last_name}, {self.nationality}')


person1 = Person('Иван', 'Иванов', 30, 'Българин')
person2 = Person('Мария', 'Петрова', 25, 'Българка')

person1.print()
person2.print()
