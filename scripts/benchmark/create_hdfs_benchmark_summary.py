from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import pandas as pd


INPUT_PATH = Path("results/benchmarks_hdfs/hdfs_benchmark_results.csv")
OUTPUT_DIR = Path("results/benchmarks_hdfs")
SUMMARY_PATH = Path("docs/hdfs_benchmark_summary.md")
DATASET_ORDER = ["100k", "500k", "1m", "3m", "7m", "10m", "14m"]
TECHNOLOGY_ORDER = ["spark_sql", "spark_core", "hive"]


def load_results() -> pd.DataFrame:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"HDFS benchmark results not found: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)
    required_columns = {
        "technology",
        "analysis",
        "dataset_label",
        "input_path",
        "output_path",
        "elapsed_seconds",
        "status",
    }
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    df["elapsed_seconds"] = pd.to_numeric(df["elapsed_seconds"], errors="coerce")
    df["dataset_label"] = pd.Categorical(df["dataset_label"], DATASET_ORDER, ordered=True)
    df["technology"] = pd.Categorical(df["technology"], TECHNOLOGY_ORDER, ordered=True)
    return df.sort_values(["analysis", "dataset_label", "technology"]).reset_index(drop=True)


def create_pivot(successful_df: pd.DataFrame, analysis: str) -> pd.DataFrame:
    pivot = successful_df[successful_df["analysis"] == analysis].pivot_table(
        index="dataset_label",
        columns="technology",
        values="elapsed_seconds",
        observed=False,
    )
    return pivot.reindex(DATASET_ORDER).reindex(columns=TECHNOLOGY_ORDER).dropna(how="all").round(4)


def create_fastest_table(successful_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (analysis, dataset_label), group in successful_df.groupby(
        ["analysis", "dataset_label"], observed=True
    ):
        if group.empty:
            continue
        fastest = group.loc[group["elapsed_seconds"].idxmin()]
        slowest = group.loc[group["elapsed_seconds"].idxmax()]
        rows.append(
            {
                "analysis": analysis,
                "dataset_label": dataset_label,
                "fastest_technology": fastest["technology"],
                "fastest_seconds": round(float(fastest["elapsed_seconds"]), 4),
                "slowest_technology": slowest["technology"],
                "slowest_seconds": round(float(slowest["elapsed_seconds"]), 4),
            }
        )
    return pd.DataFrame(rows)


def create_plot(pivot: pd.DataFrame, title: str, output_path: Path) -> None:
    if pivot.empty:
        warnings.warn(f"Skipping empty plot: {title}", stacklevel=2)
        return
    ax = pivot.plot(kind="line", marker="o")
    ax.set_title(title)
    ax.set_xlabel("Dataset size")
    ax.set_ylabel("Elapsed seconds")
    ax.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def markdown_table(df: pd.DataFrame, *, index: bool = True) -> str:
    if df.empty:
        return "No rows available."
    return df.fillna("missing").to_markdown(index=index)


def write_summary(
    analysis_1_pivot: pd.DataFrame,
    analysis_2_pivot: pd.DataFrame,
    fastest_table: pd.DataFrame,
    failed_df: pd.DataFrame,
) -> None:
    failed_columns = ["technology", "analysis", "dataset_label", "input_path", "output_path"]
    lines = [
        "# HDFS Benchmark Summary",
        "",
        "## Methodological notes",
        "",
        "- Input and output are stored on local HDFS.",
        "- HDFS runs in pseudo-distributed mode with replication factor 1.",
        "- Spark runs with `local[*]` while using HDFS storage.",
        "- Hive runs through HiveServer2 and local Hadoop MapReduce with HDFS input and output.",
        "- Timings measure each job runner, excluding HDFS upload and service startup.",
        "- The 10m and 14m datasets use controlled replication.",
        "",
        "## Analysis 1 results",
        "",
        markdown_table(analysis_1_pivot),
        "",
        "## Analysis 2 results",
        "",
        markdown_table(analysis_2_pivot),
        "",
        "## Fastest technology by dataset",
        "",
        markdown_table(fastest_table, index=False),
        "",
        "## Failed jobs",
        "",
        markdown_table(failed_df[failed_columns], index=False),
        "",
    ]
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = load_results()
    successful_df = df[df["status"] == "success"].copy()
    failed_df = df[df["status"] != "success"].copy()

    analysis_1_pivot = create_pivot(successful_df, "analysis_1")
    analysis_2_pivot = create_pivot(successful_df, "analysis_2")
    fastest_table = create_fastest_table(successful_df)

    analysis_1_pivot.to_csv(OUTPUT_DIR / "hdfs_benchmark_analysis_1_pivot.csv")
    analysis_2_pivot.to_csv(OUTPUT_DIR / "hdfs_benchmark_analysis_2_pivot.csv")
    fastest_table.to_csv(OUTPUT_DIR / "hdfs_benchmark_fastest_by_dataset.csv", index=False)
    create_plot(analysis_1_pivot, "HDFS Benchmark Analysis 1", OUTPUT_DIR / "hdfs_benchmark_analysis_1.png")
    create_plot(analysis_2_pivot, "HDFS Benchmark Analysis 2", OUTPUT_DIR / "hdfs_benchmark_analysis_2.png")
    write_summary(analysis_1_pivot, analysis_2_pivot, fastest_table, failed_df)
    print(f"HDFS benchmark summary generated: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
