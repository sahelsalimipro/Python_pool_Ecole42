import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    """Reduce spell powers with the requested operation."""
    operations: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min,
    }
    if not spells:
        return 0
    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")
    return functools.reduce(operations[operation], spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    """Create 3 specialised enchantments with power=50 and an element."""
    return {
        'fire': functools.partial(base_enchantment, 50, "fire"),
        'ice': functools.partial(base_enchantment, 50, "ice"),
        'lightning': functools.partial(base_enchantment, 50, "lightning"),
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    """Return the nth Fibonacci number (cached)."""
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    """Return a single-dispatch spell caster."""
    @functools.singledispatch
    def cast(spell: Any) -> str:
        return "Unknown spell type"

    @cast.register
    def _(spell: int) -> str:
        return f"Damage spell: {spell} damage"

    @cast.register
    def _(spell: str) -> str:
        return f"Enchantment: {spell}"

    @cast.register
    def _(spell: list) -> str:
        return f"Multi-cast: {len(spell)} spells"

    return cast


def base_enchantment(power: int, element: str, target: str) -> str:
    return f"{element.capitalize()} enchantment ({power}) on {target}"


def main() -> None:
    powers = [10, 20, 30, 40]

    print("Testing spell reducer...")
    print(f"Sum: {spell_reducer(powers, 'add')}")
    print(f"Product: {spell_reducer(powers, 'multiply')}")
    print(f"Max: {spell_reducer(powers, 'max')}")
    print(f"Min: {spell_reducer(powers, 'min')}")
    print(f"Empty: {spell_reducer([], 'add')}")
    try:
        spell_reducer(powers, 'divide')
    except ValueError as error:
        print(f"Error: {error}")

    print("\nTesting partial enchanter...")
    for name, enchant in partial_enchanter(base_enchantment).items():
        print(f"{name}: {enchant('Sword')}")

    print("\nTesting memoized fibonacci...")
    for n in (0, 1, 10, 15):
        print(f"Fib({n}): {memoized_fibonacci(n)}")
    print(memoized_fibonacci.cache_info())

    print("\nTesting spell dispatcher...")
    cast = spell_dispatcher()
    print(cast(42))
    print(cast("fireball"))
    print(cast(["fireball", "heal", "shield"]))
    print(cast(3.14))


if __name__ == "__main__":
    main()
