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

    def show(self) -> None:
        print(
            f"Plant created: {self.name}: "
            f"{round(self._height, 1)}cm,"
            f"{self._age} days old")


if __name__ == "__main__":
    print("=== Garden Security System ===")
    plant_1 = Plant("Rose", 15.0, 10)
    plant_1.show()
    print()
    result = plant_1.set_height(25)
    if result:
        print("Height updated: 25cm")
    else:
        print("Height update rejected")

    result = plant_1.set_age(30)
    if result:
        print("Age updated: 30 days")
    else:
        print("Age update rejected")
    print()

    result = plant_1.set_height(-15)
    if result:
        print("Height updated: 25cm")
    else:
        print("Height update rejected")

    result = plant_1.set_age(-10)
    if result:
        print("Age updated: 30 days")
    else:
        print("Age update rejected")
    print()

    plant_1.show()
