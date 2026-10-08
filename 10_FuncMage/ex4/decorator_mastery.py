import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def spell_timer(func: Callable) -> Callable:
    """Print how long the decorated spell takes to run."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> Callable:
    """Only run the spell if its 'power' argument is >= min_power."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # power is the last positional argument, or passed by keyword
            power = kwargs.get('power', args[-1] if args else 0)
            if power < min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable:
    """Retry the spell up to max_attempts times if it raises."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print(f"Spell failed, retrying... "
                              f"(attempt {attempt}/{max_attempts})")
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        """Valid if >= 3 chars and only letters/spaces."""
        return (len(name) >= 3
                and all(c.isalpha() or c.isspace() for c in name))

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


@spell_timer
def fireball() -> str:
    time.sleep(0.1)
    return "Fireball cast!"


@retry_spell(max_attempts=3)
def unstable_spell() -> str:
    raise RuntimeError("The spell exploded")


def make_flaky_spell() -> Callable:
    attempts = 0

    @retry_spell(max_attempts=3)
    def flaky_spell() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise RuntimeError("Not yet")
        return "Waaaaaaagh spelled !"
    return flaky_spell


def main() -> None:
    print("Testing spell timer...")
    print(f"Result: {fireball()}")

    print("\nTesting retrying spell...")
    print(unstable_spell())
    print(make_flaky_spell()())

    print("\nTesting MageGuild...")
    guild = MageGuild()
    print(MageGuild.validate_mage_name("Alex Storm"))
    print(MageGuild.validate_mage_name("X1"))
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Lightning", 5))


if __name__ == "__main__":
    main()
