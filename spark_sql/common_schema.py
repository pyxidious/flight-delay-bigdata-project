from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    DoubleType,
    StringType,
)


def get_flights_schema() -> StructType:
    return StructType(
        [
            StructField("year", IntegerType(), True),
            StructField("month", IntegerType(), True),
            StructField("day_of_month", IntegerType(), True),
            StructField("day_of_week", IntegerType(), True),
            StructField("fl_date", StringType(), True),
            StructField("airline", StringType(), True),
            StructField("origin", StringType(), True),
            StructField("origin_city_name", StringType(), True),
            StructField("origin_state_nm", StringType(), True),
            StructField("dest", StringType(), True),
            StructField("dest_city_name", StringType(), True),
            StructField("dest_state_nm", StringType(), True),
            StructField("route", StringType(), True),
            StructField("dep_delay", DoubleType(), True),
            StructField("arr_delay", DoubleType(), True),
            StructField("dep_delay_band", StringType(), True),
            StructField("cancelled", IntegerType(), True),
            StructField("cancellation_code", StringType(), True),
            StructField("diverted", IntegerType(), True),
            StructField("is_completed_flight", IntegerType(), True),
            StructField("carrier_delay", DoubleType(), True),
            StructField("weather_delay", DoubleType(), True),
            StructField("nas_delay", DoubleType(), True),
            StructField("security_delay", DoubleType(), True),
            StructField("late_aircraft_delay", DoubleType(), True),
            StructField("main_delay_cause", StringType(), True),
        ]
    )
