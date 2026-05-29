# Dataset Inspection

## Source

- Dataset path: `data/raw/flight_data_2024.csv`
- File size: **1.22 GB**
- Sample size used for inspection: **10,000 rows**

## Shape

- Total rows, excluding header: **7,079,081**
- Total columns: **35**

## Columns

- `year`
- `month`
- `day_of_month`
- `day_of_week`
- `fl_date`
- `op_unique_carrier`
- `op_carrier_fl_num`
- `origin`
- `origin_city_name`
- `origin_state_nm`
- `dest`
- `dest_city_name`
- `dest_state_nm`
- `crs_dep_time`
- `dep_time`
- `dep_delay`
- `taxi_out`
- `wheels_off`
- `wheels_on`
- `taxi_in`
- `crs_arr_time`
- `arr_time`
- `arr_delay`
- `cancelled`
- `cancellation_code`
- `diverted`
- `crs_elapsed_time`
- `actual_elapsed_time`
- `air_time`
- `distance`
- `carrier_delay`
- `weather_delay`
- `nas_delay`
- `security_delay`
- `late_aircraft_delay`

## Inferred data types on sample

| column              | inferred_type_on_sample   |
|:--------------------|:--------------------------|
| year                | int64                     |
| month               | int64                     |
| day_of_month        | int64                     |
| day_of_week         | int64                     |
| fl_date             | object                    |
| op_unique_carrier   | object                    |
| op_carrier_fl_num   | float64                   |
| origin              | object                    |
| origin_city_name    | object                    |
| origin_state_nm     | object                    |
| dest                | object                    |
| dest_city_name      | object                    |
| dest_state_nm       | object                    |
| crs_dep_time        | int64                     |
| dep_time            | float64                   |
| dep_delay           | float64                   |
| taxi_out            | float64                   |
| wheels_off          | float64                   |
| wheels_on           | float64                   |
| taxi_in             | float64                   |
| crs_arr_time        | int64                     |
| arr_time            | float64                   |
| arr_delay           | float64                   |
| cancelled           | int64                     |
| cancellation_code   | object                    |
| diverted            | int64                     |
| crs_elapsed_time    | float64                   |
| actual_elapsed_time | float64                   |
| air_time            | float64                   |
| distance            | float64                   |
| carrier_delay       | int64                     |
| weather_delay       | int64                     |
| nas_delay           | int64                     |
| security_delay      | int64                     |
| late_aircraft_delay | int64                     |

## Missing values on sample

| column              |   null_count_in_sample |   null_percentage_in_sample |
|:--------------------|-----------------------:|----------------------------:|
| cancellation_code   |                   9987 |                       99.87 |
| actual_elapsed_time |                     16 |                        0.16 |
| arr_delay           |                     16 |                        0.16 |
| air_time            |                     16 |                        0.16 |
| wheels_on           |                     14 |                        0.14 |
| taxi_in             |                     14 |                        0.14 |
| arr_time            |                     14 |                        0.14 |
| wheels_off          |                     12 |                        0.12 |
| taxi_out            |                     12 |                        0.12 |
| dep_delay           |                     10 |                        0.1  |
| dep_time            |                     10 |                        0.1  |
| day_of_month        |                      0 |                        0    |
| month               |                      0 |                        0    |
| year                |                      0 |                        0    |
| origin_state_nm     |                      0 |                        0    |
| dest                |                      0 |                        0    |
| day_of_week         |                      0 |                        0    |
| op_unique_carrier   |                      0 |                        0    |
| fl_date             |                      0 |                        0    |
| dest_state_nm       |                      0 |                        0    |
| dest_city_name      |                      0 |                        0    |
| crs_dep_time        |                      0 |                        0    |
| op_carrier_fl_num   |                      0 |                        0    |
| origin              |                      0 |                        0    |
| origin_city_name    |                      0 |                        0    |
| crs_arr_time        |                      0 |                        0    |
| cancelled           |                      0 |                        0    |
| crs_elapsed_time    |                      0 |                        0    |
| diverted            |                      0 |                        0    |
| distance            |                      0 |                        0    |
| carrier_delay       |                      0 |                        0    |
| weather_delay       |                      0 |                        0    |
| nas_delay           |                      0 |                        0    |
| security_delay      |                      0 |                        0    |
| late_aircraft_delay |                      0 |                        0    |

## Candidate columns for project analyses

The following columns are automatically identified as possible candidates. They will be manually verified before implementing the cleaning script.

### airline_or_carrier

- `op_unique_carrier`

### flight_number

- `op_carrier_fl_num`

### origin_airport

- `origin`
- `origin_city_name`
- `origin_state_nm`

### destination_airport

- `dest`
- `dest_city_name`
- `dest_state_nm`

### date_or_month

- `year`
- `month`
- `day_of_month`
- `day_of_week`
- `fl_date`

### departure_delay

- `dep_delay`

### arrival_delay

- `arr_delay`

### cancelled

- `cancelled`

### cancellation_code

- `cancellation_code`

### diverted

- `diverted`

### delay_causes

- `carrier_delay`
- `weather_delay`
- `nas_delay`
- `security_delay`
- `late_aircraft_delay`

### time_columns

- `crs_dep_time`
- `dep_time`
- `wheels_off`
- `wheels_on`
- `crs_arr_time`
- `arr_time`

### duration_or_distance

- `crs_elapsed_time`
- `actual_elapsed_time`
- `air_time`
- `distance`

## Duplicate rows on sample

- Duplicate rows in sample: **0**

## Memory usage on sample

- Sample memory usage: **6.61 MB**

## First 10 rows

|   year |   month |   day_of_month |   day_of_week | fl_date    | op_unique_carrier   |   op_carrier_fl_num | origin   | origin_city_name    | origin_state_nm   | dest   | dest_city_name   | dest_state_nm   |   crs_dep_time |   dep_time |   dep_delay |   taxi_out |   wheels_off |   wheels_on |   taxi_in |   crs_arr_time |   arr_time |   arr_delay |   cancelled |   cancellation_code |   diverted |   crs_elapsed_time |   actual_elapsed_time |   air_time |   distance |   carrier_delay |   weather_delay |   nas_delay |   security_delay |   late_aircraft_delay |
|-------:|--------:|---------------:|--------------:|:-----------|:--------------------|--------------------:|:---------|:--------------------|:------------------|:-------|:-----------------|:----------------|---------------:|-----------:|------------:|-----------:|-------------:|------------:|----------:|---------------:|-----------:|------------:|------------:|--------------------:|-----------:|-------------------:|----------------------:|-----------:|-----------:|----------------:|----------------:|------------:|-----------------:|----------------------:|
|   2024 |       1 |              1 |             1 | 2024-01-01 | 9E                  |                4814 | JFK      | New York, NY        | New York          | DTW    | Detroit, MI      | Michigan        |           1252 |       1247 |          -5 |         31 |         1318 |        1442 |         7 |           1508 |       1449 |         -19 |           0 |                 nan |          0 |                136 |                   122 |         84 |        509 |               0 |               0 |           0 |                0 |                     0 |
|   2024 |       1 |              1 |             1 | 2024-01-01 | 9E                  |                4815 | MSP      | Minneapolis, MN     | Minnesota         | CLE    | Cleveland, OH    | Ohio            |           1015 |       1001 |         -14 |         20 |         1021 |        1249 |         6 |           1325 |       1255 |         -30 |           0 |                 nan |          0 |                130 |                   114 |         88 |        622 |               0 |               0 |           0 |                0 |                     0 |
|   2024 |       1 |              1 |             1 | 2024-01-01 | 9E                  |                4817 | JFK      | New York, NY        | New York          | RIC    | Richmond, VA     | Virginia        |           1415 |       1411 |          -4 |         21 |         1432 |        1533 |         8 |           1601 |       1541 |         -20 |           0 |                 nan |          0 |                106 |                    90 |         61 |        288 |               0 |               0 |           0 |                0 |                     0 |
|   2024 |       1 |              1 |             1 | 2024-01-01 | 9E                  |                4817 | RIC      | Richmond, VA        | Virginia          | JFK    | New York, NY     | New York        |           1650 |       1643 |          -7 |         13 |         1656 |        1747 |        12 |           1841 |       1759 |         -42 |           0 |                 nan |          0 |                111 |                    76 |         51 |        288 |               0 |               0 |           0 |                0 |                     0 |
|   2024 |       1 |              1 |             1 | 2024-01-01 | 9E                  |                4818 | DTW      | Detroit, MI         | Michigan          | MKE    | Milwaukee, WI    | Wisconsin       |           1015 |       1010 |          -5 |         21 |         1031 |        1016 |         4 |           1034 |       1020 |         -14 |           0 |                 nan |          0 |                 79 |                    70 |         45 |        237 |               0 |               0 |           0 |                0 |                     0 |
|   2024 |       1 |              1 |             1 | 2024-01-01 | 9E                  |                4822 | JAX      | Jacksonville, FL    | Florida           | LGA    | New York, NY     | New York        |           1410 |       1403 |          -7 |         14 |         1417 |        1559 |         4 |           1627 |       1603 |         -24 |           0 |                 nan |          0 |                137 |                   120 |        102 |        833 |               0 |               0 |           0 |                0 |                     0 |
|   2024 |       1 |              1 |             1 | 2024-01-01 | 9E                  |                4822 | LGA      | New York, NY        | New York          | JAX    | Jacksonville, FL | Florida         |            955 |        947 |          -8 |         26 |         1013 |        1218 |        13 |           1244 |       1231 |         -13 |           0 |                 nan |          0 |                169 |                   164 |        125 |        833 |               0 |               0 |           0 |                0 |                     0 |
|   2024 |       1 |              1 |             1 | 2024-01-01 | 9E                  |                4823 | CHS      | Charleston, SC      | South Carolina    | LGA    | New York, NY     | New York        |           1140 |       1135 |          -5 |          8 |         1143 |        1309 |         5 |           1338 |       1314 |         -24 |           0 |                 nan |          0 |                118 |                    99 |         86 |        641 |               0 |               0 |           0 |                0 |                     0 |
|   2024 |       1 |              1 |             1 | 2024-01-01 | 9E                  |                4823 | LGA      | New York, NY        | New York          | CHS    | Charleston, SC   | South Carolina  |            815 |        810 |          -5 |         14 |          824 |        1005 |         8 |           1044 |       1013 |         -31 |           0 |                 nan |          0 |                149 |                   123 |        101 |        641 |               0 |               0 |           0 |                0 |                     0 |
|   2024 |       1 |              1 |             1 | 2024-01-01 | 9E                  |                4828 | ITH      | Ithaca/Cortland, NY | New York          | JFK    | New York, NY     | New York        |           1300 |       1248 |         -12 |         12 |         1300 |        1343 |        12 |           1419 |       1355 |         -24 |           0 |                 nan |          0 |                 79 |                    67 |         43 |        189 |               0 |               0 |           0 |                0 |                     0 |

## Notes

- This inspection is based on a sample for data types and missing values.
- The total number of rows is computed by scanning the full CSV file.
- Final cleaning decisions will be documented after verifying the relevant columns.
