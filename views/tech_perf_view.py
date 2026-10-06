import streamlit as st
import pandas as pd
from modules.db import fetch_data

def render():
    st.title("📈 Individual Technician Performance Reports")
    
    visits_df = fetch_data("Site_Visits")
    ratings_df = fetch_data("Employee_Ratings")
    
    if visits_df.empty:
        st.info("No operational data available yet.")
        return

    workers = visits_df['Worker_Name'].dropna().unique().tolist()
    if not workers:
        st.info("No worker records found.")
        return

    selected_worker = st.selectbox("Select Technician to View Performance", workers)
    
    w_visits = visits_df[visits_df['Worker_Name'] == selected_worker]
    
    c1, c2, c3, c4 = st.columns(4)
    total_v = len(w_visits)
    total_c = pd.to_numeric(w_visits['Amount_Collected'], errors='coerce').fillna(0).sum() if 'Amount_Collected' in w_visits.columns else 0.0
    total_h = pd.to_numeric(w_visits['Duration_Hours'], errors='coerce').fillna(0).sum() if 'Duration_Hours' in w_visits.columns else 0.0
    
    c1.metric("Total Visits Completed", total_v)
    c2.metric("Total Revenue Collected", f"₹{total_c:,.2f}")
    c3.metric("Total Hours on Field", f"{total_h:.1f} hrs")
    
    if not ratings_df.empty and 'Worker_Name' in ratings_df.columns:
        w_ratings = ratings_df[ratings_df['Worker_Name'].str.contains(selected_worker, na=False)]
        if not w_ratings.empty:
            avg_score = pd.to_numeric(w_ratings['Overall_Score'], errors='coerce').mean()
            c4.metric("Manager Overall Rating", f"{avg_score:.1f} / 10")
            st.subheader("⭐ Performance Scorecards Issued by Manager")
            st.dataframe(w_ratings[['Date', 'Manager_Name', 'Overall_Score', 'Notes']], use_container_width=True)
        else:
            c4.metric("Manager Overall Rating", "N/A")
            st.info("No rating scorecards published for this technician yet.")
    else:
        c4.metric("Manager Overall Rating", "N/A")