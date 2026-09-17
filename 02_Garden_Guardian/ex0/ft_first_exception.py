#!/usr/bin/env python3

def input_temperature(temp_str: str) -> int:
    temp = int(temp_str)
    return (temp)


def test_temperature() -> None:
    valid_input = "25"
    print(f"Input data is {valid_input}")
    temp = input_temperature(valid_input)
    print(f"Temperature is now {temp}°C")
    print()
    invalid_input = "abc"
    print(f"Input data is {invalid_input}")
    try:
        temp = input_temperature(invalid_input)
    except Exception as error:
        print(
            f"Caught input_temperature error: {error}")


if __name__ == "__main__":
    print("=== Garden Temperature ===")
    test_temperature()
    print("\nAll tests completed - program didn’t crash!")
