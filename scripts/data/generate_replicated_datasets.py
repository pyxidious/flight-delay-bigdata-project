from pathlib import Path
import argparse
import shutil


DEFAULT_INPUT = Path("data/samples/flights_7m.csv")
DEFAULT_OUTPUT_DIR = Path("data/samples")


TARGET_DATA_ROWS = {
    "10m": 10_000_000,
}

REPLICATION_FACTORS = {
    "14m": 2,
    "21m": 3,
    "28m": 4,
}

AVAILABLE_LABELS = list(TARGET_DATA_ROWS.keys()) + list(REPLICATION_FACTORS.keys())


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Generate replicated benchmark datasets from the full cleaned sample. "
            "Some datasets target an exact row count, while others use full replication factors."
        )
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="Input CSV file to replicate. Expected to include a header.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where replicated datasets will be written.",
    )
    parser.add_argument(
        "--factors",
        nargs="+",
        default=["10m", "14m"],
        choices=AVAILABLE_LABELS,
        help="Dataset labels to generate.",
    )
    return parser.parse_args()


def count_data_rows(input_path: Path) -> int:
    with input_path.open("rb") as file:
        total_lines = sum(1 for _ in file)

    return max(total_lines - 1, 0)


def write_data_rows_without_header(
    source_path: Path,
    destination_file,
    max_rows: int | None = None,
) -> int:
    written_rows = 0

    with source_path.open("rb") as source_file:
        header = source_file.readline()

        if not header:
            return 0

        for line in source_file:
            if max_rows is not None and written_rows >= max_rows:
                break

            destination_file.write(line)
            written_rows += 1

    return written_rows


def generate_exact_row_dataset(
    input_path: Path,
    output_path: Path,
    target_rows: int,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open("rb") as source_file:
        header = source_file.readline()

        if not header:
            raise ValueError(f"Input file is empty: {input_path}")

    written_rows = 0

    with output_path.open("wb") as destination_file:
        destination_file.write(header)

        while written_rows < target_rows:
            remaining_rows = target_rows - written_rows
            rows_this_round = write_data_rows_without_header(
                source_path=input_path,
                destination_file=destination_file,
                max_rows=remaining_rows,
            )

            if rows_this_round == 0:
                raise ValueError(f"No data rows could be copied from {input_path}")

            written_rows += rows_this_round


def append_without_header(source_path: Path, destination_file) -> None:
    with source_path.open("rb") as source_file:
        header = source_file.readline()

        if not header:
            return

        shutil.copyfileobj(source_file, destination_file)


def generate_replicated_dataset(
    input_path: Path,
    output_path: Path,
    replication_factor: int,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open("rb") as source_file:
        header = source_file.readline()

        if not header:
            raise ValueError(f"Input file is empty: {input_path}")

        with output_path.open("wb") as destination_file:
            destination_file.write(header)

            source_file.seek(len(header))
            shutil.copyfileobj(source_file, destination_file)

            for _ in range(replication_factor - 1):
                append_without_header(input_path, destination_file)


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    input_rows = count_data_rows(input_path)

    print("Generating replicated benchmark datasets")
    print(f"Input: {input_path}")
    print(f"Input data rows: {input_rows:,}")
    print(f"Output directory: {output_dir}")
    print()

    for label in args.factors:
        output_path = output_dir / f"flights_{label}.csv"

        if label in TARGET_DATA_ROWS:
            expected_rows = TARGET_DATA_ROWS[label]

            print(f"Creating {output_path}")
            print(f"Target data rows: {expected_rows:,}")
            print("Strategy: full dataset plus partial controlled replication")

            generate_exact_row_dataset(
                input_path=input_path,
                output_path=output_path,
                target_rows=expected_rows,
            )

        else:
            replication_factor = REPLICATION_FACTORS[label]
            expected_rows = input_rows * replication_factor

            print(f"Creating {output_path}")
            print(f"Replication factor: {replication_factor}")
            print(f"Expected data rows: {expected_rows:,}")
            print("Strategy: full controlled replication")

            generate_replicated_dataset(
                input_path=input_path,
                output_path=output_path,
                replication_factor=replication_factor,
            )

        actual_rows = count_data_rows(output_path)

        if actual_rows != expected_rows:
            raise ValueError(
                f"Unexpected row count for {output_path}: "
                f"expected {expected_rows:,}, got {actual_rows:,}"
            )

        print(f"Written data rows: {actual_rows:,}")
        print()

    print("Replicated dataset generation completed.")


if __name__ == "__main__":
    main()