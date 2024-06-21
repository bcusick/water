import requests
import json
import yaml
from datetime import datetime, timedelta

#TODO Integrate into project

with open('config.yaml', 'r') as file:
    config_data = yaml.safe_load(file)

api_key = config_data['CIMIS_KEY']
latitude = config_data['latitude']
longitude = config_data['longitude']
data_year = 2024
current_year = datetime.now().year
yesterday = datetime.now().date() - timedelta(days=1)




file_path = f'cimis_{data_year}_77.json'

start_date = datetime(data_year, 1, 1).date()
end_date = datetime(data_year, 12, 31).date()

if data_year == current_year:
    end_date = yesterday

start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')
# "lat=34.99,lng=-118.34"
# '77, 139, 158'
# station = f'lat={latitude},lng={longitude}'
station = "77"
data_items = [
             'day-eto',
             'day-asce-eto',
             'day-precip',
             ]

data_items_str = ', '.join(data_items)
base_url = 'http://et.water.ca.gov/api/data'

url = f'{base_url}?appKey={api_key}&targets={station}&startDate={start_date_str}&endDate={end_date_str}&dataItems={data_items_str}'

response = requests.get(url)
response.raise_for_status()  # Raise an error for bad status code

data = response.json()
data_processed = []

for record in data["Data"]["Providers"][0]["Records"]:

    extract = {
        'date': record["Date"],
        'eto_asce': record["DayAsceEto"]["Value"],
        'eto_cimis': record["DayEto"]["Value"],
        'rainfall': record["DayPrecip"]["Value"]
    }
    data_processed.append(extract)

with open(file_path, 'w') as f:
    json.dump(data_processed, f, indent=4)