# Flight Delay Big Data Project

Project for the Big Data course at Università degli Studi Roma Tre.

The project analyzes the Flight Delay Dataset 2024 using multiple Big Data technologies, with a focus on data preparation, distributed processing, performance comparison and reproducibility.

## Dataset

The dataset is not included in this repository because of its size.

Expected local path:

```text
data/raw/flight_data_2024.csv
```

## Technologies

The project will compare different Big Data technologies:

- Spark SQL
- Spark Core
- Hive
- Optional: MapReduce

## Repository structure

```text
flight-delay-bigdata-project/
├── data/
│   ├── raw/
│   ├── cleaned/
│   ├── samples/
│   └── output/
├── docs/
├── report/
├── results/
│   ├── output/
│   └── tmp/
├── scripts/
├── .gitignore
├── README.md
└── requirements.txt
```

## Python environment setup

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Verify the environment:

```bash
python -c "import pandas, numpy, matplotlib, pyarrow, pyspark; print('Environment OK')"
```

## Reproducibility

The repository includes:

- fixed Python dependencies in `requirements.txt`;
- scripts for data preparation and analysis;
- execution instructions;
- benchmark results and generated outputs;
- final report in PDF format.

Large datasets and generated outputs are excluded from Git versioning.
