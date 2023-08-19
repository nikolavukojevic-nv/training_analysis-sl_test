import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_resource
def load_data():
    data = pd.read_csv('nv-training-data 2.csv', delimiter=';')
    data['datetime'] = pd.to_datetime(data['datetime'], format='%Y-%m-%d %H:%M')
    return data

data = load_data()

# Title
st.title("Exercise Analysis Dashboard")

# Date Range Picker with corrected date range
start_date, end_date = st.date_input('Pick a date range', [data['datetime'].min().date(), data['datetime'].max().date()])
filtered_data = data[(data['datetime'] >= pd.Timestamp(start_date)) & (data['datetime'] <= pd.Timestamp(end_date))]

# Handling the SettingWithCopyWarning by creating an explicit copy
filtered_data = filtered_data.copy()

# Replace ',' with '.' in the 'weight' column and convert to numeric type
filtered_data['weight'] = pd.to_numeric(filtered_data['weight'].str.replace(',', '.'), errors='coerce')
filtered_data['reps'] = pd.to_numeric(filtered_data['reps'], errors='coerce')
filtered_data['sets'] = pd.to_numeric(filtered_data['sets'], errors='coerce')

# Calculate total and adjusted total work
filtered_data['total_work'] = filtered_data['weight'] * filtered_data['reps'] * filtered_data['sets']
filtered_data['adjusted_total_work'] = filtered_data['reps'] * filtered_data['sets']

# Summarize total and adjusted total work
summary = filtered_data.groupby('exercise').agg({
    'total_work': 'sum',
    'adjusted_total_work': 'sum'
})

# Bar chart for Total Work
st.subheader('Total Work by Exercise')
fig, ax = plt.subplots(figsize=(10, 6))
summary['total_work'].sort_values(ascending=True).plot(kind='barh', ax=ax)
st.pyplot(fig)

# Bar chart for Adjusted Total Work
st.subheader('Adjusted Total Work by Exercise')
fig, ax = plt.subplots(figsize=(10, 6))
summary['adjusted_total_work'].sort_values(ascending=True).plot(kind='barh', ax=ax)
st.pyplot(fig)

# Display data in a table format
st.subheader('Data Table')
st.write(filtered_data)
