
import streamlit as st
import pandas as pd
import os

# Page config
st.set_page_config(page_title="Work Risk", page_icon=":material/monitoring:", layout="wide")

# Example: Load 3 datasets
pref_df = pd.read_csv("./data/preference.csv")
Seat_df = pd.read_csv("./data/seat.csv")
Stud_df = pd.read_csv("./data/students.csv")

# Datasets in a dictionary (name → dataframe)
datasets = {
    "Student_Details": pref_df,
    "Preference_Data": Seat_df,
    "Institution_Data": Stud_df,
}

# Sidebar navigation
page = st.sidebar.radio("Select Page", ["Download Datasets"], key="main_menu")

# --- Download Page ---
if page == "Download Datasets":
    st.header("⬇️ Download Your Datasets")

    # Project description
    st.markdown("""
    ### 📘 About the Project  
    This is the data about the **Seat Allocation for Students**.  
    You are part of the **Education Board’s Data Science Team**.  
    Every year, thousands of students apply for admission into colleges after their 10th class (SSC exams).  
    Admission depends on:
    - Student’s SSC grades and rank  
    - Reservation category (GEN, SC, ST, BC, PH)  

    ### 📊 Data Descriptions  

    **Student Data**  
    - `Student_ID` | `Name` | `Gender` | `Phone` | `District` | `Category` | `Rank` | `SSC Grades`  

    **Preference Data**  
    - `Student_ID` | `Preference_Order` | `College_ID` | `College_Name`  

    **Institution Matrix**  
    - `College_ID` | `College_Name` | `District` | `Seats_GEN` | `Seats_SC` | `Seats_ST` | `Seats_BC` | `Seats_PH`  
    """)

    st.divider()  # nice separation line

    # Loop through each dataset and create a download button
    for name, df in datasets.items():
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"Download {name} (CSV)",
            data=csv_bytes,
            file_name=f"{name.replace(' ', '_').lower()}.csv",
            mime="text/csv",
        )
    
