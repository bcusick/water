
import requests
import json
import os
import yaml
from datetime import datetime, timedelta

with open('config.yaml', 'r') as file:
        config_data = yaml.safe_load(file)
    
KEY       = config_data['OPENet_KEY'] 
latitude    = config_data['latitude']
longitude   = config_data['longitude']

# Function to fetch data from API
def call_API(args):
    # set your API key before making the request
    header = {"Authorization": KEY}

    try:
        response = requests.post(
            url="https://openet-api.org/raster/timeseries/point",
            headers=header,
            json=args
        )
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error querying the API: {e}")
        return None

def fetch(data_year): #returns true if there is new data
    
    complete = False
    current_year = datetime.now().year
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    start_date_str = f"{data_year}-01-01"
    end_date_str = f"{data_year}-12-31"

    # setup date range to pass to API
    date_range = [
            start_date_str,
            end_date_str]

    if data_year == current_year:
        date_range[1] = yesterday_str
        
    # Endpoint arguments
    args = {
        "date_range": date_range,
        "interval": "daily",
        "geometry": [
            longitude,
            latitude
        ],
        "model": "Ensemble",
        "variable": "ETo",
        "reference_et": "CIMIS",
        "units": "in",
        "file_format": "JSON"
    }
  
    # Path to the JSON file
    file_path = f'ETo_{data_year}.json'

    # Check if the file exists
    if os.path.exists(file_path):
        # Load existing data
        with open(file_path, 'r') as f:
            existing_data = json.load(f)
        
        # Determine the last fetched date from existing data
        if existing_data:
            last_fetched_date_str = existing_data[-1]['time']
            last_fetched_date = datetime.strptime(last_fetched_date_str, "%Y-%m-%d")

            if last_fetched_date_str == f'{data_year}-12-31' or last_fetched_date == yesterday:
                complete = True #dataset complete
            else:
                args["date_range"] = [start_date_str, yesterday_str]
    else:
        existing_data = []

    # Fetch new data
    if not complete:
        print(args)
        new_data = call_API(args)
        
        retval = 1
        try:
            with open(file_path, 'w') as f:
                json.dump(new_data, f, indent=4)
            #print(f"Data successfully saved to {file_path}")
        except IOError as e:
            print(f"Error writing to file: {e}")
        
    else:
        retval = 0

    return retval


###############################################################################


def main():
    
    fetch(2016)

if __name__ == "__main__":
    main()

