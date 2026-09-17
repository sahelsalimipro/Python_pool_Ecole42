def ft_count_harvest_recursive() -> None:
    days = int(input("Days until harvest: "))
    recursive(days)
    print("Harvest time!")


def recursive(current):
    if current > 1:
        recursive(current - 1)
    print(f"Day {current}")

# ft_count_harvest_recursive()
