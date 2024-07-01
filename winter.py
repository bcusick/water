import pandas as pd
import numpy as np
import yaml
import json

import CIMIS
import OWM

def load(data_year):
    with open('config.yaml', 'r') as file:
        config_data = yaml.safe_load(file)
    try:
        budBreak = config_data['budbreak'][f'{data_year}']
    except:
        budBreak = config_data['budbreak'][f'default']
    vines = config_data['vines']
    end_date = config_data['end_date']

    CIMIS.fetch(data_year)
    OWM.fetch(data_year)

    # This dataset doesn't need processing, load as is
    df1 = pd.read_json(f'weather_data/CIMIS_{data_year}.json')

    # Process 2nd dataset to extract relevant fields
    with open(f'weather_data/OWM_{data_year}.json', 'r') as file:
        weather_data = json.load(file)
    weather_data_processed = []
    for entry in weather_data:
        rainfall = entry["precipitation"]["total"] / 25.4  # convert mm to inch
        new_entry = {
            "date": entry["date"],
            "min_temp": entry["temperature"]["min"],
            "max_temp": entry["temperature"]["max"],
        }
        weather_data_processed.append(new_entry)

    df2 = pd.DataFrame(weather_data_processed)

    # Set the data column as the index
    df1.set_index('date', inplace=True)
    df2.set_index('date', inplace=True)

    # ensure correct format
    df1.index = pd.to_datetime(df1.index)
    df2.index = pd.to_datetime(df2.index)

    # Merge df1 and df2 based on their indices
    merged_df = pd.merge(df1, df2, left_index=True, right_index=True)

    # Filter DataFrame based on date range
    set_start_date = pd.to_datetime(f'{data_year}-1-1')
    set_end_date = pd.to_datetime(f'{data_year}-4-1')
    #df = merged_df
    df = merged_df[(merged_df.index >= set_start_date) & (merged_df.index <= set_end_date)]

    ############################################################################
    pd.options.mode.chained_assignment = None

    # calc additional data

    #df['eto_14'] = df['eto_cimis'].ewm(span=14, adjust=False).mean()
    df['eto_rain'] = df['rainfall'] - df['eto_cimis']
    df['gallons'] = df['eto_rain'] * 450 / 231

    # Initial soil water content
    initial_content = 2.0
    max_capacity = 2.0

    # Running tally of soil water content
    soil_content = [initial_content]
    water_required = [initial_content]
    # Calculate running tally
    for index, row in df.iterrows():
        required = 0
        prev_content = soil_content[-1]
        current_content = prev_content + row['gallons']
        current_content = min(current_content, max_capacity) # Clamp to maximum capacity
        if current_content < 1:
            required = max_capacity - current_content
            current_content = current_content + required
        else:
            required = 0

        soil_content.append(current_content)
        water_required.append(required)


    # Remove the initial entry and add the result to the DataFrame
    df['soil_water_content'] = soil_content[1:]
    df['required'] = water_required[1:]
    df['total_water'] = df['required'].cumsum() * vines
    pass
    ###############################################################################

def main():
    load(2021)

if __name__ == "__main__":
    main()
