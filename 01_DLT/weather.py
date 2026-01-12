import dlt
import requests
import os
from pathlib import Path
from datetime import datetime

url = "https://polisen.se/api/events"

def get_events():
    """Fetch events from polisen API."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_weather():
    """Fetch weather data for all events."""
    event_response = get_events()
    weather_data_rows = []  

    for event in event_response:
        try:
            lat, lon = map(float, event["location"]["gps"].split(","))
            event_date = event["datetime"][0:10]
            time = event["name"].split(",")[0].split()[-1]
            full_datetime_str = f"{event_date} {time.replace('.', ':')}"
            parsed_datetime = datetime.strptime(full_datetime_str, "%Y-%m-%d %H:%M")
            target_hour = parsed_datetime.strftime("%Y-%m-%dT%H:00")
            
            weather_url = (f"https://historical-forecast-api.open-meteo.com/v1/forecast"
                           f"?latitude={lat}&longitude={lon}&start_date={event_date}&end_date={event_date}"
                           f"&hourly=temperature_2m,precipitation&timezone=Europe%2FBerlin")
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            hourly_data = weather_data.get('hourly', {})
            time_list = hourly_data.get('time', [])
            temperature_list = hourly_data.get('temperature_2m', [])
            precipitation_list = hourly_data.get('precipitation', [])

            if target_hour in time_list:
                index = time_list.index(target_hour)
                weather_data_rows.append({
                    'id': event["id"],
                    'lat': lat,
                    'lon': lon,
                    'time': target_hour,
                    'temperature': temperature_list[index],
                    'precipitation': precipitation_list[index]
                })

        except Exception as e:
            print(f"Error processing weather for event {event.get('id', 'unknown')}: {e}")

    return weather_data_rows

@dlt.resource(write_disposition="append")
def weather_resource():
    """DLT resource to load weather data."""
    weather_data = get_weather()
    for row in weather_data:
        yield row

def load_events() -> None:
    """Run the DLT pipeline to load weather data."""
    p = dlt.pipeline(
        pipeline_name='snowflake_pipeline_pipeline',
        destination='snowflake',
        dataset_name='Staging1',
    )

    load_info = p.run(weather_resource())
    print(f"Loaded data to Snowflake: {load_info}")

if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)
    load_events()
