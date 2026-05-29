#!/usr/bin/env bash

set -euo pipefail

PID_FILE="results/tmp/hive/hiveserver2.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "HiveServer2 PID file not found. Nothing to stop."
    exit 0
fi

PID="$(cat "$PID_FILE")"

if ps -p "$PID" > /dev/null 2>&1; then
    echo "Stopping HiveServer2 PID $PID..."
    kill "$PID"
else
    echo "HiveServer2 process $PID is not running."
fi

rm -f "$PID_FILE"
echo "HiveServer2 stopped."
