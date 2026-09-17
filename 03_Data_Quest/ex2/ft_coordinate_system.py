import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        text = input("Enter new coordinates as floats in format 'x,y,z': ")
        parts = text.split(',')
        if len(parts) != 3:
            print("Invalid syntax")
            continue
        try:
            x: float = float(parts[0].strip())
            y: float = float(parts[1].strip())
            z: float = float(parts[2].strip())
            return (x, y, z)
        except ValueError as e:
            print(f"Error on parameter: {e}")


def main() -> None:
    print("\nGet a first set of coordinates")
    pos1 = get_player_pos()
    print(f"Got a first tuple: {pos1}")
    print(f"It includes: x={pos1[0]}, y={pos1[1]}, z={pos1[2]}")
    distance: float = math.sqrt(pos1[0]**2 + pos1[1]**2+pos1[2]**2)
    print(f"Distance to center: {round(distance, 4)}")

    print("\nGet a second set of coordinates")
    pos2 = get_player_pos()
    distance = math.sqrt(
        (pos2[0]-pos1[0])**2
        + (pos2[1]-pos1[1])**2
        + (pos2[2]-pos1[2])**2
    )
    print(f"Distance between the 2 sets of coordinates: {round(distance, 4)}")


if __name__ == "__main__":
    print("=== Game Coordinate System ===")
    main()
