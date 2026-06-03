# Benchmark HDFS Ripetuto Ufficiale / Official HDFS Repeated Benchmark

## Italiano

L'unico entrypoint ufficiale del benchmark locale e:

```bash
bash scripts/run_benchmark.sh
```

Lo script esegue `analysis_1`, `analysis_2` e `analysis_3` in tre blocchi
tecnologici:

1. Hive
2. Spark SQL
3. Spark Core

Ogni combinazione tecnologia-analisi-dataset viene ripetuta tre volte di
default. Il timer include l'invocazione del job analitico e la scrittura
dell'output distribuito su HDFS. Cleanup, preparazione tabella Hive, ciclo di
vita di HiveServer2, controlli di memoria, listing HDFS, conteggio righe,
summary e grafici restano fuori dal timer.

### Preparazione Dei Dati

A partire da `data/raw/flight_data_2024.csv`, eseguire:

```bash
python scripts/data/inspect_dataset.py
python scripts/data/prepare_data.py
python scripts/data/validate_cleaned_data.py
bash scripts/data/generate_samples.sh
python scripts/data/generate_replicated_datasets.py --factors 10m 14m
```

Questo produce le dimensioni locali usate nella campagna ufficiale:

```text
100k 500k 1m 3m 7m 10m 14m
```

### Upload HDFS

Avviare HDFS, caricare i dataset generati e verificare la disponibilita:

```bash
bash scripts/hdfs/start_hdfs_local.sh
bash scripts/hdfs/upload_samples_to_hdfs.sh
bash scripts/hdfs/check_hdfs.sh
```

HDFS rimane attivo per tutta la campagna.

### Dry Run

Per ispezionare il piano ufficiale senza avviare Hive, Spark o job benchmark:

```bash
bash scripts/run_benchmark.sh --dry-run
```

### Campagna Ufficiale

```bash
SPARK_DRIVER_MEMORY=5g \
SPARK_SQL_SHUFFLE_PARTITIONS=64 \
bash scripts/run_benchmark.sh \
  --datasets 100k 500k 1m 3m 7m 10m 14m \
  --repetitions 3 \
  --results-dir results/benchmark \
  --campaign-tag "benchmark_$(date +%Y%m%d_%H%M%S)" \
  --reset
```

Usare `--yes` solo quando e opportuno confermare automaticamente warning di
memoria o stop di HiveServer2.

### Servizi E Configurazione

- `SPARK_DRIVER_MEMORY=5g`
- `SPARK_SQL_SHUFFLE_PARTITIONS=64`
- Hive viene eseguito su MapReduce.
- HiveServer2 viene avviato solo per il blocco Hive.
- HiveServer2 viene fermato prima di Spark SQL e Spark Core.
- Avvio e stop di HiveServer2 sono fuori dall'intervallo temporizzato.

### Risultati

Gli artefatti ufficiali vengono scritti in `results/benchmark/`:

- `benchmark_runs.csv`: una riga per ogni run ripetuta.
- `benchmark_summary.csv`: statistiche aggregate sui tempi.
- `benchmark_analysis_1.png`: grafico dei tempi di Analysis 1.
- `benchmark_analysis_2.png`: grafico dei tempi di Analysis 2.
- `benchmark_analysis_3.png`: grafico dei tempi di Analysis 3.
- `benchmark_report.md`: protocollo e report generato.
- `session.log`: diagnostica memoria, swap e JVM.
- `logs/`: un log di esecuzione per ogni run.

### Esportazione Delle Prime 10 Righe Degli Output

Per generare preview locali dalle directory HDFS gia prodotte dal benchmark:

```bash
bash scripts/export_output_previews.sh --overwrite
```

Le preview sono usate solo per la relazione finale e non fanno parte del
benchmark temporale.

### Generazione Preview Degli Output

Lo script `scripts/run_output_previews.sh` e separato dal benchmark: non misura
performance, non aggiorna i CSV del benchmark, non genera grafici ed esegue una
sola run per combinazione dataset/analisi/tecnologia. Gli output restano
distribuiti su HDFS e le prime 10 righe vengono salvate in `results/previews/`.

Comando consigliato per la relazione:

```bash
bash scripts/run_output_previews.sh --datasets 100k --overwrite
```

### Note Di Riproducibilita

Il benchmark scrive output distribuito. Non introduce un ordinamento globale
finale di sola presentazione, `coalesce(1)`, preview temporizzate o Tez.

`analysis_3` confronta ogni coppia compagnia-aeroporto con la media del ritardo
in partenza dell'aeroporto. Le medie dei ritardi in arrivo usano solo voli
completati, mentre i tassi di cancellazione usano tutti i voli. Spark SQL e Hive
usano una window partizionata per `origin`; Spark Core esegue l'ordinamento
equivalente dentro ogni gruppo aeroporto.

## English

The only official local benchmark entrypoint is:

```bash
bash scripts/run_benchmark.sh
```

It executes `analysis_1`, `analysis_2` and `analysis_3` in three technology
blocks:

1. Hive
2. Spark SQL
3. Spark Core

Each technology-analysis-dataset combination is repeated three times by
default. The timer includes analytical job invocation and distributed HDFS
output write. Cleanup, Hive table setup, HiveServer2 lifecycle, memory checks,
HDFS listing, row counting, summaries and plots remain outside the timer.

### Data Preparation

Starting from `data/raw/flight_data_2024.csv`, run:

```bash
python scripts/data/inspect_dataset.py
python scripts/data/prepare_data.py
python scripts/data/validate_cleaned_data.py
bash scripts/data/generate_samples.sh
python scripts/data/generate_replicated_datasets.py --factors 10m 14m
```

This produces the local dataset sizes used by the official campaign:

```text
100k 500k 1m 3m 7m 10m 14m
```

### HDFS Upload

Start HDFS, upload the generated datasets and verify availability:

```bash
bash scripts/hdfs/start_hdfs_local.sh
bash scripts/hdfs/upload_samples_to_hdfs.sh
bash scripts/hdfs/check_hdfs.sh
```

HDFS remains active throughout the campaign.

### Dry Run

Inspect the official plan without starting Hive, Spark or benchmark jobs:

```bash
bash scripts/run_benchmark.sh --dry-run
```

### Official Campaign

```bash
SPARK_DRIVER_MEMORY=5g \
SPARK_SQL_SHUFFLE_PARTITIONS=64 \
bash scripts/run_benchmark.sh \
  --datasets 100k 500k 1m 3m 7m 10m 14m \
  --repetitions 3 \
  --results-dir results/benchmark \
  --campaign-tag "benchmark_$(date +%Y%m%d_%H%M%S)" \
  --reset
```

Use `--yes` only when automatic confirmation of memory warnings or a
HiveServer2 stop is appropriate.

### Services And Configuration

- `SPARK_DRIVER_MEMORY=5g`
- `SPARK_SQL_SHUFFLE_PARTITIONS=64`
- Hive runs on MapReduce.
- HiveServer2 is started only for the Hive block.
- HiveServer2 is stopped before Spark SQL and Spark Core.
- HiveServer2 start and stop are outside the timed interval.

### Results

Official artifacts are written to `results/benchmark/`:

- `benchmark_runs.csv`: one row for each repeated run.
- `benchmark_summary.csv`: aggregate timing statistics.
- `benchmark_analysis_1.png`: Analysis 1 timing chart.
- `benchmark_analysis_2.png`: Analysis 2 timing chart.
- `benchmark_analysis_3.png`: Analysis 3 timing chart.
- `benchmark_report.md`: protocol and generated result report.
- `session.log`: memory, swap and JVM diagnostics.
- `logs/`: one execution log per run.

### Exporting The First 10 Output Rows

To generate local previews from HDFS directories already produced by the
benchmark:

```bash
bash scripts/export_output_previews.sh --overwrite
```

Previews are used only for the final report and are not part of benchmark
timing.

### Generating Output Previews

The `scripts/run_output_previews.sh` script is separate from the benchmark: it
does not measure performance, update benchmark CSV files or generate charts,
and it runs a single job per dataset/analysis/technology combination. Outputs
remain distributed on HDFS and the first 10 rows are saved in
`results/previews/`.

Recommended command for the final report:

```bash
bash scripts/run_output_previews.sh --datasets 100k --overwrite
```

### Reproducibility Notes

The benchmark writes distributed output. It does not add a presentation-only
global final sort, `coalesce(1)`, timed preview action or Tez execution.

Analysis 3 compares each airline-origin pair with the flight-level average
departure delay of the airport. Arrival-delay averages use completed flights
only, while cancellation rates use all flights. Spark SQL and Hive use a
window partitioned by `origin`; Spark Core performs the equivalent ordering
inside each airport group.
