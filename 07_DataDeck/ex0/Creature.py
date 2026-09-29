from abc import ABC, abstractmethod


class Creature(ABC):
    # """Abstract base class for every creature card."""

    def __init__(self, name: str, creature_type: str) -> None:
        self.name: str = name
        self.creature_type: str = creature_type

    @abstractmethod
    def attack(self) -> str:
        # """Each concrete creature must define its own attack."""
        ...

    def describe(self) -> str:
        # """Generic description shared by all creatures."""
        return f"{self.name} is a {self.creature_type} type Creature"
