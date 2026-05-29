from pathlib import Path
import argparse

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    DoubleType,
    StringType,
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


def get_schema() -> StructType:
    return StructType(
        [
            StructField("year", IntegerType(), True),
            StructField("month", IntegerType(), True),
            StructField("day_of_month", IntegerType(), True),
            StructField("day_of_week", IntegerType(), True),
            StructField("fl_date", StringType(), True),
            StructField("airline", StringType(), True),
            StructField("origin", StringType(), True),
            StructField("origin_city_name", StringType(), True),
            StructField("origin_state_nm", StringType(), True),
            StructField("dest", StringType(), True),
            StructField("dest_city_name", StringType(), True),
            StructField("dest_state_nm", StringType(), True),
            StructField("route", StringType(), True),
            StructField("dep_delay", DoubleType(), True),
            StructField("arr_delay", DoubleType(), True),
            StructField("dep_delay_band", StringType(), True),
            StructField("cancelled", IntegerType(), True),
            StructField("cancellation_code", StringType(), True),
            StructField("diverted", IntegerType(), True),
            StructField("is_completed_flight", IntegerType(), True),
            StructField("carrier_delay", DoubleType(), True),
            StructField("weather_delay", DoubleType(), True),
            StructField("nas_delay", DoubleType(), True),
            StructField("security_delay", DoubleType(), True),
            StructField("late_aircraft_delay", DoubleType(), True),
            StructField("main_delay_cause", StringType(), True),
        ]
    )


def main():
    args = parse_args()

    output_path = Path(args.output)

    spark = (
        SparkSession.builder
        .appName("SparkSQLAnalysis1AirlineStats")
        .getOrCreate()
    )

    flights_df = (
        spark.read
        .option("header", "true")
        .schema(get_schema())
        .csv(args.input)
    )

    flights_df.createOrReplaceTempView("flights")

    result = spark.sql(
        """
        WITH total_stats AS (
            SELECT
                airline,
                origin,
                COUNT(*) AS total_flights,
                SUM(cancelled) AS cancelled_flights,
                CONCAT_WS(',', SORT_ARRAY(COLLECT_SET(CAST(month AS STRING)))) AS active_months
            FROM flights
            GROUP BY airline, origin
        ),
        delay_stats AS (
            SELECT
                airline,
                origin,
                MIN(arr_delay) AS min_arr_delay,
                MAX(arr_delay) AS max_arr_delay,
                AVG(arr_delay) AS avg_arr_delay
            FROM flights
            WHERE is_completed_flight = 1
            GROUP BY airline, origin
        )
        SELECT
            total_stats.airline,
            total_stats.origin,
            total_stats.total_flights,
            delay_stats.min_arr_delay,
            delay_stats.max_arr_delay,
            ROUND(delay_stats.avg_arr_delay, 4) AS avg_arr_delay,
            total_stats.cancelled_flights,
            ROUND(total_stats.cancelled_flights / total_stats.total_flights, 6) AS cancellation_rate,
            total_stats.active_months
        FROM total_stats
        LEFT JOIN delay_stats
            ON total_stats.airline = delay_stats.airline
           AND total_stats.origin = delay_stats.origin
        ORDER BY total_stats.airline, total_stats.origin
        """
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