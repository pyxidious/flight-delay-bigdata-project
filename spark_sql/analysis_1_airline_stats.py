import argparse

from pyspark.sql import SparkSession
from common_schema import get_flights_schema

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

    output_path = args.output

    spark = (
        SparkSession.builder
        .appName("SparkSQLAnalysis1AirlineStats")
        .getOrCreate()
    )

    flights_df = (
        spark.read
        .option("header", "true")
        .schema(get_flights_schema())
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
        """
    )

    (
        result
        .write
        .mode("overwrite")
        .option("header", "true")
        .csv(output_path)
    )

    print("Spark SQL Analysis 1 completed.")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")

    spark.stop()


if __name__ == "__main__":
    main()
