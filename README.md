# Flight Delay Big Data Project

Project for the Big Data course at Universita degli Studi Roma Tre.

The repository analyzes the 2024 Flight Delay Dataset with three technologies:

- Spark SQL
- Spark Core
- Hive on MapReduce

It implements three jobs:

1. Airline statistics by origin airport.
2. Delay report by origin airport, month and departure-delay band.
3. Airline-airport performance comparison and airport ranking.

## Repository Structure

```text
data/                 local raw, prepared and scaled datasets
docs/                 data inspection, preparation and validation notes
hadoop/conf/          local HDFS configuration
hive/                 official Hive queries
results/benchmark/    official benchmark artifacts
scripts/data/         preparation and scaling tools
scripts/env/          environment helpers
scripts/hdfs/         local HDFS lifecycle and upload helpers
scripts/hive/         local HiveServer2 lifecycle helpers
scripts/run_benchmark.sh
spark_core/           official Spark Core jobs
spark_sql/            official Spark SQL jobs
archive/              preserved historical material
```

## Setup

Create the Python environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The local environment helper expects Spark, Hadoop and Hive under
`~/bigdata-tools/` and configures the required Java runtime:

```bash
source scripts/env/project_env.sh
bash scripts/env/check_environment.sh
```

## Data Preparation

Place the source CSV at:

```text
data/raw/flight_data_2024.csv
```

Prepare and validate the dataset:

```bash
python scripts/data/inspect_dataset.py
python scripts/data/prepare_data.py
python scripts/data/validate_cleaned_data.py
```

Generate increasing local datasets and upload them to HDFS:

```bash
bash scripts/data/generate_samples.sh
python scripts/data/generate_replicated_datasets.py --factors 10m 14m
bash scripts/hdfs/start_hdfs_local.sh
bash scripts/hdfs/upload_samples_to_hdfs.sh
bash scripts/hdfs/check_hdfs.sh
```

## Benchmark

The only official benchmark entrypoint is:

```bash
bash scripts/run_benchmark.sh
```

Inspect the plan without starting jobs:

```bash
bash scripts/run_benchmark.sh --dry-run
```

Official artifacts are written under `results/benchmark/`. See
[`README_BENCHMARK.md`](README_BENCHMARK.md) for the protocol, configuration
and complete reproducibility instructions.
