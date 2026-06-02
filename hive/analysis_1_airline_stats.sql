INSERT OVERWRITE DIRECTORY '${hiveconf:output_dir}'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT
    airline,
    origin,
    COUNT(*) AS total_flights,
    MIN(
        CASE
            WHEN CAST(is_completed_flight AS INT) = 1
             AND arr_delay IS NOT NULL
             AND arr_delay != ''
            THEN CAST(arr_delay AS DOUBLE)
            ELSE NULL
        END
    ) AS min_arr_delay,
    MAX(
        CASE
            WHEN CAST(is_completed_flight AS INT) = 1
             AND arr_delay IS NOT NULL
             AND arr_delay != ''
            THEN CAST(arr_delay AS DOUBLE)
            ELSE NULL
        END
    ) AS max_arr_delay,
    ROUND(
        AVG(
            CASE
                WHEN CAST(is_completed_flight AS INT) = 1
                 AND arr_delay IS NOT NULL
                 AND arr_delay != ''
                THEN CAST(arr_delay AS DOUBLE)
                ELSE NULL
            END
        ),
        4
    ) AS avg_arr_delay,
    SUM(CAST(cancelled AS INT)) AS cancelled_flights,
    ROUND(SUM(CAST(cancelled AS INT)) / COUNT(*), 6) AS cancellation_rate,
    CONCAT_WS(',', SORT_ARRAY(COLLECT_SET(CAST(CAST(month AS INT) AS STRING)))) AS active_months
FROM flights_hive
WHERE airline != 'airline'
  AND origin != 'origin'
  AND month != 'month'
GROUP BY airline, origin;
