import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
@st.cache
def load_data():
    data = pd.read_csv('nv-training-data 2.csv', delimiter=';')
    data['datetime'] = pd.to_datetime(data['datetime'])
    return data

data = load_data()

# Title
st.title("Exercise Analysis Dashboard")

# Date Range Picker
start_date, end_date = st.date_input('Pick a date range', [data['datetime'].min(), data['datetime'].max()])
filtered_data = data[(data['datetime'] >= pd.Timestamp(start_date)) & (data['datetime'] <= pd.Timestamp(end_date))]

# Calculate total and adjusted total work
filtered_data['total_work'] = filtered_data['weight'] * filtered_data['reps'] * filtered_data['sets']
filtered_data['adjusted_total_work'] = filtered_data['reps'] * filtered_data['sets']
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
