import streamlit as st
from modules.components import load_styles, render_brand_header
from modules.auth import authenticate_user
from views import tech_view, manager_view, admin_view, tech_perf_view, site_history_view

st.set_page_config(
    page_title="Sidharth Shutter & Automation",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS & Gradient Themes
load_styles()

# Authentication Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_info = None

# --- LOGIN SCREEN ---
if not st.session_state.authenticated:
    render_brand_header()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.subheader("🔐 System Login")
            login_id = st.text_input("User ID or Username", placeholder="e.g. ADM001, MGR001, W001, parvesh")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                user = authenticate_user(login_id, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_info = user
                    st.success(f"Welcome, {user['name']}!")
                    st.rerun()
                else:
                    st.error("Invalid Credentials. Please check your System ID / Username or Password.")

# --- NAVIGATION ROUTER ---
else:
    user = st.session_state.user_info
    render_brand_header(user)
    
    st.sidebar.title("Navigation Menu")
    
    # Role-Based Permissions
    if user['role'] == "Worker":
        menu = ["Daily Job Sheet Entry", "Site Timeline Audit", "My Performance Report"]
    elif user['role'] == "Manager":
        menu = ["Manager Scoreboard", "Technician Performance Reports", "Site Timeline Audit", "Daily Job Sheet Entry"]
    else:  # Admin
        menu = [
            "Admin Dashboard & Financials", 
            "Technician Performance Reports", 
            "Manager Scoreboard", 
            "Site Timeline Audit", 
            "Daily Job Sheet Entry"
        ]
        
    choice = st.sidebar.radio("Go to:", menu)
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_info = None
        st.rerun()

    # View Routing
    if choice == "Daily Job Sheet Entry":
        tech_view.render(user)
    elif choice == "Manager Scoreboard":
        manager_view.render(user)
    elif choice == "Admin Dashboard & Financials":
        admin_view.render(user)
    elif choice == "Technician Performance Reports" or choice == "My Performance Report":
        tech_perf_view.render()
    elif choice == "Site Timeline Audit":
        site_history_view.render()