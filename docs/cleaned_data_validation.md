# Cleaned Data Validation

## Shape

- Rows: **7,079,081**
- Columns: **26**

## Cardinalities

- Airlines: **15**
- Origin airports: **348**
- Destination airports: **348**
- Routes: **6,805**

## Columns

| column              |
|:--------------------|
| year                |
| month               |
| day_of_month        |
| day_of_week         |
| fl_date             |
| airline             |
| origin              |
| origin_city_name    |
| origin_state_nm     |
| dest                |
| dest_city_name      |
| dest_state_nm       |
| route               |
| dep_delay           |
| arr_delay           |
| dep_delay_band      |
| cancelled           |
| cancellation_code   |
| diverted            |
| is_completed_flight |
| carrier_delay       |
| weather_delay       |
| nas_delay           |
| security_delay      |
| late_aircraft_delay |
| main_delay_cause    |

## Missing values

| column              |   null_count |   null_percentage |
|:--------------------|-------------:|------------------:|
| arr_delay           |       113814 |            1.6078 |
| dep_delay           |        92970 |            1.3133 |
| day_of_month        |            0 |            0      |
| day_of_week         |            0 |            0      |
| fl_date             |            0 |            0      |
| airline             |            0 |            0      |
| origin              |            0 |            0      |
| origin_city_name    |            0 |            0      |
| year                |            0 |            0      |
| month               |            0 |            0      |
| dest                |            0 |            0      |
| origin_state_nm     |            0 |            0      |
| dest_state_nm       |            0 |            0      |
| dest_city_name      |            0 |            0      |
| route               |            0 |            0      |
| dep_delay_band      |            0 |            0      |
| cancelled           |            0 |            0      |
| cancellation_code   |            0 |            0      |
| diverted            |            0 |            0      |
| is_completed_flight |            0 |            0      |
| carrier_delay       |            0 |            0      |
| weather_delay       |            0 |            0      |
| nas_delay           |            0 |            0      |
| security_delay      |            0 |            0      |
| late_aircraft_delay |            0 |            0      |
| main_delay_cause    |            0 |            0      |

## Departure delay bands

| dep_delay_band   |   count |   percentage |
|:-----------------|--------:|-------------:|
| low              | 5542963 |      78.3006 |
| medium           |  934921 |      13.2068 |
| high             |  508227 |       7.1793 |
| unknown          |   92970 |       1.3133 |

## Flight status

| metric            |   count |   percentage |
|:------------------|--------:|-------------:|
| completed_flights | 6965267 |      98.3922 |
| cancelled_flights |   96315 |       1.3606 |
| diverted_flights  |   17499 |       0.2472 |

## Delay statistics on completed flights

| metric    |       count |     mean |     std |   min |   25% |   50% |   75% |   max |
|:----------|------------:|---------:|--------:|------:|------:|------:|------:|------:|
| dep_delay | 6.96527e+06 | 12.5892  | 55.8275 |   -96 |    -6 |    -2 |     9 |  3777 |
| arr_delay | 6.96527e+06 |  7.09825 | 57.9913 |  -126 |   -15 |    -6 |     9 |  3803 |

## Cancellation codes

| cancellation_code   |   count |   percentage |
|:--------------------|--------:|-------------:|
| NotCancelled        | 6982766 |      98.6394 |
| B                   |   53605 |       0.7572 |
| A                   |   30926 |       0.4369 |
| C                   |   11780 |       0.1664 |
| D                   |       4 |       0.0001 |

## Main delay causes

| main_delay_cause   |   count |   percentage |
|:-------------------|--------:|-------------:|
| NoDelayCause       | 5532796 |      78.157  |
| late_aircraft      |  571757 |       8.0767 |
| carrier            |  450784 |       6.3678 |
| nas                |  369325 |       5.2171 |
| Cancelled          |   96315 |       1.3606 |
| weather            |   54406 |       0.7685 |
| security           |    3698 |       0.0522 |
