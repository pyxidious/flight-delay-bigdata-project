import argparse
import csv
from pathlib import Path
from io import StringIO
from collections import defaultdict

from pyspark import SparkConf, SparkContext


OUTPUT_HEADER = [
    "origin",
    "month",
    "dep_delay_band",
    "flight_count",
    "avg_dep_delay",
    "avg_arr_delay",
    "top_3_causes",
]

VALID_DELAY_BANDS = {"low", "medium", "high"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Spark Core Analysis 2: delay report by origin airport, month and delay band."
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
    return str(round(value, digits))


def format_csv_row(values):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(values)
    return output.getvalue().strip()


def merge_metrics(left, right):
    (
        flight_count_l,
        dep_delay_sum_l,
        dep_delay_count_l,
        arr_delay_sum_l,
        arr_delay_count_l,
    ) = left

    (
        flight_count_r,
        dep_delay_sum_r,
        dep_delay_count_r,
        arr_delay_sum_r,
        arr_delay_count_r,
    ) = right

    return (
        flight_count_l + flight_count_r,
        dep_delay_sum_l + dep_delay_sum_r,
        dep_delay_count_l + dep_delay_count_r,
        arr_delay_sum_l + arr_delay_sum_r,
        arr_delay_count_l + arr_delay_count_r,
    )


def merge_cause_counts(left, right):
    merged = defaultdict(int)

    for cause, count in left.items():
        merged[cause] += count

    for cause, count in right.items():
        merged[cause] += count

    return dict(merged)


def build_event_cause(row, column_index):
    cancelled = safe_int(row[column_index["cancelled"]])
    cancellation_code = row[column_index["cancellation_code"]]
    main_delay_cause = row[column_index["main_delay_cause"]]

    if cancelled == 1:
        return f"Cancellation_{cancellation_code}"

    if main_delay_cause != "NoDelayCause":
        return f"Delay_{main_delay_cause}"

    return "NoCauseAvailable"


def top_3_causes_to_string(cause_counts):
    if not cause_counts:
        return "NoCauseAvailable"

    filtered_items = [
        (cause, count)
        for cause, count in cause_counts.items()
        if cause != "NoCauseAvailable"
    ]

    if not filtered_items:
        return "NoCauseAvailable"

    top_items = sorted(
        filtered_items,
        key=lambda item: (-item[1], item[0]),
    )[:3]

    return "; ".join(
        f"{rank}:{cause}={count}"
        for rank, (cause, count) in enumerate(top_items, start=1)
    )


def build_output_row(key, values):
    origin, month, dep_delay_band = key

    metrics, cause_counts_optional = values

    (
        flight_count,
        dep_delay_sum,
        dep_delay_count,
        arr_delay_sum,
        arr_delay_count,
    ) = metrics

    avg_dep_delay = (
        dep_delay_sum / dep_delay_count
        if dep_delay_count > 0
        else None
    )

    avg_arr_delay = (
        arr_delay_sum / arr_delay_count
        if arr_delay_count > 0
        else None
    )

    top_3_causes = top_3_causes_to_string(
        cause_counts_optional if cause_counts_optional is not None else {}
    )

    return [
        origin,
        month,
        dep_delay_band,
        flight_count,
        format_float(avg_dep_delay, digits=4),
        format_float(avg_arr_delay, digits=4),
        top_3_causes,
    ]


def main():
    args = parse_args()

    conf = (
        SparkConf()
        .setAppName("SparkCoreAnalysis2AirportMonthDelayReport")
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

    base_rdd = data_rdd.filter(
        lambda row: row[column_index["dep_delay_band"]] in VALID_DELAY_BANDS
    )

    def group_key(row):
        return (
            row[column_index["origin"]],
            safe_int(row[column_index["month"]]),
            row[column_index["dep_delay_band"]],
        )

    metrics = (
        base_rdd
        .map(
            lambda row: (
                group_key(row),
                build_metric_value(row, column_index),
            )
        )
        .reduceByKey(merge_metrics)
    )

    cause_counts = (
        base_rdd
        .map(
            lambda row: (
                group_key(row),
                {build_event_cause(row, column_index): 1},
            )
        )
        .reduceByKey(merge_cause_counts)
    )

    result = (
        metrics
        .leftOuterJoin(cause_counts)
        .map(lambda item: build_output_row(item[0], item[1]))
        .sortBy(lambda row: (row[0], row[1], row[2]))
    )

    output_rdd = sc.parallelize([",".join(OUTPUT_HEADER)]).union(
        result.map(format_csv_row)
    )

    if "://" not in args.output:
        output_path = Path(args.output)
        if output_path.exists():
            import shutil
            shutil.rmtree(output_path)

    output_rdd.coalesce(1).saveAsTextFile(args.output)

    print("Spark Core Analysis 2 completed.")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")

    print("First 10 rows:")
    for row in result.take(10):
        print(format_csv_row(row))

    sc.stop()


def build_metric_value(row, column_index):
    dep_delay = safe_float(row[column_index["dep_delay"]])
    arr_delay = safe_float(row[column_index["arr_delay"]])
    is_completed_flight = safe_int(row[column_index["is_completed_flight"]])

    dep_delay_sum = dep_delay if dep_delay is not None else 0.0
    dep_delay_count = 1 if dep_delay is not None else 0

    if is_completed_flight == 1 and arr_delay is not None:
        arr_delay_sum = arr_delay
        arr_delay_count = 1
    else:
        arr_delay_sum = 0.0
        arr_delay_count = 0

    return (
        1,
        dep_delay_sum,
        dep_delay_count,
        arr_delay_sum,
        arr_delay_count,
    )


if __name__ == "__main__":
    main()
