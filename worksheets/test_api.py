import requests
import json

url = "http://api.kolada.se/v2/municipality"
response = requests.get(url)
response.encoding = 'utf-8'

data = response.json()

# Print the structure of the data to understand its format
print("Data structure:")
print(json.dumps(data, ensure_ascii=False, indent=4))

# Assuming the data is a dictionary with a key 'values' that contains the list of entries
if isinstance(data, dict) and 'values' in data:
    entries = data['values']
else:
    entries = data

# Assuming each entry in the data has a 'title' field for the municipality name
municipality_name = "Stockholm"  # Replace with the specific municipality you want to filter on
filtered_data = [entry for entry in entries if isinstance(entry, dict) and entry.get('title') == municipality_name]

# Print the filtered data
print(f"Totala antal händelser för {municipality_name}: {len(filtered_data)}")
print(json.dumps(filtered_data, ensure_ascii=False, indent=4))