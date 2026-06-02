# Final Repository Check

## Check Metadata

- Checked at: `2026-06-02T14:00:32+02:00`
- Commit readiness: **READY**
- Full benchmark executed during this check: **no**
- HDFS stopped during this check: **no**

## Passed Checks

- Required repository structure is present:
  `README.md`, `README_BENCHMARK.md`, `requirements.txt`,
  `scripts/run_benchmark.sh`, `scripts/benchmark/run_benchmark.py`,
  data helpers, environment helpers, HDFS helpers, Hive helpers, Spark SQL
  jobs, Spark Core jobs, Hive queries and `results/benchmark/`.
- `Secondo progetto.md` is not present in the repository.
- No obsolete benchmark result directory is tracked.
- `.gitignore` covers virtual environments, Python caches, local archives,
  Hadoop runtime data, Hive metastore data, Derby logs and local output/temp
  directories.
- No tracked unwanted runtime files were found.
- No file larger than 50 MiB was found outside the explicitly excluded local
  data, virtual environment and HDFS runtime directories.
- `bash -n scripts/run_benchmark.sh` passed.
- Python compilation passed for the official benchmark helper and all Spark
  SQL and Spark Core jobs.
- `bash scripts/run_benchmark.sh --dry-run --datasets 100k --repetitions 1`
  passed without starting jobs.
- Dry-run output includes `analysis_1`, `analysis_2`, `analysis_3`, `hive`,
  `spark_sql`, `spark_core`, neutralized paths and `results/benchmark/`.
- No active job uses `coalesce(1)`, post-write `.show()`, `.take()` or
  `.collect()` previews.
- Active `ORDER BY` clauses are limited to the internal rankings required by
  Analysis 2 and Analysis 3.
- No Tez configuration was introduced.
- Analysis 3 exposes the required ten columns in Spark SQL, Spark Core and
  Hive.

## Official Benchmark Results

The final campaign artifacts are present under `results/benchmark/`:

- `benchmark_runs.csv`
- `benchmark_summary.csv`
- `benchmark_analysis_1.png`
- `benchmark_analysis_2.png`
- `benchmark_analysis_3.png`
- `benchmark_report.md`
- `session.log`
- `logs/`

CSV validation passed:

- Total runs: `189`
- Summary combinations: `63`
- Technologies: `hive`, `spark_sql`, `spark_core`
- Analyses: `analysis_1`, `analysis_2`, `analysis_3`
- Datasets: `100k`, `500k`, `1m`, `3m`, `7m`, `10m`, `14m`
- Repetitions per combination: `3`
- Failed runs: `0`
- `input_rows` and `input_bytes_hdfs`: populated
- `output_rows`: consistent across technologies for each analysis/dataset

## HDFS Output Equivalence Check

Existing official HDFS output was read for the `100k` dataset without
re-running jobs.

- Analysis 1: `1485` rows and `9` columns for each technology.
- Analysis 2: `847` rows and `7` columns for each technology.
- Analysis 3: `1485` rows and `10` columns for each technology.
- Hive and Spark SQL match exactly for all three analyses.
- Analysis 3 also matches exactly between Hive and Spark Core.

### Residual Rounding Note

For Analysis 1 and Analysis 2, Spark Core differs from Hive and Spark SQL in
`7` rows each only on the final displayed decimal digit. Example:
`-13.9062` versus `-13.9063`. This is caused by Python and SQL using different
tie-rounding conventions. Row counts, keys and underlying metrics remain
compatible. No analytical logic was changed during this final check.

## Documentation Check

- `README.md` explains technologies, setup, data preparation, HDFS upload,
  benchmark entrypoint, dry-run and result location.
- `README_BENCHMARK.md` explains the official campaign, Spark configuration,
  HDFS lifecycle, HiveServer2 lifecycle and output artifacts.
- `results/benchmark/benchmark_report.md` contains protocol, block order,
  HiveServer2 handling, Spark SQL configuration, summary results, failure
  section, Analysis 3 note, methodological note and AWS reuse note.
- No README requires `Secondo progetto.md`.

## Modified Files

- `.gitignore`
- `README.md`
- `README_BENCHMARK.md`
- `FINAL_REPOSITORY_CHECK.md`

The official benchmark result CSV files, charts and report are currently
untracked and should be added to the commit.

## Local Ignored Files

The following local runtime material exists on disk but is ignored and will
not enter the commit:

- `.venv/`
- `derby.log`
- `hadoop/hdfs/`
- `hadoop/logs/`
- `hive/metastore_db/`
- `results/tmp/`
- `results/output/`
- `results/benchmark/archive/`
- `results/benchmark/session.log`
- `results/benchmark/logs/`

Keeping execution logs local avoids pushing machine-specific runtime output.

## Remaining Problems

No blocking problem remains.

The only residual note is the final-digit Spark Core rounding difference for
seven `100k` rows in Analysis 1 and seven `100k` rows in Analysis 2.

## Commands

Dry-run:

```bash
bash scripts/run_benchmark.sh --dry-run
```

Official benchmark:

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

Recommended commit:

```bash
git add .gitignore README.md README_BENCHMARK.md FINAL_REPOSITORY_CHECK.md \
  results/benchmark/benchmark_runs.csv \
  results/benchmark/benchmark_summary.csv \
  results/benchmark/benchmark_analysis_1.png \
  results/benchmark/benchmark_analysis_2.png \
  results/benchmark/benchmark_analysis_3.png \
  results/benchmark/benchmark_report.md
git commit -m "Finalize benchmark results and repository checks"
```

Recommended push:

```bash
git push
```
