import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Seat Allocation Validation", page_icon=":material/verified:", layout="wide")

# Sidebar navigation
page = st.sidebar.radio("Select Page", ["Download Datasets", "Validate Allocation"], key="main_menu")

# --- Validation Page ---
if page == "Validate Allocation":
    st.header("✅ Seat Allocation Validation")

    st.markdown("""
    ### Instructions:
    1. Upload your **Assignment Completed File (CSV)**.  
    2. System will validate against backend Validation Data.  
    3. Rules:  
       - Column headers must match.  
       - Each record in Assignment must exist in Validation (Unique Id + College Id + Preference Id + Gender + Cast).  
       - Assignment can be a subset of Validation.  
    """)


    # select the group 
    
 
    # File uploader
    assignment_file = st.file_uploader("Upload Assignment Completed File (CSV)", type="csv", key="assign_file")

    if assignment_file:
        try:
            # Load uploaded assignment file
            assign_df = pd.read_csv(assignment_file)

            # Load backend validation file
            validation_df = pd.read_csv("./data/validation_file.csv")   # <-- keep validation file in backend

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
                # Merge only on all 5 columns
                merged = assign_df.merge(validation_df, how="left", 
                                         on=["uniquic id", "collage id", "preference id", "gender", "cast"], 
                                         indicator=True)

                # Rows that didn't match
                unmatched = merged[merged["_merge"] == "left_only"]

                matched = merged[merged["_merge"] == "both"]

                if unmatched.empty:
                    st.success("🎉 The allocated seats is successfully completed!")

                    # save the group number and timestmap

                    st.balloons()
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
