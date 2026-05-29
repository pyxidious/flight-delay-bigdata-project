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
FROM flights_clean_hive
WHERE airline != 'airline'
  AND origin != 'origin'
  AND month != 'month'
GROUP BY airline, origin
ORDER BY airline, origin;