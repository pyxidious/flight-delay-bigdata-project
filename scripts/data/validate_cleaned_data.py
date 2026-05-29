from pathlib import Path
import pandas as pd


CLEANED_CSV_PATH = Path("data/cleaned/flights_clean.csv")
REPORT_PATH = Path("docs/cleaned_data_validation.md")


def markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
    return df.head(max_rows).to_markdown(index=False)


def main() -> None:
    if not CLEANED_CSV_PATH.exists():
        raise FileNotFoundError(f"Cleaned dataset not found: {CLEANED_CSV_PATH}")

    print("Reading cleaned dataset...")
    df = pd.read_csv(CLEANED_CSV_PATH, low_memory=False)

    print("Computing validation statistics...")

    shape_info = {
        "rows": len(df),
        "columns": len(df.columns),
    }

    columns_df = pd.DataFrame({"column": df.columns})

    nulls_df = (
        df.isna().sum()
        .reset_index()
        .rename(columns={"index": "column", 0: "null_count"})
    )
    nulls_df["null_percentage"] = (nulls_df["null_count"] / len(df) * 100).round(4)
    nulls_df = nulls_df.sort_values("null_percentage", ascending=False)

    delay_band_df = (
        df["dep_delay_band"]
        .value_counts(dropna=False)
        .reset_index()
    )
    delay_band_df.columns = ["dep_delay_band", "count"]
    delay_band_df["percentage"] = (delay_band_df["count"] / len(df) * 100).round(4)

    status_df = pd.DataFrame(
        {
            "metric": [
                "completed_flights",
                "cancelled_flights",
                "diverted_flights",
            ],
            "count": [
                int((df["is_completed_flight"] == 1).sum()),
                int((df["cancelled"] == 1).sum()),
                int((df["diverted"] == 1).sum()),
            ],
        }
    )
    status_df["percentage"] = (status_df["count"] / len(df) * 100).round(4)

    delay_stats_df = df.loc[df["is_completed_flight"] == 1, ["dep_delay", "arr_delay"]].describe().T
    delay_stats_df = delay_stats_df.reset_index().rename(columns={"index": "metric"})

    cancellation_code_df = (
        df["cancellation_code"]
        .value_counts(dropna=False)
        .head(20)
        .reset_index()
    )
    cancellation_code_df.columns = ["cancellation_code", "count"]
    cancellation_code_df["percentage"] = (
        cancellation_code_df["count"] / len(df) * 100
    ).round(4)

    main_delay_cause_df = (
        df["main_delay_cause"]
        .value_counts(dropna=False)
        .reset_index()
    )
    main_delay_cause_df.columns = ["main_delay_cause", "count"]
    main_delay_cause_df["percentage"] = (
        main_delay_cause_df["count"] / len(df) * 100
    ).round(4)

    airline_count = df["airline"].nunique()
    origin_count = df["origin"].nunique()
    dest_count = df["dest"].nunique()
    route_count = df["route"].nunique()

    lines = [
        "# Cleaned Data Validation",
        "",
        "## Shape",
        "",
        f"- Rows: **{shape_info['rows']:,}**",
        f"- Columns: **{shape_info['columns']}**",
        "",
        "## Cardinalities",
        "",
        f"- Airlines: **{airline_count:,}**",
        f"- Origin airports: **{origin_count:,}**",
        f"- Destination airports: **{dest_count:,}**",
        f"- Routes: **{route_count:,}**",
        "",
        "## Columns",
        "",
        markdown_table(columns_df, max_rows=100),
        "",
        "## Missing values",
        "",
        markdown_table(nulls_df, max_rows=100),
        "",
        "## Departure delay bands",
        "",
        markdown_table(delay_band_df),
        "",
        "## Flight status",
        "",
        markdown_table(status_df),
        "",
        "## Delay statistics on completed flights",
        "",
        markdown_table(delay_stats_df),
        "",
        "## Cancellation codes",
        "",
        markdown_table(cancellation_code_df),
        "",
        "## Main delay causes",
        "",
        markdown_table(main_delay_cause_df),
        "",
    ]

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print("Validation completed.")
    print(f"Rows: {shape_info['rows']:,}")
    print(f"Columns: {shape_info['columns']}")
    print(f"Airlines: {airline_count:,}")
    print(f"Origin airports: {origin_count:,}")
    print(f"Routes: {route_count:,}")
    print(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
