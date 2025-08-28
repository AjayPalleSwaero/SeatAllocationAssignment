import streamlit as st
import pandas as pd
from datetime import datetime
import os
import re


# Page config
st.set_page_config(page_title="Seat Allocation Validation", page_icon=":material/verified:", layout="wide")

def normalize_col(c: str) -> str:
    """Lowercase and remove non-alphanumerics to compare/match headers."""
    return re.sub(r'[^a-z0-9]', '', str(c).lower())

# Map common variants/typos to canonical names
HEADER_SYNONYMS = {
    # unique id
    "uniqueid": "uniqueid",
    "uniquicid": "uniqueid",
    "unique_id": "uniqueid",
    "studentid": "uniqueid",
    "uid": "uniqueid",
    # college id
    "collegeid": "collegeid",
    "collageid": "collegeid",      # common typo
    "college": "collegeid",
    # preference number / id / order
    "prefnumber": "prefnumber",
    "preferenceid": "prefnumber",
    "preferenceorder": "prefnumber",
    "preference": "prefnumber",
    "pref": "prefnumber",
    "prefno": "prefnumber",
    "preference_no": "prefnumber",
    # gender
    "gender": "gender",
    "sex": "gender",
    # caste
    "caste": "caste",
    "cast": "caste",
    "category": "caste",
}

REQUIRED = ["uniqueid", "collegeid", "prefnumber", "gender", "caste"]

def canonicalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to canonical set using synonyms; returns df with renamed columns."""
    rename_map = {}
    for col in df.columns:
        key = normalize_col(col)
        canonical = HEADER_SYNONYMS.get(key)  # None if not in synonyms
        if canonical:
            rename_map[col] = canonical
        else:
            # keep normalized name if it already equals a required one, else keep original
            norm = key
            rename_map[col] = norm if norm in REQUIRED else col
    return df.rename(columns=rename_map)

def ensure_required(df: pd.DataFrame) -> bool:
    return set(REQUIRED).issubset(set(df.columns))

def clean_values(df: pd.DataFrame) -> pd.DataFrame:
    """Trim whitespace and ensure string dtype for required columns."""
    for c in REQUIRED:
        df[c] = df[c].astype(str).str.strip()
    return df


# Sidebar (single page)
page = st.sidebar.radio("Select Page", ["Validate Allocation"], key="main_menu")

# --- Validation Page ---
if page == "Validate Allocation":
    st.header("✅ Seat Allocation Validation")

    st.markdown("""
    ### 📝 Instructions
    1. Select your **Group**.  
    2. Upload your **Completed Assignment File (CSV)** (filename can be anything).  
    3. The system validates against backend data:
       - ✅ If **all rows** in your file exist in validation (on **UniqueID, CollegeID, PrefNumber, Gender, Caste**), it's **successful**.
       - ❌ Otherwise you'll see unmatched rows and can re-upload after fixing.
    """)

    # --- Step 1: Group selection ---
    group_name = st.selectbox("Select Your Group", ["Select Group"] + [f"Group - {i}" for i in range(1, 28)])

    # --- Step 2: File uploader ---
    assignment_file = st.file_uploader("Upload Assignment Completed File (CSV)", type="csv", key="assign_file")

    if group_name != "Select Group" and assignment_file:
        try:
            # Load uploaded assignment
            assign_df = pd.read_csv(assignment_file, dtype=str)
            # Get the directory of the current script
            current_dir = os.path.dirname(os.path.abspath(__file__))
           # Go up one level to project root, then into data folder
            Validation_file = os.path.join(os.path.dirname(current_dir), 'data', 'validation_file.csv')    
            # Load backend validation file
            validation_df = pd.read_csv(Validation_file)

            # Canonicalize headers
            assign_df = canonicalize_headers(assign_df)
            validation_df = canonicalize_headers(validation_df)

            # Check required headers
            if not ensure_required(assign_df):
                st.error("❌ Invalid column names in assignment file.")
                st.caption(f"Detected columns: {list(assign_df.columns)}")
                st.stop()
            if not ensure_required(validation_df):
                st.error("❌ Backend validation file format error.")
                st.caption(f"Detected columns in validation: {list(validation_df.columns)}")
                st.stop()

            # Keep only required columns and clean values
            assign_df = clean_values(assign_df[REQUIRED].copy())
            validation_df = clean_values(validation_df[REQUIRED].copy())

            # Validate: each assignment row must exist in validation
            merged = assign_df.merge(
                validation_df.drop_duplicates(),
                how="left",
                on=REQUIRED,
                indicator=True
            )

            unmatched = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])
            matched = merged[merged["_merge"] == "both"].drop(columns=["_merge"])

            if unmatched.empty:
                st.success("🎉 The allocated seats are successfully completed!")
                st.balloons()
                # Get the directory of the current script
                current_dir = os.path.dirname(os.path.abspath(__file__))
                # Go up one level to project root, then into data folder
                validation_path = os.path.join(os.path.dirname(current_dir), 'data', 'validation_log.csv')
                log_file = pd.read_csv(validation_path)
                # Save group + timestamp
               # log_file = "./data/validation_log.csv"
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = pd.DataFrame([[group_name, timestamp]], columns=["Group", "Timestamp"])

                if os.path.exists(log_file):
                    log_entry.to_csv(log_file, mode="a", header=False, index=False)
                else:
                    log_entry.to_csv(log_file, mode="w", header=True, index=False)

                st.info(f"📌 Log saved: {group_name} at {timestamp}")

            else:
                total = len(assign_df)
                st.error("❌ Some records did not match.")
                st.write(f"Matched: **{len(matched)}/{total}**  ({round(len(matched)/total*100, 2)}%)")
                st.dataframe(matched)
                st.write(f"Unmatched: **{len(unmatched)}/{total}**  ({round(len(unmatched)/total*100, 2)}%)")
                st.dataframe(unmatched)

        except Exception as e:
            st.error(f"⚠️ Error while processing file: {e}")

    elif group_name == "Select Group" and assignment_file:
        st.warning("⚠️ Please select a group before uploading file.")
