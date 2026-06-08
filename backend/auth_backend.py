import os 
import requests  
import streamlit as st 
import firebase_admin
from firebase_admin import credentials, auth, firestore

current_dir = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(current_dir, "firebase_key.json")

if not firebase_admin._apps:
    try:

        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)

    except Exception as e:

        st.error(f"Error initializing Firebase key: {e}")

db = firestore.client(database_id="db50")

# Automatically reads from your hidden .streamlit/secrets.toml file
apiKey = st.secrets["apiKey"]

def verify_password_via_rest(email, password):

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={apiKey}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True 
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("localId")
    else:

        return None

def sign_in_or_register_email(email, password, mode="Login"):

    try:
        if mode == "Login":

            uid = verify_password_via_rest(email, password)
            if uid:
                return uid
            else:
                st.error("Invalid email or password.")
                return None
            
        else:
            # Mode is "Sign Up" -> Create a brand new account securely
            try:
                user = auth.create_user(email=email, password=password)
                return user.uid
            except Exception as e:
                st.error(f"Registration failed: {e}")
                return None 
    except Exception as e:
        st.error(f"Authentication system error: {e}")
        return None
    
def process_clear_logout():

    st.session_state.auth_status = None
    st.session_state.user_profile = None
    st.rerun()


def save_chat_message(uid, session_id, role, content):

    try:
        chat_ref = db.collection("user").document(uid).collection("sessions").document(session_id)

        chat_ref.set({
            "messages": firestore.ArrayUnion([{"role": role, "content": content}]) 
        }, merge=True)
    except Exception as e:
        print(f"Error saving message: {e}")

def load_user_sessions(uid):

    sessions_dict = {}
    try:
        sessions_ref = db.collection("user").document(uid).collection("sessions").stream()
        for doc in sessions_ref:
            sessions_dict[doc.id] = doc.to_dict().get("messages", [])

        if not sessions_dict:
            sessions_dict = {"Default Chat": []}

    except Exception as e:
        print(f"Error loading sessions: {e}")
        sessions_dict = {"Default Chat": []}
    
    return sessions_dict