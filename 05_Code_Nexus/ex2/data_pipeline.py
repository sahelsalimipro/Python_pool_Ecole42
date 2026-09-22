from abc import ABC, abstractmethod
from typing import Any, Protocol


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

    def pending(self) -> int:
        # """Return the number of items currently waiting on this
        # processor, without consuming them."""
        return len(self._storage)


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
            return len(data) > 0 and all(isinstance(item, str)
                                         for item in data)
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
            return len(data) > 0 and all(self._is_log_dict(item)
                                         for item in data)
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise TypeError("Improper log data")
        if isinstance(data, list):
            self._storage.extend(self._format(item) for item in data)
        else:
            self._storage.append(self._format(data))

    @staticmethod
    # checks whether a dictionary is a valid log
    # Is d a valid log dictionary?
    def _is_log_dict(d: Any) -> bool:
        required_keys = {"log_level", "log_message"}
        return (
            isinstance(d, dict)
            and set(d.keys()) == required_keys
            and all(isinstance(v, str) for v in d.values())
        )

    @staticmethod
    # converts a valid log dictionary into a readable string.
    def _format(d: dict[str, str]) -> str:
        return f"{d['log_level']}: {d['log_message']}"


class ExportPlugin(Protocol):
    # """Structural (duck-typed) contract every export plugin must
    # satisfy. Any object exposing a matching process_output method
    # is export-compatible, with no need to inherit from this class."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    # """Exports a batch of (rank, value) tuples as a single CSV
    # row, discarding the rank and keeping only the values."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        print(",".join(value for _, value in data))


class JSONExportPlugin:
    # """Exports a batch of (rank, value) tuples as a JSON object,
    # keyed by an "item_<rank>" label."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        entries = [f'"item_{rank}": "{value}"' for rank, value in data]
        print("JSON Output:")
        print("{" + ", ".join(entries) + "}")


class DataStream:
    # """Routes heterogeneous data through a set of registered
    # DataProcessor instances, purely through polymorphic behavior:
    # it never needs to know which concrete processor type it is
    # talking to, only that each one exposes validate/ingest/output.
    # It can also export pending data through any duck-typed
    # ExportPlugin, again without knowing its concrete type."""

    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []
        self._total_processed: dict[DataProcessor, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        # """Add a new data processor able to receive elements of the
        # stream."""
        self._processors.append(proc)
        self._total_processed[proc] = 0

    def process_stream(self, stream: list[Any]) -> None:
        # """Route every element of the stream to the first registered
        # processor able to validate it. Prints an error message for
        # any element no processor can handle."""
        for element in stream:
            handled = False
            for proc in self._processors:
                if proc.validate(element):
                    before = proc.pending()
                    proc.ingest(element)
                    self._total_processed[proc] += proc.pending() - before
                    handled = True
                    break
            if not handled:
                print(
                    "DataStream error - Can't process element in "
                    f"stream: {element}"
                )

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        # """For every registered processor, consume up to nb pending
        # items (fewer if not enough are available) and hand them to
        # the given export plugin as a single batch."""
        for proc in self._processors:
            batch: list[tuple[int, str]] = []
            for _ in range(nb):
                if proc.pending() == 0:
                    break
                batch.append(proc.output())
            if batch:
                plugin.process_output(batch)

    def print_processors_stats(self) -> None:
        # """Print, for every registered processor, the total number
        # of items it has ever processed along with how many are
        # still waiting to be extracted."""
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            name = type(proc).__name__.replace("Processor", " Processor")
            total = self._total_processed[proc]
            print(
                f"{name}: total {total} items processed, "
                f"remaining {proc.pending()} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===\n")

    print("Initialize Data Stream...")
    data_stream = DataStream()
    print()
    data_stream.print_processors_stats()
    print()

    print("Registering Processors")
    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()
    data_stream.register_processor(numeric)
    data_stream.register_processor(text)
    data_stream.register_processor(log)
    print()

    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {"log_level": "WARNING",
             "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO",
             "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {batch}")
    data_stream.process_stream(batch)
    print()
    data_stream.print_processors_stats()
    print()

    print("Send 3 processed data from each processor to a CSV plugin:")
    csv_plugin = CSVExportPlugin()
    data_stream.output_pipeline(3, csv_plugin)
    print()
    data_stream.print_processors_stats()
    print()

    batch2: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {"log_level": "NOTICE",
             "log_message": "Certificate expires in 10 days"},
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"Send another batch of data: {batch2}")
    data_stream.process_stream(batch2)
    print()
    data_stream.print_processors_stats()
    print()

    print("Send 5 processed data from each processor to a JSON plugin:")
    json_plugin = JSONExportPlugin()
    data_stream.output_pipeline(5, json_plugin)
    print()
    data_stream.print_processors_stats()


if __name__ == "__main__":
    main()
