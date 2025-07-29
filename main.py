import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
import sqlite3 as sq
import streamlit as st

st.set_page_config(page_title="Activity Tracker", page_icon=":running:", layout="wide")
conn = sq.connect('database.db')
cur = conn.cursor()

try:
    options = st.sidebar.radio('Choose one', options = ['HomePage', 'Log Activities', 'Stats'])
    
    def home_page():
        st.title('✅ WELCOME TO EMXEFIT✅')
        st.write(f'''Track your fitness journey and stay motivated every step of the way. Log in to see your progress, set goals, and crush them''')
        '\n'
        st.badge('Below are some stunning fitness activity images to get you motivated')
        img1, img2, img3 = st.columns(3)
        st.markdown(f'''Copyright &copy; 2025. All right reserved. You visited on  ({date.today()})''')

        with img1:
            st.image('images\cardio1.jpg', caption='Track your fitness journey') 
            '\n'
            st.image('images\cardio2.jpg', caption = 'We offer you free service')
            '\n'
            st.image('images\cardio3.jpg', caption = 'Workout is good for your health')

        with img2:
            st.image('images\\fit1.jpg', caption = 'Get fit with us')
            '\n'
            st.image('images\\fit2.jpg', caption = 'We are here to help you')
            '\n'
            st.image('images\\fit3.jpg', caption = 'We are here to help you achieve your fitness goals')

        with img3:
            st.image('images\sport1.jpg', caption = 'Kid playing pool')
            '\n'
            st.image('images\sport2.jpg', caption = 'We are here to help you get fit')
            '\n'
            st.image('images\sport3.jpg', caption = 'Help yourself to grow')

            st.divider()
    
    def log_activities():
        st.title('Log Your Activities')
        st.write('Fill in the details of your activity below:')
        
        with st.form('activity_form'):
            name = st.text_input('Enter your name(Remember the name you use to log this activity)')
            activity_type = st.selectbox('Activity Type', ['Running', 'Cycling', 'Swimming', 'Walking'])
            duration = st.number_input('Duration (in minutes)', min_value=0.0, step=0.1)
            distance = st.number_input('Distance (in km)', min_value=0.0, step=0.1)
            d_date = st.date_input('Date', value=date.today())
            submit_button = st.form_submit_button(label='Log Activity')
            
            if submit_button:
                cur.execute('INSERT INTO activities(name, activity_type, duration, distance, date) VALUES (?, ?, ?, ?, ?)', 
                            (name, activity_type, duration, distance, d_date))
                conn.commit()
                st.success('Activity logged successfully!')
                st.balloons()
    
    def stats():
        st.title('Activity Statistics')
        cur.execute('SELECT * FROM activities')
        activities = cur.fetchall()
        
        if not activities:
            st.write('No activities logged yet.')
            return
        
        st.write('Here are your logged activities:')
        all_data = []
        for activity in activities:
            act = {'Name': activity[1], 'Type': activity[2], 'Duration': activity[3], 'Distance': activity[4], 'Date': activity[5]}
            all_data.append(act)
        df = pd.DataFrame(all_data)
        st.dataframe(df)
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader('Charts by distances')
            #st.bar_chart(hello)

        st.subheader('Want to Check your status and your stats')
        # user = st.selectbox('Enter your name', options= list(df['Name'].unique()))
        # if user:
        #     df[df['Name'] == user]
            


    if options == 'HomePage':
        home_page()
    elif options == 'Log Activities':
        log_activities()
    elif options == 'Stats':
        stats()

except sq.Error as e: 
    st.error(f'There is an error: {e}')