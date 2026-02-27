# Manual QA Report - BLOCKED

## Task: F3. Real Manual QA

**Date**: 2026-02-27  
**Status**: ❌ BLOCKED - ENVIRONMENT ISSUE

---

## Blocker Summary

Cannot execute manual QA due to missing Python package management tools.

### Environment State

- **Python Version**: 3.12.3 (system Python at /usr/bin/python3)
- **pip**: NOT AVAILABLE (python3 -m pip fails)
- **Streamlit**: NOT INSTALLED
- **Data File**: ✅ EXISTS (data/merged.csv - 1,455 rows)
- **Virtual Environment**: Broken (venv/ exists but missing activate script and pip)

### Attempted Solutions

1. ✗ Direct pip install → Command not found
2. ✗ pip3 install → Command not found  
3. ✗ python3 -m pip install → No module named pip
4. ✗ Activate existing venv → venv/bin/activate does not exist
5. ✗ Recreate venv → Requires python3-venv system package
6. ✗ Install pip via get-pip.py → Externally managed environment error
7. ✗ User-level install with --break-system-packages → Still no pip module

### Root Cause

This is a Debian/Ubuntu system with externally-managed Python environment (PEP 668).
The system requires either:
- `apt install python3-pip python3-venv` (requires sudo)
- `apt install python3-streamlit` (if available in repos)
- Working virtual environment with ensurepip

### Required to Unblock

One of:
1. **System package installation** (requires sudo):
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv python3-full
   ```

2. **Pre-configured venv** with pip and streamlit already installed

3. **pipx** for isolated app installation:
   ```bash
   sudo apt install pipx
   pipx install streamlit
   ```

---

## QA Checklist (NOT EXECUTED)

Due to blocker, the following could not be verified:

- [ ] Streamlit server starts successfully within 10 seconds
- [ ] Page title: "The Absenteeism Gap"
- [ ] All 3 tabs render: "📊 The Scale", "🔍 The Gap", "👥 The Invisible Majority"
- [ ] Tab 1: Borough bar chart + 3 metric cards visible
- [ ] Tab 2: Scatter plot with OLS trendline visible
- [ ] Tab 3: Stacked bar chart + Top 20 table visible
- [ ] COVID-19 disclaimer visible at top (st.info with ⚠️)
- [ ] Data attribution caption visible at bottom
- [ ] Screenshots saved to `.sisyphus/evidence/final-qa/`

---

## Verdict

**CANNOT APPROVE OR REJECT** - Environment prerequisites not met.

Manual QA requires functional Python package management to install and run Streamlit.

---

## Next Steps

1. Resolve pip/venv installation issue
2. Install streamlit and dependencies (streamlit, pandas, plotly, statsmodels)
3. Re-run this QA task
