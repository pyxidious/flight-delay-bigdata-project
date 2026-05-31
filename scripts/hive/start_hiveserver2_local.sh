#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/env/project_env.sh

export HIVE_CONF_DIR="$PROJECT_ROOT/hive/conf"
export HADOOP_HEAPSIZE=6144
export HADOOP_CLIENT_OPTS="-Xmx6144m ${HADOOP_CLIENT_OPTS:-}"
# Hive 4 forwards HIVE_OPTS to HiveServer2 as application arguments.
export HIVE_SERVER2_HEAPSIZE=6144

PID_FILE="results/tmp/hive/hiveserver2.pid"
LOG_FILE="results/tmp/hive/logs/hiveserver2.log"
JDBC_URL="jdbc:hive2://localhost:10000/default"

mkdir -p results/tmp/hive/logs

echo "Checking HiveServer2 availability on localhost:10000..."

if beeline -u "$JDBC_URL" -e "SELECT 1;" >/dev/null 2>&1; then
    echo "HiveServer2 is already running."
    exit 0
fi

if [ -f "$PID_FILE" ]; then
    OLD_PID="$(cat "$PID_FILE")"

    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "Found HiveServer2 PID file, but JDBC is not ready."
        echo "Stopping stale/non-ready process PID $OLD_PID..."
        kill "$OLD_PID" || true
        sleep 2
    fi

    rm -f "$PID_FILE"
fi

echo "Starting HiveServer2 on localhost:10000..."
echo "Logs: $LOG_FILE"

nohup hiveserver2 > "$LOG_FILE" 2>&1 &

echo $! > "$PID_FILE"

echo "HiveServer2 PID: $(cat "$PID_FILE")"
echo "Waiting for HiveServer2 to become available..."

for attempt in {1..30}; do
    if beeline -u "$JDBC_URL" -e "SELECT 1;" >/dev/null 2>&1; then
        echo "HiveServer2 is ready."
        exit 0
    fi

    echo "Attempt $attempt/30: HiveServer2 not ready yet..."
    sleep 2
done

echo "ERROR: HiveServer2 did not become ready in time."
echo "Last log lines:"
tail -n 80 "$LOG_FILE"
exit 1
