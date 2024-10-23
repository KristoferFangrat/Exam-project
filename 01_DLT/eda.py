from smhi_open_data import SMHIOpenDataClient, Parameter
from datetime import datetime, timedelta

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
    station_id=closest_station.id,  # ID of the closest station
    parameter=Parameter.TemperaturePast1h,  # Parameter for past 1-hour temperatures
    start_time=start_time,
    end_time=end_time
)

# Display the fetched data
for observation in observations:
    timestamp = observation['date'] / 1000  # Convert from milliseconds
    date_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    temperature = observation['value']
    print(f"Date: {date_time}, Temperature: {temperature}°C")
