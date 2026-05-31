# Benchmark Summary

## Scope

The benchmark compares the execution time of the two implemented analyses across three technologies:

- Spark SQL
- Spark Core
- Hive

The benchmark includes both natural samples of increasing size and controlled replicated datasets.

## Dataset sizes

| Dataset label | Description |
|---|---|
| 100k | First 100,000 rows of the cleaned dataset |
| 500k | First 500,000 rows of the cleaned dataset |
| 1m | First 1,000,000 rows of the cleaned dataset |
| 3m | First 3,000,000 rows of the cleaned dataset |
| 7m | Full cleaned dataset |
| 10m | Full cleaned dataset plus partial controlled replication up to 10,000,000 rows |
| 14m | Full cleaned dataset replicated 2 times |

## Methodological notes

- Benchmarks were executed on a local machine.
- Absolute execution times depend on the available hardware.
- The main focus is the relative scaling trend across technologies.
- Hive uses HiveServer2 and local Hadoop/MapReduce execution.
- The 10m and 14m datasets are generated with controlled replication.

## Analysis 1 results

| dataset_label   |   spark_sql |   spark_core |    hive |
|:----------------|------------:|-------------:|--------:|
| 100k            |      9.7335 |       7.8313 |  6.4358 |
| 500k            |     17.7531 |       9.0133 |  6.0095 |
| 1m              |     14.2316 |      10.0475 |  9.077  |
| 3m              |     21.287  |      14.7508 | 18.1905 |
| 7m              |     23.7462 |      24.1499 | 38.7453 |
| 10m             |     90.3074 |      30.233  | 56.0079 |
| 14m             |     36.3494 |      39.9491 | 95.7998 |

## Analysis 2 results

| dataset_label   |   spark_sql |   spark_core |     hive |
|:----------------|------------:|-------------:|---------:|
| 100k            |     11.246  |       7.7389 |  11.176  |
| 500k            |     12.8103 |       9.082  |  16.9733 |
| 1m              |     13.3523 |      10.4034 |  20.9947 |
| 3m              |     15.2111 |      15.3543 |  41.0753 |
| 7m              |     20.2318 |      25.8971 |  88.7832 |
| 10m             |     25.7358 |      33.4658 | 132.081  |
| 14m             |     25.8074 |      43.6489 | 168.883  |

## Fastest technology by analysis and dataset

| analysis   | dataset_label   | fastest_technology   |   fastest_seconds | slowest_technology   |   slowest_seconds |   speedup_vs_slowest |
|:-----------|:----------------|:---------------------|------------------:|:---------------------|------------------:|---------------------:|
| analysis_1 | 100k            | hive                 |            6.4358 | spark_sql            |            9.7335 |               1.5124 |
| analysis_1 | 500k            | hive                 |            6.0095 | spark_sql            |           17.7531 |               2.9542 |
| analysis_1 | 1m              | hive                 |            9.077  | spark_sql            |           14.2316 |               1.5679 |
| analysis_1 | 3m              | spark_core           |           14.7508 | spark_sql            |           21.287  |               1.4431 |
| analysis_1 | 7m              | spark_sql            |           23.7462 | hive                 |           38.7453 |               1.6316 |
| analysis_1 | 10m             | spark_core           |           30.233  | spark_sql            |           90.3074 |               2.987  |
| analysis_1 | 14m             | spark_sql            |           36.3494 | hive                 |           95.7998 |               2.6355 |
| analysis_2 | 100k            | spark_core           |            7.7389 | spark_sql            |           11.246  |               1.4532 |
| analysis_2 | 500k            | spark_core           |            9.082  | hive                 |           16.9733 |               1.8689 |
| analysis_2 | 1m              | spark_core           |           10.4034 | hive                 |           20.9947 |               2.0181 |
| analysis_2 | 3m              | spark_sql            |           15.2111 | hive                 |           41.0753 |               2.7004 |
| analysis_2 | 7m              | spark_sql            |           20.2318 | hive                 |           88.7832 |               4.3883 |
| analysis_2 | 10m             | spark_sql            |           25.7358 | hive                 |          132.081  |               5.1322 |
| analysis_2 | 14m             | spark_sql            |           25.8074 | hive                 |          168.883  |               6.544  |

## Main observations

- Spark Core is consistently competitive, especially on the larger datasets.
- Spark SQL scales well and performs particularly well on the second analysis for large inputs.
- Hive is competitive on small inputs but becomes slower on larger datasets, especially for the second analysis.
- The replicated 14M-row dataset confirms the scalability trend beyond the original full dataset size.

## Generated files

- `results/benchmarks/benchmark_analysis_1_pivot.csv`
- `results/benchmarks/benchmark_analysis_2_pivot.csv`
- `results/benchmarks/benchmark_fastest_by_dataset.csv`
- `results/benchmarks/benchmark_analysis_1.png`
- `results/benchmarks/benchmark_analysis_2.png`
