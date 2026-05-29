#!/usr/bin/env bash

set -e

echo "========================================"
echo "Flight Delay Big Data Project"
echo "Environment check"
echo "========================================"
echo

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

echo "[1/7] Project directory"
echo "PROJECT_ROOT=$PROJECT_ROOT"
echo

echo "[2/7] Loading project environment"
if [ -f "scripts/project_env.sh" ]; then
    source scripts/project_env.sh
    echo "Loaded scripts/project_env.sh"
else
    echo "ERROR: scripts/project_env.sh not found"
    exit 1
fi
echo

echo "[3/7] Environment variables"
echo "JAVA_HOME=$JAVA_HOME"
echo "BIGDATA_TOOLS_HOME=$BIGDATA_TOOLS_HOME"
echo "SPARK_HOME=$SPARK_HOME"
echo "HADOOP_HOME=$HADOOP_HOME"
echo "HIVE_HOME=$HIVE_HOME"
echo

echo "[4/7] Python environment"
python --version
python -m pip --version
python -c "import pandas, numpy, matplotlib, pyarrow, pyspark, tabulate; print('Python dependencies OK')"
echo

echo "[5/7] Java"
java -version
javac -version
echo

echo "[6/7] Big Data tools"
spark-submit --version
hadoop version
hive --version
echo

echo "[7/7] Dataset path"
if [ -f "data/raw/flight_data_2024.csv" ]; then
    echo "Dataset found: data/raw/flight_data_2024.csv"
    ls -lh data/raw/flight_data_2024.csv
else
    echo "WARNING: Dataset not found at data/raw/flight_data_2024.csv"
    echo "The dataset is not tracked by Git and must be placed manually."
fi
echo

echo "========================================"
echo "Environment check completed successfully"
echo "========================================"
