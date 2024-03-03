import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='dark')

def create_rentals_per_month(df):
    rentals_per_month = df.groupby(by=['year', 'month'], observed=False)['total_count'].sum().reset_index()
    
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    rentals_per_month['month'] = pd.Categorical(rentals_per_month['month'], categories=months_order, ordered=True)
    
    return rentals_per_month

def create_rentals_by_season(df): 
    rentals_per_season = df.groupby(by=['year', 'season'], observed=False)['total_count'].sum().reset_index()
    return rentals_per_season

def create_rentals_by_hour(df): 
    rentals_by_hour = df.groupby(by='hour_group', observed=False)['total_count'].sum()
    return rentals_by_hour

def create_rentals_per_weather(df):
    rentals_per_weather = df.groupby(by='weather_situation', observed=False)['total_count'].sum()
    return rentals_per_weather

# Load data
days_df = pd.read_csv("https://raw.githubusercontent.com/badr-ol/submission-data-analysis/main/dashboard/day_cleaned.csv")
hours_df = pd.read_csv("https://raw.githubusercontent.com/badr-ol/submission-data-analysis/main/dashboard/hour_cleaned.csv")

# Mengurutkan nilai berdasarkan tanggal dan mereset index
datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

# Data preprocessing
for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

# Membuat sidebar
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/badr-ol/submission-data-analysis/blob/main/dashboard/logo.png?raw=true")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Range',
        min_value=days_df["dteday"].min(),
        max_value=days_df["dteday"].max(),
        value=[days_df["dteday"].min(), days_df["dteday"].max()])
  
main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & (days_df["dteday"] <= str(end_date))]
main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) &  (hours_df["dteday"] <= str(end_date))]

rentals_per_month = create_rentals_per_month(main_df_days)
rentals_per_season = create_rentals_by_season(main_df_days)
rentals_by_hour = create_rentals_by_hour(main_df_hour)
rentals_per_weather = create_rentals_per_weather(main_df_hour)

# Set header and subheader
st.header('Dicoding Bike Sharing :sparkles:')
st.subheader('Daily Rentals')

# Menampilkan total rentals
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_df_hour['total_count'].sum()
    st.metric("Total Rentals", value=total_rentals)
with col2:
    total_casual = main_df_hour['casual'].sum()
    st.metric("Casual User", value=total_casual)
with col3:
    total_registed = main_df_hour['registered'].sum()
    st.metric("Registered User", value=total_registed)

# Plot Daily Sharing
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(main_df_days["dteday"], main_df_days["total_count"], marker='o', linewidth=2, color="#90CAF9")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xlabel('Date')
ax.set_ylabel('Number of Rentals')
ax.set_title('Daily Bike Rentals')
plt.grid(True)
plt.tight_layout()
st.pyplot(fig)

st.subheader('Rentals per Month')

# Plot rentals per month
plt.figure(figsize=(10, 5))
sns.lineplot(data=rentals_per_month, x='month', y='total_count', hue='year', marker='o')
plt.xlabel('Month')
plt.ylabel('Number of Rentals')
plt.title('Bike Rentals per Month (2011 vs 2012)')
plt.legend(title='Year')
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

st.subheader('Rentals by Season')

# Plot rentals by season
palette = sns.color_palette("husl", len(rentals_per_season['year'].unique()))
season_order = ['Spring', 'Summer', 'Fall', 'Winter']
plt.figure(figsize=(10, 5))
sns.barplot(data=rentals_per_season, x='season', y='total_count', hue='year', palette=palette, order=season_order)
plt.xlabel('Season')
plt.ylabel('Number of Rentals')
plt.title('Bike Rentals per Season (2011 vs 2012)')
plt.legend(title='Year')
plt.grid(axis='y')
plt.tight_layout()
st.pyplot(plt)

st.subheader('Rentals by Part of the Day')

# Plot rentals per part of the day
hour_order = ['Morning', 'Afternoon', 'Evening', 'Night']
plt.figure(figsize=(10, 5))
sns.barplot(data=rentals_by_hour, color="#90CAF9", order=hour_order)
plt.xlabel('Part of the day')
plt.ylabel('Number of Rentals')
plt.title('Bike Rentals by Part of the day')
plt.grid(axis='y')
plt.tight_layout()
st.pyplot(plt)

st.subheader('Rentals by Weather')

# Plot rentals by weather
weather_order = ['Clear', 'Misty', 'Light_RainSnow', 'Heavy_RainSnow']
plt.figure(figsize=(10, 6))
sns.barplot(data=rentals_per_weather, color='skyblue', order=weather_order)
plt.xlabel('Weather Situation')
plt.ylabel('Number of Rentals')
plt.title('Rentals per Weather Situation')
plt.grid(axis='y')
plt.tight_layout()
st.pyplot(plt)

st.subheader('Rentals by User Type')

# Plot rentals by user type
user_type_totals = main_df_days.groupby('year', observed=False)[['casual', 'registered']].sum()
combined_data = user_type_totals.T.sum(axis=1)

plt.figure(figsize=(10, 5))
plt.pie(combined_data, labels=combined_data.index, autopct='%1.1f%%', colors=["#D3D3D3", "#72BCD4"])
plt.title('Distribution of Users')
plt.axis('equal') 
plt.tight_layout()
st.pyplot(plt)