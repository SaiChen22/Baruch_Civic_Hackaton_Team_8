#!/usr/bin/env python3
"""QA Scenario 1: Verify merged dataset shape and dtypes"""

import csv

# Load merged CSV
with open('data/merged.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

print(f'ROWS:{len(data)}')

# Check row count
assert len(data) > 1300, f"Expected >1300 rows, got {len(data)}"

# Check that key columns exist and have numeric values
for row in data:
    # Test pct_students_temp_housing is numeric
    val1 = row['pct_students_temp_housing']
    try:
        float(val1)
    except ValueError:
        raise AssertionError(f"pct_students_temp_housing not numeric: {val1}")
    
    # Test pct_chronically_absent is numeric
    val2 = row['pct_chronically_absent']
    try:
        float(val2)
    except ValueError:
        raise AssertionError(f"pct_chronically_absent not numeric: {val2}")

print('SHAPE_OK')
