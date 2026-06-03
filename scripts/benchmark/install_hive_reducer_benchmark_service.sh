#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
SERVICE_NAME="${SERVICE_NAME:-flight-delay-hive-reducer-benchmark}"
ENV_FILE="/etc/${SERVICE_NAME}.env"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
S3_URI="${1:-${BENCHMARK_S3_URI:-}}"

sudo tee "$ENV_FILE" >/dev/null <<ENV
PROJECT_ROOT=$PROJECT_ROOT
BENCHMARK_S3_URI=$S3_URI
RESULTS_DIR=results/benchmark_hive_mr_reducer_tuning
DATASETS=14m
ANALYSES=analysis_2 analysis_3
HIVE_REDUCER_VARIANTS=auto r8 r16
REPETITIONS=3
HIVE_CLIENT=beeline
ENV

sudo tee "$SERVICE_FILE" >/dev/null <<SERVICE
[Unit]
Description=Flight Delay Hive MapReduce reducer tuning benchmark
After=network-online.target hadoop-hdfs-namenode.service hadoop-yarn-resourcemanager.service
Wants=network-online.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_ROOT
EnvironmentFile=$ENV_FILE
ExecStart=$PROJECT_ROOT/scripts/benchmark/run_hive_reducer_experiment_service.sh
Restart=no
StandardOutput=append:$PROJECT_ROOT/results/benchmark_hive_mr_reducer_tuning/systemd.out.log
StandardError=append:$PROJECT_ROOT/results/benchmark_hive_mr_reducer_tuning/systemd.err.log

[Install]
WantedBy=multi-user.target
SERVICE

mkdir -p "$PROJECT_ROOT/results/benchmark_hive_mr_reducer_tuning"
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME.service"

echo "Servizio installato: $SERVICE_NAME"
echo "Avvio:       sudo systemctl start $SERVICE_NAME"
echo "Stato:       systemctl status $SERVICE_NAME --no-pager"
echo "Log live:    journalctl -u $SERVICE_NAME -f"
echo "Risultati:   $PROJECT_ROOT/results/benchmark_hive_mr_reducer_tuning"
if [[ -n "$S3_URI" ]]; then
  echo "Upload S3:   $S3_URI/<campaign_tag>/"
else
  echo "Upload S3:   disabilitato; passa s3://bucket/prefix come primo argomento per abilitarlo"
fi
