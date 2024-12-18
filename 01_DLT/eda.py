import dlt
import requests
import pandas as pd
from datetime import datetime
import os
from pathlib import Path

<<<<<<< HEAD
# Initialize the SMHI client
client = SMHIOpenDataClient()

# Get available parameters (optional, if you need to know what parameters are supported)
parameters = client.list_parameters()
print(parameters)


# Replace with your location's latitude and longitude
latitude = 59.3293  # Example for Stockholm
longitude = 18.0686

# Get the closest weather station to your location
closest_station = client.get_closest_station(latitude=latitude, longitude=longitude)
print(f"Closest Station: {closest_station}")


# Get the current date and time
current_time = datetime.utcnow()

# Get the timestamp from 7 days ago
one_week_ago = current_time - timedelta(days=7)

# Convert both times to Unix timestamps
start_time = int(one_week_ago.timestamp())
end_time = int(current_time.timestamp())

# Fetch temperature observations from the closest station in the past week
observations = client.get_observations(
    parameter=Parameter.TemperaturePast1h,  # Parameter for past 1-hour temperatures
    start_time=start_time,
    end_time=end_time,
    latitude=latitude,
    longitude=longitude
=======
# Define DLT Snowflake pipeline
p = dlt.pipeline(
    pipeline_name='snowflake_pipeline_pipeline',
    destination='snowflake',
    dataset_name='Staging1',
>>>>>>> d87e0d819adc6821c87d86d1db17ab1a9a820bf6
)

# Function to get events
def get_events():
    event_url = "https://polisen.se/api/events"
    response = requests.get(event_url)
    response.raise_for_status()
    return response.json()

# DLT resource for events
@dlt.resource(write_disposition="append")
def event_resource():
    events = get_events()
    for event in events:
        yield event

# Function to get weather data
def get_weather():
    event_response = get_events()  # Fetch events to iterate over

    # Initialize DataFrame
    weather_data = []

    for event in event_response:
        try:
            id = event["id"]
            lat, lon = map(float, event["location"]["gps"].split(","))
            event_date = event["datetime"][0:10]
            raw_datetime = event["datetime"]
            parsed_datetime = datetime.strptime(raw_datetime, "%Y-%m-%d %H:%M:%S %z")
            target_hour = parsed_datetime.strftime("%Y-%m-%dT%H:00")

            # Fetch weather data
            weather_url = (
                f"https://historical-forecast-api.open-meteo.com/v1/forecast"
                f"?latitude={lat}&longitude={lon}&start_date={event_date}&end_date={event_date}"
                f"&hourly=temperature_2m,precipitation&timezone=Europe%2FBerlin"
            )
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather = weather_response.json()

            # Extract hourly weather data
            hourly_data = weather['hourly']
            time_list = hourly_data['time']
            temperature_list = hourly_data['temperature_2m']
            precipitation_list = hourly_data['precipitation']

            # Match target hour
            try:
                index = time_list.index(target_hour)
                temperature = temperature_list[index]
                precipitation = precipitation_list[index]
            except ValueError:
                temperature = None
                precipitation = None

            # Append data to list
            weather_data.append({
                'id': id,
                'lat': lat,
                'lon': lon,
                'time': target_hour,
                'temperature': temperature,
                'precipitation': precipitation
            })

        except Exception as e:
            print(f"Error processing weather data for event ID {event.get('id', 'unknown')}: {e}")

    return weather_data

# DLT resource for weather data
@dlt.resource(write_disposition="append")
def weather_resource():
    weather_data = get_weather()
    for record in weather_data:
        yield record

# Load both resources into Snowflake
def load_data_to_snowflake():
    p.run([event_resource(), weather_resource()])
    print("Data successfully loaded to Snowflake!")

# Run the pipeline
if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)
    load_data_to_snowflake()
