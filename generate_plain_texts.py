import argparse
from pathlib import Path

import pandas as pd

from src.generator.plaintext import PlainTextGenerator, TableHandler
from src.generator.rules import NumAuthorsRule, Rule

OUTPUT_DIR = "./output/txt"
TEXT_CSV_PATH = "./output/text.csv"
META_CSV_PATH = "./output/metadata.csv"
PAIR_CSV_PATH = "./output/pair.csv"


def to_txt(path: str, texts: list[str]) -> None:
    with open(path, "w") as f:
        for text in texts:
            f.write(text + "\n")


def argparse_args():
    parser = argparse.ArgumentParser(description="Generate plain text from dialog data.")
    parser.add_argument(
        "--dialog_id", type=int, required=True, help="The ID of the dialog to generate text for."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = argparse_args()

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    df_text = pd.read_csv(TEXT_CSV_PATH)
    df_meta = pd.read_csv(META_CSV_PATH)
    df_pair = pd.read_csv(PAIR_CSV_PATH)

    rules: list[Rule] = [NumAuthorsRule(num_authors=2)]

    table_handler = TableHandler(df_text, df_meta, df_pair)
    ptext_generator = PlainTextGenerator(table_handler, rules)

    plain_text = ptext_generator.generate_plain_texts(args.dialog_id)

    if plain_text is None:
        print("No valid dialog found.")
    else:
        path = f"{OUTPUT_DIR}/dialog_{args.dialog_id}.txt"
        to_txt(path, plain_text)
