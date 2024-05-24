import argparse
import os


def initArgs():
    parser = argparse.ArgumentParser(
        prog="Facial Identity Storage Project",
        description="This program is designed to store and use facial identity data.",
        # epilog="Text at the bottom of help message",
    )
    parser.add_argument(
        "--photosDir",
        help="specify directory with photos",
        required=True,
        type=dir_path,
    )
    parser.add_argument(
        "--configFile",
        help="specify configuration file",
        required=True,
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "--clearDatabase",
        help="delete all records from database before executing rest of the program",
        action="store_true",
    )

    return parser.parse_args()


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"'{path}' is not a valid directory path")
