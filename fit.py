import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from PIL import Image

# ---- PAGE CONFIGURATION ----
st.set_page_config(page_title="Personal Fitness Tracker", page_icon="💪", layout="wide")

# ---- ADD BACKGROUND IMAGE ----
def set_bg(image_file):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url({image_file});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("images/background.png")

# ---- LOAD OR INITIALIZE DATA ----
data_file = "fitness_data.csv"

try:
    df = pd.read_csv(data_file)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Activity", "Duration", "Calories Burned"])

# ---- SESSION STATE FOR UNSAVED ENTRIES ----
if "unsaved_entries" not in st.session_state:
    st.session_state.unsaved_entries = []

# ---- SIDEBAR INPUT FORM ----
st.sidebar.markdown("### 📝 Log Your Workout")
activity = st.sidebar.selectbox("Choose Activity", ["Running", "Cycling", "Swimming", "Gym Workout", "Yoga", "Other"])
duration = st.sidebar.slider("Duration (minutes)", 1, 180, 30)
calories = st.sidebar.slider("Calories Burned", 50, 1500, 300)
log_date = st.sidebar.date_input("Workout Date", datetime.date.today())

# ---- ADD ENTRY TO MEMORY ----
if st.sidebar.button("➕ Add Entry (Unsaved)"):
    new_entry = {"Date": log_date, "Activity": activity, "Duration": duration, "Calories Burned": calories}
    st.session_state.unsaved_entries.append(new_entry)
    st.sidebar.success("✅ Entry added but NOT saved yet!")

# ---- SHOW WORKOUT HISTORY (Both Saved & Unsaved) ----
st.markdown("## 🏆 Workout History")

# Combine saved and unsaved data for display
temp_df = df.copy()  # Show saved data
if st.session_state.unsaved_entries:
    temp_df = pd.concat([df, pd.DataFrame(st.session_state.unsaved_entries)], ignore_index=True)

st.dataframe(temp_df.style.set_properties(**{'background-color': '#222', 'color': '#FFF'}))

# ---- SAVE ALL DATA TO FILE ----
if st.button("💾 Save All Data"):
    df = temp_df  # Overwrite df with the updated version
    df.to_csv(data_file, index=False)
    st.session_state.unsaved_entries.clear()  # Clear unsaved entries
    st.success("✅ All data saved successfully!")

# ---- SHOW METRICS ----
if not temp_df.empty:
    total_sessions = len(temp_df)
    total_calories = temp_df["Calories Burned"].sum()
    avg_duration = temp_df["Duration"].mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric(label="🔥 Total Sessions", value=f"{total_sessions} Workouts")
    col2.metric(label="⚡ Total Calories Burned", value=f"{total_calories} kcal")
    col3.metric(label="⏳ Avg Duration", value=f"{round(avg_duration, 2)} mins")

# ---- VISUALIZATION ----
st.markdown("## 📊 Workout Progress")
if not temp_df.empty:
    temp_df["Date"] = pd.to_datetime(temp_df["Date"])
    temp_df.sort_values("Date", inplace=True)
    
    fig = px.line(temp_df, x="Date", y="Calories Burned", title="Calories Burned Over Time",
                  markers=True, template="plotly_dark")
    st.plotly_chart(fig)

# ---- SHOW IMAGES BASED ON WORKOUT TYPE ----
st.markdown("## 🏋️‍♀️ Workout Highlights")
if activity.lower() == "running":
    img = Image.open("images/running.png")
elif activity.lower() == "cycling":
    img = Image.open("images/cycling.png")
elif activity.lower() == "swimming":
    img = Image.open("images/swimming.png")
elif activity.lower() == "gym workout":
    img = Image.open("images/gym.png")
elif activity.lower() == "yoga":
    img = Image.open("images/yoga.png")
else:
    img = Image.open("images/fitness.png")

st.image(img, caption=f"Keep pushing! You're doing great with {activity}! 💪", use_container_width=True)
