*This project has been created as part of the 42 curriculum by ssalimi.*

# DataDeck: Abstract Card Architecture

## Description

DataDeck is a small creature-based card game engine written in Python 3.10+.
The game itself is only a pretext. The real goal of the project is to practice
**abstract programming patterns** and to write code that stays clean and
flexible when it grows from 4 creatures to thousands.

The project is split into three exercises, each one built on the previous one:

| Exercise | Pattern practiced | What it builds |
|---|---|---|
| `ex0` | **Abstract Factory** | Creatures grouped in families (Flame, Aqua) created through factories |
| `ex1` | **Capabilities** (multiple inheritance) | Optional abilities (heal, transform) kept separate from `Creature` |
| `ex2` | **Strategy** | Battle behaviour swapped at runtime, without the battle code knowing about abilities |

---

## Instructions

### Requirements

- Python 3.10 or later
- No external library (standard library only, `abc` and `typing`)
- Code must pass `flake8` and `mypy`

### Project structure

```
07_DataDeck/
├── battle.py            # test script for ex0
├── capacitor.py         # test script for ex1
├── tournament.py        # test script for ex2
├── ex0/
│   ├── __init__.py      # public API: abstract types + factories only
│   ├── Creature.py      # abstract Creature
│   ├── Creatures.py     # Flameling, Pyrodon, Aquabub, Torragon
│   └── Factory.py       # CreatureFactory, FlameFactory, AquaFactory
├── ex1/
│   ├── __init__.py      # public API: capabilities + factories only
│   ├── capabilities.py  # HealCapability, TransformCapability
│   ├── creatures.py     # Sproutling, Bloomelle, Shiftling, Morphagon
│   └── factory.py       # HealingCreatureFactory, TransformCreatureFactory
└── ex2/
    ├── __init__.py      # public API: strategies + exception
    └── strategy.py      # BattleStrategy, Normal/Aggressive/Defensive
```

Every exercise folder contains an `__init__.py`. It is mandatory: it is what
makes the folder a package.

### Run

Run everything from the repository root (the folder containing `battle.py`):

```bash
python3 battle.py        # ex0: factories and a basic battle
python3 capacitor.py     # ex1: healing and transforming creatures
python3 tournament.py    # ex2: strategies and a full tournament
```

### Check code quality

```bash
flake8 .
mypy .
```

### Example output (ex2)

```
$> python3 tournament.py
Tournament 1 (error)
[ (Flameling+Aggressive), (Healing+Defensive) ]
*** Tournament ***
2 opponents involved

* Battle *
Flameling is a Fire type Creature
vs.
Sproutling is a Grass type Creature
now fight!
Battle error, aborting tournament: Invalid Creature 'Flameling' for this aggressive strategy
```

---

## Part 1: Package structure and Python notation

### Packages and `__init__.py`

A folder becomes a **package** when it contains an `__init__.py` file. That
file runs when the package is imported and decides what the package shows to
the outside. Without it, Python treats the folder as a "namespace package" with
no names inside, which leads to errors like
`cannot import name 'CreatureFactory' from 'ex0' (unknown location)`.

### Absolute and relative imports

```python
from ex0 import Creature          # absolute: starts from the project root
from .creature import Creature    # relative: "." means "this package"
```

Inside a package, files use the dot form to find their neighbours. This is why
`from .strategy import ...` in `ex2/__init__.py` fails if `strategy.py` is not
inside `ex2/`.

### `__all__`: the public API

```python
__all__ = ["Creature", "CreatureFactory", "FlameFactory", "AquaFactory"]
```

`__all__` is the package's official list of public names. It controls
`from ex0 import *` and tells tools such as `mypy` that these names are
intentionally re-exported. Anything not listed is considered internal.

This is how the subject's rule is respected: *"your package cannot expose
concrete Creatures directly, it must only expose factories"*. `Flameling`
exists in the package files, but it is not imported in `__init__.py`, so it is
not part of the public API. This is **encapsulation at package level**.

### `if __name__ == "__main__":`

Every Python file has a `__name__`. It equals `"__main__"` only when the file is
run directly (`python3 battle.py`), not when it is imported by another file. So
`main()` runs when you execute the script but not on import.

### Type annotations

Annotations are checked by `mypy` before running and are ignored at runtime.

| Notation | Meaning |
|---|---|
| `name: str` | this variable or parameter is a string |
| `-> None` | the function returns nothing |
| `-> Creature` | the function returns a `Creature` |
| `self.name: str = name` | instance attribute with a declared type |
| `list[tuple[CreatureFactory, BattleStrategy]]` | a list of 2-element tuples: (a factory, a strategy) |

The lowercase `list[...]` and `tuple[...]` forms are available from Python 3.9.

### Code quality tools

- **`flake8`** checks style (PEP 8): line length, spacing, unused imports.
- **`mypy`** checks types, so many mistakes are caught before running.

### Other notation used in the code

- **f-strings**: `f"{self.name} uses Ember!"` inserts variables in text.
- **Docstrings**: the `"""..."""` text under a class or function documents it.
  In an abstract method, a docstring alone is a valid body.
- **`_`** in `for _, f, s in entries` is the convention for "I ignore this
  value".

---

## Part 2: Abstract classes (the foundation)

```python
from abc import ABC, abstractmethod

class Creature(ABC):
    @abstractmethod
    def attack(self) -> str: ...
```

- **`ABC`** (Abstract Base Class) marks a class as a template.
- **`@abstractmethod`** is a decorator saying "subclasses must override this".
- A class with unimplemented abstract methods **cannot be instantiated**:
  `Creature("x", "y")` raises `TypeError`. A subclass that forgets `attack` is
  refused the same way.

An abstract class is a **contract**: every `Creature` is guaranteed to have an
`attack()`, so any code using a `Creature` can call it safely.

**Abstract vs concrete methods in the same class.** `describe()` is concrete:
it is written once and inherited by every creature, which avoids duplication.
`attack()` is abstract because every creature attacks differently.

**`super().__init__(...)`** calls the parent constructor. `Flameling` uses it to
pass `"Flameling"` and `"Fire"` to `Creature`, which stores the name and the
type. The code is not repeated in every subclass.

**Polymorphism.** `creature.attack()` works for any creature, and each class
answers in its own way. The caller does not need to know the exact type. Anywhere
a `Creature` is expected, any subclass can be used (the Liskov substitution
principle).

---

## Part 3: Exercise 0, Abstract Factory

### The problem

If the code writes `Flameling()` everywhere, it is glued to that concrete class.
Adding or changing a family means editing all that code.

### The solution

```python
class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature: ...

    @abstractmethod
    def create_evolved(self) -> Creature: ...
```

`FlameFactory` returns `Flameling` and `Pyrodon`. `AquaFactory` returns
`Aquabub` and `Torragon`.

The key word is **family**: a factory produces *related products that belong
together* (a base form and its evolution), not just one object.

`battle.py` is written against `CreatureFactory`, never against `Flameling`:

```python
def test_factory(factory: CreatureFactory) -> None:
```

A single function works for every present and future factory. This is
**Dependency Inversion**: depend on abstractions, not on concrete classes.

### Files

| File | Role |
|---|---|
| `Creature.py` | abstract `Creature` with `name`, `creature_type`, abstract `attack`, concrete `describe` |
| `Creatures.py` | the four concrete creatures |
| `Factory.py` | abstract `CreatureFactory` and the two concrete factories |
| `__init__.py` | exposes `Creature`, `CreatureFactory`, `FlameFactory`, `AquaFactory` |

The abstract `Creature` is exported because ex1 needs it as a parent class. Only
the *concrete* creatures are hidden.

Hiding is done through the public API. It is a convention, so
`from ex0.Creatures import Flameling` still technically works for someone who
knows the file name.

### `battle.py` scenario

1. Instantiate `FlameFactory` and `AquaFactory`.
2. One function tests a factory: create base and evolved, describe and attack.
3. One function takes both factories and makes the base creatures fight.

---

## Part 4: Exercise 1, Capabilities and multiple inheritance

### The idea

Abilities such as healing or transforming are not the same thing as *being* a
creature. So `HealCapability` and `TransformCapability` are separate abstract
classes that do **not** inherit from `Creature`. This favours combining
behaviours over building one giant inheritance tree. A future `Trainer` class
could also inherit `HealCapability`.

### Multiple inheritance

```python
class Sproutling(Creature, HealCapability):
```

The class *is* a `Creature` **and** has the heal capability. It must implement
every abstract method of both parents (`attack` and `heal`).

### MRO (Method Resolution Order)

With several parents, Python needs a rule to choose which method to use. It
searches in a fixed order: the class itself, then its parents from left to right,
ending with `object`. Print it with `Shiftling.__mro__`. `super()` means "the
next class in that order".

### Why the transforming creatures initialise both parents

```python
Creature.__init__(self, "Shiftling", "Normal")
TransformCapability.__init__(self)
```

`Creature.__init__` does not chain to the other parent, so
`TransformCapability.__init__` would never run and `self.transformed` would not
exist. Calling both parents by name guarantees both run.

### State: the `transformed` attribute

```python
def attack(self) -> str:
    if self.transformed:
        return f"{self.name} performs a boosted strike!"
    return f"{self.name} attacks normally."
```

`transform()` sets `self.transformed = True` and `revert()` sets it back to
`False`. The same `attack()` call gives a different result depending on the
object's history. Data and behaviour live together, which is the point of
objects.

### Runtime checks and type narrowing

```python
if isinstance(creature, HealCapability):
    print(creature.heal())
```

`create_base()` is typed as returning `Creature`, and `Creature` has no `heal`.
`isinstance` checks at runtime **and** tells `mypy` that inside the block the
object also has `heal`. This is called **type narrowing**.

### Files

| File | Role |
|---|---|
| `capabilities.py` | `HealCapability`, `TransformCapability` (with the `transformed` state) |
| `creatures.py` | `Sproutling`, `Bloomelle` (heal), `Shiftling`, `Morphagon` (transform) |
| `factory.py` | `HealingCreatureFactory`, `TransformCreatureFactory` |
| `__init__.py` | exposes capabilities and factories only |

The two new factories inherit from the `CreatureFactory` of ex0. Ex1 builds on
ex0 as the subject requires.

---

## Part 5: Exercise 2, Abstract Strategy

### The problem

A tournament mixing healers, transformers and normal creatures would need:

```python
if can_heal: ...
elif can_transform: ...
```

Every new capability would force a change in the battle code.

### The solution

Move "how to fight" into interchangeable objects that share one interface:

```python
class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool: ...

    @abstractmethod
    def act(self, creature: Creature) -> None: ...
```

| Strategy | `is_valid` | Sequence in `act` |
|---|---|---|
| `NormalStrategy` | always `True` | attack |
| `AggressiveStrategy` | creature has `TransformCapability` | transform, attack, revert |
| `DefensiveStrategy` | creature has `HealCapability` | attack, heal |

The `battle` function only calls `strategy.act(creature)`. It has **no
knowledge** of healing or transforming. To add a new fighting style, write a new
class and leave `battle` untouched. This is the **Open/Closed principle**: open
to extension, closed to modification.

### `is_valid` vs `act`

- `is_valid` is a safe question with no side effects. It returns `False` for an
  invalid combination and never raises.
- `act` protects itself. If it is called with an invalid combination, it raises
  `InvalidStrategyError` with a clear message.

### Custom exception

```python
class InvalidStrategyError(Exception): ...

raise InvalidStrategyError("Invalid Creature 'Flameling' for this aggressive strategy")

try:
    ...
except InvalidStrategyError as error:
    print(f"Battle error, aborting tournament: {error}")
```

`raise` throws the error, `try/except` catches it, and `as error` gives access to
the message. A dedicated exception lets the code catch **only** this case and not
hide real bugs.

### The `battle` function in `tournament.py`

- It takes a list of `(CreatureFactory, BattleStrategy)` tuples.
- Every opponent fights every other opponent **exactly once**:

  ```python
  for i in range(len(opponents)):
      for j in range(i + 1, len(opponents)):
  ```

  Starting `j` at `i + 1` avoids duplicate pairs and self-fights. The number of
  battles is n(n-1)/2, so 3 opponents give 3 battles.
- Fighters are created with `create_base()` from each factory.
- The `try/except InvalidStrategyError` wraps both loops, so one invalid
  combination aborts the whole tournament, as the subject shows.

### Smaller notation in `tournament.py`

- **Tuple unpacking**: `factory1, strategy1 = opponents[i]`
- **List comprehension**: `[(f, s) for _, f, s in entries]`
- **Generator expression in `join`**: `", ".join(f"..." for ... in entries)`
- **Introspection**: `type(strategy).__name__` returns the class name as text.

---

## Part 6: The big ideas at a glance

| Concept | Where | Meaning |
|---|---|---|
| Abstraction / ABC | ex0 | define a contract and hide details |
| Polymorphism | all | same call, different behaviour per class |
| Encapsulation | `__all__` | expose only what is needed |
| Abstract Factory | ex0, ex1 | create families of objects through an interface |
| Multiple inheritance | ex1 | combine independent abilities |
| State | `transformed` | behaviour depends on stored history |
| Type narrowing | `isinstance` | runtime check that also informs `mypy` |
| Strategy | ex2 | swap behaviours without changing the caller |
| Dependency Inversion | test scripts | depend on abstractions |
| Open/Closed | ex2 | extend by adding, not by editing |

The three exercises build on each other: **ex0** handles creation, **ex1** adds
abilities, and **ex2** handles behaviour in a fight.

---

## Design decisions and questions to be ready for

1. **Why can't `Creature` be instantiated?** It has an abstract method. It is a
   contract, not a real creature.
2. **What does the factory solve compared with `Flameling()`?** The calling code
   depends only on the abstract factory, so families can be added or swapped
   without touching it.
3. **Why don't the capabilities inherit from `Creature`?** Abilities are reusable
   and could apply to things that are not creatures.
4. **What happens if `TransformCapability.__init__` is not called?**
   `self.transformed` does not exist and `attack()` raises `AttributeError`.
5. **Why `isinstance` in `capacitor.py`?** Static typing only guarantees a
   `Creature`. The specific capability must be checked, and this also satisfies
   `mypy`.
6. **Why is `is_valid` separate from `act`?** A caller can check compatibility
   without triggering behaviour or an exception, while `act` still protects
   itself.
7. **How would you add a new family?** Write the creatures and a new factory
   inheriting `CreatureFactory`. `battle.py` does not change.
8. **How would you add a new strategy?** Write a new `BattleStrategy` subclass.
   `battle` does not change.

---

## Resources

- [Python `abc` module](https://docs.python.org/3/library/abc.html)
- [Python `typing` module](https://docs.python.org/3/library/typing.html)
- [Python data model: `__init__`, MRO, `super()`](https://docs.python.org/3/reference/datamodel.html)
- [PEP 8: Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 484: Type Hints](https://peps.python.org/pep-0484/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)
- Design patterns: Abstract Factory and Strategy (Gamma et al., *Design
  Patterns*)
