# Official HDFS Repeated Benchmark

The only official benchmark entrypoint is:

```bash
bash scripts/run_benchmark.sh
```

It executes `analysis_1`, `analysis_2` and `analysis_3` in three technology
blocks:

1. Hive
2. Spark SQL
3. Spark Core

Each technology-analysis-dataset combination is repeated three times by
default. The timer includes analytical job invocation and distributed HDFS
output write. Cleanup, Hive table setup, HiveServer2 lifecycle, memory checks,
HDFS listing, row counting, summaries and plots remain outside the timer.

## Data Preparation

Starting from `data/raw/flight_data_2024.csv`, run:

```bash
python scripts/data/inspect_dataset.py
python scripts/data/prepare_data.py
python scripts/data/validate_cleaned_data.py
bash scripts/data/generate_samples.sh
python scripts/data/generate_replicated_datasets.py --factors 10m 14m
```

This produces the local dataset sizes used by the official campaign:

```text
100k 500k 1m 3m 7m 10m 14m
```

## HDFS Upload

Start HDFS, upload the generated datasets and verify availability:

```bash
bash scripts/hdfs/start_hdfs_local.sh
bash scripts/hdfs/upload_samples_to_hdfs.sh
bash scripts/hdfs/check_hdfs.sh
```

HDFS remains active throughout the campaign.

## Dry Run

Inspect the official plan without starting Hive, Spark or benchmark jobs:

```bash
bash scripts/run_benchmark.sh --dry-run
```

## Official Campaign

```bash
SPARK_DRIVER_MEMORY=5g \
SPARK_SQL_SHUFFLE_PARTITIONS=64 \
bash scripts/run_benchmark.sh \
  --datasets 100k 500k 1m 3m 7m 10m 14m \
  --repetitions 3 \
  --results-dir results/benchmark \
  --campaign-tag "benchmark_$(date +%Y%m%d_%H%M%S)" \
  --reset
```

Use `--yes` only when automatic confirmation of memory warnings or a
HiveServer2 stop is appropriate.

## Services And Configuration

- `SPARK_DRIVER_MEMORY=5g`
- `SPARK_SQL_SHUFFLE_PARTITIONS=64`
- Hive runs on MapReduce.
- HiveServer2 is started only for the Hive block.
- HiveServer2 is stopped before Spark SQL and Spark Core.
- HiveServer2 start and stop are outside the timed interval.

## Results

Official artifacts are written to `results/benchmark/`:

- `benchmark_runs.csv`: one row for each repeated run.
- `benchmark_summary.csv`: aggregate timing statistics.
- `benchmark_analysis_1.png`: Analysis 1 timing chart.
- `benchmark_analysis_2.png`: Analysis 2 timing chart.
- `benchmark_analysis_3.png`: Analysis 3 timing chart.
- `benchmark_report.md`: protocol and generated result report.
- `session.log`: memory, swap and JVM diagnostics.
- `logs/`: one execution log per run.

## Reproducibility Notes

The benchmark writes distributed output. It does not add a presentation-only
global final sort, `coalesce(1)`, timed post-write preview or Tez execution.

Analysis 3 compares each airline-origin pair with the flight-level average
departure delay of the airport. Arrival-delay averages use completed flights
only, while cancellation rates use all flights. Spark SQL and Hive use a
window partitioned by `origin`; Spark Core performs the equivalent ordering
inside each airport group.
