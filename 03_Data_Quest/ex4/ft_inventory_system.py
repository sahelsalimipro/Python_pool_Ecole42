import sys


def parse_inventory(args: list[str]) -> dict[str, int]:
    inventory: dict[str, int] = {}

    for arg in args:
        parts = arg.split(":")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            print(f"Error - invalid parameter '{arg}'")
            continue
        # tuple/list unpacking
        item_name, quantity_str = parts
        # item_name = parts[0]
        # quantity_str = parts[1]
        if item_name in inventory:
            print(f"Redundant item '{item_name}' - discarding")
            continue
        try:
            quantity = int(quantity_str)
        except ValueError as e:
            print(f"Quantity error for '{item_name}': {e}")
            continue
        # This line is a dict assignment —
        # since item_name isn't already a key
        inventory[item_name] = quantity
    return inventory


def show_inventory_stats(inventory: dict[str, int]) -> None:
    items = list(inventory.keys())
    total = sum(inventory.values())
    print(f"Item list: {items}")
    print(f"Total quantity of the {len(items)} items: {total}")

    for i in items:
        percentage = round(inventory[i]/total * 100, 1)
        print(f"Item {i} represents {percentage}%")

    most_name = items[0]
    least_name = items[0]

    for name in items:
        if inventory[name] > inventory[most_name]:
            most_name = name
        if inventory[name] < inventory[least_name]:
            least_name = name
    print(f"Item most abundant: {most_name} with quantity "
          f"{inventory[most_name]}")
    print(f"Item least abundant: {least_name} with quantity "
          f"{inventory[least_name]}")


def main() -> None:
    print("=== Inventory System Analysis ===")
    inventory = parse_inventory(sys.argv[1:])
    print(f"Got inventory: {inventory}")
    if not inventory:
        print("No valid items in inventory.")
        return
    show_inventory_stats(inventory)
    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
