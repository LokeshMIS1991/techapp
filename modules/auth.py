import streamlit as st
from modules.db import fetch_data

def authenticate_user(login_identifier: str, password_input: str):
    """
    Authenticates by matching login_identifier against System ID (e.g. ADM001, MGR001, W001)
    OR Username (e.g. admin, manager, parvesh).
    """
    users_df = fetch_data("Users")
    
    if users_df.empty:
        # Default Mock Credentials for immediate setup/testing
        mock_users = {
            "ADM001": {"username": "admin", "password": "123", "role": "Admin", "name": "System Admin", "id": "ADM001"},
            "MGR001": {"username": "manager", "password": "123", "role": "Manager", "name": "Operations Manager", "id": "MGR001"},
            "W001": {"username": "parvesh", "password": "123", "role": "Worker", "name": "Parvesh Sharma", "id": "W001"},
            "W002": {"username": "amit", "password": "123", "role": "Worker", "name": "Amit Kumar", "id": "W002"},
        }
        
        login_key = login_identifier.strip().upper()
        for uid, user in mock_users.items():
            if (login_key == uid or login_identifier.strip().lower() == user["username"].lower()) and password_input == user["password"]:
                return user
        return None

    clean_id = login_identifier.strip().lower()
    match = users_df[
        (users_df['User_ID'].astype(str).str.lower() == clean_id) | 
        (users_df['Username'].astype(str).str.lower() == clean_id)
    ]
    
    if not match.empty and str(match.iloc[0]['Password']) == password_input:
        user_row = match.iloc[0]
        return {
            "id": user_row['User_ID'],
            "username": user_row['Username'],
            "role": user_row['Role'],
            "name": user_row['Full_Name']
        }
    
    return None