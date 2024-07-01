import requests
import json
import yaml
import os
from datetime import datetime, timedelta

os.makedirs(f'weather_data', exist_ok=True)

with open('config.yaml', 'r') as file:
    config_data = yaml.safe_load(file)

api_key = config_data['OWM_KEY']
latitude = config_data['latitude']
longitude = config_data['longitude']


def fetch(data_year):  # returns true if there is new data
    file_path = f'weather_data/OWM_{data_year}.json'

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
                    start_date = data_end_date + timedelta(days=1)
                except:  # something is wrong with data
                    existing_data = []  # just start over
                complete = False
    else:
        existing_data = []

        # Fetch new data - this section API Specific
    if not complete:
        fetch_date = start_date

        while fetch_date <= end_date:
            print(f"Adding data for {fetch_date}")
            new_data = call_api(fetch_date)
            # just pull new data and append
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
def call_api(date):
    base_url = 'https://api.openweathermap.org/data/3.0/onecall/day_summary'

    try:
        date_str = date.strftime('%Y-%m-%d')
        url = f"{base_url}?lat={latitude}&lon={longitude}&date={date_str}&appid={api_key}&units=metric"
        response = requests.get(url)

        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error querying the API: {e}")
        return None


###############################################################################


def main():
    fetch(2019)


if __name__ == "__main__":
    main()
