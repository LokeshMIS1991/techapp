import streamlit as st
import pandas as pd
from modules.db import fetch_data, append_row
from modules.ratings import compute_auto_rating_suggestion

def render(user_info: dict):
    st.title("📊 Manager Scoreboard & Operational Review")
    
    visits_df = fetch_data("Site_Visits")
    
    tab1, tab2 = st.tabs(["⭐ Employee Scoreboard & Rating Panel", "📋 Daily Site Operations Log"])
    
    with tab1:
        st.subheader("Evaluate Technician Performance")
        
        tech_list = ["W001 - Parvesh Sharma", "W002 - Amit Kumar"]
        selected_tech = st.selectbox("Select Technician*", tech_list)
        tech_id = selected_tech.split(" - ")[0]
        
        suggested_score = compute_auto_rating_suggestion(tech_id, visits_df)
        st.info(f"💡 **System Auto-Suggested Rating for {selected_tech}:** `{suggested_score} / 10` (Based on photo uploads & payment collections)")
        
        c1, c2 = st.columns(2)
        with c1:
            punctuality = st.slider("⏱️ Punctuality & Timeliness", 1, 10, int(suggested_score))
            efficiency = st.slider("🛠️ Technical Work Efficiency", 1, 10, int(suggested_score))
            activeness = st.slider("⚡ Activeness & Initiative", 1, 10, int(suggested_score))
        with c2:
            professionalism = st.slider("💼 Client Professionalism", 1, 10, int(suggested_score))
            reporting = st.slider("📋 Job Sheet & Photo Accuracy", 1, 10, int(suggested_score))
            
        manager_notes = st.text_area("Manager Feedback / Review Notes", placeholder="Provide specific feedback...")
        
        final_score = round((punctuality + efficiency + activeness + professionalism + reporting) / 5.0, 1)
        st.metric("Final Evaluation Score", f"{final_score} / 10")
        
        if st.button("Publish Scorecard to Dashboard"):
            rating_record = {
                "Rating_ID": f"RAT-{pd.Timestamp.now().strftime('%Y%m%d%H%M')}",
                "Date": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "Manager_Name": user_info['name'],
                "Worker_ID": tech_id,
                "Worker_Name": selected_tech,
                "Punctuality": punctuality,
                "Efficiency": efficiency,
                "Activeness": activeness,
                "Professionalism": professionalism,
                "Reporting": reporting,
                "Overall_Score": final_score,
                "Notes": manager_notes
            }
            append_row("Employee_Ratings", rating_record)
            st.success(f"Scorecard published! {selected_tech} rated {final_score}/10.")

    with tab2:
        st.subheader("Field Activity Summary")
        if not visits_df.empty:
            st.dataframe(visits_df, use_container_width=True)
        else:
            st.info("No site visit records found.")