import numpy as np
import requests
import json
import yaml
import os
from datetime import datetime, timedelta

os.makedirs(f'weather_data', exist_ok=True)

with open('config.yaml', 'r') as file:
    config_data = yaml.safe_load(file)

api_key = config_data['CIMIS_KEY']
latitude = config_data['latitude']
longitude = config_data['longitude']


def fetch(data_year):
    file_path = f'weather_data/CIMIS_{data_year}.json'

    complete = False  # dataset complete flag
    current_year = datetime.now().year
    yesterday = datetime.now().date() - timedelta(days=1)

    start_date = datetime(data_year, 1, 1).date()
    end_date = datetime(data_year, 12, 31).date()

    if data_year == current_year:
        end_date = yesterday

    # Check if the file exists
    if os.path.exists(file_path):
        # Load existing data
        with open(file_path, 'r') as f:
            existing_data = json.load(f)

        # Determine the last fetched date from existing data
        if existing_data:
            data_days = (end_date - start_date).days + 1  # how many days should be in dataset
            if data_days == len(existing_data):
                complete = True  # dataset complete
            else:
                try:
                    data_end_date_str = existing_data[-1]['date']
                    data_end_date = datetime.strptime(data_end_date_str, "%Y-%m-%d").date()
                    #start_date = data_end_date + timedelta(days=1)
                    complete = False
                except:  # something is wrong with data
                    existing_data = []  # just start over
                    complete = False
    else:
        existing_data = []

    # Fetch new data - this section API Specific
    if not complete:
        new_data = call_api(start_date, end_date)
        try:
            with open(file_path, 'w') as f:
                json.dump(new_data, f, indent=4)

        except IOError as e:
            print(f"Error writing to file: {e}")
        retval = 1
    else:
        retval = 0

    return retval


def call_api(start_date, end_date):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    station = "77"
    data_items = [
                    'day-eto',
                    'day-asce-eto',
                    'day-precip',
                    'day-air-tmp-avg'
                 ]

    data_items_str = ', '.join(data_items)
    base_url = 'http://et.water.ca.gov/api/data'

    url = f'{base_url}?appKey={api_key}&targets={station}&startDate={start_date_str}&endDate={end_date_str}&dataItems={data_items_str}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status code

        data = response.json()
        data_processed = []

        for record in data["Data"]["Providers"][0]["Records"]:
            extract = {
                'date': record["Date"],
                'eto_asce': record["DayAsceEto"]["Value"],
                'eto_cimis': record["DayEto"]["Value"],
                'rainfall': record["DayPrecip"]["Value"],
                'temp_avg': record["DayAirTmpAvg"]["Value"]
            }
            data_processed.append(extract)
        return data_processed
    except requests.exceptions.RequestException as e:
        print(f"Error querying the API: {e}")

        return None


###############################################################################


def main():

    first = 1990
    last = 1995
    years = np.arange(first, last + 1)
    for year in years:
        print(f'Fetching data for year {year}')
        fetch(year)

if __name__ == "__main__":
    main()
