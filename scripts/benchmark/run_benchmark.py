#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import os
import shlex
import shutil
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
JDBC_URL = "jdbc:hive2://localhost:10000/default"
HDFS_INPUT_BASE = "hdfs://localhost:9000/flight-delay-project/input"
HDFS_OUTPUT_BASE = "hdfs://localhost:9000/flight-delay-project/output_benchmark"
DATASET_ROWS = {
    "100k": 100_000,
    "500k": 500_000,
    "1m": 1_000_000,
    "3m": 3_000_000,
    "7m": 7_079_081,
    "10m": 10_000_000,
    "14m": 14_158_162,
}
DATASET_ORDER = list(DATASET_ROWS)
TECHNOLOGY_ORDER = ["hive", "spark_sql", "spark_core"]
ANALYSIS_ORDER = ["analysis_1", "analysis_2", "analysis_3"]
RUN_FIELDS = [
    "timestamp",
    "campaign_tag",
    "technology",
    "analysis",
    "dataset_label",
    "run_type",
    "run_index",
    "input_rows",
    "input_bytes_hdfs",
    "output_path",
    "elapsed_seconds_job_time",
    "status",
    "error_log_path",
    "command",
    "output_part_files_count",
    "output_rows",
]
SUMMARY_FIELDS = [
    "technology",
    "analysis",
    "dataset_label",
    "input_rows",
    "input_bytes_hdfs",
    "successful_runs",
    "failed_runs",
    "mean_seconds",
    "median_seconds",
    "stddev_seconds",
    "min_seconds",
    "max_seconds",
    "best_run_seconds",
    "output_rows",
    "output_part_files_count",
]
GENERATED_FILENAMES = [
    "benchmark_runs.csv",
    "benchmark_summary.csv",
    "benchmark_analysis_1.png",
    "benchmark_analysis_2.png",
    "benchmark_analysis_3.png",
    "benchmark_report.md",
    "session.log",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Official HDFS repeated benchmark campaign."
    )
    parser.add_argument("--datasets", nargs="+", choices=DATASET_ORDER, default=DATASET_ORDER)
    parser.add_argument("--analyses", nargs="+", choices=ANALYSIS_ORDER, default=ANALYSIS_ORDER)
    parser.add_argument(
        "--results-dir", default="results/benchmark"
    )
    parser.add_argument(
        "--campaign-tag",
        default=f"benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
    )
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-hive", action="store_true")
    parser.add_argument("--skip-spark-sql", action="store_true")
    parser.add_argument("--skip-spark-core", action="store_true")
    parser.add_argument("--yes", action="store_true")
    return parser.parse_args()


def command_text(command: list[str]) -> str:
    return shlex.join(command)


def run(
    command: list[str],
    *,
    check: bool = True,
    capture: bool = True,
    log_path: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as log:
            log.write(f"\n$ {command_text(command)}\n")
            return subprocess.run(
                command,
                cwd=PROJECT_ROOT,
                check=check,
                text=True,
                stdout=log,
                stderr=subprocess.STDOUT,
            )
    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=check,
        text=True,
        capture_output=capture,
    )


def hdfs(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["hdfs", "dfs", *args], check=check)


def beeline(*args: str) -> list[str]:
    return ["beeline", "-u", JDBC_URL, *args]


def selected_technologies(args: argparse.Namespace) -> list[str]:
    skipped = {
        "hive": args.skip_hive,
        "spark_sql": args.skip_spark_sql,
        "spark_core": args.skip_spark_core,
    }
    return [technology for technology in TECHNOLOGY_ORDER if not skipped[technology]]


def input_path(dataset: str) -> str:
    return f"{HDFS_INPUT_BASE}/{dataset}/flights.csv"


def input_dir(dataset: str) -> str:
    return f"{HDFS_INPUT_BASE}/{dataset}"


def output_path(
    tag: str, technology: str, analysis: str, dataset: str, run_index: int
) -> str:
    return f"{HDFS_OUTPUT_BASE}/{tag}/{technology}/{analysis}_{dataset}_repeated_{run_index}"


def job_command(technology: str, analysis: str, dataset: str, target: str) -> list[str]:
    if technology == "hive":
        sql = {
            "analysis_1": "hive/analysis_1_airline_stats.sql",
            "analysis_2": "hive/analysis_2_airport_month_delay_report.sql",
            "analysis_3": "hive/analysis_3_airline_airport_ranking.sql",
        }[analysis]
        return beeline("--hiveconf", f"output_dir={target}", "-f", sql)

    spark_submit = ["spark-submit", "--master", "local[*]"]
    if driver_memory := os.environ.get("SPARK_DRIVER_MEMORY"):
        spark_submit.extend(["--driver-memory", driver_memory])
    if technology == "spark_sql":
        if shuffle_partitions := os.environ.get("SPARK_SQL_SHUFFLE_PARTITIONS"):
            spark_submit.extend(
                ["--conf", f"spark.sql.shuffle.partitions={shuffle_partitions}"]
            )
    if extra_conf := os.environ.get("SPARK_SUBMIT_EXTRA_CONF"):
        spark_submit.extend(shlex.split(extra_conf))

    base = "spark_sql" if technology == "spark_sql" else "spark_core"
    script = {
        "analysis_1": f"{base}/analysis_1_airline_stats.py",
        "analysis_2": f"{base}/analysis_2_airport_month_delay_report.py",
        "analysis_3": f"{base}/analysis_3_airline_airport_ranking.py",
    }[analysis]
    return [*spark_submit, script, "--input", input_path(dataset), "--output", target]


def prepare_hive_command(dataset: str) -> list[str]:
    return beeline(
        "--hiveconf",
        f"input_dir={input_dir(dataset)}",
        "-f",
        "hive/prepare_flights_table.sql",
    )


def archive_previous_results(results_dir: Path, reset: bool) -> None:
    existing = [results_dir / name for name in GENERATED_FILENAMES if (results_dir / name).exists()]
    if not existing:
        return
    if not reset:
        names = ", ".join(path.name for path in existing)
        raise RuntimeError(
            f"Results already exist in {results_dir}: {names}. "
            "Use --reset to archive them before starting a new campaign."
        )
    archive_dir = results_dir / "archive" / datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_dir.mkdir(parents=True, exist_ok=False)
    for path in existing:
        shutil.move(str(path), archive_dir / path.name)
    print(f"Archived previous generated files in {archive_dir}")


def append_session(session_log: Path, text: str) -> None:
    session_log.parent.mkdir(parents=True, exist_ok=True)
    with session_log.open("a", encoding="utf-8") as log:
        log.write(text)
        if not text.endswith("\n"):
            log.write("\n")


def snapshot_command(session_log: Path, label: str, command: list[str]) -> None:
    append_session(session_log, f"\n===== {label}: {command_text(command)} =====")
    completed = run(command, check=False)
    append_session(session_log, completed.stdout or "")
    append_session(session_log, completed.stderr or "")


def meminfo_kib(name: str) -> int:
    with Path("/proc/meminfo").open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith(f"{name}:"):
                return int(line.split()[1])
    raise RuntimeError(f"Missing {name} in /proc/meminfo")


def hiveserver2_pids() -> list[str]:
    completed = run(
        ["pgrep", "-f", "org[.]apache[.]hive[.]service[.]server[.]HiveServer2"],
        check=False,
    )
    return completed.stdout.split()


def hiveserver2_ready() -> bool:
    return run(beeline("--silent=true", "-e", "SELECT 1;"), check=False).returncode == 0


def hdfs_ready() -> bool:
    completed = run(["jps"], check=False)
    daemons = {line.split()[-1] for line in completed.stdout.splitlines() if line.split()}
    return (
        {"NameNode", "DataNode"}.issubset(daemons)
        and hdfs("-ls", "/", check=False).returncode == 0
    )


def require_hdfs() -> None:
    if not hdfs_ready():
        raise RuntimeError(
            "HDFS is not ready: NameNode and DataNode must be active and hdfs dfs -ls / must succeed. "
            "Start it first with: bash scripts/hdfs/start_hdfs_local.sh"
        )


def confirm(args: argparse.Namespace, prompt: str) -> None:
    if args.yes:
        return
    if not sys.stdin.isatty():
        raise RuntimeError(f"Confirmation required: {prompt} Re-run with --yes if appropriate.")
    answer = input(f"{prompt} [y/N] ").strip().lower()
    if answer not in {"y", "yes"}:
        raise RuntimeError("Stopped by user.")


def print_block_snapshot(
    args: argparse.Namespace, session_log: Path, technology: str
) -> None:
    for command in (
        ["free", "-h"],
        ["swapon", "--show"],
        ["jps", "-lm"],
        ["bash", "-lc", "ps aux --sort=-%mem | head -30"],
    ):
        snapshot_command(session_log, f"BEFORE {technology}", command)

    available_kib = meminfo_kib("MemAvailable")
    swap_used_kib = meminfo_kib("SwapTotal") - meminfo_kib("SwapFree")
    hive_status = "active" if hiveserver2_pids() else "stopped"
    hdfs_status = "ready" if hdfs_ready() else "not-ready"
    print(
        f"[CHECK] {technology}: available_memory={available_kib / 1024 / 1024:.2f}GiB "
        f"swap_used={swap_used_kib / 1024 / 1024:.2f}GiB "
        f"HiveServer2={hive_status} HDFS={hdfs_status}"
    )
    if technology.startswith("spark") and available_kib < 7 * 1024 * 1024:
        print("[WARN] available memory is below the recommended 7 GiB for Spark.")
        confirm(args, "Proceed despite low available memory?")
    if swap_used_kib > 1024 * 1024:
        print("[WARN] used swap exceeds the recommended 1 GiB. No swap command will run automatically.")
        confirm(args, "Proceed despite elevated swap usage?")


def start_hiveserver2(session_log: Path) -> None:
    if hiveserver2_ready():
        print("[SERVICE] HiveServer2 already active.")
        return
    print("[SERVICE] Starting HiveServer2 outside timer.")
    completed = run(
        ["bash", "scripts/hive/start_hiveserver2_local.sh"],
        check=False,
        log_path=session_log,
    )
    if completed.returncode != 0 or not hiveserver2_ready():
        raise RuntimeError(f"HiveServer2 did not become ready. Inspect {session_log}.")


def stop_hiveserver2(args: argparse.Namespace, session_log: Path, *, ask: bool) -> None:
    if not hiveserver2_pids():
        print("[SERVICE] HiveServer2 already stopped.")
        return
    if ask:
        confirm(args, "HiveServer2 is active. Stop it outside the timer before the Spark block?")
    print("[SERVICE] Stopping HiveServer2 outside timer.")
    run(
        ["bash", "scripts/hive/stop_hiveserver2_local.sh"],
        check=False,
        log_path=session_log,
    )
    if hiveserver2_pids():
        raise RuntimeError(
            "HiveServer2 is still active after the stop request. Stop it manually before continuing."
        )


def input_bytes(dataset: str) -> int:
    return int(hdfs("-stat", "%b", input_path(dataset)).stdout.strip())


def output_files(target: str) -> list[str]:
    files = []
    for line in hdfs("-ls", target).stdout.splitlines():
        if not line.startswith("-"):
            continue
        path = line.split()[-1]
        name = path.rsplit("/", 1)[-1]
        if not name.startswith(("_", ".")):
            files.append(path)
    return files


def validate_output(target: str) -> tuple[int, int]:
    files = output_files(target)
    if not files:
        raise RuntimeError(f"No output part files found in {target}")
    lines = hdfs("-cat", *files).stdout.splitlines()
    # Spark SQL writes one header per CSV part and Spark Core writes one explicit header row.
    output_rows = sum(
        1
        for line in lines
        if not line.startswith("airline,origin,total_flights,")
        and not line.startswith("origin,month,dep_delay_band,")
        and not line.startswith("origin,airline,total_flights,")
    )
    return len(files), output_rows


def execute_one(
    results_dir: Path,
    tag: str,
    technology: str,
    analysis: str,
    dataset: str,
    run_index: int,
) -> dict[str, object]:
    target = output_path(tag, technology, analysis, dataset, run_index)
    log_path = (
        results_dir
        / "logs"
        / f"{tag}_{technology}_{analysis}_{dataset}_repeated_{run_index}.log"
    )
    timestamp = datetime.now(timezone.utc).isoformat()
    hdfs("-rm", "-r", "-f", target, check=False)
    if technology == "hive":
        run(prepare_hive_command(dataset), log_path=log_path)
    command = job_command(technology, analysis, dataset, target)
    started = time.perf_counter()
    completed = run(command, check=False, log_path=log_path)
    elapsed = time.perf_counter() - started
    status = "success" if completed.returncode == 0 else "failed"
    part_count: int | str = ""
    output_rows: int | str = ""
    if status == "success":
        try:
            part_count, output_rows = validate_output(target)
        except Exception as exc:
            status = "failed_validation"
            append_session(log_path, f"\nOUTPUT VALIDATION ERROR: {exc}")
    return {
        "timestamp": timestamp,
        "campaign_tag": tag,
        "technology": technology,
        "analysis": analysis,
        "dataset_label": dataset,
        "run_type": "repeated",
        "run_index": run_index,
        "input_rows": DATASET_ROWS[dataset],
        "input_bytes_hdfs": input_bytes(dataset),
        "output_path": target,
        "elapsed_seconds_job_time": f"{elapsed:.4f}",
        "status": status,
        "error_log_path": str(log_path),
        "command": command_text(command),
        "output_part_files_count": part_count,
        "output_rows": output_rows,
    }


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def summarize(runs: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str], list[dict[str, object]]] = {}
    for row in runs:
        key = (str(row["technology"]), str(row["analysis"]), str(row["dataset_label"]))
        grouped.setdefault(key, []).append(row)
    summary = []
    for technology in TECHNOLOGY_ORDER:
        for analysis in ANALYSIS_ORDER:
            for dataset in DATASET_ORDER:
                rows = grouped.get((technology, analysis, dataset), [])
                if not rows:
                    continue
                successful = [row for row in rows if row["status"] == "success"]
                values = [float(row["elapsed_seconds_job_time"]) for row in successful]
                output_rows = successful[0]["output_rows"] if successful else ""
                part_counts = [int(row["output_part_files_count"]) for row in successful]
                summary.append(
                    {
                        "technology": technology,
                        "analysis": analysis,
                        "dataset_label": dataset,
                        "input_rows": rows[0]["input_rows"],
                        "input_bytes_hdfs": rows[0]["input_bytes_hdfs"],
                        "successful_runs": len(successful),
                        "failed_runs": len(rows) - len(successful),
                        "mean_seconds": f"{statistics.mean(values):.4f}" if values else "",
                        "median_seconds": f"{statistics.median(values):.4f}" if values else "",
                        "stddev_seconds": f"{statistics.stdev(values):.4f}" if len(values) > 1 else "",
                        "min_seconds": f"{min(values):.4f}" if values else "",
                        "max_seconds": f"{max(values):.4f}" if values else "",
                        "best_run_seconds": f"{min(values):.4f}" if values else "",
                        "output_rows": output_rows,
                        "output_part_files_count": (
                            ",".join(str(value) for value in sorted(set(part_counts)))
                            if part_counts
                            else ""
                        ),
                    }
                )
    return summary


def create_plots(
    results_dir: Path,
    summary: list[dict[str, object]],
    analyses: list[str],
) -> None:
    import matplotlib.pyplot as plt
    import pandas as pd

    frame = pd.DataFrame(summary)
    if frame.empty:
        return
    frame["dataset_label"] = pd.Categorical(frame["dataset_label"], DATASET_ORDER, ordered=True)
    frame["mean_seconds"] = pd.to_numeric(frame["mean_seconds"], errors="coerce")
    for analysis in analyses:
        subset = frame[(frame["analysis"] == analysis) & frame["mean_seconds"].notna()]
        if subset.empty:
            _, ax = plt.subplots()
        else:
            pivot = subset.pivot(index="dataset_label", columns="technology", values="mean_seconds")
            pivot = pivot.reindex(DATASET_ORDER)
            ax = pivot.plot(marker="o")
        ax.set_title(f"HDFS repeated job time - distributed output - {analysis}")
        ax.set_xlabel("Dataset label")
        ax.set_ylabel("Seconds")
        ax.grid(True)
        plt.tight_layout()
        plt.savefig(results_dir / f"benchmark_{analysis}.png", dpi=150)
        plt.close()


def write_report(
    results_dir: Path,
    args: argparse.Namespace,
    technologies: list[str],
    runs: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> None:
    import pandas as pd

    failed = [row for row in runs if row["status"] != "success"]
    lines = [
        "# HDFS Repeated Benchmark Report",
        "",
        "## Protocol",
        "",
        "- Metric: analytical job invocation plus distributed HDFS output write.",
        "- Excluded from timer: cleanup, Hive table setup, HiveServer2 start/stop, memory checks, HDFS listing, row counting, previews, summaries and plots.",
        f"- Each technology-analysis-dataset combination has `{args.repetitions}` runs: `run_type=repeated`, `run_index=1..{args.repetitions}`.",
        "- Output remains distributed. No presentation-only global final sort, `coalesce(1)`, timed preview action or Tez execution was introduced.",
        f"- Campaign tag: `{args.campaign_tag}`.",
        f"- Dataset order: `{', '.join(args.datasets)}`.",
        f"- Repetitions per combination: `{args.repetitions}`.",
        "",
        "## Block Order And Services",
        "",
        f"- Selected block order: `{', '.join(technologies)}`.",
        "- HDFS remains active throughout the campaign.",
        "- HiveServer2 is started only for the Hive block and stopped outside the timed interval.",
        "- HiveServer2 remains stopped for Spark SQL and Spark Core.",
        "",
        "## Spark SQL Configuration",
        "",
        f"- `SPARK_DRIVER_MEMORY={os.environ.get('SPARK_DRIVER_MEMORY', '<empty>')}`",
        f"- `SPARK_SQL_SHUFFLE_PARTITIONS={os.environ.get('SPARK_SQL_SHUFFLE_PARTITIONS', '<empty>')}`",
        f"- `SPARK_SUBMIT_EXTRA_CONF={os.environ.get('SPARK_SUBMIT_EXTRA_CONF', '<empty>')}`",
        "",
        "## Results",
        "",
    ]
    lines.append(pd.DataFrame(summary).to_markdown(index=False) if summary else "No runs recorded.")
    lines.extend(["", "## Failures", ""])
    if failed:
        lines.append(pd.DataFrame(failed)[
            ["technology", "analysis", "dataset_label", "status", "error_log_path"]
        ].to_markdown(index=False))
    else:
        lines.append("No failed runs were recorded.")
    lines.extend(
        [
            "",
            "## Analysis 3 Implementation Note",
            "",
            "Analysis 3 compares each airline-origin pair with the flight-level departure-delay average of the same airport. "
            "The airport average is therefore weighted by flights rather than by airline averages.",
            "",
            "For consistency with Analysis 2, departure-delay averages use the available `dep_delay` values. "
            "Arrival-delay averages use completed flights (`is_completed_flight = 1`), while cancellation rates use all flights.",
            "",
            "The job adds the required joins and ranking operation. Spark SQL and Hive use a window partitioned by `origin`; "
            "Spark Core groups by airport and sorts only that airport's airlines. These shuffles and internal sorts are part of the requested semantics.",
            "",
            "## Methodological Note",
            "",
            f"Questa campagna usa {args.repetitions} ripetizioni per combinazione e riporta media, mediana e deviazione standard. Non usa la distinzione cold/warm.",
            "",
            "## AWS Reuse",
            "",
            "Reuse the same protocol on AWS while recording instance type, RAM, core count, storage, HDFS replication and exact Spark/Hive configuration.",
            "",
        ]
    )
    (results_dir / "benchmark_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def print_dry_run(args: argparse.Namespace, technologies: list[str]) -> None:
    print("DRY RUN: no service, HDFS command, Hive query or Spark job will be started.")
    print(f"Results directory: {args.results_dir}")
    print(f"Campaign tag: {args.campaign_tag}")
    print(f"Datasets: {', '.join(args.datasets)}")
    print(f"Analyses: {', '.join(args.analyses)}")
    print(f"Repetitions: {args.repetitions}")
    print(f"Technologies: {', '.join(technologies) if technologies else '<none>'}")
    print(f"SPARK_DRIVER_MEMORY={os.environ.get('SPARK_DRIVER_MEMORY', '<empty>')}")
    print(
        "SPARK_SQL_SHUFFLE_PARTITIONS="
        f"{os.environ.get('SPARK_SQL_SHUFFLE_PARTITIONS', '<empty>')}"
    )
    print(f"SPARK_SUBMIT_EXTRA_CONF={os.environ.get('SPARK_SUBMIT_EXTRA_CONF', '<empty>')}")
    print("\nPlanned blocks:")
    for block_index, technology in enumerate(technologies, start=1):
        if technology == "hive":
            print(f"{block_index}. hive: verify HDFS, memory snapshot, start HiveServer2, run jobs, stop HiveServer2")
        elif technology == "spark_sql":
            print(f"{block_index}. spark_sql: verify HDFS, memory snapshot, ensure HiveServer2 stopped, run jobs")
        else:
            print(f"{block_index}. spark_core: verify HDFS, memory snapshot, ensure HiveServer2 stopped, run jobs")
        for analysis in args.analyses:
            for dataset in args.datasets:
                for run_index in range(1, args.repetitions + 1):
                    target = output_path(
                        args.campaign_tag, technology, analysis, dataset, run_index
                    )
                    if technology == "hive":
                        print(
                            f"   setup {run_index}/{args.repetitions}: "
                            f"{command_text(prepare_hive_command(dataset))}"
                        )
                    print(
                        f"   run {run_index}/{args.repetitions}: "
                        f"{command_text(job_command(technology, analysis, dataset, target))}"
                    )


def main() -> None:
    args = parse_args()
    if args.repetitions < 1:
        raise RuntimeError("--repetitions must be at least 1.")
    technologies = selected_technologies(args)
    if args.dry_run:
        print_dry_run(args, technologies)
        return
    if not technologies:
        raise RuntimeError("All technology blocks were skipped.")

    results_dir = PROJECT_ROOT / args.results_dir
    results_dir.mkdir(parents=True, exist_ok=True)
    archive_previous_results(results_dir, args.reset)
    (results_dir / "logs").mkdir(parents=True, exist_ok=True)
    session_log = results_dir / "session.log"
    append_session(
        session_log,
        f"Official repeated benchmark campaign {args.campaign_tag}\nStarted: {datetime.now().isoformat()}",
    )
    runs: list[dict[str, object]] = []
    for technology in technologies:
        print(f"\n=== Block: {technology} ===")
        require_hdfs()
        print_block_snapshot(args, session_log, technology)
        if technology == "hive":
            start_hiveserver2(session_log)
        else:
            stop_hiveserver2(args, session_log, ask=True)
        require_hdfs()
        try:
            for analysis in args.analyses:
                for dataset in args.datasets:
                    for run_index in range(1, args.repetitions + 1):
                        row = execute_one(
                            results_dir,
                            args.campaign_tag,
                            technology,
                            analysis,
                            dataset,
                            run_index,
                        )
                        runs.append(row)
                        write_csv(results_dir / "benchmark_runs.csv", RUN_FIELDS, runs)
                        if row["status"] == "success":
                            print(
                                f"[OK] {technology} {analysis} {dataset} "
                                f"run={run_index}/{args.repetitions} "
                                f"{row['elapsed_seconds_job_time']}s"
                            )
                        else:
                            print(
                                f"[FAIL] {technology} {analysis} {dataset} "
                                f"run={run_index}/{args.repetitions} "
                                f"{row['elapsed_seconds_job_time']}s "
                                f"log={row['error_log_path']}"
                            )
        finally:
            if technology == "hive":
                stop_hiveserver2(args, session_log, ask=False)

    summary = summarize(runs)
    write_csv(results_dir / "benchmark_summary.csv", SUMMARY_FIELDS, summary)
    create_plots(results_dir, summary, args.analyses)
    write_report(results_dir, args, technologies, runs, summary)
    success_count = sum(row["status"] == "success" for row in runs)
    print("\n=== Campaign summary ===")
    print(f"Total runs: {len(runs)}")
    print(f"Success: {success_count}")
    print(f"Failed: {len(runs) - success_count}")
    print(f"Run CSV: {results_dir / 'benchmark_runs.csv'}")
    print(f"Summary CSV: {results_dir / 'benchmark_summary.csv'}")
    print(f"Report: {results_dir / 'benchmark_report.md'}")
    print(f"Logs: {results_dir / 'logs'}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
