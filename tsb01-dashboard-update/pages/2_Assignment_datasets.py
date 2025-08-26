
import streamlit as st
import pandas as pd
import os

# Page config
st.set_page_config(page_title="Work Risk", page_icon=":material/monitoring:", layout="wide")




# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to project root, then into data folder
pref_path = os.path.join(os.path.dirname(current_dir), 'data', 'pref.csv')
seat_path = os.path.join(os.path.dirname(current_dir), 'data', 'seat.csv')
stu_path = os.path.join(os.path.dirname(current_dir), 'data', 'students.csv')




# Example: Load 3 datasets
pref_df = pd.read_csv(pref_path)
Seat_df = pd.read_csv(seat_path)
Stud_df = pd.read_csv(stu_path)

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
    ### 📊 Data Descriptions  
    Please find below the dataset for the assignment.  
    It contains student details, preferences, and seat allocation outcomes for analysis.
    
   **Student Data**  
    - `UniqueID` | `Name` | `Gender` | `Caste` | `Rank` 
                
    **Preference Data**  
    - `CollegeID` | `PrefNumber` | `UniqueID`   

    **Seat Data**  
    - `CollegeID` | `Institution` | `TOTAL No. of seats` | `TOTAL No. of students admitted` | `No. of students joined in Orphan Quota` | `No. of students Joined in PHC Quota` | `SC` | `SC-CC`| `BC` | `Minority`| `OC` 
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
    
