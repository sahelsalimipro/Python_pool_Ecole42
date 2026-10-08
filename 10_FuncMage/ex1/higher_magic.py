from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    """Return a spell that casts both spells and returns both results."""
    def combined(target: str, power: int) -> tuple[str, str]:
        return spell1(target, power), spell2(target, power)
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    """Return a spell whose power is multiplied before casting."""
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    """Return a spell that is only cast when condition is True."""
    def caster(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return caster


def spell_sequence(spells: list[Callable]) -> Callable:
    """Return a spell that casts every spell in order."""
    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells if callable(spell)]
    return sequence


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} damage"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def shield(target: str, power: int) -> str:
    return f"Shield protects {target} with {power} armor"


def main() -> None:
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    print("Combined spell result:", ', '.join(combined("Dragon", 10)))

    print("\nTesting power amplifier...")
    mega_fireball = power_amplifier(fireball, 3)
    print("Original:", fireball("Dragon", 10))
    print("Amplified:", mega_fireball("Dragon", 10))

    print("\nTesting conditional caster...")
    strong_enough = conditional_caster(
        lambda target, power: power >= 20, fireball
    )
    print("Power 50:", strong_enough("Goblin", 50))
    print("Power 5:", strong_enough("Goblin", 5))

    print("\nTesting spell sequence...")
    combo = spell_sequence([fireball, heal, shield])
    for result in combo("Knight", 15):
        print(" -", result)

    print("\nTesting composition (amplified + conditional)...")
    composed = conditional_caster(
        lambda target, power: target != "Ally",
        power_amplifier(fireball, 2),
    )
    print(composed("Troll", 25))
    print(composed("Ally", 25))


if __name__ == "__main__":
    main()
