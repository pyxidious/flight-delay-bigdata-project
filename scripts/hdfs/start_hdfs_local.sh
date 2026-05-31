#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/env/project_env.sh

export HADOOP_CONF_DIR="$PROJECT_ROOT/hadoop/conf"
export HADOOP_LOG_DIR="$PROJECT_ROOT/hadoop/logs"

mkdir -p "$HADOOP_LOG_DIR"

if jps | grep -q "NameNode" && jps | grep -q "DataNode"; then
    echo "HDFS is already running."
    exit 0
fi

echo "Starting HDFS..."
if ! jps | grep -q "NameNode"; then
    hdfs --daemon start namenode
fi
if ! jps | grep -q "DataNode"; then
    hdfs --daemon start datanode
fi

sleep 3

jps

hdfs dfs -ls / >/dev/null 2>&1 || {
    echo "ERROR: HDFS is not responding."
    exit 1
}

echo "HDFS is ready."
