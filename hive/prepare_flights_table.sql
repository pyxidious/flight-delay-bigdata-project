DROP TABLE IF EXISTS flights_hive;

CREATE EXTERNAL TABLE flights_hive (
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
