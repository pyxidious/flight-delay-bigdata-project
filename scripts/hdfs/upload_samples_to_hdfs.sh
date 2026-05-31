#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/env/project_env.sh

export HADOOP_CONF_DIR="$PROJECT_ROOT/hadoop/conf"

LOCAL_SAMPLE_DIR="data/samples"
HDFS_BASE_DIR="/flight-delay-project"

DATASETS=(
  "100k:flights_100k.csv"
  "500k:flights_500k.csv"
  "1m:flights_1m.csv"
  "3m:flights_3m.csv"
  "7m:flights_7m.csv"
  "10m:flights_10m.csv"
  "14m:flights_14m.csv"
)

echo "Uploading benchmark samples to HDFS"
echo "HADOOP_CONF_DIR=$HADOOP_CONF_DIR"
echo "HDFS base directory: $HDFS_BASE_DIR"
echo

hdfs dfs -mkdir -p "$HDFS_BASE_DIR/input"

for item in "${DATASETS[@]}"; do
    label="${item%%:*}"
    filename="${item##*:}"

    local_path="$LOCAL_SAMPLE_DIR/$filename"
    hdfs_dir="$HDFS_BASE_DIR/input/$label"
    hdfs_path="$hdfs_dir/flights.csv"

    if [ ! -f "$local_path" ]; then
        echo "ERROR: local sample not found: $local_path"
        exit 1
    fi

    echo "Uploading $local_path -> $hdfs_path"

    hdfs dfs -mkdir -p "$hdfs_dir"
    hdfs dfs -rm -f "$hdfs_path" >/dev/null 2>&1 || true
    hdfs dfs -put "$local_path" "$hdfs_path"

    echo "Uploaded:"
    hdfs dfs -ls "$hdfs_path"
    hdfs dfs -du -h "$hdfs_path"
    echo
done

echo "HDFS upload completed."
