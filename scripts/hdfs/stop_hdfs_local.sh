#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/env/project_env.sh

export HADOOP_CONF_DIR="$PROJECT_ROOT/hadoop/conf"
export HADOOP_LOG_DIR="$PROJECT_ROOT/hadoop/logs"

echo "Stopping HDFS if running..."

hdfs --daemon stop datanode || true
hdfs --daemon stop namenode || true

sleep 2

jps
