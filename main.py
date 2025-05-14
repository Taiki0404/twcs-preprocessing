import argparse
from pathlib import Path

from src.twcs.table import TableGenerator
from src.twcs.twcs import TWCS

OUTPUT_DIR = "output"


def setup_parser():
    parser = argparse.ArgumentParser(description="TWCS file processing script")
    parser.add_argument(
        "--twcs-path",
        type=str,
        required=True,
        help="Path to the TWCS file",
    )
    return parser


def get_args():
    parser = setup_parser()
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    twcs = TWCS(args.twcs_path)
    table_generator = TableGenerator(twcs)

    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    table_generator.generate_tables_as_csv(OUTPUT_DIR)
