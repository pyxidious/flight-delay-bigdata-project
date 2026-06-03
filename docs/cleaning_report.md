# Report Di Pulizia / Cleaning Report

## Italiano

### Input E Output

- Dataset grezzo: `data/raw/flight_data_2024.csv`
- CSV pulito: `data/cleaned/flights_clean.csv`
- Parquet pulito: `data/cleaned/flights_clean.parquet`

### Strategia Di Pulizia

Il processo di pulizia applica le seguenti operazioni:

1. Selezione delle sole colonne rilevanti per le analisi richieste.
2. Rinomina di `op_unique_carrier` in `airline` per maggiore leggibilita.
3. Normalizzazione dei codici compagnia e aeroporto in stringhe maiuscole.
4. Creazione della colonna `route` come `origin-dest`.
5. Creazione di `is_completed_flight` per identificare voli non cancellati, non deviati e con ritardi validi.
6. Creazione di `dep_delay_band` con tre fasce: low, medium e high.
7. Normalizzazione di `cancellation_code`, usando `NotCancelled` per voli non cancellati e `Unknown` per voli cancellati senza codice.
8. Creazione di `main_delay_cause` dalla maggiore colonna disponibile tra le cause di ritardo.
9. Salvataggio del dataset pulito sia in CSV sia in Parquet.

### Definizione Delle Fasce Di Ritardo

| Fascia | Regola |
|---|---|
| low | `dep_delay < 15` |
| medium | `15 <= dep_delay <= 60` |
| high | `dep_delay > 60` |
| unknown | `dep_delay` mancante |

### Conteggio Righe

- Righe input processate: **7,079,081**
- Righe output scritte: **7,079,081**
- Righe rimosse per chiavi obbligatorie mancanti: **0**

### Note Per Le Analisi Successive

- Le medie dei ritardi devono essere calcolate sulle righe con `is_completed_flight = 1`.
- I tassi di cancellazione devono essere calcolati su tutte le righe.
- `main_delay_cause` deriva dalle colonne delle cause di ritardo ed e utile soprattutto per i report sulle frequenze delle cause.
- `cancellation_code` e significativo soprattutto quando `cancelled = 1`.

## English

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
