from ex0 import CreatureFactory
from ex1 import (
    HealCapability,
    TransformCapability,
    HealingCreatureFactory,
    TransformCreatureFactory,
)


def test_healing(factory: CreatureFactory) -> None:
    # """Describe, attack, then heal with the base and evolved creature."""
    print("Testing Creature with healing capability")
    for label, creature in (
        ("base:", factory.create_base()),
        ("evolved:", factory.create_evolved()),
    ):
        print(label)
        print(creature.describe())
        print(creature.attack())
        # create_*() is typed as Creature, so we must check the capability
        if isinstance(creature, HealCapability):
            print(creature.heal())
        else:
            print(f"{creature.name} cannot heal")


def test_transform(factory: CreatureFactory) -> None:
    # """Describe, attack, transform, attack again, then revert."""
    print("Testing Creature with transform capability")
    for label, creature in (
        ("base:", factory.create_base()),
        ("evolved:", factory.create_evolved()),
    ):
        print(label)
        print(creature.describe())
        print(creature.attack())
        if isinstance(creature, TransformCapability):
            print(creature.transform())
            print(creature.attack())
            print(creature.revert())
        else:
            print(f"{creature.name} cannot transform")


def main() -> None:
    try:
        test_healing(HealingCreatureFactory())
        print()
        test_transform(TransformCreatureFactory())
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
