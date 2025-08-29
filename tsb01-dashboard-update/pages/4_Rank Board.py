import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page config
st.set_page_config(page_title="Rankers Board", page_icon=":material/leaderboard:", layout="wide")

# --- Rankers Board Page ---
st.header("🏆 Rankers Board")

try:
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go up one level to project root, then into data folder
    validation_path = os.path.join(os.path.dirname(current_dir), 'data', 'validation_log.csv')
    group_path = os.path.join(os.path.dirname(current_dir), 'data', 'group_details.csv')

    # Load validation log & group details
    log_df = pd.read_csv(validation_path)
    group_df = pd.read_csv(group_path)

    # Drop completely empty rows
    log_df = log_df.dropna(how="all")

    # Drop rows where Group or Timestamp is missing
    log_df = log_df.dropna(subset=["Group", "Timestamp"])

    # Parse timestamp safely
    log_df["Timestamp"] = pd.to_datetime(
        log_df["Timestamp"], 
        errors="coerce"
    )

    # Drop invalid timestamps
    log_df = log_df.dropna(subset=["Timestamp"])

    # Keep earliest submission per group
    earliest_log = (
        log_df.sort_values("Timestamp", ascending=True)   # earliest = smallest datetime
        .drop_duplicates("Group", keep="first")
    )

    # Sort again for ranking (earliest first = Rank 1)
    earliest_log = earliest_log.sort_values("Timestamp", ascending=True).reset_index(drop=True)

    # Pick top 3 rankers
    top3 = earliest_log.head(3)

    # Merge with group details
    rankers = top3.merge(group_df, on="Group", how="left")

    # Figure out which column holds member names
    member_col = None
    for col in ["Names", "Members", "Full Name", "Students"]:
        if col in group_df.columns:
            member_col = col
            break

    if not member_col:
        st.error("⚠️ Could not find a column for member names in group_details.csv")
        st.stop()

    # Display rankers with larger Rank size
    st.subheader("🥇 Top 3 Rankers Based on Earliest Uploads")
    for i, (grp, time) in enumerate(zip(top3["Group"], top3["Timestamp"])):
        members = rankers[rankers["Group"] == grp][member_col].tolist()
        st.markdown(f"""
        <h2 style="color:#2E86C1; font-size:28px;">🏅 Rank {i+1}: {grp}</h2>
        <p><b>⏰ Uploaded at:</b> {time}</p>
        <p><b>👥 Members:</b> {", ".join(members) if members else "No members listed"}</p>
        """, unsafe_allow_html=True)
        st.balloons()

except FileNotFoundError:
    st.error("⚠️ Validation log or group details file not found. Please check backend data.")
except Exception as e:
    st.error(f"⚠️ Error while processing Rankers Board: {e}")
