from ex0 import CreatureFactory, FlameFactory, AquaFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
)


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    """Make every opponent fight every other opponent exactly once.

    This function knows nothing about heal/transform: each fight is
    driven entirely by the strategy attached to each opponent.
    """
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    try:
        for i in range(len(opponents)):
            for j in range(i + 1, len(opponents)):
                factory1, strategy1 = opponents[i]
                factory2, strategy2 = opponents[j]
                fighter1 = factory1.create_base()
                fighter2 = factory2.create_base()
                print("\n* Battle *")
                print(fighter1.describe())
                print("vs.")
                print(fighter2.describe())
                print("now fight!")
                strategy1.act(fighter1)
                strategy2.act(fighter2)
    except InvalidStrategyError as error:
        print(f"Battle error, aborting tournament: {error}")


def strategy_name(strategy: BattleStrategy) -> str:
    return type(strategy).__name__.replace("Strategy", "")


def run_tournament(
    title: str,
    entries: list[tuple[str, CreatureFactory, BattleStrategy]],
) -> None:
    """Print the tournament header (using labels), then run it."""
    labels = ", ".join(
        f"({label}+{strategy_name(strategy)})"
        for label, _, strategy in entries
    )
    print(title)
    print(f"[ {labels} ]")
    battle([(factory, strategy) for _, factory, strategy in entries])


def main() -> None:
    try:
        flame = FlameFactory()
        aqua = AquaFactory()
        healing = HealingCreatureFactory()
        transform = TransformCreatureFactory()

        normal = NormalStrategy()
        aggressive = AggressiveStrategy()
        defensive = DefensiveStrategy()

        run_tournament("Tournament 0 (basic)", [
            ("Flameling", flame, normal),
            ("Healing", healing, defensive),
        ])
        print()
        run_tournament("Tournament 1 (error)", [
            ("Flameling", flame, aggressive),
            ("Healing", healing, defensive),
        ])
        print()
        run_tournament("Tournament 2 (multiple)", [
            ("Aquabub", aqua, normal),
            ("Healing", healing, defensive),
            ("Transform", transform, aggressive),
        ])
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
