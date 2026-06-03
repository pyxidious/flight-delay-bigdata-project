# Cluster EMR Repeated Benchmark Report

## Protocol

- Environment: `cluster_emr`.
- Metric: analytical job invocation plus distributed HDFS output write.
- Excluded from timer: cleanup, Hive table setup, memory/service checks, HDFS listing, row counting, previews, summaries and plots.
- Each technology-analysis-dataset combination has `3` runs: `run_type=repeated`, `run_index=1..3`.
- Output remains distributed. No presentation-only global final sort, `coalesce(1)`, timed preview action or single-file output was introduced.
- Spark cluster mode: `--master yarn --deploy-mode client`.
- Hive execution engine is forced to `mr`; EMR's default Tez engine is intentionally not used for the benchmark numbers.
- Hive reducer variants: `auto, r8, r16`.
- Hive auto reducer policy: `hive.exec.reducers.bytes.per.reducer=256000000`, `hive.exec.reducers.max=1009`; `mapreduce.job.reduces` is not pinned for variant `auto`.
- Hive pinned reducer variants set `mapreduce.job.reduces` explicitly; for example `r8` means `mapreduce.job.reduces=8`.
- Hive client: `beeline`.
- Campaign tag: `hive_mr_reducer_tuning_4workers_fixed`.
- Dataset order: `14m`.
- Repetitions per combination: `3`.
- HDFS defaultFS: `hdfs://ip-172-31-89-222.ec2.internal:8020`.

## Block Order And Services

- Selected block order: `hive/auto, hive/r8, hive/r16`.
- HDFS and YARN remain active throughout the campaign.
- HiveServer2 is not started or stopped by this script; Beeline mode requires it to already be available.

## Spark Configuration

- `SPARK_DRIVER_MEMORY=5g`
- `SPARK_SQL_SHUFFLE_PARTITIONS=64`
- `SPARK_SUBMIT_EXTRA_CONF=<empty>`

## YARN Nodes Snapshot

Total Nodes:4<br>         Node-Id	     Node-State	Node-Http-Address	Number-of-Running-Containers<br>ip-172-31-89-119.ec2.internal:8041	        RUNNING	ip-172-31-89-119.ec2.internal:8042	                           0<br>ip-172-31-86-49.ec2.internal:8041	        RUNNING	ip-172-31-86-49.ec2.internal:8042	                           0<br>ip-172-31-89-52.ec2.internal:8041	        RUNNING	ip-172-31-89-52.ec2.internal:8042	                           0<br>ip-172-31-95-3.ec2.internal:8041	        RUNNING	ip-172-31-95-3.ec2.internal:8042	                           0

## Results

| technology | variant | analysis | dataset_label | input_rows | input_bytes_hdfs | successful_runs | failed_runs | mean_seconds | median_seconds | stddev_seconds | min_seconds | max_seconds | best_run_seconds | output_rows | output_part_files_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hive | auto | analysis_2 | 14m | 14158162 | 2102362680 | 3 | 0 | 112.7073 | 114.0933 | 4.2348 | 107.9532 | 116.0755 | 107.9532 | 11902 | 1 |
| hive | auto | analysis_3 | 14m | 14158162 | 2102362680 | 3 | 0 | 156.1442 | 156.8166 | 2.7214 | 153.1496 | 158.4663 | 153.1496 | 1738 | 1 |
| hive | r8 | analysis_2 | 14m | 14158162 | 2102362680 | 3 | 0 | 114.3405 | 113.8338 | 2.6786 | 111.9514 | 117.2362 | 111.9514 | 11902 | 8 |
| hive | r8 | analysis_3 | 14m | 14158162 | 2102362680 | 3 | 0 | 165.8319 | 166.7363 | 2.5643 | 162.9379 | 167.8215 | 162.9379 | 1738 | 8 |
| hive | r16 | analysis_2 | 14m | 14158162 | 2102362680 | 3 | 0 | 142.5708 | 142.6153 | 0.1643 | 142.3888 | 142.7083 | 142.3888 | 11902 | 16 |
| hive | r16 | analysis_3 | 14m | 14158162 | 2102362680 | 3 | 0 | 195.6046 | 195.1576 | 2.3342 | 193.5262 | 198.1300 | 193.5262 | 1738 | 16 |

## Failures

No failed runs were recorded.

## Methodological Note

Local and cluster topologies are intentionally different. The comparison is valid as a context comparison because the scripts, analyses, dataset semantics, distributed-output policy and timer boundaries are kept aligned.
