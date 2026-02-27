# The Absenteeism Gap: How Homelessness Steals School Days in NYC

## TL;DR

> **Quick Summary**: Build a Streamlit dashboard that tells the data story of how student homelessness correlates with chronic absenteeism across NYC schools, using 2020-21 school-level data from NYC Open Data.
> 
> **Deliverables**:
> - `app.py` — Streamlit dashboard with 3 tabs (Scale → Gap → Invisible Majority)
> - `data/fetch_data.py` — Standalone data acquisition script
> - `data/merged.csv` — Cleaned, joined dataset ready for visualization
> - 4-5 interactive Plotly visualizations (bar chart, scatter+trendline, stacked bar, top-20 table, optional map)
> - `requirements.txt` — Reproducible environment
> 
> **Estimated Effort**: Medium (4-5 hours of active coding within 6-hour hackathon)
> **Parallel Execution**: YES — 4 waves
> **Critical Path**: Task 1 → Task 2 → Task 3 → Task 4 → Task 5/6/7 (parallel) → Task 9

---

## Context

### Original Request
Build a data-driven project for the Baruch College Civic Tech & Data Hackathon (Feb 27, 10am-4pm) using NYC Open Data. The team chose to explore how student homelessness affects school attendance — "The Absenteeism Gap."

### Interview Summary
**Key Discussions**:
- **Problem angle**: "The Absenteeism Gap" — scatter plot showing correlation between % students in temporary housing and % chronically absent, supported by borough-level and shelter-type breakdowns
- **Tech stack**: Python + Streamlit + Plotly + pandas (team decision)
- **Team size**: 2-3 people, can split data pipeline and visualization work
- **Data story structure**: 3-act narrative (Scale → Gap → Invisible Majority) using `st.tabs()`
- **Primary datasets**: Housing (3wtp-43m9) + Attendance (gqq2-hgxd), joined on DBN
- **Stretch goals**: Demographics dataset (c7ru-d68s) and borough map visualization

**Research Findings**:
- All datasets verified via Socrata API — schemas confirmed, column names mapped
- Housing dataset: 1,689 schools, 9 columns. 98 schools have suppressed ("s") values (~5.8%)
- Attendance dataset (filtered): ~1,530 schools, 0 suppressed values in chronic absenteeism
- **CRITICAL**: Socrata API default limit is 1,000 rows — housing dataset has 1,689. Must use `$limit=5000` or silently lose 40% of data
- **CRITICAL**: Percentage columns have inconsistent formats — housing uses "30.7%" (with %), attendance uses "42.2" (without %). Need universal `clean_pct()` helper
- `plotly.express.scatter(trendline="ols")` requires `statsmodels` as a silent dependency
- Borough derivable from `dbn[2]` character: M=Manhattan, X=Bronx, K=Brooklyn, Q=Queens, R=Staten Island. District 75/79 schools → "Citywide"
- ~87,000 students in temporary housing in 2020-21; ~2/3 are "doubled up" (not in shelters)
- 2020-21 was impacted by COVID-19 — need disclaimer in dashboard

### Metis Review
**Identified Gaps** (all addressed in plan):
- API rate limiting / downtime risk → App loads from local CSV, not live API
- Socrata 1,000-row default limit → All API calls use `$limit=5000`
- `statsmodels` missing from deps → Added to requirements.txt
- District 75/79 borough mapping → "Citywide" category added
- COVID-19 data disclaimer → `st.info()` banner in app
- "Chronically absent" undefined → Definition in narrative text (≥10% of enrolled days)
- Zero/tiny enrollment outliers → Filter `total_students >= 20`
- Map complexity risk → Map is cut FIRST if time is tight (stretch goal only)

---

## Work Objectives

### Core Objective
Build a 3-tab Streamlit dashboard that quantifies and visualizes the relationship between student homelessness and chronic absenteeism across ~1,400+ NYC schools, delivering an actionable data story for the hackathon presentation.

### Concrete Deliverables
- `requirements.txt` with all dependencies
- `data/fetch_data.py` — standalone data acquisition script (runs once, saves CSVs)
- `data/housing.csv`, `data/attendance.csv`, `data/merged.csv`
- `app.py` — Streamlit app with 3 tabs and 4+ Plotly visualizations
- Presentation-ready narrative text integrated into the dashboard

### Definition of Done
- [x] `streamlit run app.py --server.headless true` launches without errors
- [x] `data/merged.csv` has >1,300 rows with no "s" values in numeric columns
- [x] All 3 tabs render with visualizations and narrative text
- [x] Scatter plot shows visible OLS trendline with R² annotation
- [x] Dashboard cold-starts in under 5 seconds on local machine

### Must Have
- Local CSV data files (app never calls live API)
- `$limit=5000` on all Socrata API calls in fetch script
- Universal `clean_pct()` helper handling both "30.7%" and "42.2" formats
- Borough derived from `dbn[2]` with "Citywide" fallback for District 75/79
- COVID-19 disclaimer (`st.info()`)
- Definition of "chronically absent" in narrative text
- `total_students >= 20` filter on scatter plot
- `@st.cache_data` on data loading function
- `st.set_page_config(layout="wide", page_title="The Absenteeism Gap")` as first call

### Must NOT Have (Guardrails)
- ❌ Live API calls in app.py (only in fetch_data.py)
- ❌ `sodapy` dependency (use `requests.get()` directly)
- ❌ Interactive filters (year picker, grade selector, etc.)
- ❌ Custom CSS or theming beyond `st.set_page_config`
- ❌ Authentication, database, or cloud deployment
- ❌ More than 5 visualizations total
- ❌ `scipy` direct imports (let plotly handle OLS internally)
- ❌ Demographics dataset before core 4 charts work
- ❌ Map visualization before core 4 charts work
- ❌ Download/export buttons
- ❌ `as any`, `@ts-ignore`, empty catches, or commented-out code equivalents in Python (bare `except:`, `pass` in except blocks, commented-out code)

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO (greenfield hackathon project)
- **Automated tests**: None (hackathon time constraint — QA via agent-executed scenarios)
- **Framework**: None
- **QA is primary verification**: Every task has Playwright or Bash-based QA scenarios

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Data pipeline**: Use Bash (python -c) — Import CSV, assert shape/types/no-suppressed-values
- **Streamlit UI**: Use Playwright (playwright skill) — Navigate, click tabs, verify charts render, screenshot
- **Script execution**: Use Bash — Run script, verify output files exist with correct content

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — setup + data):
├── Task 1: Project scaffolding + requirements.txt [quick]
├── Task 2: Data acquisition script (fetch_data.py) [quick]

Wave 2 (After Wave 1 — data cleaning + app skeleton):
├── Task 3: Data cleaning & merge pipeline [unspecified-high]
├── Task 4: App.py skeleton (page config, tabs, caching, narrative) [quick]

Wave 3 (After Wave 2 — visualizations, PARALLEL):
├── Task 5: Tab 1 — "The Scale" (borough bar chart) [quick]
├── Task 6: Tab 2 — "The Gap" (scatter plot + trendline) [unspecified-high]
├── Task 7: Tab 3 — "The Invisible Majority" (stacked bar + table) [unspecified-high]

Wave 4 (After Wave 3 — stretch goals, PARALLEL):
├── Task 8: Borough map visualization (STRETCH — skip if behind) [visual-engineering]
├── Task 9: Final polish + presentation narrative [quick]

Wave FINAL (After ALL — verification):
├── Task F1: Plan compliance audit [oracle]
├── Task F2: Code quality review [unspecified-high]
├── Task F3: Real QA — full dashboard walkthrough [unspecified-high]
├── Task F4: Scope fidelity check [deep]

Critical Path: Task 1 → Task 2 → Task 3 → Task 4 → Task 6 → Task 9 → F1-F4
Parallel Speedup: ~40% faster than sequential (Wave 3 is the big win)
Max Concurrent: 3 (Wave 3)
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|-----------|--------|------|
| 1 | — | 2, 3, 4 | 1 |
| 2 | 1 | 3 | 1 |
| 3 | 2 | 5, 6, 7, 8 | 2 |
| 4 | 1 | 5, 6, 7 | 2 |
| 5 | 3, 4 | 9 | 3 |
| 6 | 3, 4 | 9 | 3 |
| 7 | 3, 4 | 9 | 3 |
| 8 | 3, 4 | 9 | 4 |
| 9 | 5, 6, 7 | F1-F4 | 4 |
| F1-F4 | 9 | — | FINAL |

### Agent Dispatch Summary

- **Wave 1**: 2 tasks — T1 → `quick`, T2 → `quick`
- **Wave 2**: 2 tasks — T3 → `unspecified-high`, T4 → `quick`
- **Wave 3**: 3 tasks — T5 → `quick`, T6 → `unspecified-high`, T7 → `unspecified-high`
- **Wave 4**: 2 tasks — T8 → `visual-engineering`, T9 → `quick`
- **FINAL**: 4 tasks — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

---

## TODOs

- [x] 1. Project Scaffolding + Requirements

  **What to do**:
  - Create project directory structure: `data/` directory
  - Create `requirements.txt` with exact dependencies:
    ```
    streamlit
    pandas
    plotly
    requests
    statsmodels
    ```
  - Create Python virtual environment and install dependencies: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
  - Verify all imports work: `python -c "import streamlit, pandas, plotly, requests, statsmodels; print('All imports OK')"`

  **Must NOT do**:
  - Do NOT install `sodapy` — use `requests.get()` directly
  - Do NOT install `folium` or `streamlit-folium` yet (stretch goal only)
  - Do NOT create app.py yet (Task 4)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple file creation + pip install, no complex logic
  - **Skills**: `[]`
    - No special skills needed for scaffolding

  **Parallelization**:
  - **Can Run In Parallel**: YES (with nothing — it's the first task)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 2, 3, 4
  - **Blocked By**: None (can start immediately)

  **References**:

  **External References**:
  - Streamlit docs: https://docs.streamlit.io/get-started/installation — for `st.set_page_config` as first call pattern
  - Plotly OLS trendline requires statsmodels: https://plotly.com/python/linear-fits/ — "You need to install statsmodels for this"

  **Acceptance Criteria**:
  - [x] `data/` directory exists
  - [x] `requirements.txt` exists with exactly: streamlit, pandas, plotly, requests, statsmodels
  - [x] `pip install -r requirements.txt` completes without error
  - [x] `python -c "import streamlit, pandas, plotly.express, requests, statsmodels; print('OK')"` prints "OK"

  **QA Scenarios:**

  ```
  Scenario: All dependencies install and import correctly
    Tool: Bash
    Preconditions: Clean virtual environment activated
    Steps:
      1. Run: pip install -r requirements.txt
      2. Run: python -c "import streamlit; import pandas; import plotly.express; import requests; import statsmodels; print('ALL_IMPORTS_OK')"
      3. Assert stdout contains "ALL_IMPORTS_OK"
    Expected Result: All packages install without error, all imports succeed
    Failure Indicators: pip error, ImportError, ModuleNotFoundError
    Evidence: .sisyphus/evidence/task-1-deps-install.txt

  Scenario: Directory structure is correct
    Tool: Bash
    Preconditions: Task 1 complete
    Steps:
      1. Run: ls -la data/
      2. Run: cat requirements.txt
      3. Assert data/ directory exists
      4. Assert requirements.txt contains "streamlit", "pandas", "plotly", "requests", "statsmodels"
    Expected Result: Directory exists, requirements.txt has all 5 packages
    Failure Indicators: "No such file or directory", missing package in requirements.txt
    Evidence: .sisyphus/evidence/task-1-structure.txt
  ```

  **Commit**: YES
  - Message: `chore: project scaffolding and requirements`
  - Files: `requirements.txt`, `data/` directory
  - Pre-commit: `pip install -r requirements.txt && python -c "import streamlit, pandas, plotly, requests, statsmodels"`

---

- [x] 2. Data Acquisition Script (fetch_data.py)

  **What to do**:
  - Create `data/fetch_data.py` — a standalone script that fetches data from NYC Open Data Socrata API and saves as local CSV files
  - **CRITICAL**: ALL API calls MUST use `$limit=5000` parameter. The housing dataset has 1,689 rows but Socrata defaults to 1,000. Without this, you silently lose 40% of data.
  - Fetch Housing data:
    ```python
    url = "https://data.cityofnewyork.us/resource/3wtp-43m9.json?$limit=5000"
    response = requests.get(url)
    housing_df = pd.DataFrame(response.json())
    housing_df.to_csv("data/housing.csv", index=False)
    ```
  - Fetch Attendance data (with server-side filter):
    ```python
    url = "https://data.cityofnewyork.us/resource/gqq2-hgxd.json"
    params = {
        "$limit": 5000,
        "$where": "year='2020-21' AND grade='All Grades' AND category='All Students'"
    }
    response = requests.get(url, params=params)
    attendance_df = pd.DataFrame(response.json())
    attendance_df.to_csv("data/attendance.csv", index=False)
    ```
  - Print row counts after each fetch to verify: `print(f"Housing: {len(housing_df)} rows")` — expect ~1,689. `print(f"Attendance: {len(attendance_df)} rows")` — expect ~1,530.
  - Script should be idempotent (safe to re-run)

  **Must NOT do**:
  - Do NOT install or use `sodapy` — plain `requests.get()` is simpler
  - Do NOT do any data cleaning in this script — just raw fetch and save
  - Do NOT call the API from app.py — this script runs ONCE during development
  - Do NOT forget `$limit=5000` — this is the single most dangerous silent bug

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Straightforward HTTP requests + CSV save, well-defined API endpoints
  - **Skills**: `[]`
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO (needs requirements from Task 1)
  - **Parallel Group**: Wave 1 (sequential after Task 1)
  - **Blocks**: Task 3
  - **Blocked By**: Task 1

  **References**:

  **API References** (exact endpoints to call):
  - Housing: `https://data.cityofnewyork.us/resource/3wtp-43m9.json?$limit=5000`
  - Attendance: `https://data.cityofnewyork.us/resource/gqq2-hgxd.json?$limit=5000&$where=year='2020-21' AND grade='All Grades' AND category='All Students'`
  - Socrata API docs: https://dev.socrata.com/docs/queries/ — for `$where` and `$limit` syntax

  **Column Names** (verified from live API — use these EXACTLY):
  - Housing columns: `dbn`, `school_name`, `total_students`, `students_in_temporary_housing`, `students_in_temporary_housing_1` (pct, has % sign), `students_residing_in_shelter`, `residing_in_dhs_shelter`, `residing_in_non_dhs_shelter`, `doubled_up`
  - Attendance columns: `dbn`, `school_name`, `grade`, `category`, `year`, `total_days`, `days_absent`, `days_present`, `attendance`, `contributing_10_total_days`, `chronically_absent`, `chronically_absent_1` (pct, NO % sign)

  **Acceptance Criteria**:
  - [x] `data/fetch_data.py` exists and runs without error: `python data/fetch_data.py`
  - [x] `data/housing.csv` exists with ~1,689 rows (NOT 1,000 — verify limit worked)
  - [x] `data/attendance.csv` exists with ~1,530 rows, all year=2020-21
  - [x] Script uses `$limit=5000` on ALL API calls
  - [x] Script does NOT use `sodapy`

  **QA Scenarios:**

  ```
  Scenario: Housing data fetched completely (not truncated)
    Tool: Bash
    Preconditions: requirements installed, internet available
    Steps:
      1. Run: python data/fetch_data.py
      2. Run: python -c "import pandas as pd; df=pd.read_csv('data/housing.csv'); print(f'ROWS:{len(df)}'); assert len(df) > 1600, f'Only {len(df)} rows — $limit missing!'"
      3. Assert row count > 1600 (expect ~1,689)
    Expected Result: housing.csv has ~1,689 rows
    Failure Indicators: Row count = 1,000 (Socrata default limit hit), HTTP error, empty file
    Evidence: .sisyphus/evidence/task-2-housing-fetch.txt

  Scenario: Attendance data fetched with correct filters
    Tool: Bash
    Preconditions: fetch_data.py has run
    Steps:
      1. Run: python -c "import pandas as pd; df=pd.read_csv('data/attendance.csv'); print(f'ROWS:{len(df)}'); print(f'YEARS:{df['year'].unique()}'); assert len(df) > 1400; assert (df['year']=='2020-21').all()"
      2. Assert all rows have year=2020-21
      3. Assert row count > 1400 (expect ~1,530)
    Expected Result: attendance.csv has ~1,530 rows, all 2020-21
    Failure Indicators: Multiple years present, row count = 1,000, wrong filter
    Evidence: .sisyphus/evidence/task-2-attendance-fetch.txt

  Scenario: No sodapy dependency used
    Tool: Bash
    Preconditions: fetch_data.py exists
    Steps:
      1. Run: grep -c "sodapy" data/fetch_data.py || echo "NOT_FOUND"
      2. Assert output is "NOT_FOUND" or "0"
    Expected Result: sodapy not referenced anywhere
    Failure Indicators: grep returns >0 matches
    Evidence: .sisyphus/evidence/task-2-no-sodapy.txt
  ```

  **Commit**: YES (group with Task 1)
  - Message: `feat(data): add data acquisition script for NYC Open Data`
  - Files: `requirements.txt`, `data/fetch_data.py`, `data/housing.csv`, `data/attendance.csv`
  - Pre-commit: `python data/fetch_data.py && python -c "import pandas as pd; assert len(pd.read_csv('data/housing.csv'))>1600"`

---

- [x] 3. Data Cleaning and Merge Pipeline

  **What to do**:
  - Add cleaning and merge logic to `data/fetch_data.py` (after the fetch section) OR create a separate `data/clean_data.py` — either is fine, but output MUST be `data/merged.csv`
  - **Create universal `clean_pct()` helper** — this is critical because formats differ between datasets:
    ```python
    import numpy as np
    def clean_pct(val):
        if pd.isna(val) or str(val).strip().lower() == 's':
            return np.nan
        val_str = str(val).strip().replace('%', '')
        try:
            return float(val_str)
        except ValueError:
            return np.nan
    ```
  - Apply `clean_pct()` to ALL percentage/numeric columns:
    - Housing: `total_students`, `students_in_temporary_housing`, `students_in_temporary_housing_1`, `students_residing_in_shelter`, `residing_in_dhs_shelter`, `residing_in_non_dhs_shelter`, `doubled_up`
    - Attendance: `chronically_absent_1`, `attendance`, `total_days`, `days_absent`, `days_present`, `chronically_absent`, `contributing_10_total_days`
  - **Derive borough** from DBN:
    ```python
    BOROUGH_MAP = {'M': 'Manhattan', 'X': 'Bronx', 'K': 'Brooklyn', 'Q': 'Queens', 'R': 'Staten Island'}
    df['borough'] = df['dbn'].str[2].map(BOROUGH_MAP).fillna('Citywide')
    ```
  - **Inner join** on `dbn`:
    ```python
    merged = housing.merge(attendance, on='dbn', suffixes=('_housing', '_attendance'))
    ```
  - **Drop rows** where key columns are NaN (from suppressed "s" values)
  - **Rename columns** for clarity: `students_in_temporary_housing` → `n_students_temp_housing`, `students_in_temporary_housing_1` → `pct_students_temp_housing`, `chronically_absent_1` → `pct_chronically_absent`, `total_students` → `total_enrollment`
  - Keep: `dbn`, `school_name` (from housing), `borough`, `total_enrollment`, `n_students_temp_housing`, `pct_students_temp_housing`, `pct_chronically_absent`, `doubled_up`, `students_residing_in_shelter`, `residing_in_dhs_shelter`, `residing_in_non_dhs_shelter`, `pct_attendance`
  - Save as `data/merged.csv`
  - Print summary stats: row count, column list, borough distribution, NaN counts

  **Must NOT do**:
  - Do NOT skip the `clean_pct()` helper — hardcoding format assumptions WILL break
  - Do NOT use `pd.to_numeric()` alone — it won't handle the "%" character
  - Do NOT leave "s" values in the merged output — they must become NaN and be dropped
  - Do NOT use left/right/outer join — inner join only

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Data cleaning logic requires careful handling of edge cases
  - **Skills**: `[]`
    - No special skills needed — pure pandas work

  **Parallelization**:
  - **Can Run In Parallel**: YES (parallel with Task 4)
  - **Parallel Group**: Wave 2 (with Task 4)
  - **Blocks**: Tasks 5, 6, 7, 8
  - **Blocked By**: Task 2 (needs raw CSV files)

  **References**:

  **Data Format References** (verified from live API):
  - Housing `students_in_temporary_housing_1`: `"30.7%"` (string WITH % sign)
  - Attendance `chronically_absent_1`: `"42.2"` (string WITHOUT % sign)
  - Housing `students_in_temporary_housing`: `"s"` for suppressed values (98 schools, ~5.8%)
  - Attendance: 0 suppressed values in filtered dataset
  - Borough codes in `dbn[2]`: M=Manhattan, X=Bronx, K=Brooklyn, Q=Queens, R=Staten Island
  - District 75/79 schools: `dbn[2]` may not match standard borough codes → map to "Citywide"

  **Acceptance Criteria**:
  - [x] `data/merged.csv` exists
  - [x] Row count > 1,300 (inner join minus suppressed values)
  - [x] No "s" values in any numeric column
  - [x] `borough` column has values from: Manhattan, Bronx, Brooklyn, Queens, Staten Island, Citywide
  - [x] `pct_students_temp_housing` and `pct_chronically_absent` are float dtype
  - [x] `clean_pct()` function exists and handles both "30.7%" and "42.2" formats

  **QA Scenarios:**

  ```
  Scenario: Merged dataset has correct shape and types
    Tool: Bash
    Preconditions: data/housing.csv and data/attendance.csv exist from Task 2
    Steps:
      1. Run the cleaning script
      2. Run: python -c "import pandas as pd; df=pd.read_csv('data/merged.csv'); print(f'ROWS:{len(df)}'); print(f'DTYPES:{df.dtypes.to_dict()}'); assert len(df)>1300; assert df['pct_students_temp_housing'].dtype=='float64'; assert df['pct_chronically_absent'].dtype=='float64'; print('SHAPE_OK')"
      3. Assert stdout contains "SHAPE_OK" and ROWS > 1300
    Expected Result: >1,300 rows, float dtypes for percentage columns
    Failure Indicators: Low row count, object dtype (strings not converted), missing columns
    Evidence: .sisyphus/evidence/task-3-merged-shape.txt

  Scenario: No suppressed values or percent signs leaked into output
    Tool: Bash
    Preconditions: data/merged.csv exists
    Steps:
      1. Run: python -c "import pandas as pd; df=pd.read_csv('data/merged.csv'); [exec(\"assert 's' not in df[c].astype(str).values and '%' not in df[c].astype(str).str.cat()\") for c in ['pct_students_temp_housing','pct_chronically_absent','n_students_temp_housing','total_enrollment']]; print('CLEAN_OK')"
      2. Assert stdout contains "CLEAN_OK"
    Expected Result: Zero "s" values, zero "%" characters in numeric columns
    Failure Indicators: AssertionError
    Evidence: .sisyphus/evidence/task-3-no-suppressed.txt
  ```

  **Commit**: YES
  - Message: `feat(data): clean and merge housing + attendance datasets`
  - Files: `data/fetch_data.py` (or `data/clean_data.py`), `data/merged.csv`
  - Pre-commit: `python -c "import pandas as pd; df=pd.read_csv('data/merged.csv'); assert len(df)>1300"`

---

- [x] 4. App.py Skeleton (Page Config, Tabs, Caching, Narrative Structure)

  **What to do**:
  - Create `app.py` with the full Streamlit skeleton:
    ```python
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import numpy as np
    
    st.set_page_config(layout="wide", page_title="The Absenteeism Gap")  # MUST be first st call
    
    @st.cache_data
    def load_data():
        return pd.read_csv("data/merged.csv")
    
    df = load_data()
    
    # Title and introduction
    st.title("The Absenteeism Gap")
    st.subheader("How Homelessness Steals School Days in NYC")
    st.info("\u26a0\ufe0f Data from the 2020-21 school year, which was significantly impacted by COVID-19 and remote/hybrid learning.")
    st.markdown("""
    In 2020-21, approximately **87,000 NYC students** lived in temporary housing \u2014 that's roughly 1 in 12.
    This dashboard explores how housing instability correlates with chronic absenteeism across ~1,400 NYC schools.
    
    **Chronically absent** means missing \u226510% of enrolled school days.
    """)
    
    tab1, tab2, tab3 = st.tabs(["\ud83d\udcca The Scale", "\ud83d\udd0d The Gap", "\ud83d\udc65 The Invisible Majority"])
    
    with tab1:
        st.header("The Scale of Student Homelessness")
        # Tab 1 content added by Task 5
        st.markdown("_Visualization loading..._")
    
    with tab2:
        st.header("The Absenteeism Gap")
        # Tab 2 content added by Task 6
        st.markdown("_Visualization loading..._")
    
    with tab3:
        st.header("The Invisible Majority")
        # Tab 3 content added by Task 7
        st.markdown("_Visualization loading..._")
    ```
  - The app must load and render with placeholder text in each tab
  - All subsequent tasks (5, 6, 7) will REPLACE the placeholder content in each tab

  **Must NOT do**:
  - Do NOT call any live API — only `pd.read_csv("data/merged.csv")`
  - Do NOT add interactive filters (`st.selectbox`, `st.slider`, etc.)
  - Do NOT add custom CSS or theming
  - Do NOT create visualizations yet — just the skeleton with placeholders

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Boilerplate Streamlit app structure, well-defined template
  - **Skills**: `[]`
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES (parallel with Task 3)
  - **Parallel Group**: Wave 2 (with Task 3)
  - **Blocks**: Tasks 5, 6, 7
  - **Blocked By**: Task 1 (needs streamlit installed)

  **References**:

  **External References**:
  - Streamlit tabs: https://docs.streamlit.io/develop/api-reference/layout/st.tabs
  - `st.cache_data`: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_data
  - `st.set_page_config`: https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config — MUST be first Streamlit command

  **Acceptance Criteria**:
  - [x] `app.py` exists in project root
  - [x] `st.set_page_config()` is the FIRST Streamlit call
  - [x] `@st.cache_data` decorates `load_data()` function
  - [x] 3 tabs created with correct labels
  - [x] COVID-19 disclaimer present as `st.info()`
  - [x] "Chronically absent" defined in intro text
  - [x] App loads from `data/merged.csv`, not from any API
  - [x] `streamlit run app.py --server.headless true` launches without error

  **QA Scenarios:**

  ```
  Scenario: App launches and shows 3 tabs
    Tool: Playwright (playwright skill)
    Preconditions: data/merged.csv exists, streamlit running
    Steps:
      1. Start: streamlit run app.py --server.headless true
      2. Navigate to http://localhost:8501
      3. Assert page title contains "The Absenteeism Gap"
      4. Assert 3 tab elements are visible with text: "The Scale", "The Gap", "The Invisible Majority"
      5. Assert COVID-19 info banner is visible (st.info element)
      6. Assert text "Chronically absent" appears on page
      7. Screenshot the page
    Expected Result: App renders with title, 3 tabs, COVID disclaimer, and definition
    Failure Indicators: Streamlit error, missing tabs, missing disclaimer
    Evidence: .sisyphus/evidence/task-4-app-skeleton.png

  Scenario: App does not call any external API
    Tool: Bash
    Preconditions: app.py exists
    Steps:
      1. Run: grep -c "requests.get\|urllib\|http" app.py || echo "0"
      2. Assert output is "0" — no HTTP calls in app.py
    Expected Result: Zero HTTP/API calls in app.py
    Failure Indicators: grep matches found
    Evidence: .sisyphus/evidence/task-4-no-api.txt
  ```

  **Commit**: NO (will commit with Task 5/6/7)

---

- [x] 5. Tab 1 — "The Scale" (Borough Bar Chart + Narrative)

  **What to do**:
  - In `app.py`, replace the Tab 1 placeholder content with:
  - **Borough bar chart**: Aggregate students in temporary housing by borough
    ```python
    with tab1:
        st.header("The Scale of Student Homelessness")
        st.markdown("""
        NYC's student homelessness crisis is not evenly distributed. The Bronx bears
        a disproportionate share, while Staten Island has the fewest affected students.
        """)
        
        borough_data = df.groupby('borough').agg(
            total_temp_housing=('n_students_temp_housing', 'sum'),
            total_schools=('dbn', 'count'),
            avg_pct=('pct_students_temp_housing', 'mean')
        ).reset_index().sort_values('total_temp_housing', ascending=False)
        
        fig = px.bar(
            borough_data,
            x='borough', y='total_temp_housing',
            color='borough',
            title='Students in Temporary Housing by Borough (2020-21)',
            labels={'total_temp_housing': 'Total Students', 'borough': 'Borough'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Schools", f"{len(df):,}")
        col2.metric("Total Students in Temp Housing", f"{int(df['n_students_temp_housing'].sum()):,}")
        col3.metric("Citywide Average", f"{df['pct_students_temp_housing'].mean():.1f}%")
    ```
  - Add 2-3 sentences of narrative context between the chart and metrics
  - The narrative should reference specific numbers from the data (not hardcoded — compute from `df`)

  **Must NOT do**:
  - Do NOT add filters or interactivity
  - Do NOT modify Tab 2 or Tab 3 content
  - Do NOT hardcode numbers in narrative text — compute from dataframe

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single plotly bar chart with straightforward groupby
  - **Skills**: `[]`
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES (parallel with Tasks 6, 7)
  - **Parallel Group**: Wave 3 (with Tasks 6, 7)
  - **Blocks**: Task 9
  - **Blocked By**: Tasks 3, 4 (needs merged.csv and app skeleton)

  **References**:

  **Data References**:
  - `data/merged.csv` columns: `borough`, `n_students_temp_housing`, `pct_students_temp_housing`, `dbn`
  - Borough values: Manhattan, Bronx, Brooklyn, Queens, Staten Island, Citywide
  - Bronx expected to have highest total (from research findings)

  **External References**:
  - `plotly.express.bar`: https://plotly.com/python/bar-charts/
  - `st.columns` + `st.metric`: https://docs.streamlit.io/develop/api-reference/layout/st.columns

  **Acceptance Criteria**:
  - [x] Tab 1 shows a Plotly bar chart with 5-6 bars (one per borough)
  - [x] Chart title includes "Borough" and "2020-21"
  - [x] 3 metric cards below the chart (total schools, total students, citywide average)
  - [x] Narrative text present between/around visualizations
  - [x] No hardcoded numbers in narrative — all computed from df

  **QA Scenarios:**

  ```
  Scenario: Borough bar chart renders with correct data
    Tool: Playwright (playwright skill)
    Preconditions: streamlit running with complete data
    Steps:
      1. Navigate to http://localhost:8501
      2. Click the "The Scale" tab
      3. Assert a Plotly chart container exists (`.js-plotly-plot` selector)
      4. Assert the chart has bars (plotly bar trace)
      5. Assert 3 metric elements are visible (st.metric components)
      6. Assert text contains "Bronx" (highest borough)
      7. Screenshot the tab
    Expected Result: Bar chart with 5-6 borough bars, 3 metrics below, narrative text
    Failure Indicators: Empty tab, missing chart, zero metrics
    Evidence: .sisyphus/evidence/task-5-tab1-scale.png

  Scenario: Tab 1 data is computed not hardcoded
    Tool: Bash
    Preconditions: app.py exists
    Steps:
      1. Run: grep -c "87,000\|87000\|1,689" app.py || echo "0"
      2. Assert zero hardcoded aggregate numbers (individual context stats in intro are OK)
    Expected Result: Metric values computed from df, not hardcoded
    Failure Indicators: Hardcoded totals found in Tab 1 section
    Evidence: .sisyphus/evidence/task-5-no-hardcode.txt
  ```

  **Commit**: NO (groups with Tasks 6, 7)

---

- [x] 6. Tab 2 — "The Gap" (Scatter Plot + OLS Trendline) — CENTERPIECE

  **What to do**:
  - In `app.py`, replace the Tab 2 placeholder content with the KEY visualization:
  - **Filter**: Only schools with `total_enrollment >= 20` (removes outlier tiny schools)
  - **Scatter plot**: X = `pct_students_temp_housing`, Y = `pct_chronically_absent`
    ```python
    with tab2:
        st.header("The Absenteeism Gap")
        st.markdown("""
        Each dot represents one NYC school. Schools with more students in temporary
        housing tend to have higher rates of chronic absenteeism. The trendline
        quantifies this relationship.
        """)
        
        scatter_df = df[df['total_enrollment'] >= 20].copy()
        
        fig = px.scatter(
            scatter_df,
            x='pct_students_temp_housing',
            y='pct_chronically_absent',
            color='borough',
            size='total_enrollment',
            hover_data=['school_name_housing', 'dbn'],
            trendline='ols',
            title='Housing Instability vs Chronic Absenteeism (2020-21)',
            labels={
                'pct_students_temp_housing': '% Students in Temporary Housing',
                'pct_chronically_absent': '% Chronically Absent'
            },
            opacity=0.6
        )
        st.plotly_chart(fig, use_container_width=True)
    ```
  - **CRITICAL**: `trendline='ols'` requires `statsmodels` to be installed (Task 1 ensures this)
  - Add narrative interpreting the trendline: what the slope means in plain language
  - Highlight outlier schools:
    - High housing instability + LOW absenteeism = "resilient schools — what are they doing right?"
    - High housing instability + HIGH absenteeism = "schools most in need of support"
  - Consider adding `st.markdown()` below the chart identifying 3-5 notable outlier schools by name

  **Must NOT do**:
  - Do NOT import scipy or statsmodels directly — let plotly handle OLS internally
  - Do NOT remove the enrollment filter (`>= 20`) — tiny schools create extreme outliers
  - Do NOT add interactive filters
  - Do NOT modify Tab 1 or Tab 3 content

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: This is the centerpiece visualization — needs careful axis labels, trendline interpretation, outlier identification, and narrative
  - **Skills**: `[]`
    - No special skills needed beyond plotly

  **Parallelization**:
  - **Can Run In Parallel**: YES (parallel with Tasks 5, 7)
  - **Parallel Group**: Wave 3 (with Tasks 5, 7)
  - **Blocks**: Task 9
  - **Blocked By**: Tasks 3, 4 (needs merged.csv and app skeleton)

  **References**:

  **Data References**:
  - `data/merged.csv` columns: `pct_students_temp_housing`, `pct_chronically_absent`, `borough`, `total_enrollment`, `school_name_housing` (or `school_name` depending on merge suffix), `dbn`
  - Filter: `total_enrollment >= 20` to exclude tiny schools
  - Expected: positive correlation (higher housing instability → higher absenteeism)

  **External References**:
  - Plotly scatter with OLS: https://plotly.com/python/linear-fits/ — `px.scatter(trendline='ols')`
  - NOTE: `trendline='ols'` shows R² on hover automatically. Requires `statsmodels` installed.

  **Acceptance Criteria**:
  - [x] Tab 2 shows a Plotly scatter plot
  - [x] Points colored by borough
  - [x] Points sized by enrollment
  - [x] OLS trendline visible on the chart
  - [x] Enrollment filter applied: only schools with >= 20 students
  - [x] Axis labels are human-readable (not raw column names)
  - [x] Narrative text interprets the trendline and highlights outliers

  **QA Scenarios:**

  ```
  Scenario: Scatter plot renders with trendline
    Tool: Playwright (playwright skill)
    Preconditions: streamlit running with complete data
    Steps:
      1. Navigate to http://localhost:8501
      2. Click the "The Gap" tab
      3. Assert a Plotly chart container exists (`.js-plotly-plot` selector)
      4. Assert chart has scatter points (multiple trace elements)
      5. Assert trendline trace exists (the OLS line)
      6. Assert axis labels contain "Temporary Housing" and "Chronically Absent"
      7. Screenshot the tab
    Expected Result: Scatter plot with colored dots, size variation, visible trendline, clear labels
    Failure Indicators: No chart, missing trendline (statsmodels issue), raw column names as labels
    Evidence: .sisyphus/evidence/task-6-tab2-gap.png

  Scenario: Enrollment filter applied correctly
    Tool: Bash
    Preconditions: app.py exists with scatter plot code
    Steps:
      1. Run: grep -c "total_enrollment.*>=.*20\|>= 20" app.py
      2. Assert output >= 1 (filter is present in code)
    Expected Result: Filter is applied before scatter plot
    Failure Indicators: No enrollment filter found in code
    Evidence: .sisyphus/evidence/task-6-filter-check.txt
  ```

  **Commit**: NO (groups with Tasks 5, 7)
  **Commit**: NO (groups with Tasks 5, 7)

---

- [x] 7. Tab 3 — "The Invisible Majority" (Stacked Bar + Top 20 Table)

  **What to do**:
  - In `app.py`, replace the Tab 3 placeholder content with:
  - **Key insight**: ~2/3 of students in temporary housing are "doubled up" (living with others), NOT in shelters. These students are invisible in shelter databases.
  - **Stacked bar chart**: Show breakdown by housing type per borough
    ```python
    with tab3:
        st.header("The Invisible Majority")
        st.markdown("""
        Most people picture shelters when they think of student homelessness.
        But the **majority of students in temporary housing are \"doubled up\"** \u2014
        living with family or friends due to economic hardship. They don't appear
        in shelter databases. They are the invisible majority.
        """)
        
        # Stacked bar: shelter type by borough
        shelter_data = df.groupby('borough').agg(
            doubled_up=('doubled_up', 'sum'),
            dhs_shelter=('residing_in_dhs_shelter', 'sum'),
            non_dhs_shelter=('residing_in_non_dhs_shelter', 'sum')
        ).reset_index()
        
        shelter_melted = shelter_data.melt(
            id_vars='borough',
            value_vars=['doubled_up', 'dhs_shelter', 'non_dhs_shelter'],
            var_name='Housing Type', value_name='Students'
        )
        shelter_melted['Housing Type'] = shelter_melted['Housing Type'].map({
            'doubled_up': 'Doubled Up',
            'dhs_shelter': 'DHS Shelter',
            'non_dhs_shelter': 'Non-DHS Shelter'
        })
        
        fig = px.bar(
            shelter_melted, x='borough', y='Students',
            color='Housing Type', barmode='stack',
            title='Housing Type Breakdown by Borough (2020-21)'
        )
        st.plotly_chart(fig, use_container_width=True)
    ```
  - **Top 20 schools table**: Highest `pct_students_temp_housing` schools
    ```python
        st.subheader("Top 20 Schools by % Students in Temporary Housing")
        top20 = df.nlargest(20, 'pct_students_temp_housing')[
            ['school_name_housing', 'borough', 'pct_students_temp_housing',
             'pct_chronically_absent', 'total_enrollment']
        ].reset_index(drop=True)
        top20.index = top20.index + 1  # 1-indexed
        top20.columns = ['School', 'Borough', '% Temp Housing', '% Chronically Absent', 'Enrollment']
        st.dataframe(top20, use_container_width=True)
    ```
  - Add narrative text highlighting that doubled-up students are the majority
  - Add a closing "Call to Action" section:
    ```python
        st.markdown("---")
        st.subheader("What Can Be Done?")
        st.markdown("""
        - **Better identification**: Schools need better systems to identify doubled-up students
        - **Targeted resources**: Social workers at high-impact schools (research shows ~1.2 percentage point attendance improvement)
        - **Data transparency**: Regular reporting on housing status and attendance outcomes
        """)
    ```

  **Must NOT do**:
  - Do NOT add more than 20 rows to the table
  - Do NOT add filters or sorting controls
  - Do NOT modify Tab 1 or Tab 2 content
  - Do NOT add a 6th visualization (we're at 4 with the stacked bar + table — room for 1 more in stretch)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Multiple visualization types (stacked bar + table) plus narrative writing
  - **Skills**: `[]`
    - No special skills needed

  **Parallelization**:
  - **Can Run In Parallel**: YES (parallel with Tasks 5, 6)
  - **Parallel Group**: Wave 3 (with Tasks 5, 6)
  - **Blocks**: Task 9
  - **Blocked By**: Tasks 3, 4 (needs merged.csv and app skeleton)

  **References**:

  **Data References**:
  - `data/merged.csv` columns: `borough`, `doubled_up`, `residing_in_dhs_shelter`, `residing_in_non_dhs_shelter`, `pct_students_temp_housing`, `pct_chronically_absent`, `school_name_housing` (or `school_name`), `total_enrollment`
  - Research finding: ~2/3 of students in temp housing are doubled up, ~1/3 in shelters
  - Social worker impact: ~1.2 percentage point attendance improvement (NYU Steinhardt study)

  **External References**:
  - Plotly stacked bar: https://plotly.com/python/bar-charts/ — `barmode='stack'`
  - `st.dataframe`: https://docs.streamlit.io/develop/api-reference/data/st.dataframe
  - Advocates for Children NYC: https://www.advocatesforchildren.org/ — source for policy recommendations

  **Acceptance Criteria**:
  - [x] Tab 3 shows stacked bar chart with 3 housing types
  - [x] Housing types labeled: "Doubled Up", "DHS Shelter", "Non-DHS Shelter"
  - [x] Top 20 table shows exactly 20 rows
  - [x] Table columns: School, Borough, % Temp Housing, % Chronically Absent, Enrollment
  - [x] "Call to Action" section present with policy recommendations
  - [x] Narrative explains "doubled up" concept

  **QA Scenarios:**

  ```
  Scenario: Stacked bar chart and table render correctly
    Tool: Playwright (playwright skill)
    Preconditions: streamlit running with complete data
    Steps:
      1. Navigate to http://localhost:8501
      2. Click the "The Invisible Majority" tab
      3. Assert a Plotly chart container exists for stacked bar
      4. Assert a dataframe/table element exists
      5. Assert table has 20 data rows (count tr or st-dataframe rows)
      6. Assert text contains "doubled up" (case insensitive)
      7. Assert text contains "What Can Be Done" or similar call-to-action header
      8. Screenshot the tab
    Expected Result: Stacked bar with 3 colors, table with 20 schools, narrative + CTA
    Failure Indicators: Missing chart, empty table, no narrative text
    Evidence: .sisyphus/evidence/task-7-tab3-invisible.png

  Scenario: Table has correct columns and row count
    Tool: Bash
    Preconditions: app.py exists with table code
    Steps:
      1. Run: python -c "import pandas as pd; df=pd.read_csv('data/merged.csv'); top20=df.nlargest(20,'pct_students_temp_housing'); assert len(top20)==20; print(f'TOP_SCHOOL:{top20.iloc[0][\"school_name_housing\"]}'); print('TABLE_OK')"
      2. Assert stdout contains "TABLE_OK"
    Expected Result: 20 rows, highest-pct school identified
    Failure Indicators: Fewer than 20 rows, KeyError on column name
    Evidence: .sisyphus/evidence/task-7-table-check.txt
  ```

  **Commit**: YES (group with Tasks 5, 6)
  - Message: `feat(dashboard): implement 3-tab Streamlit dashboard with all visualizations`
  - Files: `app.py`
  - Pre-commit: `python -c "import ast; ast.parse(open('app.py').read()); print('SYNTAX_OK')"`

---

- [~] 8. Borough Map Visualization (STRETCH GOAL — SKIPPED per plan guidance)

  **What to do**:
  - **ONLY attempt this if Tasks 5, 6, 7 are all complete and working.** If the team is behind schedule by hour 4, SKIP this task entirely.
  - Add a borough-level choropleth map to Tab 1 ("The Scale") below the bar chart
  - Option A (simpler): Use `plotly.express.choropleth_mapbox` with NYC borough GeoJSON
    - Download borough GeoJSON from: `https://data.cityofnewyork.us/resource/tqmj-j8zm.geojson`
    - Save locally as `data/nyc_boroughs.geojson` (don't rely on live API for demo)
    - Use `carto-positron` mapbox style (free, no API key needed)
  - Option B (alternative): Use `folium` + `streamlit-folium`
    - Requires adding `folium` and `streamlit-folium` to requirements.txt
  - Color boroughs by average `pct_students_temp_housing`
  - This adds 1 more visualization (bringing total to 5 — the maximum allowed)

  **Must NOT do**:
  - Do NOT attempt if Tasks 5, 6, 7 are not complete
  - Do NOT add school-level pins/markers — borough-level choropleth only
  - Do NOT use a Mapbox API key — use free `carto-positron` style
  - Do NOT break existing Tab 1 content — add map BELOW the bar chart
  - This is visualization #5 — do NOT add any more after this

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: Map visualization requires spatial data handling and careful rendering
  - **Skills**: `[]`
    - No special skills needed — plotly/folium handles the mapping

  **Parallelization**:
  - **Can Run In Parallel**: NO (must verify Tasks 5-7 work first)
  - **Parallel Group**: Wave 4 (with Task 9)
  - **Blocks**: Task 9
  - **Blocked By**: Tasks 3, 4, 5 (needs all core viz working)

  **References**:

  **Data References**:
  - Borough GeoJSON: `https://data.cityofnewyork.us/resource/tqmj-j8zm.geojson`
  - Borough aggregation: group `data/merged.csv` by `borough`, compute mean `pct_students_temp_housing`

  **External References**:
  - Plotly choropleth mapbox: https://plotly.com/python/mapbox-county-choropleth/
  - `carto-positron` style (free, no key): used via `mapbox_style='carto-positron'`
  - Folium + Streamlit alternative: https://folium.streamlit.app/

  **Acceptance Criteria**:
  - [~] Map renders in Tab 1 below the bar chart
  - [~] 5 borough shapes visible with color gradient
  - [~] No API key required — uses free map tiles
  - [~] GeoJSON file saved locally (not fetched at runtime)
  - [~] Total visualization count = 5 (not more)

  **QA Scenarios:**

  ```
  Scenario: Map renders with borough shapes
    Tool: Playwright (playwright skill)
    Preconditions: streamlit running, map code added
    Steps:
      1. Navigate to http://localhost:8501
      2. Click "The Scale" tab
      3. Scroll down past the bar chart
      4. Assert a map element exists (plotly mapbox or folium iframe)
      5. Screenshot the map area
    Expected Result: Borough choropleth map with color gradient visible
    Failure Indicators: Map not rendering, missing GeoJSON, mapbox API key error
    Evidence: .sisyphus/evidence/task-8-map.png
  ```

  **Commit**: YES
  - Message: `feat(dashboard): add borough choropleth map (stretch goal)`
  - Files: `app.py`, `data/nyc_boroughs.geojson`

---

- [x] 9. Final Polish + Presentation Narrative

  **What to do**:
  - Review all narrative text across all 3 tabs for:
    - Consistency of tone (professional but accessible)
    - Accuracy of numbers (all should be computed from df, not hardcoded)
    - Proper flow of the 3-act data story
  - Ensure the introduction clearly states:
    - What the dashboard shows
    - Why it matters
    - What "chronically absent" means (>= 10% of enrolled days missed)
  - Ensure the conclusion (Tab 3 Call to Action) ties back to the opening
  - Add `st.caption()` at the bottom with data source attribution:
    ```python
    st.caption("Data sources: NYC Open Data \u2014 2021 Students in Temporary Housing (3wtp-43m9), School End-of-Year Attendance (gqq2-hgxd). 2020-21 school year.")
    ```
  - Verify the entire app runs cleanly: `streamlit run app.py --server.headless true`
  - Verify all charts render, all tabs work, all text is readable

  **Must NOT do**:
  - Do NOT add new visualizations (we're at 4-5, that's the cap)
  - Do NOT add new features, filters, or interactivity
  - Do NOT change the data pipeline or merged.csv
  - Do NOT deploy to cloud — local only

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Text editing and final review, no new logic
  - **Skills**: `['playwright']`
    - `playwright`: Needed for visual verification that all tabs render correctly

  **Parallelization**:
  - **Can Run In Parallel**: NO (needs all previous tasks complete)
  - **Parallel Group**: Wave 4 (sequential after Wave 3)
  - **Blocks**: Final Verification Wave (F1-F4)
  - **Blocked By**: Tasks 5, 6, 7 (and optionally 8)

  **References**:

  **Pattern References**:
  - Entire `app.py` — review all tabs for consistency
  - Research finding for narrative: ~87,000 students, ~2/3 doubled up, 1 in 12 students
  - Social worker impact: ~1.2pp attendance improvement (NYU Steinhardt study)
  - Advocates for Children: 154,000+ students homeless in 2024-25 (can mention trend is worsening)

  **External References**:
  - `st.caption`: https://docs.streamlit.io/develop/api-reference/text/st.caption

  **Acceptance Criteria**:
  - [x] Data source attribution visible at bottom of app (`st.caption`)
  - [x] All narrative text is accurate and consistent
  - [x] "Chronically absent" defined in intro
  - [x] COVID-19 disclaimer present
  - [x] All 3 tabs render with charts and text
  - [x] `streamlit run app.py --server.headless true` starts without errors
  - [x] No Python traceback on any tab

  **QA Scenarios:**

  ```
  Scenario: Full dashboard walkthrough — all tabs render
    Tool: Playwright (playwright skill)
    Preconditions: streamlit running
    Steps:
      1. Navigate to http://localhost:8501
      2. Assert title "The Absenteeism Gap" visible
      3. Assert COVID-19 info banner visible
      4. Click Tab 1 "The Scale" — assert bar chart + metrics visible
      5. Click Tab 2 "The Gap" — assert scatter plot with trendline visible
      6. Click Tab 3 "The Invisible Majority" — assert stacked bar + table + CTA visible
      7. Scroll to bottom — assert data source caption visible
      8. Screenshot each tab
    Expected Result: All 3 tabs render correctly with charts, narrative, and attribution
    Failure Indicators: Any tab empty, chart missing, error traceback visible
    Evidence: .sisyphus/evidence/task-9-full-walkthrough.png

  Scenario: App cold-starts in under 5 seconds
    Tool: Bash
    Preconditions: data/merged.csv exists
    Steps:
      1. Kill any running streamlit
      2. Run: time streamlit run app.py --server.headless true &
      3. Wait 5 seconds
      4. Run: curl -s http://localhost:8501 | head -20
      5. Assert response contains HTML content
      6. Kill streamlit
    Expected Result: App serves HTML within 5 seconds of startup
    Failure Indicators: Connection refused after 5s, timeout
    Evidence: .sisyphus/evidence/task-9-cold-start.txt
  ```

  **Commit**: YES
  - Message: `feat(dashboard): final polish and presentation narrative`
  - Files: `app.py`
  - Pre-commit: `python -c "import ast; ast.parse(open('app.py').read()); print('SYNTAX_OK')"`

---

## Final Verification Wave

> 4 review agents run in PARALLEL. ALL must APPROVE. Rejection → fix → re-run.

- [x] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, run command). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in .sisyphus/evidence/. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [x] F2. **Code Quality Review** — `unspecified-high`
  Run `python -m py_compile app.py` + `python -m py_compile data/fetch_data.py`. Review all Python files for: bare `except:`, `pass` in except blocks, commented-out code, unused imports, hardcoded secrets. Check for AI slop: excessive comments, over-abstraction, generic variable names (data/result/item/temp).
  Output: `Compile [PASS/FAIL] | Files [N clean/N issues] | VERDICT`

- [x] F3. **Real Manual QA** — `unspecified-high` (+ `playwright` skill)
  Start from clean state. Run `streamlit run app.py --server.headless true`. Use Playwright to: open localhost:8501, verify page title, click all 3 tabs, verify each has chart + narrative text, verify scatter plot has trendline, verify top-20 table, check COVID disclaimer visible. Screenshot each tab. Save to `.sisyphus/evidence/final-qa/`.
  Output: `Tabs [3/3] | Charts [N/N] | Narrative [N/N] | VERDICT`

- [x] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual code. Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Check "Must NOT do" compliance: no live API in app.py, no sodapy, no filters, no custom CSS, no more than 5 charts. Flag unaccounted files.
  Output: `Tasks [N/N compliant] | Guardrails [N/N clean] | VERDICT`

---

## Commit Strategy

- **After Task 2**: `feat(data): add data acquisition script for NYC Open Data` — requirements.txt, data/fetch_data.py
- **After Task 3**: `feat(data): add data cleaning and merge pipeline` — data/merged.csv (or cleaning script)
- **After Task 7**: `feat(dashboard): implement 3-tab Streamlit dashboard with visualizations` — app.py
- **After Task 9**: `feat(dashboard): polish narrative text and final presentation` — app.py
- **After FINAL**: `chore: final verification complete` — any fixes

---

## Success Criteria

### Verification Commands
```bash
# App launches without error
timeout 10 streamlit run app.py --server.headless true 2>&1 | head -5  # Expected: "You can now view your Streamlit app"

# Data integrity
python -c "import pandas as pd; df=pd.read_csv('data/merged.csv'); print(f'Rows: {len(df)}, Cols: {list(df.columns)}')"  # Expected: >1300 rows

# No suppressed values
python -c "import pandas as pd; df=pd.read_csv('data/merged.csv'); assert 's' not in df['pct_students_temp_housing'].astype(str).values; print('OK: no suppressed values')"

# Dependencies install
pip install -r requirements.txt  # Expected: all install successfully
```

### Final Checklist
- [x] All "Must Have" items present in code
- [x] All "Must NOT Have" items absent from code
- [x] Dashboard launches and renders all 3 tabs
- [x] Scatter plot shows trendline with R²
- [x] Data has >1,300 matched schools
- [x] COVID-19 disclaimer visible
- [x] "Chronically absent" defined in narrative
- [x] Top-20 schools table renders correctly
