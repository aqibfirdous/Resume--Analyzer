# app.py
import streamlit as st
import pandas as pd
import concurrent.futures

from database import initialize_db, update_resumes, fetch_resumes
from pdf_extraction import extract_text_from_pdf
from embeddings import match_job_description

def main():
    st.title("Resume Analysis and Job Matching")
    st.write("Upload a CSV containing student details with a Resume link column to analyze resumes and match with a job description.")

    # CSV Upload and Processing Section
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        try:
            student_data = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
            return

        # Check for required columns
        required_cols = ['First name', 'Email id', 'Resume link', 'Location']
        for col in required_cols:
            if col not in student_data.columns:
                st.error(f"Missing required column: {col}")
                return

        with st.spinner("Extracting resume texts..."):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                resume_texts = list(executor.map(extract_text_from_pdf, student_data['Resume link']))
            student_data['ResumeText'] = resume_texts

        with st.spinner("Storing resumes in the database..."):
            try:
                update_resumes(student_data)
                st.success("Resumes stored successfully!")
            except Exception as e:
                st.error(f"Error updating database: {e}")

    # Section 1: City-Based Filtering
    st.header("Filter by City (Optional)")
    location_filter = st.text_input("Enter a city name to filter candidates")
    with st.spinner("Fetching resumes..."):
        resumes_df = fetch_resumes(location_filter)

    if not resumes_df.empty:
        st.success(f"Found {len(resumes_df)} candidates.")
        st.dataframe(resumes_df[['name', 'email', 'resume_link', 'location']])
    else:
        st.warning("No resumes found.")

    # Section 2: Job Description Matching
    st.header("Match Job Description with Resumes")
    job_description = st.text_area("Enter the Job Description", height=200)
    if job_description:
        threshold = st.slider("Set Similarity Threshold", 0.1, 1.0, 0.3, 0.1)
        with st.spinner("Matching resumes..."):
            matched_candidates = match_job_description(resumes_df, job_description, threshold)
        if not matched_candidates.empty:
            st.success(f"Found {len(matched_candidates)} suitable candidates.")
            st.dataframe(matched_candidates)
            csv_data = matched_candidates.to_csv(index=False).encode('utf-8')
            st.download_button("Download Matching Candidates", csv_data, "matched_candidates.csv", "text/csv")
        else:
            st.warning("No suitable candidates found.")

    # Option to Show All Stored Resumes
    if st.checkbox("Show All Stored Resumes"):
        all_resumes = fetch_resumes()
        st.dataframe(all_resumes)

if __name__ == "__main__":
    # Initialize the database when the app starts.
    initialize_db()
    main()
