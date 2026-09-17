import sys


def ft_score_analytics() -> None:

    args = sys.argv[1:]
    scores: list[int] = []
    nb_len = len(args)
    if nb_len == 0:
        print(
            "No scores provided. Usage: "
            "python3 ft_score_analytics.py"
            " <score1> <score2> ..."
        )
        return
    for arg in args:
        try:
            scores.append(int(arg))
        except ValueError:
            print(f"Invalid parameter: '{arg}'")

    if not scores:
        print(
            "No scores provided. Usage: "
            "python3 ft_score_analytics.py"
            " <score1> <score2> ..."
        )
        return

    print(f"Scores processed: {scores}")
    print(f"Total players: {nb_len}")
    print(f"Total score: {sum(scores)}")
    print(f"Average score: {sum(scores)/nb_len}")
    print(f"High score: {max(scores)}")
    print(f"Low score: {min(scores)}")
    print(f"Score range: {max(scores) - min(scores)}")


if __name__ == "__main__":
    print("=== Player Score Analytics ===")
    ft_score_analytics()
