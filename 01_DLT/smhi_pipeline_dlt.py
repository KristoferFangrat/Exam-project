import dlt
import requests
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

# Ange koordinater för platsen
latitude = 64.750244
longitude = 20.950917

api_url = f"https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{longitude}/lat/{latitude}/data.json"

def get_events():
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

def extract_relevant_data_smhi(weather_data, start_index, end_index):
    relevant_data = []
    for entry in weather_data["timeSeries"][start_index:end_index]:
        valid_time = entry["validTime"]
        tid = datetime.fromisoformat(valid_time[:])

        är_nederbörd = False
        for parameter in entry["parameters"]:
            if parameter["name"] == "t":
                temperature = parameter["values"][0]
            elif parameter["name"] == "pcat" and parameter["values"][0] > 0:
                är_nederbörd = True
                
        if är_nederbörd:
            precipitation = "Nederbörd"
        else:
            precipitation = "Ingen nederbörd"

        relevant_data.append({
            "Tid": tid,
            "Temperatur (°C)": temperature,
            "Nederbörd": precipitation,
            "Provider": "SMHI"
        })
    return relevant_data


@dlt.resource(write_disposition="append")
def event_resource():
    events = get_events()
    for event in events:
        yield event


def load_stuff() -> None:
    # specify the pipeline name, destination and dataset name when configuring pipeline,
    # otherwise the defaults will be used that are derived from the current script name
    p = dlt.pipeline(
        pipeline_name='snowflake_pipeline_pipeline',
        destination='snowflake',
        dataset_name='Staging2',
    )
    p.run(event_resource())


if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)
    load_stuff()