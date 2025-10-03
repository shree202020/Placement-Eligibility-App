import streamlit as st
import sqlite3
import pandas as pd

# Connect to database
def get_connection():
    conn = sqlite3.connect("placement.db")
    return conn

st.title("📌 Placement Eligibility Application")

# Sidebar for eligibility criteria
st.sidebar.header("Set Eligibility Criteria")

problems_solved_min = st.sidebar.number_input("Min Problems Solved", 0, 1000, 50)
softskills_min = st.sidebar.number_input("Min Soft Skills Avg (%)", 0, 100, 70)
cgpa_min = st.sidebar.number_input("Min CGPA", 0.0, 10.0, 7.0)

if st.sidebar.button("Find Eligible Students"):
    conn = get_connection()
    query = f"""
        SELECT s.student_id, s.name, s.branch, s.cgpa, 
               (ss.comm + ss.team + ss.leadership + ss.creativity + ss.adaptability + ss.time_mgmt)/6.0 AS softskills_avg,
               (p.c + p.cpp + p.java + p.python + p.ds + p.algo) AS problems_solved
        FROM students s
        JOIN soft_skills ss ON s.student_id = ss.student_id
        JOIN programming p ON s.student_id = p.student_id
        WHERE s.cgpa >= {cgpa_min}
          AND (p.c + p.cpp + p.java + p.python + p.ds + p.algo) >= {problems_solved_min}
          AND ((ss.comm + ss.team + ss.leadership + ss.creativity + ss.adaptability + ss.time_mgmt)/6.0) >= {softskills_min}
    """
    df = pd.read_sql(query, conn)
    st.subheader("✅ Eligible Students")
    st.dataframe(df)

    if df.empty:
        st.warning("No students found matching the criteria!")

    conn.close()
