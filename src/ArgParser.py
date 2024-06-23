import argparse
import os


def initArgs():
    parser = argparse.ArgumentParser(
        prog="Facial Identity Storage Project",
        description="This program is designed to store and use facial identity data.",
        # epilog="Text at the bottom of help message",
    )
    parser.add_argument(
        "--documentPhotoPath",
        help="specify document photo path",
        type=file_path,
    )
    parser.add_argument(
        "--clearDatabase",
        help="delete all records from database before executing rest of the program",
        action="store_true",
    )
    parser.add_argument(
        "--initDatabase",
        help="insert all sample data into database",
        action="store_true",
    )
    parser.add_argument(
        "--deleteRecord",
        help="delete record from database found by document photo path",
        action="store_true",
    )
    parser.add_argument(
        "--personPhotoPath",
        help="specify person photo path",
        type=file_path,
    )

    return parser.parse_args()


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"'{path}' is not a valid directory path")


def file_path(path):
    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"'{path}' is not a valid file path")
