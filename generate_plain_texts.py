import argparse
from pathlib import Path

from src.twcs.output.plaintext import PlainTextGenerator
from src.twcs.output.rules import NumAuthorsRule, RuleSet
from src.twcs.table import MetadataTable, SequenceTable, TableHandler, TextTable

OUTPUT_DIR = "./output/txt"
TEXT_CSV_PATH = "./output/text.csv"
META_CSV_PATH = "./output/metadata.csv"
SEQ_CSV_PATH = "./output/seq.csv"


def read_file_of_dialog_ids(path: str) -> list[int]:
    with open(path, "r") as f:
        lines = f.readlines()
    return [int(line.strip()) for line in lines]


def to_txt(path: str, texts: list[str]) -> None:
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

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    text_table = TextTable(TEXT_CSV_PATH)
    meta_table = MetadataTable(META_CSV_PATH)
    seq_table = SequenceTable(SEQ_CSV_PATH)

    rules = RuleSet()
    rules.add(NumAuthorsRule(num_authors=2))

    table_handler = TableHandler(text_table, meta_table, seq_table)
    ptext_generator = PlainTextGenerator(table_handler, rules)

    for dialog_id in read_file_of_dialog_ids(args.input_path):
        plain_text = ptext_generator.generate_plain_texts(dialog_id)

        if plain_text is None:
            print(f"Dialog ID {dialog_id} not found in the data.")
            # TODO: logging
        else:
            path = f"{OUTPUT_DIR}/dialog_{dialog_id}.txt"
            to_txt(path, plain_text)
