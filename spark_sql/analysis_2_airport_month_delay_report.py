from pathlib import Path
import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    avg,
    round as spark_round,
    when,
    concat,
    concat_ws,
    lit,
    collect_list,
    struct,
    sort_array,
)
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number


def parse_args():
    parser = argparse.ArgumentParser(
        description="Spark SQL Analysis 2: delay report by origin airport, month and departure delay band."
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
        .appName("SparkSQLAnalysis2AirportMonthDelayReport")
        .getOrCreate()
    )

    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(args.input)
    )

    # We keep the "unknown" delay band out of this report because the assignment
    # defines three explicit departure delay bands: low, medium and high.
    base_df = df.filter(col("dep_delay_band").isin("low", "medium", "high"))

    # Cause used for the top-3 report:
    # - cancelled flights use cancellation_code;
    # - delayed non-cancelled flights use main_delay_cause;
    # - rows without available cause are marked explicitly.
    caused_df = base_df.withColumn(
        "event_cause",
        when(
            col("cancelled") == 1,
            concat(lit("Cancellation_"), col("cancellation_code")),
        ).when(
            col("main_delay_cause") != "NoDelayCause",
            concat(lit("Delay_"), col("main_delay_cause")),
        ).otherwise(lit("NoCauseAvailable")),
    )

    metrics = (
        caused_df
        .groupBy("origin", "month", "dep_delay_band")
        .agg(
            count("*").alias("flight_count"),
            spark_round(avg("dep_delay"), 4).alias("avg_dep_delay"),
            spark_round(
                avg(
                    when(
                        col("is_completed_flight") == 1,
                        col("arr_delay"),
                    )
                ),
                4,
            ).alias("avg_arr_delay"),
        )
    )

    cause_counts = (
        caused_df
        .filter(col("event_cause") != "NoCauseAvailable")
        .groupBy("origin", "month", "dep_delay_band", "event_cause")
        .agg(count("*").alias("cause_count"))
    )

    window_spec = (
        Window
        .partitionBy("origin", "month", "dep_delay_band")
        .orderBy(col("cause_count").desc(), col("event_cause").asc())
    )

    top_causes_ranked = (
        cause_counts
        .withColumn("cause_rank", row_number().over(window_spec))
        .filter(col("cause_rank") <= 3)
        .withColumn(
            "cause_entry",
            concat(
                col("cause_rank").cast("string"),
                lit(":"),
                col("event_cause"),
                lit("="),
                col("cause_count").cast("string"),
            ),
        )
    )

    top_causes = (
        top_causes_ranked
        .groupBy("origin", "month", "dep_delay_band")
        .agg(
            concat_ws(
                "; ",
                collect_list("cause_entry"),
            ).alias("top_3_causes")
        )
    )

    result = (
        metrics
        .join(top_causes, on=["origin", "month", "dep_delay_band"], how="left")
        .fillna({"top_3_causes": "NoCauseAvailable"})
        .select(
            "origin",
            "month",
            "dep_delay_band",
            "flight_count",
            "avg_dep_delay",
            "avg_arr_delay",
            "top_3_causes",
        )
        .orderBy("origin", "month", "dep_delay_band")
    )

    (
        result
        .coalesce(1)
        .write
        .mode("overwrite")
        .option("header", "true")
        .csv(str(output_path))
    )

    print("Spark SQL Analysis 2 completed.")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print("First 10 rows:")
    result.show(10, truncate=False)

    spark.stop()


if __name__ == "__main__":
    main()
