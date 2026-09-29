# DataDeck: Abstract Card Architecture

*This project has been created as part of the 42 curriculum by ssalimi.*

## Description

DataDeck is a small creature-based card game engine used to practice advanced
object-oriented design patterns in Python. The goal is not the game itself but
the architecture behind it: how to build a system flexible enough to handle
many card types while keeping the code clean and maintainable.

The project is split into three exercises, each introducing one pattern:

| Exercise | Pattern | Idea |
|---|---|---|
| `ex0` | **Abstract Factory** | Create families of related creatures (base + evolved) through an interface, without hard-coding concrete classes. |
| `ex1` | **Capabilities** (multiple inheritance) | Add optional abilities (heal, transform) that are independent from `Creature`. |
| `ex2` | **Strategy** | Let a tournament run fights without knowing what each creature can do. |

## Requirements

- Python **3.10** or later
- No external libraries (only `abc` and `typing` from the standard library)
- Code checked with `flake8` and `mypy`

## Repository structure

```
07_DataDeck/
├── battle.py            # test script for ex0
├── capacitor.py         # test script for ex1
├── tournament.py        # test script for ex2
├── ex0/
│   ├── __init__.py      # public API: Creature, CreatureFactory, FlameFactory, AquaFactory
│   ├── creature.py      # abstract Creature
│   ├── creatures.py     # Flameling, Pyrodon, Aquabub, Torragon (hidden)
│   └── factory.py       # CreatureFactory, FlameFactory, AquaFactory
├── ex1/
│   ├── __init__.py      # public API: capabilities + factories
│   ├── capabilities.py  # HealCapability, TransformCapability
│   ├── creatures.py     # Sproutling, Bloomelle, Shiftling, Morphagon (hidden)
│   └── factory.py       # HealingCreatureFactory, TransformCreatureFactory
└── ex2/
    ├── __init__.py      # public API: strategies + InvalidStrategyError
    └── strategy.py      # BattleStrategy, Normal/Aggressive/Defensive strategies
```

## Instructions

Run every command from the root of the repository (the folder containing
`battle.py`).

```bash
python3 battle.py        # exercise 0
python3 capacitor.py     # exercise 1
python3 tournament.py    # exercise 2

flake8 .                 # coding standard
mypy .                   # type checking
```

## Exercises

### Exercise 0: Creature Factory

- `Creature` is an abstract class holding a `name` and a `creature_type`. It
  defines an abstract `attack()` and a concrete `describe()` shared by all
  creatures.
- `Flameling`, `Pyrodon`, `Aquabub` and `Torragon` are the concrete creatures.
- `CreatureFactory` is the abstract factory with `create_base()` and
  `create_evolved()`. `FlameFactory` builds Flameling / Pyrodon and
  `AquaFactory` builds Aquabub / Torragon.
- The `ex0` package exposes only the abstract types and the factories. Concrete
  creatures are not part of its public API (`__all__`).
- `battle.py` uses one function that accepts any factory, and one function that
  makes two base creatures fight.

### Exercise 1: Capabilities

- `HealCapability` (`heal`) and `TransformCapability` (`transform`, `revert`)
  are abstract classes that **do not inherit from `Creature`**, so they can be
  reused by other kinds of objects in the future.
- `TransformCapability` keeps a persistent `transformed` attribute. It changes
  the result of `attack()`: normal attack before transforming, boosted attack
  after.
- `Sproutling` and `Bloomelle` inherit from `Creature` and `HealCapability`
  (`HealingCreatureFactory`).
- `Shiftling` and `Morphagon` inherit from `Creature` and `TransformCapability`
  (`TransformCreatureFactory`).
- The factories inherit from the `CreatureFactory` defined in `ex0`.
- `capacitor.py` uses `isinstance` checks to call `heal()`, `transform()` and
  `revert()`. The factories are typed as returning `Creature`, so the
  capability has to be verified first.

### Exercise 2: Abstract Strategy

- `BattleStrategy` defines two abstract methods: `is_valid(creature)` and
  `act(creature)`.
- `NormalStrategy`: valid for any creature, uses `attack()`.
- `AggressiveStrategy`: valid for creatures with `TransformCapability`, does
  transform, attack, revert.
- `DefensiveStrategy`: valid for creatures with `HealCapability`, does attack,
  then heal.
- An invalid creature/strategy pair makes `is_valid` return `False`. Calling
  `act` with such a pair raises `InvalidStrategyError` with a clear message.
- `tournament.py` defines a single `battle()` function. It takes a list of
  `(CreatureFactory, BattleStrategy)` tuples, makes every opponent fight every
  other opponent exactly once, and aborts the tournament on an invalid pair.

## Design decisions

- **Hiding concrete creatures.** Concrete creature modules are never imported
  in a package's `__init__.py`. Outside code can only obtain a creature by
  asking a factory.
- **`battle()` knows nothing about capabilities.** All fight logic lives in the
  strategies. A new fighting style is a new `BattleStrategy` subclass and
  requires no change to `battle()`.
- **`is_valid` and `act` are separate.** `is_valid` is a side-effect-free
  question. `act` protects itself by raising an exception, so an invalid
  combination can never run silently.
- **Explicit parent initialisation** in `Shiftling` and `Morphagon`
  (`Creature.__init__` and `TransformCapability.__init__`), so the
  `transformed` state always exists.

## Resources

- [Python `abc` module](https://docs.python.org/3/library/abc.html)
- [Python data model: multiple inheritance and MRO](https://docs.python.org/3/howto/mro.html)
- [`typing` module](https://docs.python.org/3/library/typing.html)
- [PEP 8: Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [mypy documentation](https://mypy.readthedocs.io/)
- Refactoring Guru: [Abstract Factory](https://refactoring.guru/design-patterns/abstract-factory) and [Strategy](https://refactoring.guru/design-patterns/strategy)
