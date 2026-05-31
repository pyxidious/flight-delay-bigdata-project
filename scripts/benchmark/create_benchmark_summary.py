from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


INPUT_PATH = Path("results/benchmarks/benchmark_results.csv")
OUTPUT_DIR = Path("results/benchmarks")
DOCS_DIR = Path("docs")

DATASET_ORDER = ["100k", "500k", "1m", "3m", "7m", "10m", "14m"]
TECHNOLOGY_ORDER = ["spark_sql", "spark_core", "hive"]


def load_benchmark_results() -> pd.DataFrame:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Benchmark results not found: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    required_columns = {
        "technology",
        "analysis",
        "dataset_label",
        "input_file",
        "elapsed_seconds",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    df["dataset_label"] = pd.Categorical(
        df["dataset_label"],
        categories=DATASET_ORDER,
        ordered=True,
    )

    df["technology"] = pd.Categorical(
        df["technology"],
        categories=TECHNOLOGY_ORDER,
        ordered=True,
    )

    df["elapsed_seconds"] = pd.to_numeric(df["elapsed_seconds"], errors="raise")

    return df.sort_values(["analysis", "dataset_label", "technology"]).reset_index(drop=True)


def create_pivot(df: pd.DataFrame, analysis: str) -> pd.DataFrame:
    analysis_df = df[df["analysis"] == analysis]

    pivot = analysis_df.pivot_table(
        index="dataset_label",
        columns="technology",
        values="elapsed_seconds",
        observed=False,
    )

    pivot = pivot.reindex(DATASET_ORDER)
    pivot = pivot[TECHNOLOGY_ORDER]
    pivot = pivot.round(4)

    return pivot


def create_fastest_table(df: pd.DataFrame) -> pd.DataFrame:
    fastest_rows = []

    for (analysis, dataset_label), group in df.groupby(
        ["analysis", "dataset_label"],
        observed=False,
    ):
        if group.empty:
            continue

        fastest = group.sort_values("elapsed_seconds").iloc[0]
        slowest = group.sort_values("elapsed_seconds").iloc[-1]

        fastest_rows.append(
            {
                "analysis": analysis,
                "dataset_label": dataset_label,
                "fastest_technology": fastest["technology"],
                "fastest_seconds": round(float(fastest["elapsed_seconds"]), 4),
                "slowest_technology": slowest["technology"],
                "slowest_seconds": round(float(slowest["elapsed_seconds"]), 4),
                "speedup_vs_slowest": round(
                    float(slowest["elapsed_seconds"]) / float(fastest["elapsed_seconds"]),
                    4,
                ),
            }
        )

    return pd.DataFrame(fastest_rows)


def create_plot(pivot: pd.DataFrame, analysis: str, output_path: Path) -> None:
    ax = pivot.plot(kind="line", marker="o")

    ax.set_title(f"Benchmark {analysis}")
    ax.set_xlabel("Dataset size")
    ax.set_ylabel("Elapsed seconds")
    ax.grid(True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def write_markdown_summary(
    df: pd.DataFrame,
    analysis_1_pivot: pd.DataFrame,
    analysis_2_pivot: pd.DataFrame,
    fastest_table: pd.DataFrame,
) -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    summary_path = DOCS_DIR / "benchmark_summary.md"

    max_dataset = df["dataset_label"].dropna().max()

    lines = [
        "# Benchmark Summary",
        "",
        "## Scope",
        "",
        "The benchmark compares the execution time of the two implemented analyses across three technologies:",
        "",
        "- Spark SQL",
        "- Spark Core",
        "- Hive",
        "",
        "The benchmark includes both natural samples of increasing size and a replicated dataset.",
        "",
        "## Dataset sizes",
        "",
        "| Dataset label | Description |",
        "|---|---|",
        "| 100k | First 100,000 rows of the cleaned dataset |",
        "| 500k | First 500,000 rows of the cleaned dataset |",
        "| 1m | First 1,000,000 rows of the cleaned dataset |",
        "| 3m | First 3,000,000 rows of the cleaned dataset |",
        "| 7m | Full cleaned dataset |",
        "| 10m | Full cleaned dataset plus partial controlled replication up to 10,000,000 rows |",
        "| 14m | Full cleaned dataset replicated 2 times |",
        "",
        "## Analysis 1 results",
        "",
        analysis_1_pivot.to_markdown(),
        "",
        "## Analysis 2 results",
        "",
        analysis_2_pivot.to_markdown(),
        "",
        "## Fastest technology by analysis and dataset",
        "",
        fastest_table.to_markdown(index=False),
        "",
        "## Main observations",
        "",
        "- Spark Core is consistently competitive, especially on the larger datasets.",
        "- Spark SQL scales well and performs particularly well on the second analysis for large inputs.",
        "- Hive is competitive on small inputs but becomes slower on larger datasets, especially for the second analysis.",
        "- The replicated 14M-row dataset confirms the scalability trend beyond the original full dataset size.",
        "",
        "## Generated files",
        "",
        "- `results/benchmarks/benchmark_analysis_1_pivot.csv`",
        "- `results/benchmarks/benchmark_analysis_2_pivot.csv`",
        "- `results/benchmarks/benchmark_fastest_by_dataset.csv`",
        "- `results/benchmarks/benchmark_analysis_1.png`",
        "- `results/benchmarks/benchmark_analysis_2.png`",
        "",
    ]

    summary_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_benchmark_results()

    analysis_1_pivot = create_pivot(df, "analysis_1")
    analysis_2_pivot = create_pivot(df, "analysis_2")
    fastest_table = create_fastest_table(df)

    analysis_1_pivot.to_csv(OUTPUT_DIR / "benchmark_analysis_1_pivot.csv")
    analysis_2_pivot.to_csv(OUTPUT_DIR / "benchmark_analysis_2_pivot.csv")
    fastest_table.to_csv(OUTPUT_DIR / "benchmark_fastest_by_dataset.csv", index=False)

    create_plot(
        analysis_1_pivot,
        "Analysis 1",
        OUTPUT_DIR / "benchmark_analysis_1.png",
    )

    create_plot(
        analysis_2_pivot,
        "Analysis 2",
        OUTPUT_DIR / "benchmark_analysis_2.png",
    )

    write_markdown_summary(
        df=df,
        analysis_1_pivot=analysis_1_pivot,
        analysis_2_pivot=analysis_2_pivot,
        fastest_table=fastest_table,
    )

    print("Benchmark summary generated.")
    print(f"Markdown summary: {DOCS_DIR / 'benchmark_summary.md'}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
