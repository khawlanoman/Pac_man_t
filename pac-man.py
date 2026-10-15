#!/usr/bin/env python3
"""Entry point for the game."""

import argparse
from src_front import window


def parse_args():
    """Read the configuration path from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("config", default="config.json")
    return parser.parse_args()


def main() -> None:
    """Run the game."""
    args = parse_args()
    window.run(args.config)


if __name__ == "__main__":
    main()