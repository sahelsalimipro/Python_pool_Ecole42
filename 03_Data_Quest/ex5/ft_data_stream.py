import random
from typing import Generator

players: list[str] = ["alice", "bob", "charlie", "dylan"]
actions: list[str] = [
    "run", "eat", "sleep",
    "grab", "move", "climb",
    "swim", "use", "release"]


def get_event() -> Generator[tuple[str, str], None, None]:
    while True:
        name: str = random.choice(players)
        action: str = random.choice(actions)
        yield (name, action)


def custome_event(
        events: list[tuple[str, str]]
) -> Generator[tuple[str, str], None, None]:
    while events:
        index = random.randrange(len(events))
        event = events[index]
        del events[index]
        yield event


def main() -> None:
    print("=== Game Data Stream Processor ===")

    stream = get_event()
    for i in range(1000):
        name, action = next(stream)
        print(f"Event {i}: Player {name} did action {action}")
    event_list: list[tuple[str, str]] = []
    for _ in range(10):
        event_list.append(next(stream))
    print(f"Built list of 10 events: {event_list}")

    for event in custome_event(event_list):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {event_list}")


if __name__ == "__main__":
    main()
