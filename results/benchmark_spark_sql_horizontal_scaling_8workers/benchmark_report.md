# Cluster EMR Repeated Benchmark Report

## Protocol

- Environment: `cluster_emr`.
- Metric: analytical job invocation plus distributed HDFS output write.
- Excluded from timer: cleanup, Hive table setup, memory/service checks, HDFS listing, row counting, previews, summaries and plots.
- Each technology-analysis-dataset combination has `3` runs: `run_type=repeated`, `run_index=1..3`.
- Output remains distributed. No presentation-only global final sort, `coalesce(1)`, timed preview action or single-file output was introduced.
- Spark cluster mode: `--master yarn --deploy-mode client`.
- Hive execution engine is forced to `mr`; EMR's default Tez engine is intentionally not used for the benchmark numbers.
- Hive reducer variants: `auto`.
- Hive auto reducer policy: `hive.exec.reducers.bytes.per.reducer=256000000`, `hive.exec.reducers.max=1009`; `mapreduce.job.reduces` is not pinned for variant `auto`.
- Hive pinned reducer variants set `mapreduce.job.reduces` explicitly; for example `r8` means `mapreduce.job.reduces=8`.
- Hive client: `beeline`.
- Campaign tag: `spark_sql_horizontal_scaling_8workers`.
- Dataset order: `14m`.
- Repetitions per combination: `3`.
- HDFS defaultFS: `hdfs://ip-172-31-82-2.ec2.internal:8020`.

## Block Order And Services

- Selected block order: `spark_sql/default`.
- HDFS and YARN remain active throughout the campaign.
- HiveServer2 is not started or stopped by this script; Beeline mode requires it to already be available.

## Spark Configuration

- `SPARK_DRIVER_MEMORY=5g`
- `SPARK_SQL_SHUFFLE_PARTITIONS=64`
- `SPARK_SUBMIT_EXTRA_CONF=<empty>`

## YARN Nodes Snapshot

Total Nodes:8<br>         Node-Id	     Node-State	Node-Http-Address	Number-of-Running-Containers<br>ip-172-31-92-83.ec2.internal:8041	        RUNNING	ip-172-31-92-83.ec2.internal:8042	                           0<br>ip-172-31-92-179.ec2.internal:8041	        RUNNING	ip-172-31-92-179.ec2.internal:8042	                           0<br>ip-172-31-91-0.ec2.internal:8041	        RUNNING	ip-172-31-91-0.ec2.internal:8042	                           0<br>ip-172-31-90-194.ec2.internal:8041	        RUNNING	ip-172-31-90-194.ec2.internal:8042	                           0<br>ip-172-31-90-29.ec2.internal:8041	        RUNNING	ip-172-31-90-29.ec2.internal:8042	                           0<br>ip-172-31-90-46.ec2.internal:8041	        RUNNING	ip-172-31-90-46.ec2.internal:8042	                           0<br>ip-172-31-92-113.ec2.internal:8041	        RUNNING	ip-172-31-92-113.ec2.internal:8042	                           0<br>ip-172-31-95-202.ec2.internal:8041	        RUNNING	ip-172-31-95-202.ec2.internal:8042	                           0

## Results

| technology | variant | analysis | dataset_label | input_rows | input_bytes_hdfs | successful_runs | failed_runs | mean_seconds | median_seconds | stddev_seconds | min_seconds | max_seconds | best_run_seconds | output_rows | output_part_files_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| spark_sql | default | analysis_2 | 14m | 14158162 | 2102362680 | 3 | 0 | 39.3588 | 35.0049 | 9.0455 | 33.3137 | 49.7579 | 33.3137 | 11902 | 3,4 |
| spark_sql | default | analysis_3 | 14m | 14158162 | 2102362680 | 3 | 0 | 32.1696 | 32.0948 | 0.7374 | 31.4725 | 32.9415 | 31.4725 | 1738 | 1 |

## Failures

No failed runs were recorded.

## Methodological Note

Local and cluster topologies are intentionally different. The comparison is valid as a context comparison because the scripts, analyses, dataset semantics, distributed-output policy and timer boundaries are kept aligned.
