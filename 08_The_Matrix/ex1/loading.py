import sys
from importlib import import_module
from importlib.metadata import PackageNotFoundError, version
from typing import Any

REQUIRED: dict[str, str] = {
    "pandas": "Data manipulation",
    "numpy": "Numerical computation",
    "matplotlib": "Visualization",
}


def check_dependencies() -> dict[str, Any]:
    """Try to import each package; report status; exit if any missing."""
    print("Checking dependencies:")
    modules: dict[str, Any] = {}
    missing: list[str] = []

    for name, purpose in REQUIRED.items():
        try:
            modules[name] = import_module(name)
            print(f"[OK] {name} ({version(name)}) - {purpose} ready")
        except (ImportError, PackageNotFoundError):
            missing.append(name)
            print(f"[MISSING] {name} - {purpose} unavailable")

    if missing:
        print()
        print(f"ERROR: missing packages: {', '.join(missing)}")
        print("Install them with one of the following:")
        print("  pip:    pip install -r requirements.txt")
        print("  Poetry: poetry install")
        print("          poetry run python loading.py")
        sys.exit(1)
    return modules


def compare_managers(modules: dict[str, Any]) -> None:
    """Show installed versions and the pip vs Poetry differences."""
    in_venv = sys.prefix != sys.base_prefix
    print()
    print("Package versions in this environment:")
    for name in REQUIRED:
        print(f"  {name:<12} {version(name)}")
    print(f"Virtual environment active: {in_venv}")
    print()
    print("pip vs Poetry:")
    print("  pip    -> requirements.txt, no lock file, manual venv")
    print("  Poetry -> pyproject.toml, poetry.lock, automatic venv")


def analyze(modules: dict[str, Any]) -> str:
    """Simulate Matrix data with numpy, analyze with pandas, plot."""
    np = modules["numpy"]
    pd = modules["pandas"]
    mpl = modules["matplotlib"]
    mpl.use("Agg")
    plt = import_module("matplotlib.pyplot")

    print()
    print("Analyzing Matrix data...")
    rng = np.random.default_rng(42)
    size = 1000
    print(f"Processing {size} data points...")

    data = pd.DataFrame(
        {
            "tick": np.arange(size),
            "signal": np.cumsum(rng.normal(0, 1, size)),
        }
    )
    data["trend"] = data["signal"].rolling(window=50).mean()

    print(f"Mean signal: {data['signal'].mean():.2f}")
    print(f"Std deviation: {data['signal'].std():.2f}")

    print("Generating visualization...")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data["tick"], data["signal"], label="Matrix signal",
            alpha=0.5)
    ax.plot(data["tick"], data["trend"], label="Trend (50 ticks)",
            color="green")
    ax.set_title("Matrix Data Analysis")
    ax.set_xlabel("Tick")
    ax.set_ylabel("Signal")
    ax.legend()
    output = "matrix_analysis.png"
    fig.savefig(output)
    plt.close(fig)
    return output


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    print()
    modules = check_dependencies()
    output = analyze(modules)
    compare_managers(modules)
    print()
    print("Analysis complete!")
    print(f"Results saved to: {output}")


if __name__ == "__main__":
    main()
