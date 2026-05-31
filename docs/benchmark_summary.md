# Benchmark Summary

## Scope

The benchmark compares the execution time of the two implemented analyses across three technologies:

- Spark SQL
- Spark Core
- Hive

The benchmark includes both natural samples of increasing size and a replicated dataset.

## Dataset sizes

| Dataset label | Description |
|---|---|
| 100k | First 100,000 rows of the cleaned dataset |
| 500k | First 500,000 rows of the cleaned dataset |
| 1m | First 1,000,000 rows of the cleaned dataset |
| 3m | First 3,000,000 rows of the cleaned dataset |
| 7m | Full cleaned dataset |
| 14m | Full cleaned dataset replicated 2 times |

## Analysis 1 results

| dataset_label   |   spark_sql |   spark_core |     hive |
|:----------------|------------:|-------------:|---------:|
| 100k            |     10.3009 |       7.912  |   6.2415 |
| 500k            |     12.7241 |       9.0201 |   6.0467 |
| 1m              |     14.6874 |      10.0794 |   8.0841 |
| 3m              |     23.7142 |      14.9266 |  18.1449 |
| 7m              |     27.2627 |      24.1425 |  40.242  |
| 14m             |     93.806  |      48.0775 | 114.8    |

## Analysis 2 results

| dataset_label   |   spark_sql |   spark_core |     hive |
|:----------------|------------:|-------------:|---------:|
| 100k            |     11.2097 |       7.7875 |  11.087  |
| 500k            |     13.2064 |       9.2573 |  16.879  |
| 1m              |     13.243  |      10.4261 |  20.8591 |
| 3m              |     15.7831 |      15.6262 |  41.0528 |
| 7m              |     19.8396 |      26.076  |  90.2658 |
| 14m             |     38.3424 |      52.0413 | 276.202  |

## Fastest technology by analysis and dataset

| analysis   | dataset_label   | fastest_technology   |   fastest_seconds | slowest_technology   |   slowest_seconds |   speedup_vs_slowest |
|:-----------|:----------------|:---------------------|------------------:|:---------------------|------------------:|---------------------:|
| analysis_1 | 100k            | hive                 |            6.2415 | spark_sql            |           10.3009 |               1.6504 |
| analysis_1 | 500k            | hive                 |            6.0467 | spark_sql            |           12.7241 |               2.1043 |
| analysis_1 | 1m              | hive                 |            8.0841 | spark_sql            |           14.6874 |               1.8168 |
| analysis_1 | 3m              | spark_core           |           14.9266 | spark_sql            |           23.7142 |               1.5887 |
| analysis_1 | 7m              | spark_core           |           24.1425 | hive                 |           40.242  |               1.6669 |
| analysis_1 | 14m             | spark_core           |           48.0775 | hive                 |          114.8    |               2.3878 |
| analysis_2 | 100k            | spark_core           |            7.7875 | spark_sql            |           11.2097 |               1.4394 |
| analysis_2 | 500k            | spark_core           |            9.2573 | hive                 |           16.879  |               1.8233 |
| analysis_2 | 1m              | spark_core           |           10.4261 | hive                 |           20.8591 |               2.0007 |
| analysis_2 | 3m              | spark_core           |           15.6262 | hive                 |           41.0528 |               2.6272 |
| analysis_2 | 7m              | spark_sql            |           19.8396 | hive                 |           90.2658 |               4.5498 |
| analysis_2 | 14m             | spark_sql            |           38.3424 | hive                 |          276.202  |               7.2036 |

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
