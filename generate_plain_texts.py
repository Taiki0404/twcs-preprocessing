import argparse
from datetime import datetime
from pathlib import Path

from src.twcs.output.plaintext import PlainTextGenerator
from src.twcs.table import TableHandler

OUTPUT_DIR = "./output/txt"
TWEET_META_CSV_PATH = "./output/tweet_meta.csv"
DIALOT_META_CSV_PATH = "./output/dialog_meta.csv"
TEXT_CSV_PATH = "./output/text.csv"
SEQ_CSV_PATH = "./output/seq.csv"


def read_file_of_dialog_ids(path: str) -> list[int]:
    with open(path, "r") as f:
        lines = f.readlines()
    return [int(line.strip()) for line in lines]


def generate_dir_name() -> str:
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")


def to_txt(path: str, texts: list[str]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        for text in texts:
            f.write(text + "\n")


def argparse_args():
    parser = argparse.ArgumentParser(description="Generate plain text from dialog data.")
    parser.add_argument(
        "--input-path",
        type=str,
        default=None,
        help="Path to a file containing a list of dialog IDs.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = argparse_args()
    dir_name = generate_dir_name()

    table_handler = TableHandler(
        TWEET_META_CSV_PATH, DIALOT_META_CSV_PATH, TEXT_CSV_PATH, SEQ_CSV_PATH
    )
    ptext_generator = PlainTextGenerator(table_handler)

    for dialog_id in read_file_of_dialog_ids(args.input_path):
        plain_text = ptext_generator.generate_plain_texts(dialog_id)

        if plain_text is None:
            print(f"Dialog ID {dialog_id} not found in the data.")
            continue
            # TODO: logging

        path = f"{OUTPUT_DIR}/{dir_name}/dialog_{dialog_id}.txt"
        to_txt(path, plain_text)
