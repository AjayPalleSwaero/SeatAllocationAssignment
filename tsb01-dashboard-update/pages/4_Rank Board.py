import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Rankers Board", page_icon=":material/leaderboard:", layout="wide")

# Sidebar navigation
page = st.sidebar.radio("Select Page", ["Rankers Board"], key="main_menu")

# --- Rankers Board Page ---
if page == "Rankers Board":
    st.header("🏆 Rankers Board")

    try:
        # Load validation log
        log_file = "./data/validation_log.csv"
        group_file = "./data/Group_details.csv"

        log_df = pd.read_csv(log_file)
        group_df = pd.read_csv(group_file)

        # Ensure proper timestamp type
        log_df["Timestamp"] = pd.to_datetime(log_df["Timestamp"])

        # Take only the latest submission per group
        latest_log = log_df.sort_values("Timestamp", ascending=False).drop_duplicates("Group", keep="first")

        # Sort again by latest timestamp (rank order)
        latest_log = latest_log.sort_values("Timestamp", ascending=False).reset_index(drop=True)

        # Pick top 3 rankers
        top3 = latest_log.head(3)

        # Merge with group details
        rankers = top3.merge(group_df, on="Group", how="left")

        # Display rankers
        st.subheader("🥇 Top 3 Rankers Based on Latest Uploads")
        for i, (grp, time) in enumerate(zip(top3["Group"], top3["Timestamp"])):
            members = rankers[rankers["Group"] == grp]["Names"].tolist()
            st.markdown(f"""
            **Rank {i+1}: {grp}**  
            ⏰ Uploaded at: {time}  
            👥 Members: {", ".join(members) if members else "No members listed"}  
            """)
            st.balloons()
    except FileNotFoundError:
        st.error("⚠️ Validation log or group details file not found. Please check backend data.")
    except Exception as e:
        st.error(f"⚠️ Error while processing Rankers Board: {e}")
