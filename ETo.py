import requests
import json
import yaml
import os
from datetime import datetime, timedelta

with open('config.yaml', 'r') as file:
        config_data = yaml.safe_load(file)
    
KEY       = config_data['OPENet_KEY'] 
latitude    = config_data['latitude']
longitude   = config_data['longitude']

def fetch(data_year): #returns true if there is new data
    
    # Path to the JSON file
    file_path = f'ETo_{data_year}.json'

    complete = False
    current_year = datetime.now().year
    yesterday = datetime.now() - timedelta(days=1)

    start_date = datetime(data_year, 1, 1)
    end_date = datetime(data_year, 12, 31)

    if data_year == current_year:
        end_date = yesterday

    # Check if the file exists
    if os.path.exists(file_path):
        # Load existing data
        with open(file_path, 'r') as f:
            existing_data = json.load(f)
        
        # Determine the last fetched date from existing data
        if existing_data:
            last_fetched_date_str = existing_data[-1]['time']
            last_fetched_date = datetime.strptime(last_fetched_date_str, "%Y-%m-%d")

            if last_fetched_date.day == end_date.day:
                complete = True #dataset complete
            else:
                start_date = last_fetched_date + timedelta(days=1)
    else:
        existing_data = []

    # Fetch new data - this section API Specific
    if not complete:
        
        new_data = call_API(start_date, end_date)
        #pull entire history again and overwrite.  
        try:
            with open(file_path, 'w') as f:
                json.dump(new_data, f, indent=4)
            #print(f"Data successfully saved to {file_path}")
        except IOError as e:
            print(f"Error writing to file: {e}")
        retval = 1

    else:
        retval = 0

    return retval

# Function to fetch data from API
def call_API(start_date, end_date):

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    date_range = [
            start_date_str,
            end_date_str]

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

###############################################################################


def main():
    
    fetch(2024)

if __name__ == "__main__":
    main()

