import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
import sqlite3 as sq
import streamlit as st

st.set_page_config(page_title="EMXEFIT Activity Tracker", 
                   page_icon="🏋️", 
                   layout="wide")

conn = sq.connect('database.db')
cur = conn.cursor()

page_bg_img = """
<style>
.stApp {
    background: 
        linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
        url("https://raw.githubusercontent.com/emxelux/emxelux/main/uuuu.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stAppViewContainer"] {
    backdrop-filter: blur(6px);
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0) !important;
}
[data-testid="stSidebar"] {
    background: rgba(30, 30, 30, 0.75) !important;
    border-radius: 12px;
    padding: 1rem;
    backdrop-filter: blur(6px);
}
h1, h2, h3, h4, h5 {
    color: #ffffff !important;
    font-weight: 700;
    text-shadow: 1px 1px 2px #000;
}
p, label, .stMarkdown, .stText, .stSelectbox, .stDataFrame {
    color: #f1f1f1 !important;
}
.stButton button {
    border-radius: 12px;
    background: linear-gradient(135deg, #ff6f61, #ff9966);
    color: white;
    font-size: 16px;
    padding: 0.6rem 1.2rem;
    border: none;
}
.stButton button:hover {
    background: linear-gradient(135deg, #e85c50, #ff784e);
}
[data-testid="stMetricLabel"] {
    color: #e6e6e6 !important;
}
[data-testid="stMetricValue"] {
    color: #00ffcc !important;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

options = st.sidebar.radio('📌 Navigation', 
                           options=['🏠 HomePage', '📝 Log Activities', '📊 Stats'])

def home_page():
    st.markdown("<h1 style='text-align:center;'>✅ WELCOME TO EMXEFIT ✅</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Your Personal Fitness Companion</h3>", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns([2,1], gap="large")
    with col1:
        st.markdown("""
        ### 🚀 Why EMXEFIT?
        - 📈 **Track** all your workouts and visualize progress
        - 🎯 **Set goals** and achieve them step by step
        - 🏆 **Compete** with friends via rankings
        - 💡 **Stay motivated** with insights & streaks
        """)
        st.success("💪 Start logging your activities today and transform your fitness journey!")
    with col2:
        st.image("https://images.unsplash.com/photo-1594737625785-c8cb9fcf8f55?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80", 
                 caption="Stay Fit. Stay Strong.", use_container_width=True)
    st.divider()
    st.markdown(f"<p style='text-align:center; color:#d9d9d9;'>© 2025 EMXEFIT | All Rights Reserved | Visited on {date.today()}</p>", unsafe_allow_html=True)

def log_activities():
    st.markdown("<h1>📝 Log Your Activities</h1>", unsafe_allow_html=True)
    st.write("Fill in the details of your activity below:")
    with st.form('activity_form'):
        name = st.text_input('Enter your name (This will be used to track your logs)')
        activity_type = st.selectbox('Activity Type', ['Running', 'Cycling', 'Swimming', 'Walking'])
        duration = st.number_input('Duration (in minutes)', min_value=0.0, step=0.1)
        distance = st.number_input('Distance (in km)', min_value=0.0, step=0.1)
        d_date = st.date_input('Date', value=date.today())
        submit_button = st.form_submit_button(label='✅ Log Activity')
        if submit_button:
            cur.execute(
                'INSERT INTO activities(name, activity_type, duration, distance, date) VALUES (?, ?, ?, ?, ?)', 
                (name, activity_type, duration, distance, d_date)
            )
            conn.commit()
            st.success('✅ Activity logged successfully!')
            st.balloons()

def stats():
    st.markdown("<h1>📊 Activity Statistics</h1>", unsafe_allow_html=True)
    cur.execute('SELECT * FROM activities')
    activities = cur.fetchall()
    if not activities:
        st.warning('⚠ No activities logged yet.')
        return
    all_data = []
    for activity in activities:
        act = {
            'Name': activity[1], 
            'Type': activity[2], 
            'Duration': activity[3], 
            'Distance': activity[4], 
            'Date': activity[5]
        }
        all_data.append(act)
    df = pd.DataFrame(all_data)
    total_distance = df['Distance'].sum()
    total_duration = df['Duration'].sum()
    unique_users = df['Name'].nunique()
    c1, c2, c3 = st.columns(3)
    c1.metric("🌍 Total Distance (km)", f"{total_distance:.1f}")
    c2.metric("⏱ Total Duration (min)", f"{total_duration:.1f}")
    c3.metric("👥 Active Users", unique_users)
    st.divider()
    st.dataframe(df, use_container_width=True)
    st.divider()
    col1, col2, col3 = st.columns(3, gap='large')
    with col1:
        st.subheader('🏃 Top Distances by User')
        st.bar_chart(df.groupby('Name')['Distance'].sum().sort_values(ascending=True).head(10))
    with col2:
        st.subheader('👤 View Your Stats')
        name = st.text_input('Enter your name')
        if st.button('🔍 View'):
            st.line_chart(df[df['Name'] == name].set_index('Date')[['Distance','Duration']])
    with col3:
        st.subheader('⏱ Top Durations by User')
        st.bar_chart(df.groupby('Name')['Duration'].sum().head(10))
    st.divider()
    st.header('🏆 Ranking')
    st.info('⚠ Disclaimer: Ranking is based on Distance and Duration only, no real verification.')
    score = (df['Distance'] / df['Duration']).round(2) * 100
    df['Score'] = score
    ranking = df.groupby('Name')['Score'].mean().reset_index().sort_values(by='Score', ascending=True)
    ranking['Rank'] = ranking['Score'].rank(method='min', ascending=False).astype(int)
    ranking = ranking.sort_values(by='Rank', ascending=False)
    st.dataframe(ranking, use_container_width=True)

if options == '🏠 HomePage':
    home_page()
elif options == '📝 Log Activities':
    log_activities()
elif options == '📊 Stats':
    stats()
