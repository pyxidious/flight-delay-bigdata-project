# Flight Delay Big Data Project

Project for the Big Data course at Università degli Studi Roma Tre.

The project analyzes the Flight Delay Dataset 2024 using multiple Big Data technologies, with a focus on data preparation, distributed processing, performance comparison and reproducibility.

## Dataset

The dataset is not included in this repository because of its size.

Expected local path:

```text
data/raw/flight_data_2024.csv
```

## Technologies

The project will compare different Big Data technologies:

- Spark SQL
- Spark Core
- Hive
- Optional: MapReduce

## Repository structure

```text
flight-delay-bigdata-project/
├── data/
│   ├── raw/
│   ├── cleaned/
│   ├── samples/
│   └── output/
├── docs/
├── report/
├── results/
│   ├── output/
│   └── tmp/
├── scripts/
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

Verify the environment:

```bash
python -c "import pandas, numpy, matplotlib, pyarrow, pyspark; print('Environment OK')"
```

## Big Data tools setup

This project uses the following local Big Data tools:

- Apache Spark 3.5.3
- Apache Hadoop 3.3.6
- Apache Hive 4.0.1
- OpenJDK 11

The tools are expected to be extracted under:

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
source scripts/project_env.sh
```

Verify the setup:

```bash
java -version
spark-submit --version
hadoop version
hive --version
```

The project environment file sets:

```text
JAVA_HOME
SPARK_HOME
HADOOP_HOME
HIVE_HOME
PATH
```

This avoids depending on the system-wide default Java version.

## Environment check

After setting up the Python environment and extracting the Big Data tools, run:

```bash
bash scripts/check_environment.sh

This script verifies:

Python and required Python dependencies;
Java version used by the project;
Spark availability;
Hadoop availability;
Hive availability;
local dataset path.

## Step 3.12 — Controllo Git

Dopo aver creato lo script e aggiornato il README, esegui:

```bash
git status

## Reproducibility

The repository includes:

- fixed Python dependencies in `requirements.txt`;
- scripts for data preparation and analysis;
- execution instructions;
- benchmark results and generated outputs;
- final report in PDF format.

Large datasets and generated outputs are excluded from Git versioning.
