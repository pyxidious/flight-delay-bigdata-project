#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$PROJECT_ROOT"

PID_FILES=(
    "results/tmp/hive/hiveserver2.pid"
    "hive/conf/hiveserver2.pid"
)
PROCESS_PATTERN="org.apache.hive.service.server.HiveServer2"

for PID_FILE in "${PID_FILES[@]}"; do
    if [ ! -f "$PID_FILE" ]; then
        continue
    fi

    PID="$(cat "$PID_FILE")"
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Stopping HiveServer2 PID $PID from $PID_FILE..."
        kill "$PID" || true
        sleep 2
    else
        echo "HiveServer2 process $PID from $PID_FILE is not running."
    fi

    rm -f "$PID_FILE"
done

RUNNING_PIDS="$(pgrep -f "$PROCESS_PATTERN" || true)"

if [ -z "$RUNNING_PIDS" ]; then
    echo "No HiveServer2 process is running."
    exit 0
fi

echo "Found HiveServer2 process(es) without PID file:"
echo "$RUNNING_PIDS"

for PID in $RUNNING_PIDS; do
    echo "Stopping HiveServer2 PID $PID..."
    kill "$PID" || true
done

sleep 2

STILL_RUNNING_PIDS="$(pgrep -f "$PROCESS_PATTERN" || true)"

if [ -z "$STILL_RUNNING_PIDS" ]; then
    echo "HiveServer2 stopped."
else
    echo "WARNING: some HiveServer2 process(es) are still running:"
    echo "$STILL_RUNNING_PIDS"
    echo "You may need to stop them manually with: kill -9 <PID>"
fi
