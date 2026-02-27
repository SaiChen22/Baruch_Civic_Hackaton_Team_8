import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide", page_title="The Absenteeism Gap")

@st.cache_data
def load_data():
    return pd.read_csv("data/merged.csv")

df = load_data()

st.title("The Absenteeism Gap")
st.subheader("How Homelessness Steals School Days in NYC")
st.info("⚠️ Data from the 2020-21 school year, which was significantly impacted by COVID-19 and remote/hybrid learning.")
st.markdown("""
In 2020-21, approximately **87,000 NYC students** lived in temporary housing — that's roughly 1 in 12.
This dashboard explores how housing instability correlates with chronic absenteeism across ~1,400 NYC schools.

**Chronically absent** means missing ≥10% of enrolled school days.
""")

tab1, tab2, tab3 = st.tabs(["📊 The Scale", "🔍 The Gap", "👥 The Invisible Majority"])

with tab1:
    st.header("The Scale of Student Homelessness")
    st.markdown("""
    NYC's student homelessness crisis is not evenly distributed. The Bronx bears
    a disproportionate share, while Staten Island has the fewest affected students.
    """)
    
    borough_data = df.groupby('borough_housing').agg(
        total_temp_housing=('n_students_temp_housing', 'sum'),
        total_schools=('dbn', 'count'),
        avg_pct=('pct_students_temp_housing', 'mean')
    ).reset_index().sort_values('total_temp_housing', ascending=False)
    
    fig = px.bar(
        borough_data,
        x='borough_housing', y='total_temp_housing',
        color='borough_housing',
        title='Students in Temporary Housing by Borough (2020-21)',
        labels={'total_temp_housing': 'Total Students', 'borough_housing': 'Borough'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Schools", f"{len(df):,}")
    col2.metric("Total Students in Temp Housing", f"{int(df['n_students_temp_housing'].sum()):,}")
    col3.metric("Citywide Average", f"{df['pct_students_temp_housing'].mean():.1f}%")

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
        color='borough_housing',
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

with tab3:
    st.header("The Invisible Majority")
    st.markdown("""
    Most people picture shelters when they think of student homelessness.
    But the **majority of students in temporary housing are "doubled up"** —
    living with family or friends due to economic hardship. They don't appear
    in shelter databases. They are the invisible majority.
    """)
    
    # Stacked bar: shelter type by borough
    shelter_data = df.groupby('borough_housing').agg(
        doubled_up=('n_doubled_up', 'sum'),
        dhs_shelter=('n_dhs_shelter', 'sum'),
        non_dhs_shelter=('n_non_dhs_shelter', 'sum')
    ).reset_index()
    
    shelter_melted = shelter_data.melt(
        id_vars='borough_housing',
        value_vars=['doubled_up', 'dhs_shelter', 'non_dhs_shelter'],
        var_name='Housing Type', value_name='Students'
    )
    shelter_melted['Housing Type'] = shelter_melted['Housing Type'].map({
        'doubled_up': 'Doubled Up',
        'dhs_shelter': 'DHS Shelter',
        'non_dhs_shelter': 'Non-DHS Shelter'
    })
    
    fig = px.bar(
        shelter_melted, x='borough_housing', y='Students',
        color='Housing Type', barmode='stack',
        title='Housing Type Breakdown by Borough (2020-21)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Top 20 Schools by % Students in Temporary Housing")
    top20 = df.nlargest(20, 'pct_students_temp_housing')[
        ['school_name_housing', 'borough_housing', 'pct_students_temp_housing',
         'pct_chronically_absent', 'total_enrollment']
    ].reset_index(drop=True)
    top20.index = top20.index + 1  # 1-indexed
    top20.columns = ['School', 'Borough', '% Temp Housing', '% Chronically Absent', 'Enrollment']
    st.dataframe(top20, use_container_width=True)
    
    st.markdown("---")
    st.subheader("What Can Be Done?")
    st.markdown("""
    - **Better identification**: Schools need better systems to identify doubled-up students
    - **Targeted resources**: Social workers at high-impact schools (research shows ~1.2 percentage point attendance improvement)
    - **Data transparency**: Regular reporting on housing status and attendance outcomes
    """)


st.caption("Data sources: NYC Open Data — 2021 Students in Temporary Housing (3wtp-43m9), School End-of-Year Attendance (gqq2-hgxd). 2020-21 school year.")