import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st


sns.set(style='white')
st.set_option('deprecation.showPyplotGlobalUse', False)


# load the dataset
df = pd.read_csv('daycleaned.csv') 


# membuat func yang akan dipanggil untuk variable
def humidity_f(df): 
    humidity_v = df.groupby(['humidity_interval'])['total_rental'].sum().reset_index()
    return humidity_v


# membuat func yang akan dipanggil untuk variable
def workingday_f(df): 
    workingday_v = df.groupby(['workingday'])['total_rental'].sum().reset_index()
    return workingday_v


# set up variables for the dataframe
humidity_plt = humidity_f(df)
workingday_plt = workingday_f(df)


# membuat side bar filter
with st.sidebar:


    st.image("sepeda.webp")

    selected_intervals = st.multiselect('Select humidity intervals:', humidity_plt['humidity_interval'].unique())
    day_select = st.multiselect("Filter Hari kerja", workingday_plt['workingday'].unique(), default=workingday_plt['workingday'].unique())



st.header(':crown: Bicycle Rental Analysis :crown:')
st.subheader(':bike: Total Customer :bike:')
    
columns = st.columns(1)

# Card Total Customers
with columns[0]:
    total_rental_sum = df['total_rental'].sum()
    st.metric('Total Customer saat ini', total_rental_sum)


# container for filter humidity
with st.container():
    st.subheader('The Effect of Humidity on Bicycle Rental Demand:')

#penggunaan if-else untuk logic pemanggilan
if selected_intervals:
    filter_humidity = humidity_plt[humidity_plt['humidity_interval'].isin(selected_intervals)]
else:
    filter_humidity = humidity_plt  # Jika tidak ada interval yang dipilih, gunakan semua data

# Visualize data
plt.figure(figsize=(8, 5))
if not filter_humidity.empty:
    sns.barplot(data=filter_humidity,
                x="humidity_interval",
                y="total_rental",
                palette=["#FF3242", "#F6995C", "#51829B", "#EADFB4", "#9BB0C1"])
    plt.xlabel('Humidity Interval')
    plt.ylabel('Total Rental')
    plt.tight_layout()
    st.pyplot()
else:
    st.write("No data available for the selected intervals.")




# container for filter customer
with st.container():

    st.subheader('Number of Bicycle Rental Customers by Weekday / Holiday:')
    # Filter data based on selection
    filtered_day = df[df['workingday'].isin(day_select)]

    # Calculate proportions based on filtered data
    workingday_plot = filtered_day.groupby('workingday')['total_rental'].sum().reset_index()


    # Plotting menggunakan Streamlit
    plt.figure(figsize=(8, 6))
    if not workingday_plot.empty:
        plt.pie(workingday_plot['total_rental'], labels=workingday_plot['workingday'], autopct='%1.1f%%', colors=['#66c2a5', '#fc8d62'])
        st.pyplot()
    else:
        st.write("Mohon Untuk Memilih Minimal Satu Filter")


st.caption('Copyright (c) Gibran Faktian Anwar 2024')
