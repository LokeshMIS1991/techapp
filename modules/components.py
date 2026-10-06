import streamlit as st

def load_styles():
    """Injects responsive custom CSS and gradient button styling."""
    try:
        with open("assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def render_brand_header(user_info: dict = None):
    """Renders persistent header with brand identity and user role indicator."""
    c1, c2, c3 = st.columns([1, 4, 2])
    with c1:
        try:
            st.image("assets/logo.jpeg", width=110)
        except Exception:
            st.markdown("### ⚙️")
    with c2:
        st.markdown("<h2 style='margin:0; padding:0;'>SIDHARTH SHUTTER & AUTOMATION</h2>", unsafe_allow_html=True)
        st.caption("Field Operations & Smart Automation Management Engine")
    with c3:
        if user_info:
            st.markdown(f"**User:** {user_info['name']} (`{user_info['id']}`)")
            st.markdown(f"**Role:** <span class='brand-green'>{user_info['role']}</span>", unsafe_allow_html=True)
    st.divider()