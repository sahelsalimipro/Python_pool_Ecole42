from abc import ABC, abstractmethod

from .Creature import Creature
from .Creatures import Flameling, Pyrodon, Aquabub, Torragon


class CreatureFactory(ABC):
    """Abstract factory: builds the base and evolved form of a family."""

    @abstractmethod
    def create_base(self) -> Creature:
        """Create the base creature of the family."""

    @abstractmethod
    def create_evolved(self) -> Creature:
        """Create the evolved creature of the family."""


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Flameling()

    def create_evolved(self) -> Creature:
        return Pyrodon()


class AquaFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Aquabub()

    def create_evolved(self) -> Creature:
        return Torragon()
