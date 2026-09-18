from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        # Shared state for ALL subclasses: a FIFO queue of stringified
        # items, and a running counter for the "rank" (ingestion index).
        self._storage: list[str] = []
        self._next_rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        # Shared for every subclass — pops the oldest item (FIFO).
        if not self._storage:
            raise IndexError("No data available to output")
        value = self._storage.pop(0)
        rank = self._next_rank
        self._next_rank += 1
        return (rank, value)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:

    def ingest(self, data: Any) -> None:


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:

    def ingest(self, data: Any) -> None:


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:

    def ingest(self, data: Any) -> None:
