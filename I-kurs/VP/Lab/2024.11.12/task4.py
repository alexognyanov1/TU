import random


class Character:
    def __init__(self, name, health, attack_power, defense):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = defense

    def attack(self, target):
        damage = max(self.attack_power - target.defense, 1)
        target.take_damage(damage)
        print(f"{self.name} attacks {target.name} and deals {damage} damage!")

    def take_damage(self, amount):
        actual_damage = max(amount - self.defense, 0)
        self.health -= actual_damage
        print(
            f"{self.name} takes {actual_damage} damage! Remaining health: {self.health}")

    def is_alive(self):
        return self.health > 0


class Warrior(Character):
    def attack(self, target):
        if self.health < 20:
            damage = max(self.attack_power * 1.5 - target.defense, 1)
            print(f"{self.name} goes into a rage and deals {damage} damage!")
        else:
            damage = max(self.attack_power - target.defense, 1)
        target.take_damage(damage)
        print(f"{self.name} attacks {target.name} and deals {damage} damage!")


class Mage(Character):
    def attack(self, target):
        if random.random() < 0.3:
            damage = max(self.attack_power * 2 - target.defense, 1)
            print(f"{self.name} casts a powerful spell and deals {damage} damage!")
        else:
            damage = max(self.attack_power - target.defense, 1)
        target.take_damage(damage)
        print(f"{self.name} attacks {target.name} and deals {damage} damage!")


class Archer(Character):
    def attack(self, target):
        if random.random() < 0.2:
            damage = max(self.attack_power * 1.75 - target.defense, 1)
            print(f"{self.name} lands a critical hit and deals {damage} damage!")
        else:
            damage = max(self.attack_power - target.defense, 1)
        target.take_damage(damage)
        print(f"{self.name} attacks {target.name} and deals {damage} damage!")


class Enemy(Character):
    def attack(self, target):
        damage = max(self.attack_power - target.defense, 1)
        target.take_damage(damage)
        print(f"{self.name} attacks {target.name} and deals {damage} damage!")


def main():
    print("Welcome to Battle of the Realms!")
    name = input("Enter your character's name: ")
    print("Choose your class (Warrior, Mage, Archer): ")
    class_choice = input().capitalize()

    if class_choice == "Warrior":
        player = Warrior(name, 100, 15, 5)
    elif class_choice == "Mage":
        player = Mage(name, 80, 20, 3)
    elif class_choice == "Archer":
        player = Archer(name, 90, 18, 4)
    else:
        print("Invalid class choice. Defaulting to Warrior.")
        player = Warrior(name, 100, 15, 5)

    enemy = Enemy("Goblin", 50, 10, 2)
    print(f"A wild {enemy.name} appears!")

    while player.is_alive() and enemy.is_alive():
        action = input("Do you want to (A)ttack or (R)un? ").upper()
        if action == 'A':
            player.attack(enemy)
            if not enemy.is_alive():
                print(f"The {enemy.name} has been defeated! You win!")
                break

            enemy.attack(player)
            if not player.is_alive():
                print(f"{player.name} has been defeated! Game over.")
                break
        elif action == 'R':
            print("You run away from the battle!")
            break
        else:
            print("Invalid action. Choose 'A' to attack or 'R' to run.")


if __name__ == "__main__":
    main()
