import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    """Initializes Google Drive API service using Streamlit Secrets."""
    try:
        creds_dict = dict(st.secrets["connections"]["gsheets"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        st.warning(f"Google Drive API Notice: {e}")
        return None

def get_or_create_site_folder(service, parent_folder_id, site_name):
    """
    Checks if a site-specific folder exists in Drive;
    Creates a new folder if it doesn't exist.
    """
    if not service or not parent_folder_id:
        return None
        
    clean_site_name = f"Site_{site_name.strip().replace(' ', '_')}"
    query = f"'{parent_folder_id}' in parents and name = '{clean_site_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    
    try:
        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])
        
        if files:
            return files[0]['id']
        else:
            file_metadata = {
                'name': clean_site_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id]
            }
            folder = service.files().create(body=file_metadata, fields='id').execute()
            return folder.get('id')
    except Exception as e:
        st.error(f"Error managing Google Drive folders: {e}")
        return None

def upload_photo_to_drive(service, site_folder_id, uploaded_file, file_prefix):
    """Uploads an uploaded file directly to the site folder in Google Drive."""
    if not service or not site_folder_id or not uploaded_file:
        return uploaded_file.name if uploaded_file else "N/A"
        
    try:
        file_extension = uploaded_file.name.split('.')[-1]
        file_name = f"{file_prefix}.{file_extension}"
        
        file_metadata = {
            'name': file_name,
            'parents': [site_folder_id]
        }
        
        media = MediaIoBaseUpload(io.BytesIO(uploaded_file.getvalue()), mimetype=uploaded_file.type, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        return file.get('webViewLink', file_name)
    except Exception as e:
        st.warning(f"Failed to upload {uploaded_file.name} to Drive. Saving filename locally instead.")
        return uploaded_file.name