from .Creature import Creature
from .Factory import CreatureFactory, FlameFactory, AquaFactory

# Concrete creatures (Flameling, Pyrodon, ...) are intentionally NOT exposed.
# Only the abstract types and the factories are part of the public API.
__all__ = ["Creature", "CreatureFactory", "FlameFactory", "AquaFactory"]
