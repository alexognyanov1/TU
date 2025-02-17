# Description: This script defines a `Car` class to represent car information (brand, model, price, color, year) and provides functions to sort cars by price, list cars by brand, search cars by color, and find the newest cars.  The main function demonstrates the usage of these functions with a sample list of cars.
# Tags: Car Inventory, Data Management, Object-Oriented Programming, Sorting, Searching

class Car:
    def __init__(self, car_brand, car_model, car_price, car_color, manifacture_year):
        self.car_brand = car_brand
        self.car_model = car_model
        self.car_price = car_price
        self.car_color = car_color
        self.manifacture_year = manifacture_year

    def display_info(self):
        print(f"Brand: {self.car_brand}\nModel: {self.car_model}\nPrice: {self.car_price}\nColor: {self.car_color}\nYear: {self.manifacture_year}\n")


def sort_price(cars):
    cars.sort(key=lambda x: x.car_price)
    return cars


def list_by_brand(cars, brand):
    c = []

    for car in cars:
        if car.car_brand == brand:
            c.append(car)

    for car in c:
        car.display_info()


def search_color(cars, color):
    c = []

    for car in cars:
        if car.car_color == color:
            c.append(car)

    c = sort_price(c)

    for car in c:
        car.display_info()


def newest_car(cars):
    c = []

    for car in cars:
        if car.manifacture_year == 2022:
            c.append(car)

    return c


def main():
    cars = [Car("Toyota", "Corolla", 20000, "Black", 2015),
            Car("BMW", "X5", 50000, "White", 2018),
            Car("Audi", "A6", 35000, "Red", 2016),
            Car("Mercedes", "E-class", 45000, "Black", 2017),
            Car("Ford", "Focus", 15000, "Blue", 2014),
            Car("Volkswagen", "Passat", 25000, "Silver", 2015),
            Car("Nissan", "Qashqai", 18000, "Green", 2016)]

    sorted_cars = sort_price(cars)
    for car in sorted_cars:
        car.display_info()

    print()
    print()

    list_by_brand(cars, "Toyota")
    print()
    print()

    search_color(cars, "Black")
    print()
    print()

    print(newest_car(cars))


if __name__ == "__main__":
    main()