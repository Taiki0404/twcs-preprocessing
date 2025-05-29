import argparse
from pathlib import Path

from src.twcs.rules import SequenceLength
from src.twcs.sampling.sampler import Sampler
from src.twcs.table import TableHandler

OUTPUT_DIR = "./output/samples"
TWEET_META_CSV_PATH = "./output/tweet_meta.csv"
DIALOT_META_CSV_PATH = "./output/dialog_meta.csv"
TEXT_CSV_PATH = "./output/text.csv"
SEQ_CSV_PATH = "./output/seq.csv"


def to_txt(path: str, ids: list[int]) -> None:
    with open(path, "w") as f:
        for i in ids:
            f.write(str(i) + "\n")


def argparse_args():
    parser = argparse.ArgumentParser(description="Sample dialog data.")
    parser.add_argument(
        "--company", "-c", type=str, required=True, help="Company name to sample from."
    )
    parser.add_argument(
        "--n-samples", "-n", type=int, required=True, help="Number of samples to generate."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = argparse_args()

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    table_handler = TableHandler(
        TWEET_META_CSV_PATH, DIALOT_META_CSV_PATH, TEXT_CSV_PATH, SEQ_CSV_PATH
    )
    sampler = Sampler(table_handler)

    seq_len = SequenceLength(min=2, max=6)

    samples = sampler.sample_dialog_id_by_author(
        author_id=args.company, n_samples=args.n_samples, n_authors=2, seq_len=seq_len
    )
    sorted_samples = sorted(samples)

    to_txt(f"{OUTPUT_DIR}/{args.company}_{len(samples)}.txt", sorted_samples)
