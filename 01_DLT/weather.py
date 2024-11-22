import dlt
import requests
import os
from pathlib import Path
import pandas as pd

event_url = "https://polisen.se/api/events"
def get_events():
    response = requests.get(event_url)
    response.raise_for_status()
    event_response = response.json()
    # Split the "gps" field into latitude and longitude
    lat, lon = map(float, event_response[0]["location"]["gps"].split(","))
    event_time = event_response[0]["datetime"][0:10]
    # print(event_time)
    
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={event_time}&end_date={event_time}&hourly=temperature_2m,precipitation"
    response = requests.get(url)
    response.raise_for_status()
    print(response.json())

get_events()


