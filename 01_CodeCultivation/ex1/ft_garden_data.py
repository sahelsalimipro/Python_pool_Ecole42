#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self.height = height
        self.age = age

    def show(self):
        print(f"{self.name}:  {self.height}cm, {self.age} days old")


if __name__ == "__main__":
    print("=== Garden Plant Registry ===")
    plant_1 = Plant("Rose", 25, 30)
    plant_1.show()
    plant_2 = Plant("Sunflower", 80, 45)
    plant_2.show()
    plant_3 = Plant("Cactus", 15, 120)
    plant_3.show()
