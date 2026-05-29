# Cleaning Report

## Input and output

- Raw dataset: `data/raw/flight_data_2024.csv`
- Cleaned CSV: `data/cleaned/flights_clean.csv`
- Cleaned Parquet: `data/cleaned/flights_clean.parquet`

## Cleaning strategy

The cleaning process applies the following operations:

1. Select only columns relevant to the required analyses.
2. Rename `op_unique_carrier` to `airline` for readability.
3. Normalize carrier and airport codes to uppercase strings.
4. Create a `route` column as `origin-dest`.
5. Create `is_completed_flight` to identify non-cancelled and non-diverted flights with valid delay values.
6. Create `dep_delay_band` with three bands: low, medium and high.
7. Normalize `cancellation_code`, using `NotCancelled` for non-cancelled flights and `Unknown` for cancelled flights without a code.
8. Create `main_delay_cause` from the largest available delay-cause column.
9. Save the cleaned dataset both as CSV and Parquet.

## Delay band definition

| Band | Rule |
|---|---|
| low | `dep_delay < 15` |
| medium | `15 <= dep_delay <= 60` |
| high | `dep_delay > 60` |
| unknown | missing `dep_delay` |

## Row counts

- Input rows processed: **7,079,081**
- Output rows written: **7,079,081**
- Rows removed because of missing required keys: **0**

## Notes for later analyses

- Delay averages should be computed on rows where `is_completed_flight = 1`.
- Cancellation rates should be computed on all rows.
- `main_delay_cause` is derived from delay-cause columns and is mainly useful for delay-cause frequency reports.
- `cancellation_code` is meaningful mainly when `cancelled = 1`.
