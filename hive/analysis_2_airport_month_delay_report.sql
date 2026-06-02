SET mapreduce.map.memory.mb=6144;
SET mapreduce.reduce.memory.mb=6144;
SET mapreduce.map.java.opts=-Xmx4915m;
SET mapreduce.reduce.java.opts=-Xmx4915m;
SET hive.mapred.local.mem=6144;
SET hive.auto.convert.join=false;
SET hive.exec.parallel=false;

WITH caused AS (
    SELECT
        origin,
        CAST(month AS INT) AS month,
        dep_delay_band,
        CAST(dep_delay AS DOUBLE) AS dep_delay,
        CAST(arr_delay AS DOUBLE) AS arr_delay,
        CAST(is_completed_flight AS INT) AS is_completed_flight,
        CASE
            WHEN CAST(cancelled AS INT) = 1 THEN CONCAT('Cancellation_', cancellation_code)
            WHEN main_delay_cause != 'NoDelayCause' THEN CONCAT('Delay_', main_delay_cause)
            ELSE 'NoCauseAvailable'
        END AS event_cause
    FROM flights_hive
    WHERE origin != 'origin'
      AND month != 'month'
      AND dep_delay_band != 'dep_delay_band'
      AND dep_delay_band IN ('low', 'medium', 'high')
),
cause_metrics AS (
    SELECT
        origin,
        month,
        dep_delay_band,
        event_cause,
        COUNT(*) AS cause_flight_count,
        SUM(dep_delay) AS dep_delay_sum,
        COUNT(dep_delay) AS dep_delay_count,
        SUM(CASE WHEN is_completed_flight = 1 THEN arr_delay ELSE NULL END) AS arr_delay_sum,
        COUNT(CASE WHEN is_completed_flight = 1 THEN arr_delay ELSE NULL END) AS arr_delay_count
    FROM caused
    GROUP BY origin, month, dep_delay_band, event_cause
),
ranked AS (
    SELECT
        origin,
        month,
        dep_delay_band,
        event_cause,
        cause_flight_count,
        SUM(cause_flight_count) OVER (
            PARTITION BY origin, month, dep_delay_band
        ) AS flight_count,
        SUM(dep_delay_sum) OVER (
            PARTITION BY origin, month, dep_delay_band
        ) AS dep_delay_sum,
        SUM(dep_delay_count) OVER (
            PARTITION BY origin, month, dep_delay_band
        ) AS dep_delay_count,
        SUM(arr_delay_sum) OVER (
            PARTITION BY origin, month, dep_delay_band
        ) AS arr_delay_sum,
        SUM(arr_delay_count) OVER (
            PARTITION BY origin, month, dep_delay_band
        ) AS arr_delay_count,
        ROW_NUMBER() OVER (
            PARTITION BY origin, month, dep_delay_band
            ORDER BY
                CASE
                    WHEN event_cause IS NOT NULL
                     AND event_cause != 'NoCauseAvailable'
                    THEN 0
                    ELSE 1
                END,
                cause_flight_count DESC,
                event_cause ASC
        ) AS cause_rank
    FROM cause_metrics
),
collapsed AS (
    SELECT
        origin,
        month,
        dep_delay_band,
        MAX(flight_count) AS flight_count,
        ROUND(MAX(dep_delay_sum) / MAX(dep_delay_count), 4) AS avg_dep_delay,
        ROUND(MAX(arr_delay_sum) / MAX(arr_delay_count), 4) AS avg_arr_delay,
        CASE
            WHEN MAX(
                CASE
                    WHEN event_cause IS NOT NULL
                     AND event_cause != 'NoCauseAvailable'
                    THEN 1
                    ELSE 0
                END
            ) = 0
            THEN 'NoCauseAvailable'
            ELSE CONCAT_WS(
                '; ',
                SORT_ARRAY(
                    COLLECT_LIST(
                        CASE
                            WHEN event_cause IS NOT NULL
                             AND event_cause != 'NoCauseAvailable'
                             AND cause_rank <= 3
                            THEN CONCAT(
                                CAST(cause_rank AS STRING),
                                ':',
                                event_cause,
                                '=',
                                CAST(cause_flight_count AS STRING)
                            )
                            ELSE NULL
                        END
                    )
                )
            )
        END AS top_3_causes
    FROM ranked
    GROUP BY origin, month, dep_delay_band
)
INSERT OVERWRITE DIRECTORY '${hiveconf:output_dir}'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT
    origin,
    month,
    dep_delay_band,
    flight_count,
    avg_dep_delay,
    avg_arr_delay,
    top_3_causes
FROM collapsed;
