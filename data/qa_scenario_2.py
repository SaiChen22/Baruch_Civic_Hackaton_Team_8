#!/usr/bin/env python3
"""QA Scenario 2: Verify no suppressed values leaked"""

import csv

# Load merged CSV
with open('data/merged.csv', 'r') as f:
    reader = csv.DictReader(f)
    data = list(reader)

# Check key columns for 's' or '%' characters
key_cols = ['pct_students_temp_housing', 'pct_chronically_absent', 
            'n_students_temp_housing', 'total_enrollment']

for row in data:
    for col in key_cols:
        value = str(row[col])
        
        # Check for 's' (suppressed value marker)
        if 's' in value.lower():
            raise AssertionError(f"Found 's' in {col}: {value}")
        
        # Check for '%' (should be stripped)
        if '%' in value:
            raise AssertionError(f"Found '%' in {col}: {value}")

print('CLEAN_OK')
