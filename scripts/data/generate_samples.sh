#!/usr/bin/env bash

set -euo pipefail

INPUT_FILE="data/cleaned/flights_clean.csv"
OUTPUT_DIR="data/samples"

mkdir -p "$OUTPUT_DIR"

if [ ! -f "$INPUT_FILE" ]; then
    echo "ERROR: cleaned dataset not found at $INPUT_FILE"
    echo "Run: python scripts/prepare_data.py"
    exit 1
fi

echo "Generating benchmark samples from $INPUT_FILE"
echo

generate_sample() {
    local rows="$1"
    local output_file="$2"

    echo "Creating $output_file with $rows data rows..."

    # +1 because the CSV header must be included.
    head -n "$((rows + 1))" "$INPUT_FILE" > "$output_file"

    local actual_rows
    actual_rows=$(($(wc -l < "$output_file") - 1))

    echo "Written rows: $actual_rows"
    echo
}

generate_sample 100000 "$OUTPUT_DIR/flights_100k.csv"
generate_sample 500000 "$OUTPUT_DIR/flights_500k.csv"
generate_sample 1000000 "$OUTPUT_DIR/flights_1m.csv"
generate_sample 3000000 "$OUTPUT_DIR/flights_3m.csv"

echo "Copying full cleaned dataset as 7M sample..."
cp "$INPUT_FILE" "$OUTPUT_DIR/flights_7m.csv"

echo
echo "Generated files:"
ls -lh "$OUTPUT_DIR"

echo
echo "Sample generation completed."
