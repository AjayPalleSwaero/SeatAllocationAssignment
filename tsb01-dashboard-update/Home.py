import streamlit as st
import streamlit as st
import os

# Page config
st.set_page_config(page_title="Data Science Training Program @ RGUKT Basar", layout="wide")

# Title
st.title("📊 Data Science Training Program @ RGUKT Basar")
st.markdown("### A TANLA Foundation CSR Initiative | Implemented by Swinfy Solutions")

# Introduction
st.markdown("""
Imagine walking into a place where you don’t just sit through boring lectures, but actually build apps, 
train AI models, and solve problems that matter. That’s exactly what this program feels like.  

The **Data Science Training Program at RGUKT Basara**, launched under the CSR initiative of **TANLA Foundation** 
and implemented by **Swinfy Solutions Pvt Ltd**, is designed to equip students with industry-relevant 
skills in **Data Science, AI, and Analytics**.
""")

st.markdown("""
✨ Here, every project makes you go *“Wow, I never thought I could do this!”*  
Whether it’s creating a chatbot, designing a smart website, or analyzing real data, you see your ideas come alive.  

At **Swinfy**, learning feels less like studying and more like being part of a mission to use technology to change the world 🌍.  

It’s not about memorizing. It’s about **building, experimenting, breaking things, fixing them again, and celebrating when it finally works**.  
That *moment of excitement* when your code runs, your app loads, or your AI predicts correctly, is what makes this program special.  
""")

st.success("Here, you don’t just learn skills – you discover your power to create, innovate, and dream bigger than ever before!")

# Project Assignment
st.header("🎯 Project Assignment: Student College Allotment System")

st.markdown("""
You are part of the **Intermediate Education Board’s Team**.  
Every year, thousands of students apply for admission into colleges after their 10th class (SSC exams).  
The admission process depends on:
- Student’s **Rank**  
- **Reservation category** (SC, SC-CC, ST, BC, Minority, OC)  
- **Student’s preferred colleges**  
- **Seat availability** in each institution  

Your task is to **simulate this real admission process** using data and logic.
""")

# Data Provided
st.subheader("📂 Data Provided")
st.markdown("""
**Students**  
`UniqueID | Name | Gender | Category | Rank`  

**Preferences**  
`CollegeID | PrefNumber | UniqueID`  

**Seats**  
`CollegeID | Institution | Total Seats | Total Admitted | Orphan Quota | PHC Quota | SC | SC-CC | ST | BC | Minority | OC`  
""")

# Process Flow
st.subheader("⚙️ Process Flow")
st.markdown("""
1. Sort students by rank (**Rank 1 first**)  
2. For each student, check their 1st preference college  
3. If a seat is available in their category → **Allot & reduce seat count**  
4. If not → Move to the **next preference**  
5. If none of the preferences have a seat → Mark as **No College Available**  
6. Continue until all students are processed  
""")

# Example Walkthrough
st.subheader("📌 Example Walkthrough")
st.markdown("""
**Student:** Ramesh (Rank = 1, Category = BC)  
Preferences: College A → College B → College C  

- College A: No BC seats → ❌ Not allotted  
- College B: 2 BC seats available → ✅ Allotted  
- Update College B’s BC seats → Now 1 left  

**Result:** Ramesh → College B (Preference Used = 2)  
""")

# Tasks
st.subheader("📝 Your Tasks")
st.markdown("""
**Step 1 – Manual Simulation**  
Do this process manually for the first 10 students. Record results in a table:  

| Student Name | Allotted College | Preference Order Used |  

**Step 2 – Automation with Python**  
Write a Python program to:  
- Sort students by rank  
- Iterate through preferences  
- Allocate a seat if available  
- Update seat count  
- Handle *No college available* cases  
""")

# Expected Output
st.subheader("📊 Expected Output Format")
st.table({
    "Student_ID": [101, 102, 103],
    "Name": ["Ramesh", "Sita", "Ravi"],
    "Category": ["BC", "SC", "OC"],
    "Rank": [1, 2, 3],
    "Allotted College": ["College B", "College A", "No College Available"],
    "Preference_Order_Used": [2, 1, "-"]
})

# Process Flow Diagram
st.subheader("🔄 Process Flow Diagram")
st.code("""
flowchart TD
    A[Start with Student List] --> B[Sort Students by Rank]
    B --> C[Pick Next Student]
    C --> D[Check 1st Preference College]
    D --> E{Seat Available in Category?}
    E -- Yes --> F[Allot College & Update Seats]
    E -- No --> G[Check Next Preference]
    G --> E
    E -- None Left --> H[Mark: No College Available]
    F --> I[Move to Next Student]
    H --> I
    I --> C
""", language="markdown")

# Learning Outcomes
st.subheader("🎓 Learning Outcomes")
st.markdown("""
- Understand logic behind real admission systems (EAMCET/NEET Counselling)  
- Practice **data filtering, iteration, dataset updates**  
- Learn to combine **manual + automation** approaches  
- Build a **real-world allocation system from scratch**  
""")




