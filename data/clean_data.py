#!/usr/bin/env python3
"""
Data Cleaning and Merge Pipeline (Pure Python - no pandas)
Task 3: Clean housing and attendance data, derive borough, merge on dbn
"""

import csv
import json

# Borough mapping based on dbn[2]
BOROUGH_MAP = {
    'M': 'Manhattan',
    'X': 'Bronx', 
    'K': 'Brooklyn',
    'Q': 'Queens',
    'R': 'Staten Island'
}


def clean_pct(value):
    """
    Universal percentage cleaner that handles:
    - "30.7%" format (with percent sign)
    - "42.2" format (without percent sign)
    - "s" (suppressed values) → empty string (will be filtered later)
    - Already numeric values
    
    Returns string representation of float or empty string for invalid
    """
    if not value or str(value).strip() == '':
        return ''
    
    # Convert to string for processing
    s = str(value).strip()
    
    # Handle suppressed values
    if s.lower() == 's':
        return ''
    
    # Remove % sign if present
    s = s.replace('%', '')
    
    # Convert to float and back to string
    try:
        return str(float(s))
    except (ValueError, TypeError):
        return ''


def derive_borough(dbn):
    """Extract borough from dbn[2] character"""
    if not dbn or len(str(dbn)) < 3:
        return 'Citywide'
    
    borough_code = str(dbn)[2]
    return BOROUGH_MAP.get(borough_code, 'Citywide')


def load_csv(filepath):
    """Load CSV file as list of dicts"""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def main():
    print("Loading data files...")
    
    # Load raw CSVs
    housing = load_csv('data/housing.csv')
    attendance = load_csv('data/attendance.csv')
    
    print(f"Housing: {len(housing)} rows")
    print(f"Attendance: {len(attendance)} rows")
    
    # Clean housing numeric columns
    print("\nCleaning housing data...")
    housing_numeric_cols = [
        'total_students',
        'students_in_temporary_housing', 
        'students_in_temporary_housing_1',  # This has %
        'students_residing_in_shelter',
        'residing_in_dhs_shelter',
        'residing_in_non_dhs_shelter',
        'doubled_up'
    ]
    
    for row in housing:
        for col in housing_numeric_cols:
            if col in row:
                row[col] = clean_pct(row[col])
        row['borough'] = derive_borough(row.get('dbn', ''))
    
    # Rename housing columns
    housing_col_map = {
        'total_students': 'total_enrollment',
        'students_in_temporary_housing': 'n_students_temp_housing',
        'students_in_temporary_housing_1': 'pct_students_temp_housing',
        'students_residing_in_shelter': 'n_students_in_shelter',
        'residing_in_dhs_shelter': 'n_dhs_shelter',
        'residing_in_non_dhs_shelter': 'n_non_dhs_shelter',
        'doubled_up': 'n_doubled_up'
    }
    
    for row in housing:
        for old_col, new_col in housing_col_map.items():
            if old_col in row:
                row[new_col] = row.pop(old_col)
    
    # Clean attendance numeric columns
    print("Cleaning attendance data...")
    attendance_numeric_cols = [
        'chronically_absent_1',  # No % sign
        'attendance',
        'total_days',
        'days_absent',
        'days_present',
        'chronically_absent',
        'contributing_10_total_days'
    ]
    
    for row in attendance:
        for col in attendance_numeric_cols:
            if col in row:
                row[col] = clean_pct(row[col])
        row['borough'] = derive_borough(row.get('dbn', ''))
    
    # Rename attendance columns
    attendance_col_map = {
        'chronically_absent_1': 'pct_chronically_absent',
        'chronically_absent': 'n_chronically_absent',
        'contributing_10_total_days': 'n_contributing_students'
    }
    
    for row in attendance:
        for old_col, new_col in attendance_col_map.items():
            if old_col in row:
                row[new_col] = row.pop(old_col)
    
    # Create index for attendance by dbn for faster lookup
    print("\nMerging datasets on dbn (inner join)...")
    attendance_by_dbn = {}
    for row in attendance:
        dbn = row.get('dbn', '')
        if dbn:
            attendance_by_dbn[dbn] = row
    
    # Inner join: iterate housing, lookup attendance
    merged = []
    for h_row in housing:
        dbn = h_row.get('dbn', '')
        if dbn in attendance_by_dbn:
            a_row = attendance_by_dbn[dbn]
            
            # Merge rows with suffixes
            merged_row = {}
            
            # Add housing columns with _housing suffix (except dbn)
            for key, value in h_row.items():
                if key == 'dbn':
                    merged_row['dbn'] = value
                elif key in ['school_name', 'borough']:
                    merged_row[f'{key}_housing'] = value
                else:
                    merged_row[key] = value
            
            # Add attendance columns with _attendance suffix (except dbn)
            for key, value in a_row.items():
                if key == 'dbn':
                    continue  # Already added
                elif key in ['school_name', 'borough']:
                    merged_row[f'{key}_attendance'] = value
                else:
                    merged_row[key] = value
            
            merged.append(merged_row)
    
    print(f"Merged: {len(merged)} rows")
    
    # Drop rows with missing key columns
    key_cols = ['pct_students_temp_housing', 'pct_chronically_absent', 
                'n_students_temp_housing', 'total_enrollment']
    
    print(f"\nFiltering rows with complete key columns: {key_cols}")
    before = len(merged)
    filtered_merged = []
    for row in merged:
        # Check if all key columns have non-empty values
        if all(row.get(col, '') != '' for col in key_cols):
            filtered_merged.append(row)
    
    after = len(filtered_merged)
    print(f"Dropped {before - after} rows with missing key columns")
    print(f"Final: {after} rows")
    
    # Save merged dataset
    output_path = 'data/merged.csv'
    if filtered_merged:
        fieldnames = list(filtered_merged[0].keys())
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_merged)
        
        print(f"\n✓ Saved merged dataset to {output_path}")
        print(f"\n=== Summary ===")
        print(f"Rows: {len(filtered_merged)}")
        print(f"Columns: {len(fieldnames)}")
        
        # Count boroughs
        borough_counts = {}
        for row in filtered_merged:
            borough = row.get('borough_housing', 'Unknown')
            borough_counts[borough] = borough_counts.get(borough, 0) + 1
        
        print(f"\nBorough distribution:")
        for borough in sorted(borough_counts.keys()):
            print(f"  {borough}: {borough_counts[borough]}")
    else:
        print("ERROR: No rows to save after filtering!")


if __name__ == '__main__':
    main()
