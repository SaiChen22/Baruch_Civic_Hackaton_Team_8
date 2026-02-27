import re

with open('app.py', 'r') as f:
    content = f.read()

checks = {
    "st.set_page_config on line 6": "st.set_page_config(layout=\"wide\", page_title=\"The Absenteeism Gap\")" in content,
    "@st.cache_data decorator": "@st.cache_data" in content,
    "load_data function": "def load_data():" in content,
    "pd.read_csv('data/merged.csv')": "pd.read_csv(\"data/merged.csv\")" in content,
    "st.title present": "st.title(\"The Absenteeism Gap\")" in content,
    "st.info with warning emoji": "⚠️" in content and "st.info(" in content,
    "COVID-19 disclaimer": "COVID-19" in content,
    "Chronically absent definition": "Chronically absent" in content,
    "st.tabs with 3 tabs": "st.tabs([\"📊 The Scale\", \"🔍 The Gap\", \"👥 The Invisible Majority\"])" in content,
    "Placeholder text in tabs": "_Visualization loading..._" in content,
    "No requests.get calls": "requests.get" not in content,
    "No urllib calls": "urllib" not in content,
    "No http calls": "http" not in content,
}

print("✓ APP.PY VERIFICATION:")
all_pass = True
for check, result in checks.items():
    status = "✓" if result else "✗"
    print(f"  {status} {check}")
    if not result:
        all_pass = False

print(f"\nAll checks passed: {all_pass}")
