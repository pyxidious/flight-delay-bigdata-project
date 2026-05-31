#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/env/project_env.sh

export HADOOP_CONF_DIR="$PROJECT_ROOT/hadoop/conf"

echo "HADOOP_CONF_DIR=$HADOOP_CONF_DIR"
echo "Default FS:"
DEFAULT_FS="$(hdfs getconf -confKey fs.defaultFS)"
echo "$DEFAULT_FS"

if [ "$DEFAULT_FS" != "hdfs://localhost:9000" ]; then
    echo "ERROR: expected fs.defaultFS=hdfs://localhost:9000"
    exit 1
fi

echo
echo "Java processes:"
jps

echo
echo "HDFS root:"
hdfs dfs -ls /

echo
echo "HDFS check completed."
