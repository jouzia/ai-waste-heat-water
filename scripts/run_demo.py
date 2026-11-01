"""Run the presentation-safe Research 2 demo."""
import json

from ai_water.demo import run_demo


def main() -> None:
    print(json.dumps(run_demo(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
