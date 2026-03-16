import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Agri-Scan Pro",
    page_icon="🌱",
    layout="centered", # Better for mobile view
    initial_sidebar_state="collapsed"
)

# --- 2. SHARED DATABASE (Temporary) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {'Time': '10:30 AM', 'lat': 14.4644, 'lon': 75.9218, 'Crop': 'Maize', 'Disease': 'Rust'},
        {'Time': '11:15 AM', 'lat': 14.4601, 'lon': 75.9105, 'Crop': 'Paddy', 'Disease': 'Blast'}
    ])

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🍀 Agri-Scan Menu")
page = st.sidebar.radio("Go to:", ["My Profile", "Scan Crop", "District Map"])

# --- 4. INTERFACE 1: FARMER PROFILE ---
if page == "My Profile":
    st.title("👤 Farmer Details")
    
    # Farmer ID Card
    with st.container(border=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            # Placeholder for User Photo
            st.image("https://cdn-icons-png.flaticon.com/512/1995/1995531.png", width=80)
        with col2:
            st.subheader("Vinithkumar S")
            st.caption("Computer Science (Data Science) Student")
            st.write("📍 **Region:** Davangere, KA")
            st.write("🆔 **ID:** BIET25CD046")

    st.subheader("Your Activity History")
    st.dataframe(st.session_state.db, use_container_width=True, hide_index=True)

# --- 5. INTERFACE 2: SCAN CROP (The "App" Part) ---
elif page == "Scan Crop":
    st.title("📷 Disease Scanner")
    st.write("Point your camera at the infected leaf.")

    # Using camera_input makes it feel like a real mobile app
    img_file = st.camera_input("Take a Photo")

    if img_file:
        # Display the captured image
        img = Image.open(img_file)
        st.image(img, caption="Captured Leaf", use_container_width=True)
        
        # --- LOGIC SECTION ---
        # Simulated Result (In the hackathon, put your model prediction here)
        disease = "Paddy Blast"
        kannada_name = "ಭತ್ತದ ಬೆಂಕಿ ರೋಗ"
        remedy = "Spray Tricyclazole 75 WP at 0.6 g/liter."
        
        with st.container(border=True):
            st.error(f"**Detected:** {disease}")
            st.warning(f"**ಕನ್ನಡದಲ್ಲಿ:** {kannada_name}")
            st.info(f"**Remedy:** {remedy}")

        if st.button("📢 Report to Admin", use_container_width=True):
            # Create a new GPS report near Davangere
            new_report = {
                'Time': datetime.datetime.now().strftime("%H:%M"),
                'lat': 14.4644 + np.random.uniform(-0.01, 0.01),
                'lon': 75.9218 + np.random.uniform(-0.01, 0.01),
                'Crop': 'Paddy',
                'Disease': 'Blast'
            }
            # Add to Database
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_report])], ignore_index=True)
            st.success("Report successfully sent to District Dashboard!")

# --- 6. INTERFACE 3: ADMIN DASHBOARD (Location Map) ---
elif page == "District Map":
    st.title("📊 Disease Tracker")
    st.write("Monitoring Davangere District Crop Health")

    # Map showing all reported points
    st.map(st.session_state.db)
    
    st.subheader("Live Outbreak List")
    st.table(st.session_state.db[['Time', 'Crop', 'Disease']])
