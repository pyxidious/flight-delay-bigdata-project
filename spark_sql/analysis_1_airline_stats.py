from pathlib import Path
import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    min as spark_min,
    max as spark_max,
    avg,
    sum as spark_sum,
    collect_set,
    sort_array,
    round as spark_round,
    concat_ws,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Spark SQL Analysis 1: airline statistics by origin airport."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input cleaned CSV path.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output directory path.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    output_path = Path(args.output)

    spark = (
        SparkSession.builder
        .appName("SparkSQLAnalysis1AirlineStats")
        .getOrCreate()
    )

    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(args.input)
    )

    completed = df.filter(col("is_completed_flight") == 1)

    delay_stats = (
        completed
        .groupBy("airline", "origin")
        .agg(
            spark_min("arr_delay").alias("min_arr_delay"),
            spark_max("arr_delay").alias("max_arr_delay"),
            avg("arr_delay").alias("avg_arr_delay"),
        )
    )

    total_stats = (
        df
        .groupBy("airline", "origin")
        .agg(
            count("*").alias("total_flights"),
            spark_sum("cancelled").alias("cancelled_flights"),
            sort_array(collect_set("month")).alias("active_months"),
        )
    )

    result = (
        total_stats
        .join(delay_stats, on=["airline", "origin"], how="left")
        .withColumn(
            "cancellation_rate",
            spark_round(col("cancelled_flights") / col("total_flights"), 6),
        )
        .withColumn("avg_arr_delay", spark_round(col("avg_arr_delay"), 4))
        .withColumn("active_months", concat_ws(",", col("active_months")))
        .select(
            "airline",
            "origin",
            "total_flights",
            "min_arr_delay",
            "max_arr_delay",
            "avg_arr_delay",
            "cancelled_flights",
            "cancellation_rate",
            "active_months",
        )
        .orderBy("airline", "origin")
    )

    (
        result
        .coalesce(1)
        .write
        .mode("overwrite")
        .option("header", "true")
        .csv(str(output_path))
    )

    print("Spark SQL Analysis 1 completed.")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")

    print("First 10 rows:")
    result.show(10, truncate=False)

    spark.stop()


if __name__ == "__main__":
    main()
