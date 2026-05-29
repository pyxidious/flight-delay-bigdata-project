DROP TABLE IF EXISTS flights_clean_hive;

CREATE EXTERNAL TABLE flights_clean_hive (
    year STRING,
    month STRING,
    day_of_month STRING,
    day_of_week STRING,
    fl_date STRING,
    airline STRING,
    origin STRING,
    origin_city_name STRING,
    origin_state_nm STRING,
    dest STRING,
    dest_city_name STRING,
    dest_state_nm STRING,
    route STRING,
    dep_delay STRING,
    arr_delay STRING,
    dep_delay_band STRING,
    cancelled STRING,
    cancellation_code STRING,
    diverted STRING,
    is_completed_flight STRING,
    carrier_delay STRING,
    weather_delay STRING,
    nas_delay STRING,
    security_delay STRING,
    late_aircraft_delay STRING,
    main_delay_cause STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar" = "\"",
    "escapeChar" = "\\"
)
STORED AS TEXTFILE
LOCATION '${hiveconf:input_dir}'
TBLPROPERTIES ("skip.header.line.count"="1");

WITH base AS (
    SELECT *
    FROM flights_clean_hive
    WHERE dep_delay_band IN ('low', 'medium', 'high')
),
caused AS (
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
    FROM base
),
metrics AS (
    SELECT
        origin,
        month,
        dep_delay_band,
        COUNT(*) AS flight_count,
        ROUND(AVG(dep_delay), 4) AS avg_dep_delay,
        ROUND(AVG(CASE WHEN is_completed_flight = 1 THEN arr_delay ELSE NULL END), 4) AS avg_arr_delay
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
INSERT OVERWRITE DIRECTORY '${hiveconf:output_dir}'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
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
ORDER BY metrics.origin, metrics.month, metrics.dep_delay_band;