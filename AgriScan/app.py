import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# --- CONFIGURATION ---
st.set_page_config(page_title="Agri-Scan JITD", layout="wide")

# --- DATABASE (Shared Memory) ---
if 'db' not in st.session_state:
    # Initial mock data for the Admin Map
    st.session_state.db = pd.DataFrame([
        {'lat': 14.4644, 'lon': 75.9218, 'Status': 'Maize Rust'},
        {'lat': 14.4601, 'lon': 75.9105, 'Status': 'Healthy'}
    ])

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🍀 Emerge 2026")
page = st.sidebar.radio("Select Interface:", ["Farmer: Scan", "Admin: Dashboard"])

# --- INTERFACE 1: FARMER SCANNER ---
if page == "Farmer: Scan":
    st.title("🌱 Farmer Leaf Scanner")
    st.write("Upload a photo to detect disease and get a Kannada remedy.")

    file = st.file_uploader("Upload Leaf Photo", type=['jpg','png'])

    if file:
        img = Image.open(file)
        st.image(img, width=300)
        
        # This is where your AI logic will go. For now, we simulate a result:
        st.error("Detected: Maize Rust (ಮೆಕ್ಕೆಜೋಳದ ತುಕ್ಕು ರೋಗ)")
        st.info("Solution: Spray Hexaconazole 5% EC.")

        if st.button("Report to District Admin"):
            # Create a new random point near Davangere for the demo
            new_report = {
                'lat': 14.4644 + np.random.uniform(-0.02, 0.02),
                'lon': 75.9218 + np.random.uniform(-0.02, 0.02),
                'Status': 'Maize Rust'
            }
            # Update the database
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_report])], ignore_index=True)
            st.success("Report Sent! Switch to Admin View to see the updated map.")

# --- INTERFACE 2: ADMIN DASHBOARD ---
else:
    st.title("📊 District Disease Dashboard")
    st.write("Real-time tracking for Davangere Agriculture Officers.")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Total Scans", len(st.session_state.db))
        st.write("Recent Activity:")
        st.table(st.session_state.db.tail(5)) # Shows last 5 scans

    with col2:
        st.subheader("Regional Outbreak Map")
        st.map(st.session_state.db)