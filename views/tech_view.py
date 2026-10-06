import streamlit as st
import pandas as pd
from modules.db import fetch_data, append_row, generate_visit_id
from modules.drive_helper import get_drive_service, get_or_create_site_folder, upload_photo_to_drive

def render(user_info: dict):
    st.title("👷 Technician / Worker Portal")
    
    today_str = pd.Timestamp.now().strftime("%Y-%m-%d")
    visits_df = fetch_data("Site_Visits")
    
    # Calculate daily visit count
    if not visits_df.empty and 'Date' in visits_df.columns:
        worker_today = visits_df[(visits_df['Worker_ID'] == user_info['id']) & (visits_df['Date'] == today_str)]
        daily_count = len(worker_today) + 1
    else:
        daily_count = 1

    visit_id = generate_visit_id(user_info['id'], daily_count)
    st.info(f"**Today's Visits Completed:** {daily_count - 1} | **Current Dynamic Visit ID:** `{visit_id}`")
    
    with st.form("job_sheet_form", clear_on_submit=True):
        st.subheader("📋 Daily Site Job Sheet Entry")
        
        c1, c2 = st.columns(2)
        with c1:
            site_name = st.text_input("Site / Customer Name*", placeholder="e.g. Apex Industrial Estate")
            site_address = st.text_area("Site Address*", placeholder="Enter full address")
        with c2:
            work_type = st.selectbox("Type of Work*", ["Service / Repair", "New Installation"])
            duration = st.number_input("Time Spent on Site (Hours)*", min_value=0.5, max_value=24.0, step=0.5)

        # Payment Logic
        payment_status = "N/A"
        amount_collected = 0.0
        reason_not_collected = "N/A"
        
        if work_type == "Service / Repair":
            st.markdown("---")
            st.subheader("💰 Service Payment Collection")
            payment_status = st.selectbox("Payment Status*", ["Collected", "Not Collected"])
            
            if payment_status == "Collected":
                amount_collected = st.number_input("Amount Collected (₹)*", min_value=0.0, step=100.0)
            else:
                reason_not_collected = st.selectbox("Reason for Non-Collection*", [
                    "Client requested official invoice first",
                    "Online bank transfer pending",
                    "Owner / Decision maker not present",
                    "Work incomplete / Follow-up required",
                    "Other (Specify in notes)"
                ])
        
        st.markdown("---")
        work_details = st.text_area("Detailed Summary of Work Done*", placeholder="Specify motors repaired, sensors calibrated, or shutters installed...")
        
        # MANDATORY PHOTOS
        st.markdown("### 📸 Mandatory Site Photos")
        p1, p2, p3 = st.columns(3)
        with p1:
            pre_photo = st.file_uploader("Pre-Work Photo (Before Start)*", type=["jpg", "png", "jpeg"])
        with p2:
            post_photo = st.file_uploader("Post-Work Photo (After Completion)*", type=["jpg", "png", "jpeg"])
        with p3:
            jobsheet_photo = st.file_uploader("Signed Job Sheet Photo*", type=["jpg", "png", "jpeg"])
            
        submitted = st.form_submit_button("Submit Job Sheet")
        
        if submitted:
            if not site_name or not pre_photo or not post_photo or not jobsheet_photo or not work_details:
                st.error("⚠ Mandatory Enforcement: You MUST fill all required fields (*) and upload Pre-Work, Post-Work, AND Job Sheet photos!")
            else:
                main_folder_id = st.secrets.get("connections", {}).get("gsheets", {}).get("drive_parent_folder_id", None)
                drive_service = get_drive_service()
                
                if drive_service and main_folder_id:
                    site_folder_id = get_or_create_site_folder(drive_service, main_folder_id, site_name)
                    pre_url = upload_photo_to_drive(drive_service, site_folder_id, pre_photo, f"{visit_id}_PreWork")
                    post_url = upload_photo_to_drive(drive_service, site_folder_id, post_photo, f"{visit_id}_PostWork")
                    sheet_url = upload_photo_to_drive(drive_service, site_folder_id, jobsheet_photo, f"{visit_id}_JobSheet")
                else:
                    pre_url, post_url, sheet_url = pre_photo.name, post_photo.name, jobsheet_photo.name

                record = {
                    "Visit_ID": visit_id,
                    "Date": today_str,
                    "Worker_ID": user_info['id'],
                    "Worker_Name": user_info['name'],
                    "Site_Name": site_name.strip(),
                    "Site_Address": site_address.strip(),
                    "Work_Type": work_type,
                    "Payment_Status": payment_status,
                    "Amount_Collected": amount_collected,
                    "Non_Collection_Reason": reason_not_collected,
                    "Duration_Hours": duration,
                    "Work_Details": work_details,
                    "Pre_Work_Photo": pre_url,
                    "Post_Work_Photo": post_url,
                    "JobSheet_Photo": sheet_url,
                    "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                append_row("Site_Visits", record)
                st.success(f"Job Sheet Successfully Uploaded! Visit ID: {visit_id}")
                st.rerun()