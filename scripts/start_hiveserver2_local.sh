#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/project_env.sh

export HIVE_CONF_DIR="$PROJECT_ROOT/hive/conf"

mkdir -p results/tmp/hive/logs

echo "Starting HiveServer2 on localhost:10000..."
echo "Logs: results/tmp/hive/logs/hiveserver2.log"

nohup hiveserver2 > results/tmp/hive/logs/hiveserver2.log 2>&1 &

echo $! > results/tmp/hive/hiveserver2.pid

echo "HiveServer2 PID: $(cat results/tmp/hive/hiveserver2.pid)"
echo "Waiting for HiveServer2 to become available..."

for attempt in {1..30}; do
    if beeline -u "jdbc:hive2://localhost:10000/default" -e "SELECT 1;" >/dev/null 2>&1; then
        echo "HiveServer2 is ready."
        exit 0
    fi

    echo "Attempt $attempt/30: HiveServer2 not ready yet..."
    sleep 2
done

echo "ERROR: HiveServer2 did not become ready in time."
echo "Last log lines:"
tail -n 80 results/tmp/hive/logs/hiveserver2.log
exit 1
