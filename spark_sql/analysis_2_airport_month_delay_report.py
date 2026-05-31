import argparse

from pyspark.sql import SparkSession
from common_schema import get_flights_schema


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

    output_path = args.output

    spark = (
        SparkSession.builder
        .appName("SparkSQLAnalysis2AirportMonthDelayReport")
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
        WITH base AS (
            SELECT *
            FROM flights
            WHERE dep_delay_band IN ('low', 'medium', 'high')
        ),
        caused AS (
            SELECT
                origin,
                month,
                dep_delay_band,
                dep_delay,
                arr_delay,
                is_completed_flight,
                CASE
                    WHEN cancelled = 1 THEN CONCAT('Cancellation_', cancellation_code)
                    WHEN main_delay_cause != 'NoDelayCause' THEN CONCAT('Delay_', main_delay_cause)
                    ELSE 'NoCauseAvailable'
                END AS event_cause
            FROM base
        ),
        metrics AS (
            SELECT
                origin,
                month,
                dep_delay_band,
                COUNT(*) AS flight_count,
                ROUND(AVG(dep_delay), 4) AS avg_dep_delay,
                ROUND(AVG(CASE WHEN is_completed_flight = 1 THEN arr_delay END), 4) AS avg_arr_delay
            FROM caused
            GROUP BY origin, month, dep_delay_band
        ),
        cause_counts AS (
            SELECT
                origin,
                month,
                dep_delay_band,
                event_cause,
                COUNT(*) AS cause_count
            FROM caused
            WHERE event_cause != 'NoCauseAvailable'
            GROUP BY origin, month, dep_delay_band, event_cause
        ),
        ranked_causes AS (
            SELECT
                origin,
                month,
                dep_delay_band,
                event_cause,
                cause_count,
                ROW_NUMBER() OVER (
                    PARTITION BY origin, month, dep_delay_band
                    ORDER BY cause_count DESC, event_cause ASC
                ) AS cause_rank
            FROM cause_counts
        ),
        top_causes AS (
            SELECT
                origin,
                month,
                dep_delay_band,
                CONCAT_WS(
                    '; ',
                    COLLECT_LIST(
                        CONCAT(
                            CAST(cause_rank AS STRING),
                            ':',
                            event_cause,
                            '=',
                            CAST(cause_count AS STRING)
                        )
                    )
                ) AS top_3_causes
            FROM ranked_causes
            WHERE cause_rank <= 3
            GROUP BY origin, month, dep_delay_band
        )
        SELECT
            metrics.origin,
            metrics.month,
            metrics.dep_delay_band,
            metrics.flight_count,
            metrics.avg_dep_delay,
            metrics.avg_arr_delay,
            COALESCE(top_causes.top_3_causes, 'NoCauseAvailable') AS top_3_causes
        FROM metrics
        LEFT JOIN top_causes
            ON metrics.origin = top_causes.origin
           AND metrics.month = top_causes.month
           AND metrics.dep_delay_band = top_causes.dep_delay_band
        ORDER BY metrics.origin, metrics.month, metrics.dep_delay_band
        """
    )

    (
        result
        .coalesce(1)
        .write
        .mode("overwrite")
        .option("header", "true")
        .csv(output_path)
    )

    print("Spark SQL Analysis 2 completed.")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")

    print("First 10 rows:")
    result.show(10, truncate=False)

    spark.stop()


if __name__ == "__main__":
    main()
