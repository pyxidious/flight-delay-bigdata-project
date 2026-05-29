from pathlib import Path
import pandas as pd
import numpy as np


RAW_DATASET_PATH = Path("data/raw/flight_data_2024.csv")
CLEANED_CSV_PATH = Path("data/cleaned/flights_clean.csv")
CLEANED_PARQUET_PATH = Path("data/cleaned/flights_clean.parquet")
REPORT_PATH = Path("docs/cleaning_report.md")

CHUNK_SIZE = 500_000

USE_COLUMNS = [
    "year",
    "month",
    "day_of_month",
    "day_of_week",
    "fl_date",
    "op_unique_carrier",
    "origin",
    "origin_city_name",
    "origin_state_nm",
    "dest",
    "dest_city_name",
    "dest_state_nm",
    "dep_delay",
    "arr_delay",
    "cancelled",
    "cancellation_code",
    "diverted",
    "carrier_delay",
    "weather_delay",
    "nas_delay",
    "security_delay",
    "late_aircraft_delay",
]

RENAME_COLUMNS = {
    "op_unique_carrier": "airline",
}

DELAY_CAUSE_COLUMNS = [
    "carrier_delay",
    "weather_delay",
    "nas_delay",
    "security_delay",
    "late_aircraft_delay",
]


def classify_departure_delay(delay: float) -> str:
    if pd.isna(delay):
        return "unknown"
    if delay < 15:
        return "low"
    if delay <= 60:
        return "medium"
    return "high"


def compute_main_delay_cause(df: pd.DataFrame) -> pd.Series:
    causes = df[DELAY_CAUSE_COLUMNS].fillna(0)

    max_values = causes.max(axis=1)
    max_columns = causes.idxmax(axis=1)

    main_cause = max_columns.str.replace("_delay", "", regex=False)

    main_cause = main_cause.where(max_values > 0, "NoDelayCause")
    main_cause = main_cause.where(df["cancelled"] == 0, "Cancelled")

    return main_cause


def clean_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    chunk = chunk.copy()

    chunk = chunk.rename(columns=RENAME_COLUMNS)

    before_rows = len(chunk)

    required_columns = [
        "year",
        "month",
        "fl_date",
        "airline",
        "origin",
        "dest",
        "cancelled",
        "diverted",
    ]

    chunk = chunk.dropna(subset=required_columns)

    chunk["year"] = chunk["year"].astype("int16")
    chunk["month"] = chunk["month"].astype("int8")
    chunk["day_of_month"] = chunk["day_of_month"].astype("int8")
    chunk["day_of_week"] = chunk["day_of_week"].astype("int8")

    chunk["airline"] = chunk["airline"].astype(str).str.strip().str.upper()
    chunk["origin"] = chunk["origin"].astype(str).str.strip().str.upper()
    chunk["dest"] = chunk["dest"].astype(str).str.strip().str.upper()

    chunk["origin_city_name"] = chunk["origin_city_name"].astype(str).str.strip()
    chunk["origin_state_nm"] = chunk["origin_state_nm"].astype(str).str.strip()
    chunk["dest_city_name"] = chunk["dest_city_name"].astype(str).str.strip()
    chunk["dest_state_nm"] = chunk["dest_state_nm"].astype(str).str.strip()

    chunk["cancelled"] = chunk["cancelled"].astype("int8")
    chunk["diverted"] = chunk["diverted"].astype("int8")

    numeric_columns = [
        "dep_delay",
        "arr_delay",
        "carrier_delay",
        "weather_delay",
        "nas_delay",
        "security_delay",
        "late_aircraft_delay",
    ]

    for column in numeric_columns:
        chunk[column] = pd.to_numeric(chunk[column], errors="coerce")

    for column in DELAY_CAUSE_COLUMNS:
        chunk[column] = chunk[column].fillna(0)

    chunk["route"] = chunk["origin"] + "-" + chunk["dest"]

    chunk["is_completed_flight"] = (
        (chunk["cancelled"] == 0)
        & (chunk["diverted"] == 0)
        & chunk["dep_delay"].notna()
        & chunk["arr_delay"].notna()
    ).astype("int8")

    chunk["dep_delay_band"] = chunk["dep_delay"].apply(classify_departure_delay)

    chunk["cancellation_code"] = chunk["cancellation_code"].fillna("")
    chunk["cancellation_code"] = chunk["cancellation_code"].astype(str).str.strip()

    chunk["cancellation_code"] = np.where(
        chunk["cancelled"] == 0,
        "NotCancelled",
        np.where(
            chunk["cancellation_code"] == "",
            "Unknown",
            chunk["cancellation_code"],
        ),
    )

    chunk["main_delay_cause"] = compute_main_delay_cause(chunk)

    selected_columns = [
        "year",
        "month",
        "day_of_month",
        "day_of_week",
        "fl_date",
        "airline",
        "origin",
        "origin_city_name",
        "origin_state_nm",
        "dest",
        "dest_city_name",
        "dest_state_nm",
        "route",
        "dep_delay",
        "arr_delay",
        "dep_delay_band",
        "cancelled",
        "cancellation_code",
        "diverted",
        "is_completed_flight",
        "carrier_delay",
        "weather_delay",
        "nas_delay",
        "security_delay",
        "late_aircraft_delay",
        "main_delay_cause",
    ]

    cleaned = chunk[selected_columns]

    after_rows = len(cleaned)
    removed_rows = before_rows - after_rows

    return cleaned, before_rows, after_rows, removed_rows


def write_report(stats: dict) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Cleaning Report",
        "",
        "## Input and output",
        "",
        f"- Raw dataset: `{RAW_DATASET_PATH}`",
        f"- Cleaned CSV: `{CLEANED_CSV_PATH}`",
        f"- Cleaned Parquet: `{CLEANED_PARQUET_PATH}`",
        "",
        "## Cleaning strategy",
        "",
        "The cleaning process applies the following operations:",
        "",
        "1. Select only columns relevant to the required analyses.",
        "2. Rename `op_unique_carrier` to `airline` for readability.",
        "3. Normalize carrier and airport codes to uppercase strings.",
        "4. Create a `route` column as `origin-dest`.",
        "5. Create `is_completed_flight` to identify non-cancelled and non-diverted flights with valid delay values.",
        "6. Create `dep_delay_band` with three bands: low, medium and high.",
        "7. Normalize `cancellation_code`, using `NotCancelled` for non-cancelled flights and `Unknown` for cancelled flights without a code.",
        "8. Create `main_delay_cause` from the largest available delay-cause column.",
        "9. Save the cleaned dataset both as CSV and Parquet.",
        "",
        "## Delay band definition",
        "",
        "| Band | Rule |",
        "|---|---|",
        "| low | `dep_delay < 15` |",
        "| medium | `15 <= dep_delay <= 60` |",
        "| high | `dep_delay > 60` |",
        "| unknown | missing `dep_delay` |",
        "",
        "## Row counts",
        "",
        f"- Input rows processed: **{stats['input_rows']:,}**",
        f"- Output rows written: **{stats['output_rows']:,}**",
        f"- Rows removed because of missing required keys: **{stats['removed_rows']:,}**",
        "",
        "## Notes for later analyses",
        "",
        "- Delay averages should be computed on rows where `is_completed_flight = 1`.",
        "- Cancellation rates should be computed on all rows.",
        "- `main_delay_cause` is derived from delay-cause columns and is mainly useful for delay-cause frequency reports.",
        "- `cancellation_code` is meaningful mainly when `cancelled = 1`.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if not RAW_DATASET_PATH.exists():
        raise FileNotFoundError(f"Raw dataset not found: {RAW_DATASET_PATH}")

    CLEANED_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    if CLEANED_CSV_PATH.exists():
        CLEANED_CSV_PATH.unlink()

    if CLEANED_PARQUET_PATH.exists():
        if CLEANED_PARQUET_PATH.is_dir():
            import shutil
            shutil.rmtree(CLEANED_PARQUET_PATH)
        else:
            CLEANED_PARQUET_PATH.unlink()

    total_input_rows = 0
    total_output_rows = 0
    total_removed_rows = 0

    print("Starting data preparation...")
    print(f"Input: {RAW_DATASET_PATH}")
    print(f"Chunk size: {CHUNK_SIZE:,}")
    print()

    first_chunk = True
    cleaned_chunks_for_parquet = []

    reader = pd.read_csv(
        RAW_DATASET_PATH,
        usecols=USE_COLUMNS,
        chunksize=CHUNK_SIZE,
        low_memory=False,
    )

    for chunk_index, chunk in enumerate(reader, start=1):
        cleaned, before_rows, after_rows, removed_rows = clean_chunk(chunk)

        cleaned.to_csv(
            CLEANED_CSV_PATH,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False,
        )

        cleaned_chunks_for_parquet.append(cleaned)

        total_input_rows += before_rows
        total_output_rows += after_rows
        total_removed_rows += removed_rows

        print(
            f"Chunk {chunk_index}: "
            f"input={before_rows:,}, output={after_rows:,}, removed={removed_rows:,}"
        )

        first_chunk = False

    print()
    print("Writing Parquet output...")
    full_cleaned_df = pd.concat(cleaned_chunks_for_parquet, ignore_index=True)
    full_cleaned_df.to_parquet(CLEANED_PARQUET_PATH, index=False)

    stats = {
        "input_rows": total_input_rows,
        "output_rows": total_output_rows,
        "removed_rows": total_removed_rows,
    }

    write_report(stats)

    print()
    print("Data preparation completed.")
    print(f"Cleaned CSV: {CLEANED_CSV_PATH}")
    print(f"Cleaned Parquet: {CLEANED_PARQUET_PATH}")
    print(f"Cleaning report: {REPORT_PATH}")
    print(f"Input rows: {total_input_rows:,}")
    print(f"Output rows: {total_output_rows:,}")
    print(f"Removed rows: {total_removed_rows:,}")


if __name__ == "__main__":
    main()
