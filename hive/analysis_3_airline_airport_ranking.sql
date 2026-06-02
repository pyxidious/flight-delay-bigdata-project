SET mapreduce.map.memory.mb=6144;
SET mapreduce.reduce.memory.mb=6144;
SET mapreduce.map.java.opts=-Xmx4915m;
SET mapreduce.reduce.java.opts=-Xmx4915m;
SET hive.mapred.local.mem=6144;
SET hive.auto.convert.join=false;
SET hive.exec.parallel=false;

WITH base AS (
    SELECT
        origin,
        airline,
        CAST(dep_delay AS DOUBLE) AS dep_delay,
        CAST(arr_delay AS DOUBLE) AS arr_delay,
        CAST(cancelled AS INT) AS cancelled,
        CAST(is_completed_flight AS INT) AS is_completed_flight
    FROM flights_hive
    WHERE origin != 'origin'
      AND airline != 'airline'
),
airline_airport_stats AS (
    SELECT
        origin,
        airline,
        COUNT(*) AS total_flights,
        AVG(dep_delay) AS avg_dep_delay,
        AVG(CASE WHEN is_completed_flight = 1 THEN arr_delay ELSE NULL END) AS avg_arr_delay,
        SUM(cancelled) AS cancelled_flights,
        ROUND(SUM(cancelled) / COUNT(*), 6) AS cancellation_rate
    FROM base
    GROUP BY origin, airline
),
airport_stats AS (
    SELECT
        origin,
        AVG(dep_delay) AS airport_avg_dep_delay
    FROM base
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
        ROUND(airline_stats.avg_dep_delay - airport_stats.airport_avg_dep_delay, 4)
            AS dep_delay_diff_from_airport
    FROM airline_airport_stats airline_stats
    INNER JOIN airport_stats
        ON airline_stats.origin = airport_stats.origin
),
ranked AS (
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
)
INSERT OVERWRITE DIRECTORY '${hiveconf:output_dir}'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT
    origin,
    airline,
    total_flights,
    avg_dep_delay,
    avg_arr_delay,
    cancelled_flights,
    cancellation_rate,
    airport_avg_dep_delay,
    dep_delay_diff_from_airport,
    airport_rank_by_avg_dep_delay
FROM ranked;
