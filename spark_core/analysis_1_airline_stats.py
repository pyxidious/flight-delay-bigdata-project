import argparse
import csv
from pathlib import Path
from io import StringIO

from pyspark import SparkConf, SparkContext


OUTPUT_HEADER = [
    "airline",
    "origin",
    "total_flights",
    "min_arr_delay",
    "max_arr_delay",
    "avg_arr_delay",
    "cancelled_flights",
    "cancellation_rate",
    "active_months",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Spark Core Analysis 1: airline statistics by origin airport."
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


def parse_csv_line(line):
    reader = csv.reader(StringIO(line))
    return next(reader)


def safe_float(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def safe_int(value, default=0):
    if value is None or value == "":
        return default
    try:
        return int(float(value))
    except ValueError:
        return default


def format_float(value, digits=4):
    if value is None:
        return ""
    rounded = round(value, digits)
    return str(rounded)


def format_csv_row(values):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(values)
    return output.getvalue().strip()


def merge_total_stats(left, right):
    total_flights_l, cancelled_l, months_l = left
    total_flights_r, cancelled_r, months_r = right

    return (
        total_flights_l + total_flights_r,
        cancelled_l + cancelled_r,
        months_l.union(months_r),
    )


def merge_delay_stats(left, right):
    min_l, max_l, sum_l, count_l = left
    min_r, max_r, sum_r, count_r = right

    return (
        min(min_l, min_r),
        max(max_l, max_r),
        sum_l + sum_r,
        count_l + count_r,
    )


def main():
    args = parse_args()

    conf = (
        SparkConf()
        .setAppName("SparkCoreAnalysis1AirlineStats")
    )

    sc = SparkContext(conf=conf)

    input_rdd = sc.textFile(args.input)

    header = input_rdd.first()
    columns = parse_csv_line(header)
    column_index = {column: index for index, column in enumerate(columns)}

    data_rdd = (
        input_rdd
        .filter(lambda line: line != header)
        .map(parse_csv_line)
    )

    def key_by_airline_origin(row):
        airline = row[column_index["airline"]]
        origin = row[column_index["origin"]]
        return airline, origin

    total_stats = (
        data_rdd
        .map(
            lambda row: (
                key_by_airline_origin(row),
                (
                    1,
                    safe_int(row[column_index["cancelled"]]),
                    {safe_int(row[column_index["month"]])},
                ),
            )
        )
        .reduceByKey(merge_total_stats)
    )

    completed_delay_stats = (
        data_rdd
        .filter(lambda row: safe_int(row[column_index["is_completed_flight"]]) == 1)
        .map(
            lambda row: (
                key_by_airline_origin(row),
                safe_float(row[column_index["arr_delay"]]),
            )
        )
        .filter(lambda item: item[1] is not None)
        .map(
            lambda item: (
                item[0],
                (
                    item[1],
                    item[1],
                    item[1],
                    1,
                ),
            )
        )
        .reduceByKey(merge_delay_stats)
    )

    joined = total_stats.leftOuterJoin(completed_delay_stats)

    result = joined.map(
        lambda item: build_output_row(item[0], item[1])
    )

    output_rdd = sc.parallelize([",".join(OUTPUT_HEADER)]).union(
        result.map(format_csv_row)
    )

    if "://" not in args.output:
        output_path = Path(args.output)
        if output_path.exists():
            import shutil
            shutil.rmtree(output_path)

    output_rdd.saveAsTextFile(args.output)

    print("Spark Core Analysis 1 completed.")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")

    sc.stop()


def build_output_row(key, values):
    airline, origin = key

    total_stats, delay_stats_optional = values

    total_flights, cancelled_flights, active_months_set = total_stats

    if delay_stats_optional is None:
        min_arr_delay = ""
        max_arr_delay = ""
        avg_arr_delay = ""
    else:
        min_delay, max_delay, sum_delay, delay_count = delay_stats_optional
        min_arr_delay = format_float(min_delay, digits=1)
        max_arr_delay = format_float(max_delay, digits=1)
        avg_arr_delay = format_float(sum_delay / delay_count, digits=4)

    cancellation_rate = round(cancelled_flights / total_flights, 6)

    active_months = ",".join(
        str(month)
        for month in sorted(active_months_set)
    )

    return [
        airline,
        origin,
        total_flights,
        min_arr_delay,
        max_arr_delay,
        avg_arr_delay,
        cancelled_flights,
        cancellation_rate,
        active_months,
    ]


if __name__ == "__main__":
    main()
