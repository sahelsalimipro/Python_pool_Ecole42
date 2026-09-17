#!/usr/bin/env python3

def input_temperature(temp_str: str) -> int:
    temp_int = int(temp_str)

    if temp_int < 0:
        raise ValueError(f"{temp_int}°C is too cold for plants (min 0°C)")
    if temp_int > 40:
        raise ValueError(f"{temp_int}°C is too hot for plants (max 40°C)")
    return temp_int


def test_temperature() -> None:
    tests = ["25", "abc", "100", "-50"]

    for value in tests:
        print(f"Input data is {value}")
        try:
            temp = input_temperature(value)
            print(f"Temperature is now {temp}°C\n")
        except ValueError as error:
            print(f"Caught input_temperature error: {error}\n")


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===\n")
    test_temperature()
    print("\nAll tests completed - program didn’t crash!")
