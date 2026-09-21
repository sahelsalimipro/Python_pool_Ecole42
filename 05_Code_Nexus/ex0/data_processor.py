from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    # """Abstract base class defining the common processing interface
    # shared by every specialized data processor."""

    def __init__(self) -> None:
        self._storage: list[str] = []
        self._next_rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        # """Return True if data is appropriate for this processor."""
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        # """Process and store data. Raise if data is invalid."""
        ...

    def output(self) -> tuple[int, str]:
        # """Extract and remove the oldest stored piece of data,
        # along with its processing rank."""
        if not self._storage:
            raise IndexError("No data available to output")
        value = self._storage.pop(0)
        rank = self._next_rank
        self._next_rank += 1
        return (rank, value)


class NumericProcessor(DataProcessor):
    # """Processes int, float, and lists of both (mixed types allowed)."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        if isinstance(data, list):
            return len(data) > 0 and all(
                isinstance(item, (int, float)) and not isinstance(item, bool)
                for item in data
            )
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric data")
        if isinstance(data, list):
            self._storage.extend(str(item) for item in data)
        else:
            self._storage.append(str(data))


class TextProcessor(DataProcessor):
    # """Processes str and lists of str."""

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return len(data) > 0 and all(isinstance(item, str) for item in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise TypeError("Improper text data")
        if isinstance(data, list):
            self._storage.extend(data)
        else:
            self._storage.append(data)


class LogProcessor(DataProcessor):
    # """Processes dict[str, str] log entries (with log_level and
    # log_message keys) and lists of such dicts."""

    def validate(self, data: Any) -> bool:
        if self._is_log_dict(data):
            return True
        if isinstance(data, list):
            return len(data) > 0 and all(self._is_log_dict(item) for item in data)
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise TypeError("Improper log data")
        if isinstance(data, list):
            self._storage.extend(self._format(item) for item in data)
        else:
            self._storage.append(self._format(data))

    @staticmethod
    def _is_log_dict(d: Any) -> bool:
        required_keys = {"log_level", "log_message"}
        return (
            isinstance(d, dict)
            and set(d.keys()) == required_keys
            and all(isinstance(v, str) for v in d.values())
        )

    @staticmethod
    def _format(d: dict[str, str]) -> str:
        return f"{d['log_level']}: {d['log_message']}"


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")

    # --- Numeric Processor ---
    print("Testing Numeric Processor...")
    numeric = NumericProcessor()
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")

    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric.ingest("foo")  # type: ignore[arg-type]
    except TypeError as exc:
        print(f"Got exception: {exc}")

    data: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {data}")
    numeric.ingest(data)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")
    print()

    # --- Text Processor ---
    print("Testing Text Processor...")
    text = TextProcessor()
    print(f"Trying to validate input '42': {text.validate(42)}")

    data_text = ["Hello", "Nexus", "World"]
    print(f"Processing data: {data_text}")
    text.ingest(data_text)
    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")
    print()

    # --- Log Processor ---
    print("Testing Log Processor...")
    log = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")

    data_log = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {data_log}")
    log.ingest(data_log)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
