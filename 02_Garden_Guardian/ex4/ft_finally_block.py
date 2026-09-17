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
    if plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"watering {plant_name}:  [OK]")


def ft_finally_block() -> None:
    print("Testing valid plants...")
    print("Opening watering system")
    try:
        check_plant("Tomato")
        check_plant("Lettuce")
        check_plant("Carrots")

    except PlantError as error:
        print(f"Caught PlantError: {error}")
    finally:
        print("Closing watering system")

    print()
    print("Testing invalid plants...")
    print("Opening watering system")
    try:
        check_plant("Tomato")
        check_plant("lettuce")
        check_plant("carrots")
        print(".. ending tests and returning to main")
    except PlantError as error:
        print(f"Caught PlantError: {error}")
    finally:
        print("Closing watering system")


if __name__ == "__main__":
    print("=== Garden Watering System ===")
    print()
    ft_finally_block()
    print("\nCleanup always happens, even with errors!")
