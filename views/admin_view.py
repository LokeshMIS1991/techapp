import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.db import fetch_data

def render(user_info: dict):
    st.title("👑 Master Admin Portal & Financial KPIs")
    
    visits_df = fetch_data("Site_Visits")
    
    st.subheader("📅 Financial & Operational Date Range")
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        filter_preset = st.selectbox("Preset Ranges", [
            "Current Month", "Last 7 Days", "Last 15 Days", "Last 30 Days", "Last 3 Months", "Custom Date Range"
        ])
        
    today = datetime.now().date()
    if filter_preset == "Last 7 Days":
        start_date, end_date = today - timedelta(days=7), today
    elif filter_preset == "Last 15 Days":
        start_date, end_date = today - timedelta(days=15), today
    elif filter_preset == "Current Month":
        start_date, end_date = today.replace(day=1), today
    elif filter_preset == "Last 3 Months":
        start_date, end_date = today - timedelta(days=90), today
    else:
        with f_col2:
            start_date = st.date_input("Start Date", today - timedelta(days=30))
            end_date = st.date_input("End Date", today)

    if not visits_df.empty and 'Amount_Collected' in visits_df.columns:
        total_collected = pd.to_numeric(visits_df['Amount_Collected'], errors='coerce').fillna(0).sum()
        total_visits = len(visits_df)
        success_collections = len(visits_df[visits_df['Payment_Status'] == 'Collected'])
        pending_collections = len(visits_df[visits_df['Payment_Status'] == 'Not Collected'])
    else:
        total_collected, total_visits, success_collections, pending_collections = 0.0, 0, 0, 0

    st.markdown("### 📊 Financial & Collection KPIs")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Collected (All Techs)", f"₹{total_collected:,.2f}")
    k2.metric("Total Sites Visited", total_visits)
    k3.metric("Successful Payment Sites", success_collections)
    k4.metric("Pending Payment Sites", pending_collections)

    st.divider()

    st.subheader("🔍 Interactive Data Drill-Down")
    drill_choice = st.radio("Select View Mode:", ["All Visits Master List", "⚠️ Pending Payment Sites Detail"], horizontal=True)

    if drill_choice == "⚠️ Pending Payment Sites Detail":
        st.markdown("### 📋 Detailed List of Sites with Pending Service Payments")
        if not visits_df.empty:
            pending_df = visits_df[visits_df['Payment_Status'] == 'Not Collected']
            if not pending_df.empty:
                st.dataframe(
                    pending_df[['Visit_ID', 'Date', 'Site_Name', 'Worker_Name', 'Non_Collection_Reason', 'Work_Details']],
                    use_container_width=True
                )
            else:
                st.success("🎉 No pending payments! All service visits are collected.")
        else:
            st.info("No visit records found.")
    else:
        if not visits_df.empty:
            st.dataframe(visits_df, use_container_width=True)