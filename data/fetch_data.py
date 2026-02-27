#!/usr/bin/env python
"""
Fetch data from NYC Open Data Socrata API.
Saves data to CSV files locally.
"""

import requests
import json
import csv
import os

# Ensure data directory exists
data_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(data_dir, exist_ok=True)

# API endpoints
HOUSING_URL = "https://data.cityofnewyork.us/resource/3wtp-43m9.json"
ATTENDANCE_URL = "https://data.cityofnewyork.us/resource/gqq2-hgxd.json"

# Parameters with $limit=5000 to fetch all data (Socrata default is 1000)
housing_params = {
    "$limit": 5000
}

attendance_params = {
    "$limit": 5000,
    "$where": "year='2020-21' AND grade='All Grades' AND category='All Students'"
}

def fetch_housing_data():
    """Fetch housing data from Socrata API."""
    print("Fetching housing data...")
    try:
        response = requests.get(HOUSING_URL, params=housing_params)
        response.raise_for_status()
        data = response.json()
        print(f"Housing: {len(data)} rows")
        return data
    except Exception as e:
        print(f"Error fetching housing data: {e}")
        raise

def fetch_attendance_data():
    """Fetch attendance data from Socrata API with server-side filters."""
    print("Fetching attendance data...")
    try:
        response = requests.get(ATTENDANCE_URL, params=attendance_params)
        response.raise_for_status()
        data = response.json()
        print(f"Attendance: {len(data)} rows")
        return data
    except Exception as e:
        print(f"Error fetching attendance data: {e}")
        raise

def save_to_csv(data, filename):
    """Save list of dicts to CSV file."""
    if not data:
        print(f"No data to save to {filename}")
        return
    
    # Get fieldnames from first record
    fieldnames = list(data[0].keys())
    
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Saved {len(data)} rows to {filepath}")

def main():
    """Fetch all data and save to CSV files."""
    # Fetch data
    housing_data = fetch_housing_data()
    attendance_data = fetch_attendance_data()
    
    # Save to CSV
    save_to_csv(housing_data, "housing.csv")
    save_to_csv(attendance_data, "attendance.csv")
    
    print("\nData acquisition complete!")

if __name__ == "__main__":
    main()
