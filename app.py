import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide", page_title="The Absenteeism Gap")

@st.cache_data
def load_data():
    try:
        attendance = pd.read_csv("data/attendance_all_years.csv")
    except FileNotFoundError:
        attendance = pd.read_csv("data/attendance.csv")
    housing_all_years = pd.read_csv("data/housing_all_years.csv")

    for col in [
        "students_in_temporary_housing",
        "students_in_temporary_housing_1",
        "students_residing_in_shelter",
        "residing_in_dhs_shelter",
        "residing_in_non_dhs_shelter",
        "doubled_up",
    ]:
        if col in housing_all_years.columns:
            housing_all_years[col] = (
                housing_all_years[col]
                .astype(str)
                .str.replace("%", "", regex=False)
                .replace("s", np.nan)
                .replace("", np.nan)
            )
            housing_all_years[col] = pd.to_numeric(housing_all_years[col], errors="coerce")

    borough_map = {
        "M": "Manhattan",
        "X": "Bronx",
        "K": "Brooklyn",
        "Q": "Queens",
        "R": "Staten Island",
    }
    housing_all_years["borough"] = (
        housing_all_years["dbn"].astype(str).str[2].map(borough_map).fillna("Citywide")
    )
    attendance["chronically_absent_1"] = pd.to_numeric(
        attendance["chronically_absent_1"], errors="coerce"
    )
    attendance["total_enrollment"] = pd.to_numeric(
        attendance["contributing_10_total_days"], errors="coerce"
    )
    return attendance, housing_all_years

attendance_df, housing_all_years = load_data()

available_years = sorted(housing_all_years["school_year"].dropna().unique())

header_col, year_col = st.columns([5, 1])
with header_col:
    st.title("The Absenteeism Gap")
    st.subheader("How Homelessness Steals School Days in NYC")

with year_col:
    st.markdown("**School year**")
    selected_year = st.selectbox(
        "School year",
        available_years,
        index=len(available_years) - 1,
        label_visibility="collapsed",
    )

housing_year_df = housing_all_years[housing_all_years["school_year"] == selected_year].copy()

attendance_year_df = attendance_df[attendance_df["year"] == selected_year].copy()

gap_df = housing_year_df.merge(
    attendance_year_df[["dbn", "school_name", "chronically_absent_1", "total_enrollment"]],
    on="dbn",
    how="inner",
    suffixes=("_housing", "_attendance"),
)

gap_df = gap_df.rename(
    columns={
        "students_in_temporary_housing_1": "pct_students_temp_housing",
        "chronically_absent_1": "pct_chronically_absent",
        "school_name_housing": "school_name_housing",
    }
)

if attendance_year_df.empty:
    st.warning(
        f"No attendance rows found for {selected_year} in your local attendance file. "
        "Gap tab needs same-year attendance data."
    )
st.info("⚠️ All tabs use selected year. Gap tab uses same-year attendance when available in attendance data.")
st.markdown("""
In approximately **87,000 NYC students** lived in temporary housing — that's roughly 1 in 12.
This dashboard explores multi-year housing patterns and how housing instability correlates with chronic absenteeism.

**Chronically absent** means missing ≥10% of enrolled school days.
""")

tab1, tab2, tab3 = st.tabs(["📊 The Scale", "🔍 The Gap", "👥 The Invisible Majority"])

with tab1:
    st.header("The Scale of Student Homelessness")
    st.markdown("""
    NYC's student homelessness crisis is not evenly distributed. The Bronx bears
    a disproportionate share, while Staten Island has the fewest affected students.
    """)
    
    borough_data = housing_year_df.groupby('borough').agg(
        total_temp_housing=('students_in_temporary_housing', 'sum'),
        total_schools=('dbn', 'count'),
        avg_pct=('students_in_temporary_housing_1', 'mean')
    ).reset_index().sort_values('total_temp_housing', ascending=False)
    
    fig = px.bar(
        borough_data,
        x='borough', y='total_temp_housing',
        color='borough',
        title=f'Students in Temporary Housing by Borough ({selected_year})',
        labels={'total_temp_housing': 'Total Students', 'borough': 'Borough'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Schools", f"{len(housing_year_df):,}")
    col2.metric("Total Students in Temp Housing", f"{int(housing_year_df['students_in_temporary_housing'].sum()):,}")
    col3.metric("Citywide Average", f"{housing_year_df['students_in_temporary_housing_1'].mean():.1f}%")

with tab2:
    st.header("The Absenteeism Gap")
    st.markdown("""
    Each dot represents one NYC school. Schools with more students in temporary
    housing tend to have higher rates of chronic absenteeism. The trendline
    quantifies this relationship.
    """)
    
    scatter_df = gap_df[gap_df['total_enrollment'] >= 20].copy()

    if scatter_df.empty:
        st.info(f"No matched housing + attendance rows for {selected_year}.")
    else:
        fig = px.scatter(
            scatter_df,
            x='pct_students_temp_housing',
            y='pct_chronically_absent',
            color='borough',
            size='total_enrollment',
            hover_data=['school_name_housing', 'dbn'],
            trendline='ols',
            title=f'Housing Instability vs Chronic Absenteeism ({selected_year})',
            labels={
                'pct_students_temp_housing': '% Students in Temporary Housing',
                'pct_chronically_absent': '% Chronically Absent'
            },
            opacity=0.6
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("The Invisible Majority")
    st.markdown("""
    Most people picture shelters when they think of student homelessness.
    But the **majority of students in temporary housing are "doubled up"** —
    living with family or friends due to economic hardship. They don't appear
    in shelter databases. They are the invisible majority.
    """)
    
    # Stacked bar: shelter type by borough
    shelter_data = housing_year_df.groupby('borough').agg(
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
        title=f'Housing Type Breakdown by Borough ({selected_year})'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Top 20 Schools by % Students in Temporary Housing")
    top20 = housing_year_df.nlargest(20, 'students_in_temporary_housing_1')[
        ['school_name', 'borough', 'students_in_temporary_housing_1',
         'students_in_temporary_housing', 'total_students']
    ].reset_index(drop=True)
    top20.index = top20.index + 1  # 1-indexed
    top20.columns = ['School', 'Borough', '% Temp Housing', 'Students in Temp Housing', 'Enrollment']
    st.dataframe(top20, use_container_width=True)
    
    st.markdown("---")
    st.subheader("What Can Be Done?")
    st.markdown("""
    - **Better identification**: Schools need better systems to identify doubled-up students
    - **Targeted resources**: Social workers at high-impact schools (research shows ~1.2 percentage point attendance improvement)
    - **Data transparency**: Regular reporting on housing status and attendance outcomes
    """)


st.caption("Data sources: NYC Open Data — Students in Temporary Housing by school year (2017-18, 2018-19, 2019-20, 2020-21) and School End-of-Year Attendance (gqq2-hgxd, 2020-21).")