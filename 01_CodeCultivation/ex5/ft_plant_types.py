class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self._height = 0.0
        self._age = 0

        self.set_height(height)
        self.set_age(age)

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age

    def set_height(self, height: float) -> bool:
        if height < 0:
            print(f"{self.name}: Error, height can't be negative")
            return False
        else:
            self._height = height
            return True

    def set_age(self, age: int) -> bool:
        if age < 0:
            print(f"{self.name}: Error, age can't be negative")
            return False
        else:
            self._age = age
            return True

    def grow(self, day):
        self._height += (2.1 * day)

    def age(self, day):
        self._age += day

    def show(self) -> None:
        print(
            f"{self.name}: {round(self._height, 1)}cm,", end=" ")
        print(f"{self._age} days old")


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str):
        super().__init__(name, height, age)
        self.color = color
        self.bloomed = False

    def show(self):
        super().show()
        print(f"Color: {self.color}")
        if self.bloomed is False:
            print(f"{self.name} has not bloomed yet")
        else:
            print(f"{self.name} is blooming beautifully!")

    def bloom(self):
        self.bloomed = True


class Tree(Plant):
    def __init__(self, name: str, height: float, age: int, trunk: float):
        super().__init__(name, height, age)
        self.trunk = trunk

    def show(self):
        super().show()
        print(f"Trunk diameter: {self.trunk}cm")

    def produce_shade(self):
        print(
            f"Tree {self.name} now produces a shade of ", end=" ")
        print(f"{round(self._height, 1)}cm long", end=" ")
        print(f"and {round(self.trunk, 1)}cm wide.")


class Vegetable(Plant):
    def __init__(self, name: str, height: float, age: int, Harvest: str):
        super().__init__(name, height, age)
        self.Harvest = Harvest
        self.Nutritional = 0

    def show(self):
        super().show()
        print(f"Harvest season: {self.Harvest}")
        print(f"Nutritional value: {self.Nutritional}")

    def grow(self, day):
        super().grow(day)
        self.Nutritional += day


if __name__ == "__main__":
    print("=== Garden Plant Types ===")
    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "Red")
    rose.show()
    rose.bloom()
    print("[asking the Rose to bloom]")
    rose.show()

    print()
    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print("[asking the Oak to produce shade]")
    oak.produce_shade()

    print()
    print("=== Vegetable")
    tomato = Vegetable("Tomato", 5.0, 10, "April")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    tomato.age(20)
    tomato.grow(20)
    tomato.show()
