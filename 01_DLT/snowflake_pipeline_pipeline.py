import dlt
import requests
import os
from pathlib import Path


url = "https://polisen.se/api/events"
def get_events():
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


@dlt.resource(write_disposition="append")
def event_resource():
    events = get_events()
    for event in events:
        yield event


def load_events() -> None:

    p = dlt.pipeline(
        pipeline_name='snowflake_pipeline_pipeline',
        destination='snowflake',
        dataset_name='Staging1',
    )
    p.run(event_resource())
 
    


if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)
    load_events()

