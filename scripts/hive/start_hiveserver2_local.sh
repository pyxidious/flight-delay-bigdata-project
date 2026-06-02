#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$PROJECT_ROOT"

source scripts/env/project_env.sh

export HIVE_CONF_DIR="$PROJECT_ROOT/hive/conf"
if [ -d "$PROJECT_ROOT/hadoop/conf" ]; then
    export HADOOP_CONF_DIR="$PROJECT_ROOT/hadoop/conf"
fi
export HADOOP_HEAPSIZE=6144
export HADOOP_CLIENT_OPTS="-Xmx6144m ${HADOOP_CLIENT_OPTS:-}"
# Hive 4 forwards HIVE_OPTS to HiveServer2 as application arguments.
export HIVE_SERVER2_HEAPSIZE=6144

PID_FILE="results/tmp/hive/hiveserver2.pid"
HIVE_PID_FILE="$HIVE_CONF_DIR/hiveserver2.pid"
LOG_FILE="results/tmp/hive/logs/hiveserver2.log"
JDBC_URL="jdbc:hive2://localhost:10000/default"
HIVE_BEELINE="$HIVE_HOME/bin/beeline"
HIVE_SERVER2_BIN="$HIVE_HOME/bin/hiveserver2"
STARTUP_ATTEMPTS="${HIVE_SERVER2_STARTUP_ATTEMPTS:-60}"

mkdir -p results/tmp/hive/logs results/tmp/hive/java_tmp results/tmp/hive/operation_logs results/tmp/hive/resources

wait_for_process_exit() {
    local pid="$1"

    for _ in {1..10}; do
        if ! ps -p "$pid" > /dev/null 2>&1; then
            return 0
        fi

        sleep 1
    done

    return 1
}

print_log_tail() {
    echo "Last HiveServer2 log lines:"
    tail -n 120 "$LOG_FILE" 2>/dev/null || true
}

if [ ! -f "$HIVE_CONF_DIR/hive-site.xml" ]; then
    echo "ERROR: missing $HIVE_CONF_DIR/hive-site.xml"
    echo "Run: bash scripts/hive/init_hive_local.sh"
    exit 1
fi

if ! hdfs dfs -ls / >/dev/null 2>&1; then
    echo "ERROR: HDFS is not responding."
    echo "Run: bash scripts/hdfs/start_hdfs_local.sh"
    exit 1
fi

for daemon in NameNode DataNode; do
    if ! jps | awk '{ print $2 }' | grep -qx "$daemon"; then
        echo "ERROR: required HDFS daemon $daemon is not running."
        echo "Run: bash scripts/hdfs/start_hdfs_local.sh"
        exit 1
    fi
done

hdfs dfs -mkdir -p /tmp /tmp/hive /user/hive/warehouse /flight-delay-project
hdfs dfs -chmod 1777 /tmp
hdfs dfs -chmod 1777 /tmp/hive
hdfs dfs -chmod 775 /user/hive/warehouse

echo "Checking HiveServer2 availability on localhost:10000..."

if "$HIVE_BEELINE" -u "$JDBC_URL" -e "SELECT 1;" >/dev/null 2>&1; then
    echo "HiveServer2 is already running."
    exit 0
fi

for EXISTING_PID_FILE in "$PID_FILE" "$HIVE_PID_FILE"; do
    if [ ! -f "$EXISTING_PID_FILE" ]; then
        continue
    fi

    OLD_PID="$(cat "$EXISTING_PID_FILE")"
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "Found HiveServer2 PID file $EXISTING_PID_FILE, but JDBC is not ready."
        echo "Stopping stale/non-ready process PID $OLD_PID..."
        kill "$OLD_PID" || true

        if ! wait_for_process_exit "$OLD_PID"; then
            echo "ERROR: stale HiveServer2 process PID $OLD_PID did not stop."
            echo "Stop it manually before retrying."
            exit 1
        fi
    fi

    rm -f "$EXISTING_PID_FILE"
done

echo "Starting HiveServer2 on localhost:10000..."
echo "Logs: $LOG_FILE"

nohup setsid "$HIVE_SERVER2_BIN" > "$LOG_FILE" 2>&1 < /dev/null &

HIVE_SERVER2_PID=$!
echo "$HIVE_SERVER2_PID" > "$PID_FILE"

echo "HiveServer2 PID: $(cat "$PID_FILE")"
echo "Waiting for HiveServer2 to become available..."

for ((attempt = 1; attempt <= STARTUP_ATTEMPTS; attempt++)); do
    if ! ps -p "$HIVE_SERVER2_PID" > /dev/null 2>&1; then
        echo "ERROR: HiveServer2 process PID $HIVE_SERVER2_PID exited during startup."
        rm -f "$PID_FILE" "$HIVE_PID_FILE"
        print_log_tail
        exit 1
    fi

    if "$HIVE_BEELINE" -u "$JDBC_URL" -e "SELECT 1;" >/dev/null 2>&1; then
        echo "HiveServer2 is ready."
        exit 0
    fi

    echo "Attempt $attempt/$STARTUP_ATTEMPTS: HiveServer2 not ready yet..."
    sleep 2
done

echo "ERROR: HiveServer2 did not become ready in time."
print_log_tail
bash scripts/hive/stop_hiveserver2_local.sh || true
exit 1
