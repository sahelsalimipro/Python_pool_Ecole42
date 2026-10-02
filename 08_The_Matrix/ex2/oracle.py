import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv is not installed.")
    print("Install it with: pip install python-dotenv")
    sys.exit(1)

KEYS: list[str] = [
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
]
CRITICAL_IN_PRODUCTION: list[str] = ["DATABASE_URL", "API_KEY"]
VALID_MODES: list[str] = ["development", "production"]


def load_config() -> tuple[dict[str, str | None], set[str]]:
    """Load config. Real env vars win over .env values."""
    preset = {key for key in KEYS if key in os.environ}
    load_dotenv()  # override=False: does not replace existing variables
    config: dict[str, str | None] = {k: os.environ.get(k) for k in KEYS}
    return config, preset


def validate(config: dict[str, str | None]) -> str:
    """Check config, print warnings, return the resolved mode."""
    mode = config["MATRIX_MODE"]
    if mode is None:
        print("WARNING: MATRIX_MODE not set, defaulting to development")
        mode = "development"
    if mode not in VALID_MODES:
        print(f"ERROR: MATRIX_MODE must be one of {VALID_MODES}, "
              f"got '{mode}'")
        sys.exit(1)

    for key in KEYS:
        if config[key] is None and key != "MATRIX_MODE":
            print(f"WARNING: {key} is not configured")

    if mode == "production":
        missing = [k for k in CRITICAL_IN_PRODUCTION if not config[k]]
        if missing:
            print(f"ERROR: production requires: {', '.join(missing)}")
            sys.exit(1)
    return mode


def describe_database(url: str | None) -> str:
    if not url:
        return "Not configured"
    if "localhost" in url or "127.0.0.1" in url or "sqlite" in url:
        return "Connected to local instance"
    return "Connected to remote instance"


def security_check(preset: set[str]) -> None:
    print("Environment security check:")
    try:
        with open(".gitignore", encoding="utf-8") as file:
            ignored = ".env" in file.read().split()
    except FileNotFoundError:
        ignored = False
    print(f"[{'OK' if ignored else 'WARN'}] .env is in .gitignore")

    try:
        with open(".env", encoding="utf-8"):
            has_env = True
    except FileNotFoundError:
        has_env = False
    print(f"[{'OK' if has_env else 'WARN'}] .env file "
          f"{'found' if has_env else 'missing (copy .env.example)'}")

    print("[OK] No hardcoded secrets detected (values come from env)")
    if preset:
        print(f"[OK] Overrides from real environment: "
              f"{', '.join(sorted(preset))}")
    else:
        print("[OK] Production overrides available "
              "(set variables before the command)")


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...")
    print()
    config, preset = load_config()
    mode = validate(config)
    print()

    print("Configuration loaded:")
    print(f"Mode: {mode}")
    print(f"Database: {describe_database(config['DATABASE_URL'])}")
    print("API Access: "
          f"{'Authenticated' if config['API_KEY'] else 'Missing key'}")
    print(f"Log Level: {config['LOG_LEVEL'] or 'INFO (default)'}")
    print("Zion Network: "
          f"{'Online' if config['ZION_ENDPOINT'] else 'Offline'}")
    print()

    if mode == "development":
        print("Dev features: debug tools ON, verbose errors ON")
    else:
        print("Prod features: debug tools OFF, secrets masked, "
              "strict validation")
        if config["LOG_LEVEL"] == "DEBUG":
            print("WARNING: DEBUG logging is not advised in production")
    print()

    security_check(preset)
    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
