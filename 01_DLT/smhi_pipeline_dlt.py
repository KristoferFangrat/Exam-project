import dlt
import requests
import os
from pathlib import Path
<<<<<<< HEAD
=======
import pandas as pd
Timsbranch
import smhi_open_data as sod

>>>>>>> 4c71c1686068e0d9e3726d16f277e4d62ea57fd1
from datetime import datetime

# Ange koordinater för platsen
latitude = 64.750244
longitude = 20.950917

api_url = f"https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{longitude}/lat/{latitude}/data.json"

def get_events():
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

def extract_relevant_data_smhi(weather_data):
    relevant_data = []
    for entry in weather_data["timeSeries"]:
        valid_time = entry["validTime"]
        tid = datetime.fromisoformat(valid_time)

        temperature = None
        precipitation = None
        for parameter in entry["parameters"]:
            if parameter["name"] == "t":
                temperature = parameter["values"][0]
            elif parameter["name"] == "pcat":
                precipitation = parameter["values"][0]
                
        relevant_data.append({
            "Time": tid,
            "Temperature": temperature,
            "Precipitation": precipitation
        })
    return relevant_data

@dlt.resource(write_disposition="replace")
def event_resource():
    events = get_events()
    relevant_data = extract_relevant_data_smhi(events)
    for event in relevant_data:
        # print(event)  # Debugging: Print each event before yielding
        yield event

def load_stuff() -> None:
    # specify the pipeline name, destination and dataset name when configuring pipeline,
    # otherwise the defaults will be used that are derived from the current script name
    p = dlt.pipeline(
        pipeline_name='snowflake_pipeline_pipeline',
        destination='snowflake',
        dataset_name='Staging2'
    )
    p.run(event_resource())

if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)
    load_stuff()
<<<<<<< HEAD

# OLiEVoiNA_1915!
=======
    
>>>>>>> 4c71c1686068e0d9e3726d16f277e4d62ea57fd1
