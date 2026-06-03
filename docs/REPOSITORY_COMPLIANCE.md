# Checklist Di Conformita Del Repository / Repository Compliance Checklist

## Italiano

Questo file collega il repository ai requisiti della traccia e alla relazione finale.

### Analisi Implementate

Sono implementate tutte e tre le analisi richieste:

| Analisi | Hive | Spark Core | Spark SQL |
|---|---|---|---|
| `analysis_1` statistiche compagnia-aeroporto | `hive/analysis_1_airline_stats.sql` | `spark_core/analysis_1_airline_stats.py` | `spark_sql/analysis_1_airline_stats.py` |
| `analysis_2` report ritardi per aeroporto, mese e fascia | `hive/analysis_2_airport_month_delay_report.sql` | `spark_core/analysis_2_airport_month_delay_report.py` | `spark_sql/analysis_2_airport_month_delay_report.py` |
| `analysis_3` ranking compagnia-aeroporto | `hive/analysis_3_airline_airport_ranking.sql` | `spark_core/analysis_3_airline_airport_ranking.py` | `spark_sql/analysis_3_airline_airport_ranking.py` |

Le tecnologie selezionate sono Hive-on-MapReduce, Spark Core e Spark SQL.

### Preparazione Dei Dati

Preparazione e validazione sono coperte da:

- `scripts/data/inspect_dataset.py`
- `scripts/data/prepare_data.py`
- `scripts/data/validate_cleaned_data.py`
- `scripts/data/generate_samples.sh`
- `scripts/data/generate_replicated_datasets.py`
- `docs/dataset_inspection.md`
- `docs/cleaning_report.md`
- `docs/cleaned_data_validation.md`

La convenzione di upload HDFS e:

```text
/flight-delay-project/input/<dataset_label>/flights.csv
```

### Script Di Esecuzione

Servizi locali e upload dati:

- `scripts/hdfs/init_hdfs_local.sh`
- `scripts/hdfs/start_hdfs_local.sh`
- `scripts/hdfs/check_hdfs.sh`
- `scripts/hdfs/upload_samples_to_hdfs.sh`
- `scripts/hdfs/stop_hdfs_local.sh`
- `scripts/hive/init_hive_local.sh`
- `scripts/hive/start_hiveserver2_local.sh`
- `scripts/hive/stop_hiveserver2_local.sh`

Entrypoint benchmark:

- `scripts/run_benchmark.sh`
- `scripts/run_benchmark_cluster.sh`

Entrypoint preview output:

- `scripts/run_output_previews.sh`
- `scripts/export_output_previews.sh`

### Artefatti Dei Risultati

Gli artefatti del benchmark locale sono disponibili in:

- `results/benchmark/`
- `results/benchmark_local/`

Gli artefatti cluster e degli esperimenti extra sono disponibili in:

- `results/benchmark_cluster/`
- `results/hive_reducer_tuning_4workers/`
- `results/benchmark_hive_mr_horizontal_scaling_8workers_auto/`
- `results/benchmark_spark_sql_horizontal_scaling_8workers/`

Le prime 10 righe degli output sono disponibili in:

```text
results/previews/<dataset>/<analysis>/<technology>_first10.csv
results/previews/output_previews.md
```

### Vincoli Metodologici

Il benchmark temporizzato mantiene output distribuito su HDFS. Non introduce:

- output single-file;
- `coalesce(1)` o forzature equivalenti a singola partizione;
- ordinamento globale finale di sola presentazione;
- azioni `show`, `take` o preview dentro i job;
- Tez per Hive.

Gli script di preview sono esterni alla campagna di misura dei tempi.

## English

This file maps the project repository to the requirements in the assignment trace and to the final report.

### Implemented Analyses

All three requested analyses are implemented:

| Analysis | Hive | Spark Core | Spark SQL |
|---|---|---|---|
| `analysis_1` airline statistics by origin airport | `hive/analysis_1_airline_stats.sql` | `spark_core/analysis_1_airline_stats.py` | `spark_sql/analysis_1_airline_stats.py` |
| `analysis_2` delay report by airport, month and delay band | `hive/analysis_2_airport_month_delay_report.sql` | `spark_core/analysis_2_airport_month_delay_report.py` | `spark_sql/analysis_2_airport_month_delay_report.py` |
| `analysis_3` airline-airport ranking | `hive/analysis_3_airline_airport_ranking.sql` | `spark_core/analysis_3_airline_airport_ranking.py` | `spark_sql/analysis_3_airline_airport_ranking.py` |

The selected technologies are Hive-on-MapReduce, Spark Core and Spark SQL.

### Data Preparation

Preparation and validation are covered by:

- `scripts/data/inspect_dataset.py`
- `scripts/data/prepare_data.py`
- `scripts/data/validate_cleaned_data.py`
- `scripts/data/generate_samples.sh`
- `scripts/data/generate_replicated_datasets.py`
- `docs/dataset_inspection.md`
- `docs/cleaning_report.md`
- `docs/cleaned_data_validation.md`

The HDFS upload convention is:

```text
/flight-delay-project/input/<dataset_label>/flights.csv
```

### Execution Scripts

Local services and data upload:

- `scripts/hdfs/init_hdfs_local.sh`
- `scripts/hdfs/start_hdfs_local.sh`
- `scripts/hdfs/check_hdfs.sh`
- `scripts/hdfs/upload_samples_to_hdfs.sh`
- `scripts/hdfs/stop_hdfs_local.sh`
- `scripts/hive/init_hive_local.sh`
- `scripts/hive/start_hiveserver2_local.sh`
- `scripts/hive/stop_hiveserver2_local.sh`

Benchmark entrypoints:

- `scripts/run_benchmark.sh`
- `scripts/run_benchmark_cluster.sh`

Output preview entrypoints:

- `scripts/run_output_previews.sh`
- `scripts/export_output_previews.sh`

### Result Artifacts

Local benchmark artifacts are available under both:

- `results/benchmark/`
- `results/benchmark_local/`

Cluster and extra experiment artifacts are available under:

- `results/benchmark_cluster/`
- `results/hive_reducer_tuning_4workers/`
- `results/benchmark_hive_mr_horizontal_scaling_8workers_auto/`
- `results/benchmark_spark_sql_horizontal_scaling_8workers/`

The first 10 output rows are available under:

```text
results/previews/<dataset>/<analysis>/<technology>_first10.csv
results/previews/output_previews.md
```

### Methodological Guardrails

The timed benchmark keeps output distributed on HDFS. It does not introduce:

- single-file output;
- `coalesce(1)` or equivalent single-partition forcing;
- a presentation-only global final sort;
- in-job `show`, `take` or preview actions;
- Tez for Hive.

The output preview scripts are outside the benchmark timing campaign.
