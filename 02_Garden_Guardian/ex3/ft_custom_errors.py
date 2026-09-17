#!/usr/bin/env python3

class GardenError(Exception):
    def __init__(self, message="Unknown garden error"):
        self.message = message
        super().__init__(self.message)


class PlantError(GardenError):
    def __init__(self, message="Unknown plant error"):
        self.message = message
        super().__init__(self.message)


class WaterError(GardenError):
    def __init__(self, message="Unknown water error"):
        self.message = message
        super().__init__(self.message)


def check_plant(plant_name: str):
    if plant_name == "tomato":
        raise PlantError("The tomato plant is wilting!")


def check_water(water: int):
    if water <= 0:
        raise WaterError("Not enough water in the tank!")


def ft_custom_error() -> None:
    print("Testing PlantError...")
    try:
        check_plant("tomato")
    except PlantError as error:
        print(f"Caught PlantError: {error}")

    print()
    print("Testing WaterError...")
    try:
        check_water(0)
    except WaterError as error:
        print(f"Caught WaterError: {error}")

    print("\nTesting catching all garden errors...")
    try:
        check_plant("tomato")
    except GardenError as error:
        print(f"Caught GardenError: {error}")
    try:
        check_water(0)
    except GardenError as error:
        print(f"Caught GardenError: {error}")


if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===")
    print()
    ft_custom_error()
    print("\nAll custom error types work correctly!")
