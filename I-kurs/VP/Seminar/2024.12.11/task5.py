class Employee:
    def __init__(self, name, position, salary):
        self.name = name
        self.position = position
        self.salary = salary

    def display_info(self):
        return f"Name: {self.name}, Position: {self.position}, Salary: {self.salary}"


class Manager(Employee):
    def __init__(self, name, position, salary, department):
        super().__init__(name, position, salary)
        self.department = department

    def calculate_bonus(self):
        return self.salary * 0.10 + 1000

    def display_info(self):
        return f"{super().display_info()}, Department: {self.department}"


class Developer(Employee):
    def __init__(self, name, position, salary, programming_languages):
        super().__init__(name, position, salary)
        self.programming_languages = programming_languages

    def calculate_bonus(self):
        return self.salary * 0.15 + 200 * len(self.programming_languages)

    def display_info(self):
        languages = ", ".join(self.programming_languages)
        return f"{super().display_info()}, Programming Languages: {languages}"


class Company:
    def __init__(self):
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def total_salary_expense(self):
        return sum(employee.salary for employee in self.employees)

    def display_all_employees(self):
        for employee in self.employees:
            print(employee.display_info())


if __name__ == "__main__":
    company = Company()

    manager = Manager("Alice", "Manager", 5000, "IT")
    developer = Developer("Bob", "Developer", 4000, ["Python", "JavaScript"])

    company.add_employee(manager)
    company.add_employee(developer)

    company.display_all_employees()
    print(f"Total Salary Expense: {company.total_salary_expense()}")
