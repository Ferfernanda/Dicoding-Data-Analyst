import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='darkgrid')

# DataFrame Day
df_day = pd.read_csv("cleaned_bike-sharing_day.csv")
df_day.head()

# DataFrame Hour
df_hour = pd.read_csv("cleaned_bike-sharing_hour.csv")
df_hour.head()

df_day = df_day.drop("instant", axis=1)
df_hour = df_hour.drop("instant", axis=1)

# # Rename Column
# column_day = {'dteday': 'date', 
#               'yr': 'year', 
#               'mnth': 'month',
#               'temp': 'temperature', 
#               'hum': 'humidity',
#               'cnt': 'count'}

# column_hour = {'dteday': 'date', 
#                'yr': 'year', 
#                'mnth': 'month',
#                'hr': 'hour', 
#                'temp': 'temperature', 
#                'hum': 'humidity',
#                'cnt': 'count'}

# df_day.rename(columns=column_day, inplace=True)
# df_hour.rename(columns=column_hour, inplace=True)

# Categorical Data

seasons = {1: 'Spring', 
           2: 'Summer', 
           3: 'Fall', 
           4: 'Winter'}

years = {0: '2011', 1: '2012'}

months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
         7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

holidays = {0: 'No', 1: 'Yes'}

weekdays = {0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 
        4: 'Thu', 5: 'Fri', 6: 'Sat'}

weathersits = {1: 'Clear/Partly Cloudy',
            2: 'Misty/Cloudy',
            3: 'Light Snow/Rain',
            4: 'Severe Weather'}     

workingdays = {0: 'Holiday', 1: 'Workingday'}

categorical = ['season', 'year', 'month', 'holiday', 'weekday', 'workingday', 'weathersit']
cat_data = [seasons, years, months, holidays, weekdays, workingdays, weathersits]

cat_dict = dict(zip(categorical, cat_data))

# # Date Time - Categorical Day
# df_day['date'] = pd.to_datetime(df_day['date'])

# for cat, data in cat_dict.items():
#   df_day[cat] = df_day[cat].map(data)
#   df_day[cat] = df_day[cat].astype('category')

# # Date Time - Categorical Hour
# df_hour['date'] = pd.to_datetime(df_hour['date'])

# for cat, data in cat_dict.items():
#   df_hour[cat] = df_hour[cat].map(data)
#   df_hour[cat] = df_hour[cat].astype('category')  
    
# # Season_rent_df
# def create_season_rent_df(df):
#     season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
#     return season_rent_df

# # Monthly_rent_df
# def create_monthly_rent_df(df):
#     monthly_rent_df = df.groupby(by='month').agg({
#         'count': 'sum'
#     })
#     ordered_months = [
#         'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
#         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
#     ]
#     monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
#     return monthly_rent_df

# # Weather_rent_df
# def create_weather_rent_df(df):
#     weather_rent_df = df.groupby(by='weathersit').agg({
#         'count': 'sum'
#     })
#     return weather_rent_df


# komponen filter
min_date = pd.to_datetime(df_day['date']).dt.date.min()
max_date = pd.to_datetime(df_day['date']).dt.date.max()
 
with st.sidebar:
    
    # start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = df_day[(df_day['date'] >= str(start_date)) & 
                (df_day['date'] <= str(end_date))]

# # dataframe
# season_rent_df = create_season_rent_df(main_df)
# monthly_rent_df = create_monthly_rent_df(main_df)
# weather_rent_df = create_weather_rent_df(main_df)



# judul
st.header('Ferfernanda Bicycle Rental')

# Bicycle rent trends by year

plt.figure(figsize=(10, 6))
sns.barplot(data=df_day, x='month', y='count', hue='year', palette='viridis', order=list(months.values()))
plt.title('Bicycle rent trends by year')
plt.xlabel('Month')
plt.ylabel('Counts Total')
plt.xticks(rotation=45)
plt.legend(title='Year')
plt.tight_layout()
st.pyplot(plt)


filtered_data = df_day[(df_day['month'] == 'Sep')]

# Plotting
plt.figure(figsize=(12, 6))
sns.barplot(data=filtered_data, x='date', y='count', hue='year')
plt.title('Bicycle Rent Trends in September 2012')
plt.xlabel('Date')
plt.ylabel('Counts Total')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)


hour = df_hour[(df_hour['date'] == '2012-09-15')]

# Plotting
plt.figure(figsize=(12, 6))
sns.barplot(data=hour, x='hour', y='count')
plt.title('Bicycle Rent Trends on September 15 2012')
plt.xlabel('Hour')
plt.ylabel('Counts Total')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)


# Tren peminjaman sepeda berdasarkan musim
plt.figure(figsize=(10, 6))
sns.barplot(data=df_day, x='season', y='count', hue='weathersit', order=list(seasons.values()))
plt.title('Tren Bicycle lending trends based on season')
plt.xlabel('Season')
plt.ylabel('Counts Total')
st.pyplot(plt)


# Bicycle usage patterns based on hours
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_hour, x='hour', y='count', estimator='mean')
plt.title('Bicycle usage patterns based on hours')
plt.xlabel('Hour')
plt.ylabel('Counts Total Mean')
st.pyplot(plt)

# Checking pattern of non working days using lineplot
mask_holiday = ((df_hour['workingday']=='Holiday') | (df_hour['holiday']=='Yes'))
df_holiday = df_hour[mask_holiday]

columns = ['count','casual','registered']
color_palette = sns.color_palette("Set2")

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1) 
for i, col in enumerate(columns):
    sns.lineplot(x='hour', y=col, data=df_holiday, label=col, color=color_palette[i])
plt.title('Bicycle Rent Patterns in Holidays')
plt.xlabel('Hour')
plt.ylabel('Count Total')
plt.legend()

# Checking pattern of working days using lineplot
mask_working = ((df_hour['workingday']=='Workingday') & (df_hour['holiday']=='No'))
df_working = df_hour[mask_working]

plt.subplot(1, 2, 2)  
for i, col in enumerate(columns):
    sns.lineplot(x='hour', y=col, data=df_working, label=col, color=color_palette[i])
plt.title('Bicycle Rent Patterns in Working Days')
plt.xlabel('Hour')
plt.ylabel('Counts Total')
plt.legend()

plt.tight_layout()
st.pyplot(plt)


st.caption('Copyright (c) Ferfernanda Simple Webs 2024')