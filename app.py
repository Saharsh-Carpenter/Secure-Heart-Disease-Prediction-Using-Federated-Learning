import streamlit as st
import sqlite3
import hashlib
import numpy as np
from tensorflow.keras.models import load_model

# Page setting
st.set_page_config(page_title="Heart Disease Predictor", layout="centered")

# --- DATABASE & SECURITY FUNCTIONS ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def create_usertable():
    conn = sqlite3.connect('hospital_users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT UNIQUE, password TEXT)')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('hospital_users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO userstable(username, password) VALUES (?,?)', (username, password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False 
    conn.close()
    return success

def login_user(username, password):
    conn = sqlite3.connect('hospital_users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    conn.close()
    return data

create_usertable()

# --- SESSION STATES ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = ""
if 'auth_mode' not in st.session_state:
    st.session_state['auth_mode'] = 'login'


# --- LOGIN & SIGNUP PORTAL ---

if not st.session_state['logged_in']:
    st.markdown("<h2 style='text-align: center;'>🏥 Hospital Portal</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 1. LOGIN PAGE VIEW
    if st.session_state['auth_mode'] == 'login':
        st.subheader("Secure Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
        if st.button("Login", type="primary"):
            hashed_pswd = make_hashes(password)
            result = login_user(username, hashed_pswd)
            
            if result:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = username
                st.rerun()
            else:
                st.error("Incorrect Username or Password")
                
        st.write("")
        st.write("Don't have an account?")
        if st.button("Create an account"):
            st.session_state['auth_mode'] = 'signup'
            st.rerun()

    # 2. SIGNUP PAGE VIEW
    elif st.session_state['auth_mode'] == 'signup':
        st.subheader("Create a New Account")
        new_user = st.text_input("Choose Username")
        new_password = st.text_input("Choose Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password') 
        
        if st.button("Sign Up", type="primary"):
            if new_user == "" or new_password == "" or confirm_password == "":
                st.warning("Please fill all fields.")
            elif new_password != confirm_password: # Validation check
                st.error("Passwords do not match!")
            else:
                hashed_new_password = make_hashes(new_password)
                if add_user(new_user, hashed_new_password):
                    st.success("Account Created! You can now login.")
                    st.session_state['auth_mode'] = 'login'
                    st.rerun()
                else:
                    st.error("Username already exists!")
                    
        st.write("")
        st.write("Already have an account?")
        if st.button("Back to Login"):
            st.session_state['auth_mode'] = 'login'
            st.rerun()
            
    st.stop()


# --- MAIN HOSPITAL SYSTEM ---

col_header1, col_header2 = st.columns([8, 2])
with col_header1:
    st.write(f"Logged in as: **{st.session_state['current_user']}** ✅")
with col_header2:
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['current_user'] = ""
        st.rerun()

st.markdown("<h2 style='text-align: center;'>🫀 Heart Disease Prediction System</h2>", unsafe_allow_html=True)
st.write("Enter patient details to run the federated ML prediction.")
st.markdown("---")

@st.cache_resource
def load_my_model():
    return load_model('heart_disease_model.h5') 

try:
    model = load_my_model()
except:
    st.error("Model file not found!")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Patient Age", min_value=1, max_value=120, value=50)
    sex = st.selectbox("Sex", options=["Male", "Female"])
    cp = st.selectbox("Chest Pain Type (0-3)", options=[0, 1, 2, 3])
    trestbps = st.number_input("Resting Blood Pressure (mm Hg)", value=120)
    chol = st.number_input("Cholesterol (mg/dl)", value=200)
    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl?", options=["No", "Yes"])
    restecg = st.selectbox("Resting ECG Results (0-2)", options=[0, 1, 2])

with col2:
    thalach = st.number_input("Maximum Heart Rate Achieved", value=150)
    exang = st.selectbox("Exercise Induced Angina?", options=["No", "Yes"])
    oldpeak = st.number_input("Oldpeak (ST depression)", value=1.0)
    slope = st.selectbox("Slope of Peak Exercise (0-2)", options=[0, 1, 2])
    ca = st.selectbox("Number of Major Vessels (0-3)", options=[0, 1, 2, 3])
    thal = st.selectbox("Thalassemia Type (1-3)", options=[1, 2, 3])

sex_val = 1 if sex == "Male" else 0
fbs_val = 1 if fbs == "Yes" else 0
exang_val = 1 if exang == "Yes" else 0

st.markdown("---")

if st.button("Predict Heart Disease Risk", type="primary"):
    input_features = np.array([[age, sex_val, cp, trestbps, chol, fbs_val, restecg, thalach, exang_val, oldpeak, slope, ca, thal]])
    
    try:
        prediction = model.predict(input_features)
        st.markdown("<br>", unsafe_allow_html=True)
        if prediction[0][0] > 0.5:
            st.error("⚠️ Prediction: High Risk of Heart Disease Detected.")
        else:
            st.success("✅ Prediction: Low Risk. No Heart Disease Detected.")
    except Exception as e:
        st.warning(f"Error: {e}")