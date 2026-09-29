from abc import ABC, abstractmethod


class HealCapability(ABC):
    """Capability: can heal. Does NOT inherit from Creature on purpose,
    so it could later be reused by non-creature objects."""

    @abstractmethod
    def heal(self) -> str:
        """Return a string describing the healing action."""


class TransformCapability(ABC):
    """Capability: can transform and revert.

    The `transformed` attribute keeps the state between calls. Concrete
    creatures read it inside `attack` to change their behaviour.
    """

    def __init__(self) -> None:
        self.transformed: bool = False

    @abstractmethod
    def transform(self) -> str:
        """Enter the transformed state and describe it."""

    @abstractmethod
    def revert(self) -> str:
        """Leave the transformed state and describe it."""
