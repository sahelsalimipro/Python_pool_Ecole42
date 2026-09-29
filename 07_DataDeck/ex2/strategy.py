from abc import ABC, abstractmethod

from ex0 import Creature
from ex1 import HealCapability, TransformCapability


class InvalidStrategyError(Exception):
    """Raised when a strategy is used with a Creature it doesn't suit."""


class BattleStrategy(ABC):
    """Abstract strategy: decides HOW a creature behaves during a fight."""

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        """Return True if the creature is suitable for this strategy."""

    @abstractmethod
    def act(self, creature: Creature) -> None:
        """Perform the creature's turn (raises if the strategy is invalid
        for this creature)."""


class NormalStrategy(BattleStrategy):
    """Suitable for any creature: just attack."""

    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> None:
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    """Suitable for transforming creatures: transform, attack, revert."""

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not isinstance(creature, TransformCapability):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this aggressive strategy"
            )
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())


class DefensiveStrategy(BattleStrategy):
    """Suitable for healing creatures: attack, then heal."""

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> None:
        if not isinstance(creature, HealCapability):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this defensive strategy"
            )
        print(creature.attack())
        print(creature.heal())
