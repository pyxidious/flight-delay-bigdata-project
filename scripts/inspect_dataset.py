from pathlib import Path
import pandas as pd


RAW_DATASET_PATH = Path("data/raw/flight_data_2024.csv")
REPORT_PATH = Path("docs/dataset_inspection.md")
SAMPLE_SIZE = 10_000


def format_bytes(size_in_bytes: int) -> str:
    """Convert bytes into a human-readable format."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_in_bytes)

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} PB"


def markdown_table_from_dataframe(df: pd.DataFrame, max_rows: int = 20) -> str:
    """Convert a small DataFrame into a Markdown table."""
    return df.head(max_rows).to_markdown(index=False)


def identify_candidate_columns(columns: list[str]) -> dict[str, list[str]]:
    """
    Identify possible useful columns for the required analyses.

    The mapping is intentionally conservative:
    it avoids treating delay-related columns or flight numbers as airline identifiers.
    """
    expected_columns_by_category = {
        "airline_or_carrier": [
            "op_unique_carrier",
        ],
        "flight_number": [
            "op_carrier_fl_num",
        ],
        "origin_airport": [
            "origin",
            "origin_city_name",
            "origin_state_nm",
        ],
        "destination_airport": [
            "dest",
            "dest_city_name",
            "dest_state_nm",
        ],
        "date_or_month": [
            "year",
            "month",
            "day_of_month",
            "day_of_week",
            "fl_date",
        ],
        "departure_delay": [
            "dep_delay",
        ],
        "arrival_delay": [
            "arr_delay",
        ],
        "cancelled": [
            "cancelled",
        ],
        "cancellation_code": [
            "cancellation_code",
        ],
        "diverted": [
            "diverted",
        ],
        "delay_causes": [
            "carrier_delay",
            "weather_delay",
            "nas_delay",
            "security_delay",
            "late_aircraft_delay",
        ],
        "time_columns": [
            "crs_dep_time",
            "dep_time",
            "wheels_off",
            "wheels_on",
            "crs_arr_time",
            "arr_time",
        ],
        "duration_or_distance": [
            "crs_elapsed_time",
            "actual_elapsed_time",
            "air_time",
            "distance",
        ],
    }

    available_columns = set(columns)

    candidates = {
        category: [
            column
            for column in expected_columns
            if column in available_columns
        ]
        for category, expected_columns in expected_columns_by_category.items()
    }

    return candidates


def main() -> None:
    if not RAW_DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_DATASET_PATH}. "
            "Make sure the CSV file is placed in data/raw/."
        )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    file_size = RAW_DATASET_PATH.stat().st_size

    print("Reading dataset sample...")
    sample_df = pd.read_csv(RAW_DATASET_PATH, nrows=SAMPLE_SIZE, low_memory=False)

    print("Counting total rows. This may take a little while...")
    with RAW_DATASET_PATH.open("r", encoding="utf-8", errors="replace") as file:
        total_lines = sum(1 for _ in file)

    total_rows = total_lines - 1
    total_columns = len(sample_df.columns)

    dtypes_df = (
        sample_df.dtypes.astype(str)
        .reset_index()
        .rename(columns={"index": "column", 0: "inferred_type_on_sample"})
    )

    nulls_df = (
        sample_df.isna().sum()
        .reset_index()
        .rename(columns={"index": "column", 0: "null_count_in_sample"})
    )
    nulls_df["null_percentage_in_sample"] = (
        nulls_df["null_count_in_sample"] / len(sample_df) * 100
    ).round(2)

    nulls_df = nulls_df.sort_values(
        by="null_percentage_in_sample",
        ascending=False
    )

    candidate_columns = identify_candidate_columns(sample_df.columns.tolist())

    duplicated_rows_in_sample = sample_df.duplicated().sum()
    memory_usage_sample = sample_df.memory_usage(deep=True).sum()

    report_lines = []

    report_lines.append("# Dataset Inspection")
    report_lines.append("")
    report_lines.append("## Source")
    report_lines.append("")
    report_lines.append(f"- Dataset path: `{RAW_DATASET_PATH}`")
    report_lines.append(f"- File size: **{format_bytes(file_size)}**")
    report_lines.append(f"- Sample size used for inspection: **{SAMPLE_SIZE:,} rows**")
    report_lines.append("")
    report_lines.append("## Shape")
    report_lines.append("")
    report_lines.append(f"- Total rows, excluding header: **{total_rows:,}**")
    report_lines.append(f"- Total columns: **{total_columns}**")
    report_lines.append("")
    report_lines.append("## Columns")
    report_lines.append("")
    for col in sample_df.columns:
        report_lines.append(f"- `{col}`")
    report_lines.append("")
    report_lines.append("## Inferred data types on sample")
    report_lines.append("")
    report_lines.append(markdown_table_from_dataframe(dtypes_df, max_rows=100))
    report_lines.append("")
    report_lines.append("## Missing values on sample")
    report_lines.append("")
    report_lines.append(markdown_table_from_dataframe(nulls_df, max_rows=100))
    report_lines.append("")
    report_lines.append("## Candidate columns for project analyses")
    report_lines.append("")
    report_lines.append(
        "The following columns are automatically identified as possible candidates. "
        "They will be manually verified before implementing the cleaning script."
    )
    report_lines.append("")

    for category, matches in candidate_columns.items():
        report_lines.append(f"### {category}")
        report_lines.append("")
        if matches:
            for match in matches:
                report_lines.append(f"- `{match}`")
        else:
            report_lines.append("- No candidate column detected")
        report_lines.append("")

    report_lines.append("## Duplicate rows on sample")
    report_lines.append("")
    report_lines.append(f"- Duplicate rows in sample: **{duplicated_rows_in_sample:,}**")
    report_lines.append("")
    report_lines.append("## Memory usage on sample")
    report_lines.append("")
    report_lines.append(f"- Sample memory usage: **{format_bytes(memory_usage_sample)}**")
    report_lines.append("")
    report_lines.append("## First 10 rows")
    report_lines.append("")
    report_lines.append(markdown_table_from_dataframe(sample_df.head(10), max_rows=10))
    report_lines.append("")
    report_lines.append("## Notes")
    report_lines.append("")
    report_lines.append(
        "- This inspection is based on a sample for data types and missing values."
    )
    report_lines.append(
        "- The total number of rows is computed by scanning the full CSV file."
    )
    report_lines.append(
        "- Final cleaning decisions will be documented after verifying the relevant columns."
    )
    report_lines.append("")

    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")

    print()
    print("Dataset inspection completed.")
    print(f"Dataset path: {RAW_DATASET_PATH}")
    print(f"File size: {format_bytes(file_size)}")
    print(f"Total rows: {total_rows:,}")
    print(f"Total columns: {total_columns}")
    print(f"Report saved to: {REPORT_PATH}")
    print()
    print("Candidate columns:")
    for category, matches in candidate_columns.items():
        print(f"- {category}: {matches if matches else 'not detected'}")


if __name__ == "__main__":
    main()
