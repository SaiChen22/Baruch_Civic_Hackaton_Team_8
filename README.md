# The Absenteeism Gap

**How Homelessness Steals School Days in NYC**

A data-driven Streamlit dashboard analyzing the relationship between student homelessness and chronic absenteeism across 1,454 NYC schools (2020-21 school year).

Created for the **Baruch College Civic Tech & Data Hackathon** (Feb 27, 2026).

---

## 📊 The Story

In 2020-21, approximately **87,000 NYC students** lived in temporary housing — roughly 1 in 12 students. This dashboard explores:

- **The Scale**: Geographic distribution of student homelessness across NYC's five boroughs
- **The Gap**: Clear correlation between housing instability and chronic absenteeism
- **The Invisible Majority**: 2/3 of homeless students are "doubled up" (living with others), not in shelters

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone or download this repository
cd Baruch_hackton_Team_9_o

# Install dependencies
pip install -r requirements.txt
```

### Run the Dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at **http://localhost:8501**

---

## 📁 Project Structure

```
Baruch_hackton_Team_9_o/
├── app.py                  # Main Streamlit dashboard (133 lines)
├── requirements.txt        # Python dependencies
├── data/
│   ├── fetch_data.py       # Data acquisition script
│   ├── clean_data.py       # Data cleaning pipeline
│   ├── housing.csv         # Raw housing data (1,689 rows)
│   ├── attendance.csv      # Raw attendance data (1,530 rows)
│   └── merged.csv          # Clean merged dataset (1,454 schools)
└── README.md               # This file
```

---

## 📈 Dashboard Features

### Tab 1: "📊 The Scale"
- **Borough bar chart**: Shows distribution of students in temporary housing
- **Key metrics**: Total schools, total students affected, citywide average
- **Insight**: The Bronx bears the highest burden, Staten Island the lowest

### Tab 2: "🔍 The Gap" (CENTERPIECE)
- **Scatter plot with OLS trendline**: Quantifies the correlation between housing instability and chronic absenteeism
- **Interactive**: Hover over points to see school names and details
- **Filter**: Excludes schools with <20 students (statistical outliers)

### Tab 3: "👥 The Invisible Majority"
- **Stacked bar chart**: Breaks down housing types (Doubled Up, DHS Shelter, Non-DHS Shelter) by borough
- **Top 20 table**: Schools with highest percentage of students in temporary housing
- **Call to Action**: 3 policy recommendations backed by research

---

## 📊 Data Sources

All data from **NYC Open Data** (2020-21 school year):

- **Students in Temporary Housing**: Dataset ID `3wtp-43m9`
  - https://data.cityofnewyork.us/Education/2021-Students-in-Temporary-Housing/3wtp-43m9
- **School Attendance**: Dataset ID `gqq2-hgxd`
  - https://data.cityofnewyork.us/Education/School-End-of-Year-Attendance/gqq2-hgxd

### Data Processing
1. **Fetch**: `data/fetch_data.py` pulls data from NYC Open Data Socrata API
2. **Clean**: `data/clean_data.py` merges datasets, handles percentage formats, derives borough from DBN
3. **Load**: `app.py` loads the final `merged.csv` (1,454 schools)

### Key Definitions
- **Chronically absent**: Missing ≥10% of enrolled school days
- **Doubled up**: Students living with others due to economic hardship (not in shelters)
- **Temporary housing**: Includes doubled-up, DHS shelters, and non-DHS shelters

---

## 🛠️ Technical Details

### Dependencies
- **streamlit**: Web app framework
- **pandas**: Data manipulation
- **plotly**: Interactive visualizations
- **requests**: API data fetching
- **statsmodels**: OLS trendline calculation

### Data Pipeline
```
NYC Open Data API
    ↓ (fetch_data.py with $limit=5000)
housing.csv (1,689 rows) + attendance.csv (1,530 rows)
    ↓ (clean_data.py: merge, clean, filter)
merged.csv (1,454 schools, 22 columns)
    ↓ (app.py with @st.cache_data)
Interactive Dashboard (3 tabs, 3 visualizations)
```

### Performance
- **Cold start**: <5 seconds
- **Data caching**: Single load with `@st.cache_data`
- **No live API calls**: All data served from local CSV files

---

## 🎯 Key Findings

1. **Scale**: 87,000+ students affected citywide (1 in 12)
2. **Correlation**: Clear positive relationship between housing instability and chronic absenteeism
3. **Hidden Reality**: 2/3 of homeless students are "doubled up" — invisible in shelter databases
4. **Geographic Disparity**: Bronx has highest concentration; Staten Island has lowest

---

## 💡 Recommended Actions

Based on the data analysis:

1. **Better identification systems**: Schools need tools to identify doubled-up students who don't appear in shelter databases
2. **Targeted resources**: Deploy social workers to high-impact schools (research shows ~1.2 percentage point attendance improvement)
3. **Data transparency**: Regular public reporting on housing status and attendance outcomes

---

## ⚠️ Important Note

This dashboard uses **2020-21 school year data**, which was significantly impacted by:
- COVID-19 pandemic
- Remote and hybrid learning models
- Unprecedented disruptions to normal school operations

While the correlation between housing instability and absenteeism remains valid, absolute rates may not reflect typical years.

---

## 🔧 Development

### Regenerate Data (Optional)

If you want to fetch fresh data from NYC Open Data:

```bash
# Fetch latest data
python data/fetch_data.py

# Clean and merge
python data/clean_data.py
```

**Note**: This will overwrite existing CSV files. The current data is from 2020-21 (latest available with complete housing data).

### Project Stats
- **Total Code**: 576 lines (app 133 + fetch 86 + clean 224 + tests 133)
- **Data Processing**: 1,689 → 1,530 → 1,454 rows (clean pipeline)
- **Development Time**: ~2-3 hours (hackathon sprint)
- **Verification**: 4-stage QA process (compliance, quality, manual, fidelity)

---

## 📝 License

Created for educational purposes as part of the Baruch College Civic Tech & Data Hackathon.

Data sourced from NYC Open Data (public domain).

---

## 🙏 Acknowledgments

- **NYC Open Data**: For providing comprehensive, accessible public datasets
- **Baruch College**: For hosting the Civic Tech & Data Hackathon
- **Advocates for Children of New York**: For ongoing research and advocacy on student homelessness
- **NYU Steinhardt**: For research on social worker interventions and attendance outcomes

---

## 📧 Questions?

This dashboard was built as a hackathon project to demonstrate:
- Data storytelling with public datasets
- Correlation analysis with OLS regression
- Policy-relevant insights from civic data
- Accessible visualization for non-technical audiences

For more information about student homelessness in NYC, visit [Advocates for Children of New York](https://www.advocatesforchildren.org/).

---

**Built with ❤️ for NYC students experiencing homelessness**
