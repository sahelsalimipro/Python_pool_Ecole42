#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int):
        self.name = name
        self.height = height
        self.age = age

    def show(self):
        print(f"{self.name}:  {round(self.height, 1)}cm, {self.age} days old")

    def grow(self):
        self.height += 0.8

    def ages(self):
        self.age += 1


if __name__ == "__main__":
    print("=== Garden Plant Growth ===")
    plant_1 = Plant("Rose", 25.0, 30)
    plant_1.show()

    start_height = plant_1.height

    for days in range(1, 8):
        print(f"=== Day {days} ===")
        plant_1.grow()
        plant_1.ages()
        plant_1.show()

    growth = plant_1.height - start_height

    print(f"Growth this week: {round(growth, 1)}cm")
