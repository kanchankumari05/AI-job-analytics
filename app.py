import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Global AI & DS Job Market 2026", layout="wide")

st.title("Global Job Market & AI Skills Demand Dashboard")
st.markdown("Real-time analysis of salaries, AI tool adoption, and hiring trends.")

@st.cache_data
def load_data():
    df = pd.read_csv('ai_ds_job_salaries_2026.csv')
    return df

try:
    df = load_data()

    st.subheader("Key Market Indicators")
    col1, col2, col3, col4 = st.columns(4)

    avg_salary = int(df['salary_usd'].mean())
    total_jobs = len(df)
    remote_pct = round((df['remote_ratio'] == 100).mean() * 100, 1)
    ai_adoption = round(df['uses_ai_tools_daily'].mean() * 100, 1)

    col1.metric("Average Salary ($)", f"${avg_salary:,}")
    col2.metric("Total Profiles Analyzed", f"{total_jobs:,}")
    col3.metric("Fully Remote Jobs (%)", f"{remote_pct}%")
    col4.metric("Daily AI Tools Users", f"{ai_adoption}%")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Top 10 Highest Paying AI/DS Roles")
        top_jobs = df.groupby('job_title')['salary_usd'].mean().reset_index()
        top_jobs = top_jobs.sort_values(by='salary_usd', ascending=False).head(10)
        fig1 = px.bar(top_jobs, x='salary_usd', y='job_title', orientation='h',
                      color='salary_usd', color_continuous_scale='Viridis',
                      labels={'salary_usd': 'Avg Salary ($)', 'job_title': 'Job Title'})
        st.plotly_chart(fig1, use_container_width=True)

    with col_right:
        st.subheader("Salary vs Experience Level")
        fig2 = px.box(df, x='experience_level', y='salary_usd', color='experience_level',
                      labels={'experience_level': 'Experience', 'salary_usd': 'Salary ($)'})
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Industry Share by Average Salary")
        ind_sal = df.groupby('industry')['salary_usd'].mean().reset_index().sort_values(by='salary_usd', ascending=False)
        fig3 = px.pie(ind_sal, names='industry', values='salary_usd', hole=0.4)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Remote Work Ratio Distribution")
        remote_df = df['remote_ratio'].value_counts().reset_index()
        remote_df.columns = ['Remote Ratio (%)', 'Count']
        fig4 = px.bar(remote_df, x='Remote Ratio (%)', y='Count', color='Count')
        st.plotly_chart(fig4, use_container_width=True)

except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.info("Please make sure 'ai_ds_job_salaries_2026.csv' file is in the same folder.")