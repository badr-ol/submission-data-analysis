import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.ticker as ticker

# Load data
all_df = pd.read_csv("all_data.csv")

# Data preprocessing
datetime_columns = ["dteday"]
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Sidebar
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

def filter_data(df, start_date, end_date):
    return df[(df["dteday"] >= str(start_date)) & (df["dteday"] <= str(end_date))]

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data based on selected date range
main_df = filter_data(all_df, start_date, end_date)

# Set header and subheader
st.header('Dicoding Bike Rental :sparkles:')

# Exploratory Data Analysis (EDA) - Daily Rentals
st.subheader('Daily Rentals')

col1, col2, col3 = st.columns(3)
 
with col1:
    # Menghitung total rentals
    total_rentals = main_df['cnt_y'].sum()
    st.metric("Total Rentals", value=total_rentals)

with col2:
    total_casual = main_df['casual_y'].sum()
    st.metric("Casual User", value=total_casual)
 
with col3:
    total_registed = main_df['registered_y'].sum()
    st.metric("Registered User", value=total_registed)

def plot_daily_rentals(df):
    daily_rentals = df.groupby(df["dteday"])["cnt_y"].sum()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(daily_rentals.index, daily_rentals.values, marker='', linestyle='-')

    # Label dan judul
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Rentals')
    ax.set_title('Daily Bike Rentals')

    # Tampilkan plot
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

plot_daily_rentals(main_df)

st.subheader('Rentals per user type')
def plot_rentals_per_user_type(df):
    # Check if the selected date range is within a single year
    single_year = start_date.year == end_date.year

    # Group rentals per user type and year
    rentals_per_user_type = df.groupby([df["yr_y"], df["yr_y"] * single_year]).agg({"casual_y": "sum", "registered_y": "sum"})

    # Visualization & Explanatory Analysis - Pertanyaan 5
    fig, ax = plt.subplots()

    if single_year:
        # If the selected date range is within a single year, plot only for that year
        plt.bar(["2011"], rentals_per_user_type.loc[0, "casual_y"], label="Casual Users")
        plt.bar(["2011"], rentals_per_user_type.loc[0, "registered_y"], bottom=rentals_per_user_type.loc[0, "casual_y"], label="Registered Users")
    else:
        # Plot for both years
        plt.bar(["2011", "2012"], rentals_per_user_type["casual_y"], label="Casual Users")
        plt.bar(["2011", "2012"], rentals_per_user_type["registered_y"], bottom=rentals_per_user_type["casual_y"], label="Registered Users")

    plt.title("Total Rentals per Year and User Type")
    plt.xlabel("Year")
    plt.ylabel("Total Rentals")
    plt.legend()
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))  # Penyesuaian formatter sumbu y-axis
    st.pyplot(fig)

plot_rentals_per_user_type(main_df)

st.subheader('Rentals per year')
def plot_rentals_per_year(df):
    rentals_per_month = df.groupby(['yr_y', 'mnth_y'])['cnt_y'].sum()

    # Ubah indeks bulan menjadi nama bulan
    rentals_per_month.index = rentals_per_month.index.set_levels(
        [['2011', '2012'], 
         ['January', 'February', 'March', 'April', 'May', 'June', 
          'July', 'August', 'September', 'October', 'November', 'December']],
        level=[0, 1]
    )

    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']

    # Jumlah peminjaman sepeda per bulan untuk tahun 2011 dan 2012
    rentals_2011 = rentals_per_month['2011']
    rentals_2012 = rentals_per_month['2012']

    # Buat plot
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(months, rentals_2011, marker='o', label='2011')
    ax.plot(months, rentals_2012, marker='o', label='2012')

    # Label dan judul
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Rentals')
    ax.set_title('Bike Rentals per Month (2011 vs 2012)')
    plt.xticks(rotation=45)

    # Tampilkan legenda
    plt.legend()

    # Tampilkan plot
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(fig)

plot_rentals_per_year(all_df)

st.subheader('Rentals by season')
def plot_rentals_per_season_per_year(df):
    seasons = ['Spring', 'Summer', 'Fall', 'Winter']

    # Filter data for each year and season, fill missing values with 0
    rentals_per_season_2011 = df[df["yr_y"] == 0].groupby(df["season_y"])["cnt_y"].sum().reindex(index=[1, 2, 3, 4], fill_value=0)
    rentals_per_season_2012 = df[df["yr_y"] == 1].groupby(df["season_y"])["cnt_y"].sum().reindex(index=[1, 2, 3, 4], fill_value=0)

    # Buat plot
    plt.figure(figsize=(10, 5))

    plt.bar(seasons, rentals_per_season_2011, color='blue', width=0.4, align='center', label='2011')
    plt.bar(seasons, rentals_per_season_2012, color='orange', width=0.4, align='edge', label='2012')

    # Label dan judul
    plt.xlabel('Season')
    plt.ylabel('Number of Rentals')
    plt.title('Bike Rentals per Season (2011 vs 2012)')
    plt.legend()

    # Tampilkan plot
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt.gcf())

plot_rentals_per_season_per_year(main_df)

st.subheader('Rentals by parts of the day')
def plot_rentals_per_hour_group(df):
    def categorize_hour(hour):
        if 5 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 17:
            return 'Afternoon'
        elif 17 <= hour < 22:
            return 'Evening'
        else:
            return 'Night'

    df['hour_group'] = df['hr'].apply(categorize_hour)
    rentals_per_hour_group = df.groupby('hour_group')['cnt_y'].sum()

    # Visualization & Explanatory Analysis - Pertanyaan 3
    fig, ax = plt.subplots()
    sns.barplot(x=rentals_per_hour_group.index, y=rentals_per_hour_group.values, ax=ax)
    plt.title("Total Rentals per Hour Group")
    plt.xlabel("Hour Group")
    plt.ylabel("Total Rentals")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))  # Penyesuaian formatter sumbu y-axis
    st.pyplot(fig)

plot_rentals_per_hour_group(main_df)

st.subheader('Rentals by weather')
def plot_rentals_per_weather(df):
    # Rename weather index
    df["weathersit_y"] = df["weathersit_y"].replace({1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'})

    rentals_per_weather = df.groupby(df["weathersit_y"])["cnt_y"].sum()

    # Visualization & Explanatory Analysis - Pertanyaan 4
    fig, ax = plt.subplots()
    sns.barplot(x=rentals_per_weather.index, y=rentals_per_weather.values, ax=ax)
    plt.title("Total Rentals per Weather Situation")
    plt.xlabel("Weather Situation")
    plt.ylabel("Total Rentals")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.0f}"))  # Penyesuaian formatter sumbu y-axis
    st.pyplot(fig)

plot_rentals_per_weather(main_df)

