# Flight Delay Big Data Project

Project for the Big Data course at Università degli Studi Roma Tre.

The project analyzes the 2024 flight delay dataset using multiple Big Data technologies.  
The main goals are data preparation, distributed processing, comparison between technologies, performance evaluation and reproducibility.

## Project goals

The project implements two analyses using three Big Data technologies:

- Spark SQL
- Spark Core
- Hive

The selected analyses are:

1. **Airline statistics by origin airport**
   - total number of flights;
   - minimum, maximum and average arrival delay;
   - cancellation rate;
   - active months.

2. **Delay report by origin airport and month**
   - number of flights by departure delay band;
   - average departure delay;
   - average arrival delay;
   - top three delay or cancellation causes.

Spark SQL, Spark Core and Hive outputs are compared automatically to verify result consistency.

## Dataset

The dataset is not included in this repository because of its size.

Expected local path:

```text
data/raw/flight_data_2024.csv
```

The current dataset used during development contains:

```text
7,079,081 rows
35 original columns
approximately 1.22 GB
```

The cleaned dataset is generated locally and saved under:

```text
data/cleaned/
```

Benchmark samples are generated under:

```text
data/samples/
```

Generated datasets are excluded from Git versioning.

## Technologies

The project uses:

- Python 3.12
- pandas
- NumPy
- PyArrow
- PySpark
- Apache Spark 3.5.3
- Apache Hadoop 3.3.6
- Apache Hive 4.0.1
- OpenJDK 11

The implemented technologies are:

```text
Spark SQL
Spark Core
Hive
```

MapReduce/Hadoop Streaming is not part of the main implementation because the project already satisfies the requirement of using at least three Big Data technologies.

## Repository structure

```text
flight-delay-bigdata-project/
├── data/
│   ├── raw/                 # local raw dataset, not versioned
│   ├── cleaned/             # cleaned CSV and Parquet files, not versioned
│   ├── samples/             # benchmark samples, not versioned
│   └── output/
├── docs/                    # inspection, validation and comparison reports
├── hive/                    # HiveQL analyses
├── report/                  # final report files
├── results/
│   ├── output/              # full generated outputs, not versioned
│   ├── tables/              # small preview tables, versioned
│   └── tmp/                 # temporary runtime files, not versioned
├── scripts/                 # setup, preparation, runners and comparison scripts
├── spark_core/              # Spark Core implementations
├── spark_sql/               # Spark SQL implementations
├── .gitignore
├── README.md
└── requirements.txt
```

## Python environment setup

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Verify the Python environment:

```bash
python -c "import pandas, numpy, matplotlib, pyarrow, pyspark; print('Environment OK')"
```

## Big Data tools setup

This project uses local Big Data tools extracted under:

```text
~/bigdata-tools/
```

Expected paths:

```text
~/bigdata-tools/spark-3.5.3-bin-hadoop3
~/bigdata-tools/hadoop-3.3.6
~/bigdata-tools/apache-hive-4.0.1-bin
```

Before running Spark, Hadoop or Hive commands, load the project environment:

```bash
source scripts/env/project_env.sh
```

The project environment file sets:

```text
JAVA_HOME
SPARK_HOME
HADOOP_HOME
HIVE_HOME
BIGDATA_TOOLS_HOME
PATH
```

The project uses OpenJDK 11 even if the system default Java version is different.

Verify the Big Data setup:

```bash
java -version
javac -version
spark-submit --version
hadoop version
hive --version
```

## Environment check

After setting up the Python environment and extracting the Big Data tools, run:

```bash
bash scripts/env/check_environment.sh
```

This script verifies:

- project directory;
- project environment variables;
- Python version;
- required Python dependencies;
- Java version used by the project;
- Spark availability;
- Hadoop availability;
- Hive availability;
- local dataset path.

## Data inspection

Inspect the raw dataset:

```bash
python scripts/data/inspect_dataset.py
```

The inspection report is saved to:

```text
docs/dataset_inspection.md
```

The report includes:

- dataset path;
- file size;
- number of rows;
- number of columns;
- inferred data types on sample;
- missing values on sample;
- candidate columns for the required analyses.

## Data preparation

Prepare the cleaned dataset:

```bash
python scripts/data/prepare_data.py
```

Generated files:

```text
data/cleaned/flights_clean.csv
data/cleaned/flights_clean.parquet
docs/cleaning_report.md
```

The cleaning step:

- selects relevant columns;
- renames carrier column to `airline`;
- normalizes airline and airport codes;
- creates the `route` column;
- creates `is_completed_flight`;
- creates `dep_delay_band`;
- normalizes cancellation codes;
- derives the `main_delay_cause` column;
- saves CSV and Parquet outputs.

Validate the cleaned dataset:

```bash
python scripts/data/validate_cleaned_data.py
```

Validation report:

```text
docs/cleaned_data_validation.md
```

## Benchmark samples

Generate benchmark samples:

```bash
bash scripts/data/generate_samples.sh
```

Generated files:

```text
data/samples/flights_100k.csv
data/samples/flights_500k.csv
data/samples/flights_1m.csv
data/samples/flights_3m.csv
data/samples/flights_7m.csv
```

These files are generated locally and excluded from Git versioning.

## Implemented analyses

### Analysis 1 — Airline statistics by origin airport

Implemented with:

```text
spark_sql/analysis_1_airline_stats.py
spark_core/analysis_1_airline_stats.py
hive/analysis_1_airline_stats.sql
```

Output columns:

```text
airline
origin
total_flights
min_arr_delay
max_arr_delay
avg_arr_delay
cancelled_flights
cancellation_rate
active_months
```

### Analysis 2 — Delay report by airport and month

Implemented with:

```text
spark_sql/analysis_2_airport_month_delay_report.py
spark_core/analysis_2_airport_month_delay_report.py
hive/analysis_2_airport_month_delay_report.sql
```

Output columns:

```text
origin
month
dep_delay_band
flight_count
avg_dep_delay
avg_arr_delay
top_3_causes
```

## Running individual analyses

### Spark SQL

Analysis 1:

```bash
bash scripts/run/run_spark_sql_analysis_1.sh \
  data/samples/flights_100k.csv \
  results/output/spark_sql/analysis_1_100k \
  results/tables/spark_sql_analysis_1_100k_preview.csv
```

Analysis 2:

```bash
bash scripts/run/run_spark_sql_analysis_2.sh \
  data/samples/flights_100k.csv \
  results/output/spark_sql/analysis_2_100k \
  results/tables/spark_sql_analysis_2_100k_preview.csv
```

### Spark Core

Analysis 1:

```bash
bash scripts/run/run_spark_core_analysis_1.sh \
  data/samples/flights_100k.csv \
  results/output/spark_core/analysis_1_100k \
  results/tables/spark_core_analysis_1_100k_preview.csv
```

Analysis 2:

```bash
bash scripts/run/run_spark_core_analysis_2.sh \
  data/samples/flights_100k.csv \
  results/output/spark_core/analysis_2_100k \
  results/tables/spark_core_analysis_2_100k_preview.csv
```

### Hive

Initialize Hive local configuration:

```bash
bash scripts/hive/init_hive_local.sh
```

Start HiveServer2:

```bash
bash scripts/hive/start_hiveserver2_local.sh
```

Analysis 1:

```bash
bash scripts/run/run_hive_analysis_1.sh \
  data/samples/flights_100k.csv \
  results/output/hive/analysis_1_100k \
  results/tables/hive_analysis_1_100k_preview.csv
```

Analysis 2:

```bash
bash scripts/run/run_hive_analysis_2.sh \
  data/samples/flights_100k.csv \
  results/output/hive/analysis_2_100k \
  results/tables/hive_analysis_2_100k_preview.csv
```

Stop HiveServer2:

```bash
bash scripts/hive/stop_hiveserver2_local.sh
```

## Running all analyses

Run all implemented analyses on a selected dataset:

```bash
bash scripts/run/run_all_analyses.sh 100k data/samples/flights_100k.csv
```

The script runs:

```text
Spark SQL Analysis 1
Spark SQL Analysis 2
Spark Core Analysis 1
Spark Core Analysis 2
Hive Analysis 1
Hive Analysis 2
```

It also checks whether HiveServer2 is already running.  
If HiveServer2 is not running, the script starts it automatically and stops it at the end.

## Result previews

Full outputs are saved under:

```text
results/output/
```

Full outputs are excluded from Git versioning.

Small preview tables are saved under:

```text
results/tables/
```

Preview files contain the header and the first ten rows of each output.  
These files are versioned because they are useful for documentation and for the final report.

## Output comparison

Spark SQL and Spark Core outputs are compared with:

```bash
python scripts/compare/compare_analysis_1_outputs.py \
  --spark-sql-output results/output/spark_sql/analysis_1_100k \
  --spark-core-output results/output/spark_core/analysis_1_100k \
  --report docs/analysis_1_output_comparison.md
```

```bash
python scripts/compare/compare_analysis_2_outputs.py \
  --spark-sql-output results/output/spark_sql/analysis_2_100k \
  --spark-core-output results/output/spark_core/analysis_2_100k \
  --report docs/analysis_2_output_comparison.md
```

Hive and Spark SQL outputs are compared with:

```bash
python scripts/compare/compare_analysis_1_hive_spark_sql.py \
  --spark-sql-output results/output/spark_sql/analysis_1_100k \
  --hive-output results/output/hive/analysis_1_100k \
  --report docs/analysis_1_hive_spark_sql_comparison.md
```

```bash
python scripts/compare/compare_analysis_2_hive_spark_sql.py \
  --spark-sql-output results/output/spark_sql/analysis_2_100k \
  --hive-output results/output/hive/analysis_2_100k \
  --report docs/analysis_2_hive_spark_sql_comparison.md
```

The comparisons use a small floating-point tolerance to account for minor numerical differences between engines.

## Reproducibility

The repository includes:

- fixed Python dependencies in `requirements.txt`;
- project environment setup in `scripts/env/project_env.sh`;
- environment verification script;
- data inspection script;
- data preparation script;
- cleaned data validation script;
- benchmark sample generation script;
- analysis implementations for Spark SQL, Spark Core and Hive;
- runners for individual analyses;
- runner for all analyses;
- automatic output comparison scripts;
- generated preview tables;
- documentation reports under `docs/`.

Large datasets, full generated outputs and local runtime files are excluded from Git versioning.
