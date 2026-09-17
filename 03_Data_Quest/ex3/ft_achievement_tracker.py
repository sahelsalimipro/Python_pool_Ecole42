import random


ALL_ACHIEVEMENTS: list[str] = [
    "Crafting Genius",
    "World Savior",
    "Master Explorer",
    "Collector Supreme",
    "Untouchable",
    "Boss Slayer",
    "Strategist",
    "Speed Runner",
    "Survivor",
    "Treasure Hunter",
    "First Steps",
    "Sharp Mind",
    "Unstoppable",
    "Hidden Path Finder",
]


def gen_player_achievements() -> set[str]:
    count: int = random.randint(3, 9)
    achievements: list[str] = random.sample(ALL_ACHIEVEMENTS, count)
    return set(achievements)


def main() -> None:
    players: dict[str, set[str]] = {
        "Alice": gen_player_achievements(),
        "Bob": gen_player_achievements(),
        "Charlie": gen_player_achievements(),
        "Dylan": gen_player_achievements(),
    }
    for name, achievements in players.items():
        print(f"player {name}: {achievements}")

    all: set[str] = set()
    for value in players.values():
        all = all.union(value)
    print(f"All distinct achievements: {all}")

    common: set[str] = players["Alice"]
    for value in players.values():
        common = common.intersection(value)
    print(f"Common achievements: {common}\n")

    for name, achieve in players.items():
        others: set[str] = set()
        for other_name, other_achieve in players.items():
            if other_name != name:
                others = others.union(other_achieve)
        result: set[str] = achieve.difference(others)
        print(f"Only {name} has: {result}")

    for name, a in players.items():
        miss: set[str] = set(ALL_ACHIEVEMENTS).difference(a)
        print(f"{name} is missing: {miss}")


if __name__ == "__main__":
    print("=== Achievement Tracker System ===")
    main()
