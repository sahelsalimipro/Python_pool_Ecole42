import random

players: list[str] = ["Alice", "bob", "Charlie",
                      "dylan", "Charlie", "dylan",
                      "Emma", "Gregory", "john",
                      "kevin", "Liam"]


def main() -> None:
    capitalized = [name.capitalize() for name in players]
    already_capitalized = [name for name in players if name[0].isupper()]

    print(f"Initial list of players: {players}")
    print(f"New list with all names capitalized: {capitalized}")
    print(f"New list of capitalized names only: {already_capitalized}")
    print()
    built_scores = {name: random.randint(1, 1000) for name in capitalized}
    print(f"Score dict: {built_scores}")
    average = sum(built_scores.values()) / len(built_scores)
    print(f"Score average is {round(average, 2)}")
    high_scores = {name: score for name,
                   score in built_scores.items() if score > average}
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    print("=== Game Data Alchemist ===\n")
    main()
