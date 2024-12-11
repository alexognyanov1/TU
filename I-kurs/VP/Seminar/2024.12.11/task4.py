class Food:
    def __init__(self, carbs, protein, fat):
        self.carbs = carbs
        self.protein = protein
        self.fat = fat

    def calories(self):
        return (self.carbs * 4) + (self.protein * 4) + (self.fat * 9)


class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def calories(self):
        return sum(ingredient.calories() for ingredient in self.ingredients)

    def __str__(self):
        return self.name


def main():
    try:
        n = int(input("Enter the number of recipes (between 5 and 14): "))
        if n < 5 or n > 14:
            raise ValueError("Number of recipes must be between 5 and 14.")
    except ValueError as e:
        print(e)
        return

    recipes = []
    for i in range(n):
        name = input(f"Enter the name of recipe {i+1}: ")
        ingredients = []
        num_ingredients = int(
            input(f"Enter the number of ingredients for {name}: "))
        for j in range(num_ingredients):
            carbs = float(input(f"Enter carbs for ingredient {j+1}: "))
            protein = float(input(f"Enter protein for ingredient {j+1}: "))
            fat = float(input(f"Enter fat for ingredient {j+1}: "))
            ingredients.append(Food(carbs, protein, fat))
        recipes.append(Recipe(name, ingredients))

    for recipe in recipes:
        print(f"Recipe: {recipe}, Calories: {recipe.calories()}")


if __name__ == "__main__":
    main()
