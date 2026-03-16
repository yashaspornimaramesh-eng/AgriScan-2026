import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Agri-Scan", layout="wide")

# --- DATABASE FOR MULTIPLE FARMERS ---
if 'farmers_db' not in st.session_state:
    st.session_state.farmers_db = []

# --- SIDEBAR ---
st.sidebar.title("🍀 Agri-Scan")
menu = st.sidebar.radio("Menu", ["Register Farmer", "View Farmers", "Farmer: Scan", "Admin: Dashboard"])

# --- INTERFACE 1: REGISTRATION ---
if menu == "Register Farmer":
    st.title("📝 Farmer Registration")
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        place = st.text_input("Village / Place")
        crop = st.selectbox("Crop Type", ["Maize", "Paddy", "Cotton", "Tomato", "Other"])
        submit = st.form_submit_button("Register & Save")
        
        if submit and name:
            st.session_state.farmers_db.append({"Name": name, "Place": place, "Crop": crop})
            st.success(f"Registered {name} successfully!")

# --- INTERFACE 2: VIEW ALL FARMERS ---
elif menu == "View Farmers":
    st.title("👥 Registered Farmers")
    if st.session_state.farmers_db:
        df = pd.DataFrame(st.session_state.farmers_db)
        st.table(df)
    else:
        st.info("No farmers registered yet.")

# --- (Rest of your Scan and Admin code follows here) ---
