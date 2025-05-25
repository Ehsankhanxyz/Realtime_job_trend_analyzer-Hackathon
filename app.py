import streamlit as st
import pandas as pd
import datetime

# Load your scraped data  
df = pd.read_csv("indeed_jobs.csv")

# Function to convert relative date strings to actual dates
def parse_posted_date(date_str):
    today = datetime.date.today()
    if isinstance(date_str, str):
        if 'Today' in date_str or 'Just posted' in date_str:
            return today
        elif 'day' in date_str:
            days = int(date_str.split()[0])
            return today - datetime.timedelta(days=days)
    return None

# Apply date conversion
df['Posted Date'] = df['Date Posted'].apply(parse_posted_date)

# Streamlit Dashboard
st.title("Job Market Insights Dashboard - Rozee.pk")

# 1. Top 5 most in-demand job titles
st.subheader("Top 5 Most In-Demand Job Titles")
top_titles = df['Job Title'].value_counts().head(5)
st.bar_chart(top_titles)

# 2. Companies with the most job postings
st.subheader("Top Companies Hiring")
top_companies = df['Company'].value_counts().head(5)
st.bar_chart(top_companies)

# 3. Job Postings Over Time (if Posted Date exists)
if df['Posted Date'].notnull().any():
    st.subheader("Job Postings Over Time")
    jobs_by_date = df['Posted Date'].value_counts().sort_index()
    st.line_chart(jobs_by_date)

# 4. Filter by keyword
st.subheader("Search Jobs by Keyword")
keyword = st.text_input("Enter keyword:")
if keyword:
    filtered = df[df['Job Title'].str.contains(keyword, case=False, na=False)]
    st.write(f"Found {len(filtered)} jobs with keyword '{keyword}':")
    st.dataframe(filtered)
else:
    st.dataframe(df.head(50))  # Show first 50 rows by default