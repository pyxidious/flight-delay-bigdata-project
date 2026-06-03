#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$HOME/flight-delay-bigdata-project}"
cd "$PROJECT_ROOT"

CAMPAIGN_TAG="${CAMPAIGN_TAG:-hive_mr_reducer_tuning_$(date -u +%Y%m%d_%H%M%S)}"
RESULTS_DIR="${RESULTS_DIR:-results/benchmark_hive_mr_reducer_tuning}"
S3_ARGS=()
if [[ -n "${BENCHMARK_S3_URI:-}" ]]; then
  S3_ARGS=(--s3-upload --s3-uri "$BENCHMARK_S3_URI")
fi

exec scripts/run_benchmark_cluster.sh \
  --skip-spark-sql \
  --skip-spark-core \
  --datasets "${DATASETS:-14m}" \
  --analyses ${ANALYSES:-analysis_2 analysis_3} \
  --hive-reducer-variants ${HIVE_REDUCER_VARIANTS:-auto r8 r16} \
  --repetitions "${REPETITIONS:-3}" \
  --campaign-tag "$CAMPAIGN_TAG" \
  --results-dir "$RESULTS_DIR" \
  --reset \
  --yes \
  "${S3_ARGS[@]}"
