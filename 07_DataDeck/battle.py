from ex0 import CreatureFactory, FlameFactory, AquaFactory


def test_factory(factory: CreatureFactory) -> None:
    """Check a factory can build base + evolved creatures and use them."""
    print("Testing factory")
    base = factory.create_base()
    evolved = factory.create_evolved()
    for creature in (base, evolved):
        print(creature.describe())
        print(creature.attack())


def battle(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    """Make the base creatures of two factories fight."""
    print("Testing battle")
    fighter1 = factory1.create_base()
    fighter2 = factory2.create_base()
    print(fighter1.describe())
    print("vs.")
    print(fighter2.describe())
    print("fight!")
    print(fighter1.attack())
    print(fighter2.attack())


def main() -> None:
    try:
        flame = FlameFactory()
        aqua = AquaFactory()
        test_factory(flame)
        print()
        test_factory(aqua)
        print()
        battle(flame, aqua)
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
