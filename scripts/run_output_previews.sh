#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

source scripts/env/project_env.sh
if [[ -f ".venv/bin/activate" ]]; then
  source .venv/bin/activate
fi

export HADOOP_CONF_DIR="$PROJECT_ROOT/hadoop/conf"
export HIVE_CONF_DIR="$PROJECT_ROOT/hive/conf"
export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/flight-delay-matplotlib}"
export SPARK_DRIVER_MEMORY="${SPARK_DRIVER_MEMORY:-5g}"
export SPARK_SQL_SHUFFLE_PARTITIONS="${SPARK_SQL_SHUFFLE_PARTITIONS:-64}"

JDBC_URL="jdbc:hive2://localhost:10000/default"
HDFS_INPUT_ROOT="hdfs://localhost:9000/flight-delay-project/input"
HDFS_OUTPUT_ROOT="/flight-delay-project/output/previews"
OUTPUT_DIR="results/previews"
DATASETS=(100k)
ANALYSES=(analysis_1 analysis_2 analysis_3)
TECHNOLOGIES=(hive spark_core spark_sql)
DRY_RUN=false
OVERWRITE=false
YES=false

info() {
  echo "[INFO] $*"
}

usage() {
  cat <<'EOF'
Usage: bash scripts/run_output_previews.sh [options]

Options:
  --datasets VALUES...       Dataset labels (default: 100k)
  --analyses VALUES...       Analyses (default: analysis_1 analysis_2 analysis_3)
  --technologies VALUES...   Technologies (default: hive spark_core spark_sql)
  --output-dir DIR           Local preview output directory (default: results/previews)
  --hdfs-output-root PATH    HDFS preview output root (default: /flight-delay-project/output/previews)
  --overwrite                Replace existing HDFS preview outputs and local preview files
  --dry-run                  Print the plan without checking HDFS or running jobs
  --yes                      Reserved for non-interactive confirmations
  -h, --help                 Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --datasets)
      shift
      DATASETS=()
      while [[ $# -gt 0 && "$1" != --* ]]; do
        DATASETS+=("$1")
        shift
      done
      ;;
    --analyses)
      shift
      ANALYSES=()
      while [[ $# -gt 0 && "$1" != --* ]]; do
        ANALYSES+=("$1")
        shift
      done
      ;;
    --technologies)
      shift
      TECHNOLOGIES=()
      while [[ $# -gt 0 && "$1" != --* ]]; do
        TECHNOLOGIES+=("$1")
        shift
      done
      ;;
    --output-dir)
      OUTPUT_DIR="${2:-}"
      shift 2
      ;;
    --hdfs-output-root)
      HDFS_OUTPUT_ROOT="${2:-}"
      shift 2
      ;;
    --overwrite)
      OVERWRITE=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --yes)
      YES=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[FAIL] unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ ${#DATASETS[@]} -eq 0 || ${#ANALYSES[@]} -eq 0 || ${#TECHNOLOGIES[@]} -eq 0 ]]; then
  echo "[FAIL] datasets, analyses and technologies must not be empty" >&2
  exit 2
fi

validate_values() {
  local kind=$1
  shift
  local allowed=("$1")
  shift
  local values=("$@")

  local value
  for value in "${values[@]}"; do
    case " ${allowed[*]} " in
      *" $value "*) ;;
      *)
        echo "[FAIL] invalid $kind: $value" >&2
        echo "[FAIL] allowed $kind values: ${allowed[*]}" >&2
        exit 2
        ;;
    esac
  done
}

validate_values "dataset" "100k 500k 1m 3m 7m 10m 14m" "${DATASETS[@]}"
validate_values "analysis" "analysis_1 analysis_2 analysis_3" "${ANALYSES[@]}"
validate_values "technology" "hive spark_core spark_sql" "${TECHNOLOGIES[@]}"

contains_technology() {
  local needle=$1
  local item
  for item in "${TECHNOLOGIES[@]}"; do
    [[ "$item" == "$needle" ]] && return 0
  done
  return 1
}

hdfs_input_file() {
  local dataset=$1
  printf '%s/%s/flights.csv' "$HDFS_INPUT_ROOT" "$dataset"
}

hdfs_input_dir() {
  local dataset=$1
  printf '%s/%s' "$HDFS_INPUT_ROOT" "$dataset"
}

hdfs_output_path() {
  local dataset=$1
  local analysis=$2
  local technology=$3
  printf '%s/%s/%s/%s' "${HDFS_OUTPUT_ROOT%/}" "$dataset" "$analysis" "$technology"
}

preview_file_path() {
  local dataset=$1
  local analysis=$2
  local technology=$3
  printf '%s/%s/%s/%s_first10.csv' "${OUTPUT_DIR%/}" "$dataset" "$analysis" "$technology"
}

log_file_path() {
  local dataset=$1
  local analysis=$2
  local technology=$3
  printf '%s/logs/%s_%s_%s.log' "${OUTPUT_DIR%/}" "$dataset" "$analysis" "$technology"
}

hive_sql_file() {
  case "$1" in
    analysis_1) printf 'hive/analysis_1_airline_stats.sql' ;;
    analysis_2) printf 'hive/analysis_2_airport_month_delay_report.sql' ;;
    analysis_3) printf 'hive/analysis_3_airline_airport_ranking.sql' ;;
  esac
}

spark_script() {
  local technology=$1
  local analysis=$2
  local base
  base="$technology"

  case "$analysis" in
    analysis_1) printf '%s/analysis_1_airline_stats.py' "$base" ;;
    analysis_2) printf '%s/analysis_2_airport_month_delay_report.py' "$base" ;;
    analysis_3) printf '%s/analysis_3_airline_airport_ranking.py' "$base" ;;
  esac
}

job_command_text() {
  local dataset=$1
  local analysis=$2
  local technology=$3
  local target=$4

  case "$technology" in
    hive)
      printf 'beeline -u %q --hiveconf hive.execution.engine=mr --hiveconf output_dir=%q -f %q' \
        "$JDBC_URL" "$target" "$(hive_sql_file "$analysis")"
      ;;
    spark_core)
      printf 'spark-submit --master local[*] --driver-memory %q %q --input %q --output %q' \
        "$SPARK_DRIVER_MEMORY" "$(spark_script "$technology" "$analysis")" "$(hdfs_input_file "$dataset")" "$target"
      ;;
    spark_sql)
      printf 'spark-submit --master local[*] --driver-memory %q --conf spark.sql.shuffle.partitions=%q %q --input %q --output %q' \
        "$SPARK_DRIVER_MEMORY" "$SPARK_SQL_SHUFFLE_PARTITIONS" "$(spark_script "$technology" "$analysis")" "$(hdfs_input_file "$dataset")" "$target"
      ;;
  esac
}

require_hdfs() {
  info "checking HDFS prerequisites"
  if ! command -v hdfs >/dev/null 2>&1; then
    echo "[FAIL] hdfs command not found; source project environment first." >&2
    exit 1
  fi
  if ! command -v jps >/dev/null 2>&1; then
    echo "[FAIL] jps command not found; JAVA_HOME/PATH is not configured." >&2
    exit 1
  fi
  for daemon in NameNode DataNode; do
    if ! jps | awk '{ print $2 }' | grep -qx "$daemon"; then
      echo "[FAIL] HDFS is not active: missing $daemon. Run: bash scripts/hdfs/start_hdfs_local.sh" >&2
      exit 1
    fi
  done
  if ! hdfs dfs -ls / >/dev/null 2>&1; then
    echo "[FAIL] HDFS is not responding to: hdfs dfs -ls /" >&2
    echo "[FAIL] Run: bash scripts/hdfs/start_hdfs_local.sh" >&2
    exit 1
  fi
  info "HDFS ready"
}

start_hive_if_needed() {
  if contains_technology hive; then
    info "starting HiveServer2 if needed"
    bash scripts/hive/start_hiveserver2_local.sh >/dev/null
    info "HiveServer2 ready"
  fi
}

stop_hive_if_needed() {
  if contains_technology hive; then
    info "stopping HiveServer2"
    bash scripts/hive/stop_hiveserver2_local.sh >/dev/null || true
    info "HiveServer2 stop requested"
  fi
}

prepare_hive_dataset() {
  local dataset=$1
  local log_file=$2
  {
    printf '\n$ beeline -u %q --hiveconf hive.execution.engine=mr --hiveconf input_dir=%q -f hive/prepare_flights_table.sql\n' \
      "$JDBC_URL" "$(hdfs_input_dir "$dataset")"
    beeline \
      -u "$JDBC_URL" \
      --hiveconf hive.execution.engine=mr \
      --hiveconf "input_dir=$(hdfs_input_dir "$dataset")" \
      -f hive/prepare_flights_table.sql
  } >> "$log_file" 2>&1
}

run_job() {
  local dataset=$1
  local analysis=$2
  local technology=$3
  local target=$4
  local log_file=$5

  case "$technology" in
    hive)
      {
        printf '\n$ %s\n' "$(job_command_text "$dataset" "$analysis" "$technology" "$target")"
        beeline \
          -u "$JDBC_URL" \
          --hiveconf hive.execution.engine=mr \
          --hiveconf "output_dir=$target" \
          -f "$(hive_sql_file "$analysis")"
      } >> "$log_file" 2>&1
      ;;
    spark_core)
      {
        printf '\n$ %s\n' "$(job_command_text "$dataset" "$analysis" "$technology" "$target")"
        spark-submit \
          --master "local[*]" \
          --driver-memory "$SPARK_DRIVER_MEMORY" \
          "$(spark_script "$technology" "$analysis")" \
          --input "$(hdfs_input_file "$dataset")" \
          --output "$target"
      } >> "$log_file" 2>&1
      ;;
    spark_sql)
      {
        printf '\n$ %s\n' "$(job_command_text "$dataset" "$analysis" "$technology" "$target")"
        spark-submit \
          --master "local[*]" \
          --driver-memory "$SPARK_DRIVER_MEMORY" \
          --conf "spark.sql.shuffle.partitions=$SPARK_SQL_SHUFFLE_PARTITIONS" \
          "$(spark_script "$technology" "$analysis")" \
          --input "$(hdfs_input_file "$dataset")" \
          --output "$target"
      } >> "$log_file" 2>&1
      ;;
  esac
}

extract_preview() {
  local target=$1
  local preview_file=$2
  local log_file=${3:-}
  local tmp_file
  local err_file
  local cat_status
  local head_status
  local ls_status
  local ls_output
  local line
  local path
  local name
  local pipeline_status
  local err_text
  local data_files=()

  tmp_file="$(mktemp)"
  err_file="$(mktemp)"

  set +e
  ls_output="$(hdfs dfs -ls "$target" 2>"$err_file")"
  ls_status=$?
  set -e

  if [[ "$ls_status" -ne 0 ]]; then
    err_text="$(tr '\n' ' ' < "$err_file" | sed 's/[[:space:]][[:space:]]*/ /g' | cut -c 1-500)"
    if [[ -n "$log_file" ]]; then
      printf 'PREVIEW EXTRACTION ERROR: unable to list output=%s status=%s error=%s\n' "$target" "$ls_status" "$err_text" >> "$log_file"
    fi
    rm -f "$tmp_file" "$err_file"
    return 1
  fi

  while IFS= read -r line; do
    [[ "$line" == -* ]] || continue
    path="${line##* }"
    name="${path##*/}"
    [[ "$name" == _* || "$name" == .* ]] && continue
    data_files+=("$path")
  done <<< "$ls_output"

  if [[ ${#data_files[@]} -eq 0 ]]; then
    if [[ -n "$log_file" ]]; then
      printf 'PREVIEW EXTRACTION ERROR: no data files found in output=%s\n' "$target" >> "$log_file"
    fi
    rm -f "$tmp_file" "$err_file"
    return 1
  fi

  if [[ -n "$log_file" ]]; then
    {
      printf '\n$ hdfs dfs -cat'
      printf ' %q' "${data_files[@]}"
      printf ' | head -n 10 > %q\n' "$preview_file"
      printf 'PREVIEW EXTRACTION FILES: %s\n' "${data_files[*]}"
    } >> "$log_file"
  fi

  : > "$err_file"
  set +e
  hdfs dfs -cat "${data_files[@]}" 2>"$err_file" | head -n 10 > "$tmp_file"
  pipeline_status=("${PIPESTATUS[@]}")
  set -e
  cat_status=${pipeline_status[0]:-1}
  head_status=${pipeline_status[1]:-1}
  err_text="$(tr '\n' ' ' < "$err_file" | sed 's/[[:space:]][[:space:]]*/ /g' | cut -c 1-500)"

  if [[ "$head_status" -ne 0 ]]; then
    if [[ -n "$log_file" ]]; then
      printf 'PREVIEW EXTRACTION ERROR: head_status=%s cat_status=%s error=%s\n' "$head_status" "$cat_status" "$err_text" >> "$log_file"
    fi
    rm -f "$tmp_file" "$err_file"
    return 1
  fi

  if [[ "$cat_status" -ne 0 && "$cat_status" -ne 141 ]]; then
    if [[ ! -s "$tmp_file" ]] || [[ "$err_text" != *"Unable to write to output stream"* && "$err_text" != *"Broken pipe"* ]]; then
      if [[ -n "$log_file" ]]; then
        printf 'PREVIEW EXTRACTION ERROR: head_status=%s cat_status=%s error=%s\n' "$head_status" "$cat_status" "$err_text" >> "$log_file"
      fi
      rm -f "$tmp_file" "$err_file"
      return 1
    fi
    if [[ -n "$log_file" ]]; then
      printf 'PREVIEW EXTRACTION NOTE: ignored expected pipe close from head; cat_status=%s error=%s\n' "$cat_status" "$err_text" >> "$log_file"
    fi
  fi

  mkdir -p "$(dirname "$preview_file")"
  mv "$tmp_file" "$preview_file"
  rm -f "$err_file"
}

write_markdown() {
  local report="${OUTPUT_DIR%/}/output_previews.md"
  mkdir -p "$OUTPUT_DIR"
  {
    printf '# Preview degli output dei job\n\n'
    printf 'Le righe mostrate sono le prime 10 righe fisiche lette dagli output distribuiti HDFS. Poiché non viene applicato un ordinamento globale finale, l'\''ordine delle righe può variare tra esecuzioni o ambienti diversi. La semantica e lo schema degli output rimangono invariati.\n\n'
    printf 'Queste run sono state eseguite solo per produrre preview dei risultati e non fanno parte del benchmark temporale.\n\n'

    local dataset analysis technology preview_file
    for dataset in "${DATASETS[@]}"; do
      printf '## %s\n\n' "$dataset"
      for analysis in "${ANALYSES[@]}"; do
        printf '### %s\n\n' "$analysis"
        for technology in "${TECHNOLOGIES[@]}"; do
          preview_file="$(preview_file_path "$dataset" "$analysis" "$technology")"
          printf '#### %s\n\n' "$technology"
          printf '```text\n'
          if [[ -f "$preview_file" ]]; then
            sed 's/\r$//' "$preview_file"
          else
            printf '[WARN] preview non disponibile\n'
          fi
          printf '\n```\n\n'
        done
      done
    done
  } > "$report"
}

if [[ "$DRY_RUN" == true ]]; then
  echo "[DRY] datasets: ${DATASETS[*]}"
  echo "[DRY] analyses: ${ANALYSES[*]}"
  echo "[DRY] technologies: ${TECHNOLOGIES[*]}"
  for dataset in "${DATASETS[@]}"; do
    echo "[DRY] input: $(hdfs_input_file "$dataset")"
    if contains_technology hive; then
      echo "[DRY] hive prepare: beeline -u $JDBC_URL --hiveconf hive.execution.engine=mr --hiveconf input_dir=$(hdfs_input_dir "$dataset") -f hive/prepare_flights_table.sql"
    fi
    for analysis in "${ANALYSES[@]}"; do
      for technology in "${TECHNOLOGIES[@]}"; do
        target="$(hdfs_output_path "$dataset" "$analysis" "$technology")"
        preview_file="$(preview_file_path "$dataset" "$analysis" "$technology")"
        echo "[DRY] output: $target"
        echo "[DRY] preview: $preview_file"
        echo "[DRY] command: $(job_command_text "$dataset" "$analysis" "$technology" "$target")"
      done
    done
  done
  exit 0
fi

mkdir -p "$OUTPUT_DIR/logs" "$MPLCONFIGDIR"

info "output directory: $OUTPUT_DIR"
info "HDFS output root: $HDFS_OUTPUT_ROOT"
info "selected datasets: ${DATASETS[*]}"
info "selected analyses: ${ANALYSES[*]}"
info "selected technologies: ${TECHNOLOGIES[*]}"
info "overwrite: $OVERWRITE"

require_hdfs
start_hive_if_needed
trap stop_hive_if_needed EXIT

declare -A DATASET_AVAILABLE=()

info "checking HDFS inputs"
for dataset in "${DATASETS[@]}"; do
  info "checking input for dataset $dataset: $(hdfs_input_file "$dataset")"
  if hdfs dfs -test -e "$(hdfs_input_file "$dataset")"; then
    DATASET_AVAILABLE["$dataset"]=true
    info "$dataset input found"
  else
    DATASET_AVAILABLE["$dataset"]=false
    echo "[WARN] $dataset input not found: $(hdfs_input_file "$dataset")"
  fi
done

total_jobs=0
for dataset in "${DATASETS[@]}"; do
  [[ "${DATASET_AVAILABLE[$dataset]}" == true ]] || continue
  total_jobs=$((total_jobs + ${#ANALYSES[@]} * ${#TECHNOLOGIES[@]}))
done
current_job=0
info "planned executable jobs: $total_jobs"

for dataset in "${DATASETS[@]}"; do
  [[ "${DATASET_AVAILABLE[$dataset]}" == true ]] || continue
  info "dataset $dataset started"

  if contains_technology hive; then
    prepare_log="${OUTPUT_DIR%/}/logs/${dataset}_hive_prepare.log"
    : > "$prepare_log"
    info "$dataset preparing Hive external table log=$prepare_log"
    if ! prepare_hive_dataset "$dataset" "$prepare_log"; then
      echo "[FAIL] $dataset hive prepare log=$prepare_log"
      DATASET_AVAILABLE["$dataset"]=false
      continue
    fi
    info "$dataset Hive external table ready"
  fi

  for analysis in "${ANALYSES[@]}"; do
    info "$dataset $analysis started"
    for technology in "${TECHNOLOGIES[@]}"; do
      current_job=$((current_job + 1))
      target="$(hdfs_output_path "$dataset" "$analysis" "$technology")"
      preview_file="$(preview_file_path "$dataset" "$analysis" "$technology")"
      log_file="$(log_file_path "$dataset" "$analysis" "$technology")"
      mkdir -p "$(dirname "$log_file")"
      : > "$log_file"
      info "job $current_job/$total_jobs $dataset $analysis $technology output=$target log=$log_file"

      if hdfs dfs -test -e "$target"; then
        if [[ "$OVERWRITE" == true ]]; then
          info "$dataset $analysis $technology removing existing HDFS output"
          hdfs dfs -rm -r -f "$target" >> "$log_file" 2>&1
        else
          info "$dataset $analysis $technology output exists; extracting preview only"
          if extract_preview "$target" "$preview_file" "$log_file"; then
            echo "[SKIP] $dataset $analysis $technology preview extracted from existing output"
          else
            echo "[SKIP] $dataset $analysis $technology output exists; preview not readable log=$log_file"
          fi
          continue
        fi
      fi

      info "$dataset $analysis $technology running job"
      if ! run_job "$dataset" "$analysis" "$technology" "$target" "$log_file"; then
        echo "[FAIL] $dataset $analysis $technology log=$log_file"
        continue
      fi

      info "$dataset $analysis $technology extracting first 10 rows"
      if extract_preview "$target" "$preview_file" "$log_file"; then
        echo "[OK] $dataset $analysis $technology preview generated"
      else
        echo "[FAIL] $dataset $analysis $technology preview extraction log=$log_file"
      fi
    done
  done
  info "dataset $dataset completed"
done

info "writing Markdown report: ${OUTPUT_DIR%/}/output_previews.md"
write_markdown
info "preview generation completed"
