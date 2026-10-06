import streamlit as st
import pandas as pd
from modules.db import fetch_data

def render():
    st.title("🔍 Multi-Visit Site Audit Trail & History")
    st.caption("Search any site to review all historic technician visits, work done, and attached photos.")
    
    visits_df = fetch_data("Site_Visits")
    
    if visits_df.empty:
        st.info("No site visit records available in database yet.")
        return

    sites_list = sorted(visits_df['Site_Name'].dropna().unique().tolist())
    selected_site = st.selectbox("Search or Select Site Name", ["-- Select Site --"] + sites_list)
    
    if selected_site != "-- Select Site --":
        site_records = visits_df[visits_df['Site_Name'] == selected_site].sort_values(by="Date", ascending=False)
        
        st.markdown(f"### Chronological Timeline for **{selected_site}** ({len(site_records)} Total Visits)")
        
        for idx, row in site_records.iterrows():
            with st.expander(f"📍 Visit Date: {row['Date']} | Tech: {row['Worker_Name']} (`{row['Worker_ID']}`) | Type: {row['Work_Type']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Dynamic Visit ID:** `{row['Visit_ID']}`")
                    st.write(f"**Duration:** {row.get('Duration_Hours', 'N/A')} Hours")
                    st.write(f"**Work Performed:** {row['Work_Details']}")
                with col2:
                    st.write(f"**Payment Status:** {row['Payment_Status']}")
                    if row['Payment_Status'] == 'Collected':
                        st.write(f"**Amount Collected:** ₹{row['Amount_Collected']}")
                    elif row['Payment_Status'] == 'Not Collected':
                        st.write(f"**Non-Collection Reason:** {row['Non_Collection_Reason']}")
                
                st.markdown("---")
                st.markdown("**📸 Photos & Documentation Links:**")
                p1, p2, p3 = st.columns(3)
                p1.write(f"**Pre-Work Photo:** {row.get('Pre_Work_Photo', 'N/A')}")
                p2.write(f"**Post-Work Photo:** {row.get('Post_Work_Photo', 'N/A')}")
                p3.write(f"**Signed Job Sheet:** {row.get('JobSheet_Photo', 'N/A')}")