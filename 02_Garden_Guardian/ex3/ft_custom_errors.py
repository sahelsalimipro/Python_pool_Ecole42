#!/usr/bin/env python3

class plant:
    def __init__(self, name: str, height: float, age: int):
        self.name = name
        self.height = height
        self.age = age

    def show(self):
        print(
            f"Created: {self.name}: {round(self.height, 1)}cm, "
            f"{self.age} days old"
        )


if __name__ == "__main__":
    print("=== Plant Factory Output ===")
    plant_1 = plant("Rose", 25.0, 30)
    plant_2 = plant("Oak", 200.0, 365)
    plant_3 = plant("Cactus", 5.0, 90)
    plant_4 = plant("Sunflower", 280.0, 45)
    plant_5 = plant("Fern", 15.0, 120)
    plants = [plant_1, plant_2, plant_3, plant_4, plant_5]

    for p in plants:
        p.show()
