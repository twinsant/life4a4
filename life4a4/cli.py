"""CLI entry point: interactive REPL for the life4a4 coding agent."""

import argparse
import sys


def _print_tool_call(name: str, inputs: dict, result: str) -> None:
    preview = result[:200] + ("…" if len(result) > 200 else "")
    print(f"  \033[90m[{name}] {inputs}\033[0m")
    print(f"  \033[90m→ {preview}\033[0m")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="life4a4",
        description="A simple CLI coding agent",
    )
    parser.add_argument(
        "--model",
        default="claude-3-5-haiku-20241022",
        help="Claude model to use (default: claude-3-5-haiku-20241022)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    args = parser.parse_args()

    try:
        from life4a4.agent import Agent
    except ImportError as exc:
        print(f"Error: {exc}")
        print("Install dependencies with:  pip install anthropic")
        sys.exit(1)

    agent = Agent(model=args.model)

    print("\033[1mlife4a4\033[0m – a simple coding agent")
    print("Commands: /clear  /exit   Ctrl-C to quit")
    print("─" * 50)

    while True:
        try:
            user_input = input("\n\033[32m>\033[0m ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("/exit", "/quit"):
            print("Goodbye!")
            break

        if user_input.lower() == "/clear":
            agent.clear()
            print("\033[90m[Conversation cleared]\033[0m")
            continue

        try:
            response = agent.chat(user_input, on_tool_call=_print_tool_call)
            print(f"\n\033[1mAssistant:\033[0m {response}")
        except KeyboardInterrupt:
            print("\n\033[90m[Interrupted]\033[0m")
        except Exception as exc:  # noqa: BLE001
            print(f"\n\033[31mError: {exc}\033[0m")


if __name__ == "__main__":
    main()
