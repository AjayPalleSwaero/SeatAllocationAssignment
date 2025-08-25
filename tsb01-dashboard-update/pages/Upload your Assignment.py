import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page config
st.set_page_config(page_title="Seat Allocation Validation", page_icon=":material/verified:", layout="wide")

# Sidebar navigation
page = st.sidebar.radio("Select Page", ["Validate Allocation"], key="main_menu")

# --- Validation Page ---
if page == "Validate Allocation":
    st.header("✅ Seat Allocation Validation")

    st.markdown("""
    ### Instructions:
    1. Select your **Group**.  
    2. Upload your **Assignment Completed File (CSV)**.  
    3. System will validate against backend Validation Data.  
    4. If successful → group name & timestamp are saved.  
    """)

    # --- Step 1: Group selection ---
    group_name = st.selectbox("Select Your Group", ["Select Group", "Group - 1", "Group - 2", "Group - 3", "Group - 4"])

    # --- Step 2: File uploader ---
    assignment_file = st.file_uploader("Upload Assignment Completed File (CSV)", type="csv", key="assign_file")

    if group_name != "Select Group" and assignment_file:
        try:
            # Load uploaded assignment file
            assign_df = pd.read_csv(assignment_file)

            # Load backend validation file
            validation_df = pd.read_csv("./data/validation_file.csv")   # <-- backend validation file

            # Standardize column names
            assign_df.columns = assign_df.columns.str.strip().str.lower()
            validation_df.columns = validation_df.columns.str.strip().str.lower()

            # Expected headers
            expected_columns = ["uniquic id", "collage id", "preference id", "gender", "cast"]

            # --- Step 1: Validate headers ---
            if list(assign_df.columns) != expected_columns:
                st.error("❌ The data is not correct, please check (Invalid column names).")
            elif list(validation_df.columns) != expected_columns:
                st.error("❌ Backend validation file format error.")
            else:
                # --- Step 2: Validate records row-by-row (subset logic) ---
                merged = assign_df.merge(
                    validation_df,
                    how="left",
                    on=["uniquic id", "collage id", "preference id", "gender", "cast"],
                    indicator=True
                )

                unmatched = merged[merged["_merge"] == "left_only"]
                matched = merged[merged["_merge"] == "both"]

                if unmatched.empty:
                    st.success("🎉 The allocated seats is successfully completed!")
                    st.balloons()
                    # --- Step 3: Save group name + timestamp ---
                    log_file = "./data/validation_log.csv"
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_entry = pd.DataFrame([[group_name, timestamp]], columns=["Group", "Timestamp"])

                    if os.path.exists(log_file):
                        log_entry.to_csv(log_file, mode="a", header=False, index=False)
                    else:
                        log_entry.to_csv(log_file, mode="w", header=True, index=False)

                    st.info(f"📌 Log saved: {group_name} at {timestamp}")
                    
                elif matched.shape[0]>1:
                    st.error("❌ The data is not correct, please check (Some records did not match).")



                    st.write(f"Percentage of total matches { round(matched.shape[0]/assign_df.shape[0]*100, 2)}""")
                    # Total matched recordss
                    st.write("Total matched records:")  
                    st.dataframe(matched.drop(columns=["_merge"]))  

                    # Total Unmatched records
                    st.write(f"Percentage of total unmatches{ round(unmatched.shape[0]/assign_df.shape[0]*100, 2)}""")

                    st.write("Unmatched records from assignment file:")
                    st.dataframe(unmatched.drop(columns=["_merge"]))

                else:
                    st.error("❌ The data is not correct, please check (Some records did not match).")
                    st.write("Unmatched records from assignment file:")
                    st.dataframe(unmatched.drop(columns=["_merge"]))
                

        except Exception as e:
            st.error(f"⚠️ Error while processing file: {e}")
    elif group_name == "Select Group" and assignment_file:
        st.warning("⚠️ Please select a group before uploading file.")
