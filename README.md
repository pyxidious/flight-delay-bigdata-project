# Flight Delay Big Data Project

## Italiano

Progetto per il corso di Big Data dell'Universita degli Studi Roma Tre.

Il repository analizza il Flight Delay Dataset 2024 utilizzando tre tecnologie:

- Hive on MapReduce
- Spark Core
- Spark SQL

Sono implementate tre analisi:

1. Statistiche delle compagnie aeree per aeroporto di partenza.
2. Report dei ritardi per aeroporto di partenza, mese e fascia di ritardo.
3. Confronto delle prestazioni compagnia-aeroporto e ranking per aeroporto.

### Struttura Del Repository

```text
data/                 dataset locali grezzi, puliti e scalati
docs/                 ispezione dati, preparazione, validazione e conformita
hadoop/conf/          configurazione HDFS locale
hive/                 query Hive ufficiali
results/benchmark/    artefatti benchmark ufficiali locali
results/benchmark_local/ artefatti benchmark locale usati nella relazione finale
results/benchmark_cluster/ artefatti benchmark EMR usati nella relazione finale
results/previews/     prime 10 righe degli output per la relazione finale
scripts/data/         strumenti di preparazione e scaling
scripts/env/          helper di ambiente
scripts/hdfs/         gestione HDFS locale e upload
scripts/hive/         gestione HiveServer2 locale
scripts/run_benchmark.sh
scripts/run_output_previews.sh
spark_core/           job Spark Core ufficiali
spark_sql/            job Spark SQL ufficiali
```

### Setup

Creare l'ambiente Python e installare le dipendenze:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

L'helper locale si aspetta Spark, Hadoop e Hive sotto `~/bigdata-tools/` e
configura il runtime Java richiesto:

```bash
source scripts/env/project_env.sh
bash scripts/env/check_environment.sh
```

### Preparazione Dei Dati

Posizionare il CSV sorgente in:

```text
data/raw/flight_data_2024.csv
```

Preparare e validare il dataset:

```bash
python scripts/data/inspect_dataset.py
python scripts/data/prepare_data.py
python scripts/data/validate_cleaned_data.py
```

Generare dataset locali di dimensione crescente e caricarli in HDFS:

```bash
bash scripts/data/generate_samples.sh
python scripts/data/generate_replicated_datasets.py --factors 10m 14m
bash scripts/hdfs/start_hdfs_local.sh
bash scripts/hdfs/upload_samples_to_hdfs.sh
bash scripts/hdfs/check_hdfs.sh
```

### Benchmark

Prima di eseguire il benchmark, inizializzare il setup locale di Hive:

```bash
bash scripts/hive/init_hive_local.sh
```

L'unico entrypoint ufficiale del benchmark locale e:

```bash
bash scripts/run_benchmark.sh
```

Per ispezionare il piano senza avviare job:

```bash
bash scripts/run_benchmark.sh --dry-run
```

Gli artefatti ufficiali vengono scritti in `results/benchmark/`. Vedere
[`README_BENCHMARK.md`](README_BENCHMARK.md) per protocollo, configurazione e
istruzioni complete di riproducibilita.

### Varianti Del Comando Benchmark

Le opzioni principali di `scripts/run_benchmark.sh` permettono di selezionare
dataset, analisi, numero di ripetizioni, tecnologie da escludere e directory di
output. Tutte le varianti mantengono lo stesso protocollo: output distribuito su
HDFS, nessun ordinamento globale finale di presentazione e nessuna preview
dentro il timer.

Mostrare il piano senza eseguire job:

```bash
bash scripts/run_benchmark.sh --dry-run
```

Eseguire la campagna completa locale usata come riferimento:

```bash
SPARK_DRIVER_MEMORY=5g \
SPARK_SQL_SHUFFLE_PARTITIONS=64 \
bash scripts/run_benchmark.sh \
  --datasets 100k 500k 1m 3m 7m 10m 14m \
  --analyses analysis_1 analysis_2 analysis_3 \
  --repetitions 3 \
  --results-dir results/benchmark \
  --campaign-tag "benchmark_$(date +%Y%m%d_%H%M%S)" \
  --reset
```

Eseguire un test rapido su un solo dataset e una sola analisi:

```bash
bash scripts/run_benchmark.sh \
  --datasets 100k \
  --analyses analysis_1 \
  --repetitions 1 \
  --results-dir results/benchmark_smoke \
  --campaign-tag smoke_100k_a1 \
  --reset
```

Eseguire solo Spark SQL e Spark Core, saltando Hive:

```bash
bash scripts/run_benchmark.sh \
  --datasets 100k 500k \
  --skip-hive \
  --repetitions 1 \
  --results-dir results/benchmark_spark_only \
  --reset
```

Eseguire solo Hive, saltando Spark SQL e Spark Core:

```bash
bash scripts/run_benchmark.sh \
  --datasets 100k \
  --skip-spark-sql \
  --skip-spark-core \
  --repetitions 1 \
  --results-dir results/benchmark_hive_only \
  --reset
```

Significato delle opzioni principali:

- `--datasets`: sceglie le dimensioni di input da leggere da HDFS.
- `--analyses`: limita la campagna a una o piu analisi.
- `--repetitions`: imposta quante run ripetute eseguire per ogni combinazione.
- `--results-dir`: cambia la directory locale degli artefatti CSV, log e grafici.
- `--campaign-tag`: cambia il prefisso usato per gli output HDFS e per i log.
- `--reset`: archivia eventuali artefatti gia presenti nella directory risultati.
- `--skip-hive`, `--skip-spark-sql`, `--skip-spark-core`: escludono una tecnologia.
- `--yes`: conferma automaticamente alcuni avvisi interattivi.

Per il benchmark su cluster EMR si usa:

```bash
bash scripts/run_benchmark_cluster.sh --dry-run
```

Esempio di campagna EMR principale:

```bash
bash scripts/run_benchmark_cluster.sh \
  --datasets 100k 500k 1m 3m 7m 10m 14m \
  --analyses analysis_1 analysis_2 analysis_3 \
  --repetitions 3 \
  --results-dir results/benchmark_cluster \
  --campaign-tag cluster_4core_all_datasets_mr_final \
  --reset
```

Esempio di variante cluster per esperimenti sui reducer Hive:

```bash
bash scripts/run_benchmark_cluster.sh \
  --datasets 14m \
  --analyses analysis_2 analysis_3 \
  --skip-spark-sql \
  --skip-spark-core \
  --hive-reducer-variants auto r8 r16 \
  --repetitions 3 \
  --results-dir results/hive_reducer_tuning_4workers \
  --reset
```

Nel runner cluster, `--hive-reducer-variants` esegue piu configurazioni
MapReduce per Hive; `--s3-uri` e `--s3-upload` possono caricare gli artefatti
finali su S3 al termine della campagna.

Il repository include anche gli artefatti usati nella relazione finale:

- `results/benchmark_local/`: benchmark locale ripetuto su HDFS.
- `results/benchmark_cluster/`: benchmark ripetuto su AWS EMR a 4 worker.
- `results/hive_reducer_tuning_4workers/`: esperimento extra sui reducer Hive.
- `results/benchmark_hive_mr_horizontal_scaling_8workers_auto/`: esperimento extra Hive a 8 worker.
- `results/benchmark_spark_sql_horizontal_scaling_8workers/`: esperimento extra Spark SQL a 8 worker.

### Preview Degli Output

La relazione finale richiede le prime 10 righe prodotte dai job. Le run di
preview sono separate dal benchmark temporale:

```bash
bash scripts/run_output_previews.sh --datasets 100k --overwrite
```

Per rigenerare le preview per tutti i dataset:

```bash
bash scripts/run_output_previews.sh --datasets 100k 500k 1m 3m 7m 10m 14m --overwrite
```

Gli artefatti vengono scritti in `results/previews/` e non fanno parte della
campagna di misura dei tempi.

## English

Project for the Big Data course at Universita degli Studi Roma Tre.

The repository analyzes the 2024 Flight Delay Dataset with three technologies:

- Hive on MapReduce
- Spark Core
- Spark SQL

It implements three jobs:

1. Airline statistics by origin airport.
2. Delay report by origin airport, month and departure-delay band.
3. Airline-airport performance comparison and airport ranking.

### Repository Structure

```text
data/                 local raw, prepared and scaled datasets
docs/                 data inspection, preparation, validation and compliance notes
hadoop/conf/          local HDFS configuration
hive/                 official Hive queries
results/benchmark/    official local benchmark artifacts
results/benchmark_local/ local benchmark artifacts used in the final report
results/benchmark_cluster/ EMR benchmark artifacts used in the final report
results/previews/     first 10 output rows for the final report
scripts/data/         preparation and scaling tools
scripts/env/          environment helpers
scripts/hdfs/         local HDFS lifecycle and upload helpers
scripts/hive/         local HiveServer2 lifecycle helpers
scripts/run_benchmark.sh
scripts/run_output_previews.sh
spark_core/           official Spark Core jobs
spark_sql/            official Spark SQL jobs
```

### Setup

Create the Python environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The local environment helper expects Spark, Hadoop and Hive under
`~/bigdata-tools/` and configures the required Java runtime:

```bash
source scripts/env/project_env.sh
bash scripts/env/check_environment.sh
```

### Data Preparation

Place the source CSV at:

```text
data/raw/flight_data_2024.csv
```

Prepare and validate the dataset:

```bash
python scripts/data/inspect_dataset.py
python scripts/data/prepare_data.py
python scripts/data/validate_cleaned_data.py
```

Generate increasing local datasets and upload them to HDFS:

```bash
bash scripts/data/generate_samples.sh
python scripts/data/generate_replicated_datasets.py --factors 10m 14m
bash scripts/hdfs/start_hdfs_local.sh
bash scripts/hdfs/upload_samples_to_hdfs.sh
bash scripts/hdfs/check_hdfs.sh
```

### Benchmark

Before running the benchmark, initialize the local Hive setup:

```bash
bash scripts/hive/init_hive_local.sh
```

The only official local benchmark entrypoint is:

```bash
bash scripts/run_benchmark.sh
```

Inspect the plan without starting jobs:

```bash
bash scripts/run_benchmark.sh --dry-run
```

Official artifacts are written under `results/benchmark/`. See
[`README_BENCHMARK.md`](README_BENCHMARK.md) for the protocol, configuration
and complete reproducibility instructions.

### Benchmark Command Variants

The main `scripts/run_benchmark.sh` options let you select datasets, analyses,
repetition count, technologies to skip and output directory. All variants keep
the same protocol: distributed HDFS output, no presentation-only global final
sort and no preview action inside the timed interval.

Show the plan without running jobs:

```bash
bash scripts/run_benchmark.sh --dry-run
```

Run the complete local reference campaign:

```bash
SPARK_DRIVER_MEMORY=5g \
SPARK_SQL_SHUFFLE_PARTITIONS=64 \
bash scripts/run_benchmark.sh \
  --datasets 100k 500k 1m 3m 7m 10m 14m \
  --analyses analysis_1 analysis_2 analysis_3 \
  --repetitions 3 \
  --results-dir results/benchmark \
  --campaign-tag "benchmark_$(date +%Y%m%d_%H%M%S)" \
  --reset
```

Run a quick smoke test on one dataset and one analysis:

```bash
bash scripts/run_benchmark.sh \
  --datasets 100k \
  --analyses analysis_1 \
  --repetitions 1 \
  --results-dir results/benchmark_smoke \
  --campaign-tag smoke_100k_a1 \
  --reset
```

Run only Spark SQL and Spark Core, skipping Hive:

```bash
bash scripts/run_benchmark.sh \
  --datasets 100k 500k \
  --skip-hive \
  --repetitions 1 \
  --results-dir results/benchmark_spark_only \
  --reset
```

Run only Hive, skipping Spark SQL and Spark Core:

```bash
bash scripts/run_benchmark.sh \
  --datasets 100k \
  --skip-spark-sql \
  --skip-spark-core \
  --repetitions 1 \
  --results-dir results/benchmark_hive_only \
  --reset
```

Main option meanings:

- `--datasets`: selects the HDFS input sizes.
- `--analyses`: limits the campaign to one or more analyses.
- `--repetitions`: sets repeated runs per combination.
- `--results-dir`: changes the local artifact directory for CSV files, logs and charts.
- `--campaign-tag`: changes the prefix used for HDFS outputs and logs.
- `--reset`: archives existing artifacts in the result directory.
- `--skip-hive`, `--skip-spark-sql`, `--skip-spark-core`: exclude one technology.
- `--yes`: automatically confirms some interactive warnings.

For the EMR cluster benchmark, use:

```bash
bash scripts/run_benchmark_cluster.sh --dry-run
```

Example main EMR campaign:

```bash
bash scripts/run_benchmark_cluster.sh \
  --datasets 100k 500k 1m 3m 7m 10m 14m \
  --analyses analysis_1 analysis_2 analysis_3 \
  --repetitions 3 \
  --results-dir results/benchmark_cluster \
  --campaign-tag cluster_4core_all_datasets_mr_final \
  --reset
```

Example cluster variant for Hive reducer experiments:

```bash
bash scripts/run_benchmark_cluster.sh \
  --datasets 14m \
  --analyses analysis_2 analysis_3 \
  --skip-spark-sql \
  --skip-spark-core \
  --hive-reducer-variants auto r8 r16 \
  --repetitions 3 \
  --results-dir results/hive_reducer_tuning_4workers \
  --reset
```

In the cluster runner, `--hive-reducer-variants` runs multiple Hive MapReduce
configurations; `--s3-uri` and `--s3-upload` can upload final artifacts to S3
after the campaign completes.

The repository also includes the benchmark artifacts used in the final report:

- `results/benchmark_local/`: local HDFS repeated benchmark.
- `results/benchmark_cluster/`: AWS EMR 4-worker repeated benchmark.
- `results/hive_reducer_tuning_4workers/`: extra Hive reducer experiment.
- `results/benchmark_hive_mr_horizontal_scaling_8workers_auto/`: extra Hive 8-worker scaling experiment.
- `results/benchmark_spark_sql_horizontal_scaling_8workers/`: extra Spark SQL 8-worker scaling experiment.

### Output Previews

The final report requires the first 10 rows produced by the jobs. Preview runs
are intentionally separated from the timed benchmark:

```bash
bash scripts/run_output_previews.sh --datasets 100k --overwrite
```

To regenerate previews for every dataset:

```bash
bash scripts/run_output_previews.sh --datasets 100k 500k 1m 3m 7m 10m 14m --overwrite
```

Preview artifacts are written to `results/previews/` and are not part of the
benchmark timing campaign.
