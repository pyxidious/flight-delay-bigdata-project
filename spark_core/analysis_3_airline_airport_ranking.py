import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP
from io import StringIO
from pathlib import Path

from pyspark import SparkConf, SparkContext


OUTPUT_HEADER = [
    "origin",
    "airline",
    "total_flights",
    "avg_dep_delay",
    "avg_arr_delay",
    "cancelled_flights",
    "cancellation_rate",
    "airport_avg_dep_delay",
    "dep_delay_diff_from_airport",
    "airport_rank_by_avg_dep_delay",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Spark Core Analysis 3: airline performance ranking by origin airport."
    )
    parser.add_argument("--input", required=True, help="Input cleaned CSV path.")
    parser.add_argument("--output", required=True, help="Output directory path.")
    return parser.parse_args()


def parse_csv_line(line):
    return next(csv.reader(StringIO(line)))


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
    quantum = Decimal(1).scaleb(-digits)
    rounded = Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_UP)
    return str(float(rounded))


def format_csv_row(values):
    output = StringIO()
    csv.writer(output).writerow(values)
    return output.getvalue().strip()


def merge_stats(left, right):
    return tuple(left_value + right_value for left_value, right_value in zip(left, right))


def build_stats(row, column_index):
    dep_delay = safe_float(row[column_index["dep_delay"]])
    arr_delay = safe_float(row[column_index["arr_delay"]])
    is_completed_flight = safe_int(row[column_index["is_completed_flight"]])

    return (
        1,
        dep_delay if dep_delay is not None else 0.0,
        1 if dep_delay is not None else 0,
        arr_delay if is_completed_flight == 1 and arr_delay is not None else 0.0,
        1 if is_completed_flight == 1 and arr_delay is not None else 0,
        safe_int(row[column_index["cancelled"]]),
    )


def average(total, count):
    return total / count if count > 0 else None


def build_compared_row(item):
    origin, (airline_stats, airport_stats) = item
    airline, stats = airline_stats
    (
        total_flights,
        dep_delay_sum,
        dep_delay_count,
        arr_delay_sum,
        arr_delay_count,
        cancelled_flights,
    ) = stats
    _, airport_dep_delay_sum, airport_dep_delay_count, _, _, _ = airport_stats

    avg_dep_delay = average(dep_delay_sum, dep_delay_count)
    avg_arr_delay = average(arr_delay_sum, arr_delay_count)
    airport_avg_dep_delay = average(airport_dep_delay_sum, airport_dep_delay_count)
    dep_delay_diff = (
        avg_dep_delay - airport_avg_dep_delay
        if avg_dep_delay is not None and airport_avg_dep_delay is not None
        else None
    )

    return (
        origin,
        (
            airline,
            total_flights,
            avg_dep_delay,
            avg_arr_delay,
            cancelled_flights,
            cancelled_flights / total_flights,
            airport_avg_dep_delay,
            dep_delay_diff,
        ),
    )


def rank_airlines(item):
    origin, airlines = item
    ordered = sorted(
        airlines,
        key=lambda values: (
            values[2] is not None,
            values[2] if values[2] is not None else 0.0,
            values[0],
        ),
    )
    return [
        [
            origin,
            airline,
            total_flights,
            format_float(avg_dep_delay),
            format_float(avg_arr_delay),
            cancelled_flights,
            format_float(cancellation_rate, digits=6),
            format_float(airport_avg_dep_delay),
            format_float(dep_delay_diff),
            rank,
        ]
        for rank, (
            airline,
            total_flights,
            avg_dep_delay,
            avg_arr_delay,
            cancelled_flights,
            cancellation_rate,
            airport_avg_dep_delay,
            dep_delay_diff,
        ) in enumerate(ordered, start=1)
    ]


def main():
    args = parse_args()
    sc = SparkContext(
        conf=SparkConf().setAppName("SparkCoreAnalysis3AirlineAirportRanking")
    )

    input_rdd = sc.textFile(args.input)
    header = input_rdd.first()
    columns = parse_csv_line(header)
    column_index = {column: index for index, column in enumerate(columns)}
    data_rdd = input_rdd.filter(lambda line: line != header).map(parse_csv_line)

    def pair_key(row):
        return row[column_index["origin"]], row[column_index["airline"]]

    pair_stats = (
        data_rdd
        .map(lambda row: (pair_key(row), build_stats(row, column_index)))
        .reduceByKey(merge_stats)
    )
    airport_stats = (
        pair_stats
        .map(lambda item: (item[0][0], item[1]))
        .reduceByKey(merge_stats)
    )
    compared = (
        pair_stats
        .map(lambda item: (item[0][0], (item[0][1], item[1])))
        .join(airport_stats)
        .map(build_compared_row)
    )
    result = compared.groupByKey().flatMap(rank_airlines)
    output_rdd = sc.parallelize([",".join(OUTPUT_HEADER)]).union(result.map(format_csv_row))

    if "://" not in args.output:
        output_path = Path(args.output)
        if output_path.exists():
            import shutil
            shutil.rmtree(output_path)

    output_rdd.saveAsTextFile(args.output)

    print("Spark Core Analysis 3 completed.")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    sc.stop()


if __name__ == "__main__":
    main()
