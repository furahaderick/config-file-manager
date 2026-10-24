"""A small command-line interface."""

import argparse
from pathlib import Path

from config_manager.manager import convert_config, list_configs, read_config


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Manage JSON, CSV, and XML config files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    convert_parser = subparsers.add_parser(
        "convert", help="Convert between supported formats."
    )
    convert_parser.add_argument("source", type=Path)
    convert_parser.add_argument("destination", type=Path)

    list_parser = subparsers.add_parser(
        "list", help="Find config files in a directory."
    )
    list_parser.add_argument("directory", type=Path)
    list_parser.add_argument("--recursive", action="store_true")

    show_parser = subparsers.add_parser("show", help="Read and print a config file.")
    show_parser.add_argument("path", type=Path)

    args = parser.parse_args()
    if args.command == "convert":
        convert_config(args.source, args.destination)
        print(f"Converted {args.source} to {args.destination}")
    elif args.command == "list":
        for path in list_configs(args.directory, args.recursive):
            print(path)
    elif args.command == "show":
        for entry in read_config(args.path):
            print(entry)


if __name__ == "__main__":
    main()
