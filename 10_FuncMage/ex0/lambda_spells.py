def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    """Sort artifacts by power, strongest first."""
    return sorted(artifacts, key=lambda a: a['power'], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    """Keep only mages whose power is >= min_power."""
    return list(filter(lambda m: m['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    """Wrap every spell name with '* ' and ' *'."""
    return list(map(lambda s: f"* {s} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    """Return max, min and average power of the mages."""
    if not mages:
        return {'max_power': 0, 'min_power': 0, 'avg_power': 0.0}
    return {
        'max_power': max(mages, key=lambda m: m['power'])['power'],
        'min_power': min(mages, key=lambda m: m['power'])['power'],
        'avg_power': round(
            sum(map(lambda m: m['power'], mages)) / len(mages), 2
        ),
    }


def main() -> None:
    artifacts = [
        {'name': 'Crystal Orb', 'power': 85, 'type': 'orb'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'staff'},
        {'name': 'Shadow Ring', 'power': 47, 'type': 'ring'},
    ]
    mages = [
        {'name': 'Alex', 'power': 78, 'element': 'fire'},
        {'name': 'Jordan', 'power': 55, 'element': 'water'},
        {'name': 'Riley', 'power': 91, 'element': 'earth'},
        {'name': 'Sam', 'power': 34, 'element': 'air'},
    ]
    spells = ['fireball', 'heal', 'shield']

    print("Testing artifact sorter...")
    ordered = artifact_sorter(artifacts)
    print(f"{ordered[0]['name']} ({ordered[0]['power']} power) comes before "
          f"{ordered[1]['name']} ({ordered[1]['power']} power)")

    print("\nTesting power filter...")
    strong = power_filter(mages, 50)
    print("Mages with power >= 50:",
          ', '.join(map(lambda m: m['name'], strong)))

    print("\nTesting spell transformer...")
    print(' '.join(spell_transformer(spells)))

    print("\nTesting mage stats...")
    print(mage_stats(mages))


if __name__ == "__main__":
    main()
