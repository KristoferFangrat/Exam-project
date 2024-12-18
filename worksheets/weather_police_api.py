import requests
import openmeteo_requests
import requests_cache
import requests
import pandas as pd
import numpy as np
from retry_requests import retry
import matplotlib.pyplot as plt

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 59.3533,
    "longitude": 18.0978,
    "start_date": "2024-10-15",
    "end_date": "2024-11-01",
    "hourly": ["temperature_2m", "precipitation"],
    "daily": ["precipitation_sum", "precipitation_hours"],
    "timezone": "auto"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = np.round(hourly.Variables(0).ValuesAsNumpy(), 1)
hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()

hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ),
    "temperature_2m": hourly_temperature_2m,
    "precipitation": hourly_precipitation
}

hourly_dataframe = pd.DataFrame(data=hourly_data)
print(hourly_dataframe)

# Plot hourly temperature and precipitation
plt.figure(figsize=(14, 7))

plt.subplot(2, 1, 1)
plt.plot(hourly_dataframe['date'], hourly_dataframe['temperature_2m'], label='Temperature (°C)')
plt.title('Hourly Temperature')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(hourly_dataframe['date'], hourly_dataframe['precipitation'], label='Precipitation (mm)', color='b')
plt.title('Hourly Precipitation')
plt.xlabel('Date')
plt.ylabel('Precipitation (mm)')
plt.legend()

plt.tight_layout()
plt.show()

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_precipitation_sum = daily.Variables(0).ValuesAsNumpy()
daily_precipitation_hours = daily.Variables(1).ValuesAsNumpy()

daily_data = {
    "date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    ),
    "precipitation_sum": daily_precipitation_sum,
    "precipitation_hours": daily_precipitation_hours
}

daily_dataframe = pd.DataFrame(data=daily_data)
print(daily_dataframe)

# Plot daily precipitation sum and hours
plt.figure(figsize=(14, 7))

plt.subplot(2, 1, 1)
plt.plot(daily_dataframe['date'], daily_dataframe['precipitation_sum'], label='Precipitation Sum (mm)')
plt.title('Daily Precipitation Sum')
plt.xlabel('Date')
plt.ylabel('Precipitation Sum (mm)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(daily_dataframe['date'], daily_dataframe['precipitation_hours'], label='Precipitation Hours', color='b')
plt.title('Daily Precipitation Hours')
plt.xlabel('Date')
plt.ylabel('Precipitation Hours')
plt.legend()

plt.tight_layout()
plt.show()

def fetch_police_events():
    # Hämta data från polisens API
    polisen_url = "https://polisen.se/api/events"
    polisen_response = requests.get(polisen_url)
    polisen_data = polisen_response.json()

    # Filtrera trafikolyckor
    trafikolyckor = [event for event in polisen_data if event['type'] == 'Trafikolycka']

    return trafikolyckor

def process_traffic_accidents(trafikolyckor, hourly_dataframe):
    # Kontrollera om några trafikolyckor hittades
    if not trafikolyckor:
        print("Inga trafikolyckor hittades i polisens API-data.")
        return []

    # Jämför datumen och hämta koordinater
    accidents = []
    for olycka in trafikolyckor:
        olycka_date = pd.to_datetime(olycka['datetime']).date()
        if olycka_date in hourly_dataframe['date'].dt.date.values:
            location = olycka['location']
            accidents.append({
                'date': olycka_date,
                'location_name': location['name'],
                'coordinates': location['gps']
            })
    return accidents