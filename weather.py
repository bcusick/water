import requests
import json
import yaml
import os
from datetime import datetime, timedelta

# Path to the JSON file
file_path = f'weather_{data_year}.json'

with open('config.yaml', 'r') as file:
        config_data = yaml.safe_load(file)
    
KEY       = config_data['OPENWeather_KEY'] 
latitude    = config_data['latitude']
longitude   = config_data['longitude']

def fetch(data_year): #returns true if there is new data
    
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
            last_fetched_date_str = existing_data[-1]['date']
            last_fetched_date = datetime.strptime(last_fetched_date_str, "%Y-%m-%d")

            if last_fetched_date == end_date:
                complete = True #dataset complete
            else:
                start_date = last_fetched_date + timedelta(days=1)
    else:
        existing_data = []    
           
    # Fetch new data - this section API Specific
    if not complete:
        fetch_date = start_date

        while fetch_date <= end_date:
            print(f"Adding data for {fetch_date}")
            new_data = call_API(fetch_date)  
            #just pull new data and append      
            existing_data.append(new_data)
            fetch_date += timedelta(days=1)
        try:
            with open(file_path, 'w') as f:
                json.dump(existing_data, f, indent=4)
            
        except IOError as e:
            print(f"Error writing to file: {e}")

        retval = 1
      
    else:
      retval = 0

    return retval

# Function to fetch data from API
def call_API(date):
    API_KEY = KEY
    BASE_URL = 'https://api.openweathermap.org/data/3.0/onecall/day_summary'

    try:
        date_str = date.strftime('%Y-%m-%d')
        url = f"{BASE_URL}?lat={latitude}&lon={longitude}&date={date_str}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        
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