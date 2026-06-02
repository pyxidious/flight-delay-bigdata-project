import argparse

from pyspark.sql import SparkSession
from common_schema import get_flights_schema


def parse_args():
    parser = argparse.ArgumentParser(
        description="Spark SQL Analysis 3: airline performance ranking by origin airport."
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

    spark = (
        SparkSession.builder
        .appName("SparkSQLAnalysis3AirlineAirportRanking")
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
        WITH airline_airport_stats AS (
            SELECT
                origin,
                airline,
                COUNT(*) AS total_flights,
                AVG(dep_delay) AS avg_dep_delay,
                AVG(CASE WHEN is_completed_flight = 1 THEN arr_delay END) AS avg_arr_delay,
                SUM(cancelled) AS cancelled_flights,
                ROUND(SUM(cancelled) / COUNT(*), 6) AS cancellation_rate
            FROM flights
            GROUP BY origin, airline
        ),
        airport_stats AS (
            SELECT
                origin,
                AVG(dep_delay) AS airport_avg_dep_delay
            FROM flights
            GROUP BY origin
        ),
        compared AS (
            SELECT
                airline_stats.origin,
                airline_stats.airline,
                airline_stats.total_flights,
                airline_stats.avg_dep_delay,
                airline_stats.avg_arr_delay,
                airline_stats.cancelled_flights,
                airline_stats.cancellation_rate,
                airport_stats.airport_avg_dep_delay,
                ROUND(
                    airline_stats.avg_dep_delay - airport_stats.airport_avg_dep_delay,
                    4
                ) AS dep_delay_diff_from_airport
            FROM airline_airport_stats airline_stats
            INNER JOIN airport_stats
                ON airline_stats.origin = airport_stats.origin
        )
        SELECT
            origin,
            airline,
            total_flights,
            ROUND(avg_dep_delay, 4) AS avg_dep_delay,
            ROUND(avg_arr_delay, 4) AS avg_arr_delay,
            cancelled_flights,
            cancellation_rate,
            ROUND(airport_avg_dep_delay, 4) AS airport_avg_dep_delay,
            dep_delay_diff_from_airport,
            ROW_NUMBER() OVER (
                PARTITION BY origin
                ORDER BY avg_dep_delay ASC, airline ASC
            ) AS airport_rank_by_avg_dep_delay
        FROM compared
        """
    )

    (
        result
        .write
        .mode("overwrite")
        .option("header", "true")
        .csv(args.output)
    )

    print("Spark SQL Analysis 3 completed.")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")

    spark.stop()


if __name__ == "__main__":
    main()
