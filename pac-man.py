#!/usr/bin/env python3
"""Entry point for the game."""

import argparse
import sys


def parse_args() -> argparse.Namespace:
    """Read the configuration path from the command line."""
    parser = argparse.ArgumentParser(description="Play Pac-Man.")
    parser.add_argument("config", help="path to the JSON config file")
    return parser.parse_args()


def main() -> None:
    """Run the game, turning every failure into one clear sentence."""
    args = parse_args()
    try:
        from src_front import window
        window.run(args.config)
    except KeyboardInterrupt:
        print("\npac-man: stopped.", file=sys.stderr)
        sys.exit(1)
    except ImportError as error:
        print(f"pac-man: missing module ({error.name}). "
              "Run 'make install' first.", file=sys.stderr)
        sys.exit(1)
    except Exception as error:
        print(f"pac-man: {type(error).__name__}: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
