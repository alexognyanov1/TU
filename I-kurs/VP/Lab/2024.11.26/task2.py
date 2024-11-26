# Description: This script simulates a zoo, allowing users to add, remove, transfer, and list animals in different enclosures.  It uses object-oriented programming to represent animals (Mammals, Birds, Reptiles) and their attributes, and the zoo itself as a container for enclosures and animals.  The script demonstrates basic zoo management functionalities.
# Tags: Zoo Simulation, Object-Oriented Programming, Animal Management, Enclosure Management

class Animal:
    def __init__(self, name, species, age, health):
        self.name = name
        self.species = species
        self.age = age
        self.health = health

    def print_info(self):
        print(
            f"Name: {self.name}, Species: {self.species}, Age: {self.age}, Health: {self.health}")


class Mammal(Animal):
    def __init__(self, name, species, age, health, fur_color, diet):
        super().__init__(name, species, age, health)
        self.fur_color = fur_color
        self.diet = diet

    def print_info(self):
        super().print_info()
        print(f"Fur Color: {self.fur_color}, Diet: {self.diet}")


class Bird(Animal):
    def __init__(self, name, species, age, health, wing_span, can_fly):
        super().__init__(name, species, age, health)
        self.wing_span = wing_span
        self.can_fly = can_fly

    def print_info(self):
        super().print_info()
        print(
            f"Wing Span: {self.wing_span} cm, Can Fly: {'Yes' if self.can_fly else 'No'}")


class Reptile(Animal):
    def __init__(self, name, species, age, health, is_venomous, preferred_temperature):
        super().__init__(name, species, age, health)
        self.is_venomous = is_venomous
        self.preferred_temperature = preferred_temperature

    def print_info(self):
        super().print_info()
        print(
            f"Venomous: {'Yes' if self.is_venomous else 'No'}, Preferred Temperature: {self.preferred_temperature}°C")


class Zoo:
    def __init__(self):
        self.enclosures = {}

    def add_animal(self, animal, enclosure_number):
        if enclosure_number not in self.enclosures:
            self.enclosures[enclosure_number] = []
        self.enclosures[enclosure_number].append(animal)

    def remove_animal(self, name):
        for enclosure in self.enclosures.values():
            for animal in enclosure:
                if animal.name == name:
                    enclosure.remove(animal)
                    return

    def list_animals_in_enclosure(self, enclosure_number):
        if enclosure_number in self.enclosures:
            for animal in self.enclosures[enclosure_number]:
                animal.print_info()

    def transfer_animal(self, name, from_enclosure, to_enclosure):
        if from_enclosure in self.enclosures:
            for animal in self.enclosures[from_enclosure]:
                if animal.name == name:
                    self.enclosures[from_enclosure].remove(animal)
                    self.add_animal(animal, to_enclosure)
                    return

    def find_animals_by_species(self, species):
        for enclosure in self.enclosures.values():
            for animal in enclosure:
                if animal.species == species:
                    animal.print_info()


if __name__ == "__main__":
    zoo = Zoo()

    lion = Mammal("Simba", "Lion", 5, "Healthy", "Golden", "Carnivore")
    eagle = Bird("Eagle Eye", "Eagle", 3, "Healthy", 200, True)
    snake = Reptile("Slither", "Snake", 2, "Healthy", True, 30)

    zoo.add_animal(lion, 1)
    zoo.add_animal(eagle, 2)
    zoo.add_animal(snake, 3)

    print("Animals in enclosure 1:")
    zoo.list_animals_in_enclosure(1)
    print("\nAnimals in enclosure 2:")
    zoo.list_animals_in_enclosure(2)
    print("\nAnimals in enclosure 3:")
    zoo.list_animals_in_enclosure(3)

    print("\nTransferring Simba from enclosure 1 to enclosure 2")
    zoo.transfer_animal("Simba", 1, 2)
    print("\nAnimals in enclosure 1 after transfer:")
    zoo.list_animals_in_enclosure(1)
    print("\nAnimals in enclosure 2 after transfer:")
    zoo.list_animals_in_enclosure(2)

    print("\nFinding all Eagles in the zoo:")
    zoo.find_animals_by_species("Eagle")

    print("\nRemoving Slither from the zoo")
    zoo.remove_animal("Slither")
    print("\nAnimals in enclosure 3 after removal:")
    zoo.list_animals_in_enclosure(3)