class Worker:
    def __init__(self, worker_num, fname, lname, work_experience_company, total_years_experience, salary, age):
        self.worker_num = worker_num
        self.fname = fname
        self.lname = lname
        self.work_experience_company = work_experience_company
        self.total_years_experience = total_years_experience
        self.salary = salary
        self.age = age

    def worker_information(self):
        return f"Worker Number: {self.worker_num}, Name: {self.fname} {self.lname}, Work Experience in Company: {self.work_experience_company} years, Total Work Experience: {self.total_years_experience} years, Salary: {self.salary}, Age: {self.age}"

    def salary_bonus(self):
        if self.work_experience_company < 5:
            bonus = 0.5
        elif 5 <= self.work_experience_company <= 10:
            bonus = 1.5
        else:
            bonus = 2.0
        return self.salary * (1 + bonus / 100)


def search_by_num(workers_list, worker_num):
    for worker in workers_list:
        if worker.worker_num == worker_num:
            return True
    return False


def search_by_name_experience(workers_list, fname, work_experience_company):
    result = []
    for worker in workers_list:
        if worker.fname == fname and worker.work_experience_company == work_experience_company:
            result.append(worker.worker_information())
    return result


def add_worker(workers_list, worker):
    workers_list.append(worker)


def remove_worker(workers_list, worker_num):
    for worker in workers_list:
        if worker.worker_num == worker_num:
            workers_list.remove(worker)
            print("Information deleted !!!")
            return
    print("Wrong worker_num!!!")


def main():
    workers_list = []
    worker1 = Worker(1, "John", "Doe", 6, 10, 50000, 30)
    worker2 = Worker(2, "Jane", "Smith", 3, 5, 45000, 28)
    add_worker(workers_list, worker1)
    add_worker(workers_list, worker2)
    print(search_by_num(workers_list, 1))
    print(search_by_name_experience(workers_list, "John", 6))
    remove_worker(workers_list, 1)
    print(search_by_num(workers_list, 1))


if __name__ == "__main__":
    main()
