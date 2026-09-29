*This project has been created as part of the 42 curriculum by ssalimi.*

# The Codex — Mastering Python's Import Mysteries

## Description

The Codex is a Python module from the 42 curriculum that teaches how the
Python import system works, through a small "alchemy laboratory" package.
Every function is deliberately trivial (it returns a string), so the focus
stays on **how imports are resolved**, not on business logic.

The project covers four "mysteries":

1. **Package initialization**: how `__init__.py` turns a folder into a
   package and decides what `import alchemy` exposes.
2. **Import pathways**: reaching code in distant modules (nested imports,
   aliases, re-exports).
3. **Absolute vs relative imports**: two paths to the same module, and
   when to use each.
4. **Circular dependencies**: why they crash, and how to break them.

## Requirements

- Python 3.10 or later
- `flake8` and `mypy` (for the coding-standard checks)
- Only imports of modules written in this project are allowed
- `sys.path` must not be modified, and `eval()` / `exec()` are forbidden

## Project structure

```
.
├── alchemy
│   ├── __init__.py
│   ├── elements.py            # create_earth, create_air
│   ├── grimoire
│   │   ├── __init__.py
│   │   ├── dark_spellbook.py
│   │   ├── dark_validator.py
│   │   ├── light_spellbook.py
│   │   └── light_validator.py
│   ├── potions.py             # healing_potion, strength_potion
│   └── transmutation
│       ├── __init__.py
│       └── recipes.py         # lead_to_gold
├── elements.py                # create_fire, create_water
├── ft_alembic_0.py ... ft_alembic_5.py
├── ft_distillation_0.py, ft_distillation_1.py
├── ft_transmutation_0.py ... ft_transmutation_2.py
└── ft_kaboom_0.py, ft_kaboom_1.py
```

## Instructions

Run every script from the **root of the repository**, so that the root
folder is on Python's module search path:

```bash
python3 ft_alembic_0.py
python3 ft_distillation_0.py
python3 ft_transmutation_0.py
python3 ft_kaboom_0.py
```

Check the coding standard and type annotations:

```bash
flake8 .
mypy .
```

`ft_alembic_4.py` produces one **intentional** mypy error
(`Module has no attribute "create_earth"`), and `ft_kaboom_1.py`
intentionally ends with an uncaught `ImportError`.

## Parts

### Part I: The Alembic

Six scripts, each using a different way to reach the elements:

| Script | Import style | Target |
|---|---|---|
| `ft_alembic_0.py` | `import elements` | root `elements.py` |
| `ft_alembic_1.py` | `from elements import ...` | root `elements.py` |
| `ft_alembic_2.py` | `import alchemy.elements` | `alchemy/elements.py` |
| `ft_alembic_3.py` | `from alchemy.elements import ...` | `alchemy/elements.py` |
| `ft_alembic_4.py` | `import alchemy` | package interface |
| `ft_alembic_5.py` | `from alchemy import ...` | package interface |

`alchemy/__init__.py` exposes `create_air` but **not** `create_earth`, so
`alchemy.create_earth()` raises an `AttributeError` at runtime and is also
flagged by mypy. This shows that `__init__.py` defines a package's public
interface.

### Part II: Distillation

`alchemy/potions.py` builds potions from all four elements. Fire and water
come from the root `elements.py` (absolute import); earth and air come from
`alchemy/elements.py` (relative import).

`alchemy/__init__.py` also exposes `strength_potion` and an alias
`heal` for `healing_potion` (`from .potions import healing_potion as heal`).

### Part III: The Great Transmutation

`alchemy/transmutation/recipes.py` defines `lead_to_gold()` and mixes both
import styles:

```python
from elements import create_fire        # absolute
from ..elements import create_air       # relative
from ..potions import strength_potion   # relative
```

`lead_to_gold` is re-exported by `alchemy/transmutation/__init__.py` and by
`alchemy/__init__.py`, so it can be reached through the file, the
`transmutation` package, or the `alchemy` package.

**Absolute vs relative:** absolute imports are explicit, easy to read and
work everywhere (including scripts). Relative imports are shorter and
survive a package rename, but only work inside a package.

### Part IV: Avoid the Explosion

The `grimoire` package contains two spellbook/validator pairs:

- **Light magic** (`light_spellbook.py`, `light_validator.py`): the
  spellbook owns the allowed ingredients and the validator needs them,
  while the spellbook needs the validator to record a spell. The circular
  dependency is broken with a **deferred import** inside
  `light_spell_record()`.
- **Dark magic** (`dark_spellbook.py`, `dark_validator.py`): the same
  design with plain top-level imports on both sides. Importing it raises
  `ImportError: cannot import name ... from partially initialized module
  ... (most likely due to a circular import)`.

`grimoire/__init__.py` only exposes the light magic, so the dark files stay
reachable only by their full path (`ft_kaboom_1.py`).

**Why it explodes:** Python runs a module top to bottom. While
`dark_spellbook` is stuck on its first line importing `dark_validator`,
the validator asks for `dark_spell_allowed_ingredients`, which has not
been defined yet.

**Other ways to break a cycle:** import the module instead of the name
(`from . import module`), move shared data into a third module, or pass the
data as an argument.

## Resources

- [Python docs: The import system](https://docs.python.org/3/reference/import.html)
- [Python docs: Modules and packages](https://docs.python.org/3/tutorial/modules.html)
- [PEP 8: Imports](https://peps.python.org/pep-0008/#imports)
- [PEP 328: Absolute and relative imports](https://peps.python.org/pep-0328/)

### Use of AI

AI was used as a learning aid to explain import concepts (namespaces,
`__init__.py`, relative imports, circular imports) and to help debug errors.
All code was reviewed, tested and is understood by the author.
