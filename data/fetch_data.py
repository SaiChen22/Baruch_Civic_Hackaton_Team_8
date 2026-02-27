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
HOUSING_DATASETS = {
    "2020-21": "3wtp-43m9",
    "2019-20": "ec4f-sy8r",
    "2018-19": "4e3j-75af",
    "2017-18": "b22r-9izv",
}
ATTENDANCE_URL = "https://data.cityofnewyork.us/resource/gqq2-hgxd.json"
ATTENDANCE_YEARS = ["2017-18", "2018-19", "2019-20", "2020-21"]

# Parameters with $limit=5000 to fetch all data (Socrata default is 1000)
housing_params = {
    "$limit": 5000
}

attendance_params = {
    "$limit": 5000,
    "$where": "year='2020-21' AND grade='All Grades' AND category='All Students'"
}

def fetch_housing_data(dataset_id, school_year):
    """Fetch one school-year housing dataset from Socrata API."""
    url = f"https://data.cityofnewyork.us/resource/{dataset_id}.json"
    print(f"Fetching housing data for {school_year} ({dataset_id})...")
    try:
        response = requests.get(url, params=housing_params)
        response.raise_for_status()
        data = response.json()
        for row in data:
            row['school_year'] = school_year
        print(f"Housing {school_year}: {len(data)} rows")
        return data
    except Exception as e:
        print(f"Error fetching housing data for {school_year}: {e}")
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

def fetch_attendance_all_years():
    """Fetch attendance data for all configured school years."""
    print("Fetching attendance data for all years...")
    all_rows = []
    for year in ATTENDANCE_YEARS:
        params = {
            "$limit": 5000,
            "$where": f"year='{year}' AND grade='All Grades' AND category='All Students'"
        }
        try:
            response = requests.get(ATTENDANCE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            print(f"Attendance {year}: {len(data)} rows")
            all_rows.extend(data)
        except Exception as e:
            print(f"Error fetching attendance data for {year}: {e}")
            raise
    print(f"Attendance all years total: {len(all_rows)} rows")
    return all_rows

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
    # Fetch housing data by year
    housing_by_year = {}
    for school_year, dataset_id in HOUSING_DATASETS.items():
        housing_by_year[school_year] = fetch_housing_data(dataset_id, school_year)

    # Combine all housing rows for archival/extended analysis
    combined_housing = []
    for school_year in ["2017-18", "2018-19", "2019-20", "2020-21"]:
        combined_housing.extend(housing_by_year.get(school_year, []))

    # Keep existing pipeline compatibility: housing.csv remains 2020-21
    housing_data = housing_by_year["2020-21"]

    # Fetch attendance data
    attendance_data = fetch_attendance_data()
    attendance_all_years = fetch_attendance_all_years()
    
    # Save compatibility files
    save_to_csv(housing_data, "housing.csv")
    save_to_csv(attendance_data, "attendance.csv")
    save_to_csv(attendance_all_years, "attendance_all_years.csv")

    # Save additional housing datasets
    save_to_csv(housing_by_year["2019-20"], "housing_2019_20.csv")
    save_to_csv(housing_by_year["2018-19"], "housing_2018_19.csv")
    save_to_csv(housing_by_year["2017-18"], "housing_2017_18.csv")
    save_to_csv(combined_housing, "housing_all_years.csv")
    
    print("\nData acquisition complete!")

if __name__ == "__main__":
    main()
