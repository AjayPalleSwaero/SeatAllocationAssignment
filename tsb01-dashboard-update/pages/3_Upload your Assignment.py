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
    "uniqueid": "uniqueid",
    "uniquicid": "uniqueid",
    "unique_id": "uniqueid",
    "studentid": "uniqueid",
    "uid": "uniqueid",
    "name": "name",
    "fullname": "name",
    "studentname": "name",
    "collegeid": "collegeid",
    "collageid": "collegeid",
    "college": "collegeid",
    "institution": "institution",
    "college_name": "institution",
    "rank": "rank",
    "ranking": "rank",
    "prefnumber": "prefnumber",
    "preferenceid": "prefnumber",
    "preferenceorder": "prefnumber",
    "preference": "prefnumber",
    "pref": "prefnumber",
    "prefno": "prefnumber",
    "preference_no": "prefnumber",
    "gender": "gender",
    "sex": "gender",
    "caste": "caste",
    "cast": "caste",
    "category": "caste",
}

REQUIRED = ["uniqueid", "name", "gender", "caste", "rank", "collegeid", "institution", "prefnumber"]

def canonicalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to canonical set using synonyms; returns df with renamed columns."""
    rename_map = {}
    for col in df.columns:
        key = normalize_col(col)
        canonical = HEADER_SYNONYMS.get(key)
        if canonical:
            rename_map[col] = canonical
        else:
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
    2. Upload your **Completed Assignment File (CSV)**.  
    3. Upload your **Python Code File (.py)** for reference. 
    4.REQUIRED fileds "uniqueid", "name", "gender", "caste", "rank", "collegeid", "institution", "prefnumber"    
    5. Click **Submit** at the bottom to save your files and log.  
    6. Validation will be done automatically against backend data.
    """)

    # --- Step 1: Group selection ---
    group_name = st.selectbox("Select Your Group", ["Select Group"] + [f"Group - {i}" for i in range(1, 28)])

    # --- Step 2: File uploader (Assignment CSV) ---
    assignment_file = st.file_uploader("Upload Assignment Completed File (CSV)", type="csv", key="assign_file")

    # --- Step 3: Optional upload (Python code) ---
    py_file = st.file_uploader("Upload Your Python Code (.py)", type="py", key="code_file")
    if py_file:
        st.success(f"✅ Python file `{py_file.name}` uploaded successfully.")
        code_content = py_file.read().decode("utf-8")
        with st.expander("📂 View Uploaded Python Code"):
            st.code(code_content, language="python")

    # --- Step 4: Submit button ---
    if st.button("📥 Submit"):
        if group_name == "Select Group":
            st.warning("⚠️ Please select a group before submitting.")
        elif not assignment_file:
            st.warning("⚠️ Please upload your assignment CSV before submitting.")
        else:
            try:
                # Load uploaded assignment
                assign_df = pd.read_csv(assignment_file, dtype=str)

                # Load backend validation file
                current_dir = os.path.dirname(os.path.abspath(__file__))
                validation_file = os.path.join(os.path.dirname(current_dir), 'data', 'validation_file.csv')
                validation_df = pd.read_csv(validation_file)

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
                else:
                    total = len(assign_df)
                    st.error("❌ Some records did not match.")
                    st.write(f"Matched: **{len(matched)}/{total}**  ({round(len(matched)/total*100, 2)}%)")
                    st.dataframe(matched[REQUIRED])
                    st.write(f"Unmatched: **{len(unmatched)}/{total}**  ({round(len(unmatched)/total*100, 2)}%)")
                    st.dataframe(unmatched[REQUIRED])

                # --- Save submissions in group folder ---
                group_folder = os.path.join(os.path.dirname(current_dir), "data", "submissions", group_name.replace(" ", "_"))
                os.makedirs(group_folder, exist_ok=True)

                # Save assignment file
                csv_path = os.path.join(group_folder, f"{group_name}_submission.csv")
                assign_df.to_csv(csv_path, index=False)
                st.info(f"📂 Assignment CSV saved to `{csv_path}`")

                # Save Python file if uploaded
                if py_file:
                    py_path = os.path.join(group_folder, f"{group_name}_code.py")
                    with open(py_path, "w", encoding="utf-8") as f:
                        f.write(code_content)
                    st.info(f"📂 Python file saved to `{py_path}`")

                # Save log
                validation_log = os.path.join(os.path.dirname(current_dir), 'data', 'validation_log.csv')
                os.makedirs(os.path.dirname(validation_log), exist_ok=True)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = pd.DataFrame([[group_name, timestamp]], columns=["Group", "Timestamp"])

                if os.path.exists(validation_log):
                    log_entry.to_csv(validation_log, mode="a", header=False, index=False)
                else:
                    log_entry.to_csv(validation_log, mode="w", header=True, index=False)

                st.success(f"📌 Log saved for {group_name} at {timestamp}")

            except Exception as e:
                st.error(f"⚠️ Error while processing file: {e}")
