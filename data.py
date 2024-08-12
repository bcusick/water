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
    set_start_date = pd.to_datetime(f'{data_year}-{budBreak}')
    set_end_date = pd.to_datetime(f'{data_year}-{end_date}')
    df = merged_df
    df = merged_df[(merged_df.index >= set_start_date) & (merged_df.index <= set_end_date)]

    ############################################################################
    pd.options.mode.chained_assignment = None

    # calc additional data
    df['day_of_year'] = df.index.dayofyear
    df['mean_temp'] = df[['min_temp', 'max_temp']].mean(axis=1)
    df['max_temp_F'] = df['max_temp'] * 9 / 5 + 32
    df['eto_14'] = df['eto_cimis'].ewm(span=14, adjust=False).mean()
    df['eto_rain_raw'] = df['eto_cimis'] - df['rainfall']
    df['eto_rain'] = df['eto_rain_raw'].apply(lambda x: max(0, x))  # Replace negative values with zero
    df['eto_rain_14'] = df['eto_rain'].ewm(span=14, adjust=False).mean()
    df['dd'] = df['mean_temp'] - 10
    df['dd'] = df['dd'].apply(lambda x: max(0, x))  # Replace negative values with zero
    df['dd_sum'] = df['dd'].cumsum()
    df['kc'] = 0.87 / (1 + np.exp(-1 * ((df['dd_sum'] - 525) / 301)))

    df['gal_100'] = 4 * 6 * 144 * df['eto_rain_14'] / 231 * df['kc'] * 1
    df['gal_75'] = 4 * 6 * 144 * df['eto_rain_14'] / 231 * df['kc'] * 0.75
    df['gal_50'] = 4 * 6 * 144 * df['eto_rain_14'] / 231 * df['kc'] * 0.5
    df['gal_50_daily'] = 4 * 6 * 144 * df['eto_rain'] / 231 * df['kc'] * 0.5
    df['def_min'] = (4.5 / 6) / df['gal_100'] * 100
    df['def_max'] = (2 / 6) / df['gal_100'] * 100

    df['def_min'] = df['def_min'].apply(lambda x: min(x, 100))
    df['def_max'] = df['def_max'].apply(lambda x: min(x, 100))

    df['inch_50'] = df['eto_rain'] * df['kc'] * 0.5 *5

    df['mins_100'] = 4 * 6 * 144 * df['eto_rain'] / 231 * df['kc'] * 1 * 60
    df['mins_50'] = 4 * 6 * 144 * df['eto_rain'] / 231 * df['kc'] * 0.5 * 60

    df['control_50'] = np.ceil(df['mins_50'] / 10) * 10
    df['step_gals_50'] = df['control_50'] / 60 * vines
    df['step_gals_50_sum'] = df['step_gals_50'].cumsum()

    df['control_100'] = np.ceil(df['mins_100'] / 10) * 10
    df['control_100'] = df['control_100'].apply(lambda x: min(x, 60))

    df['control'] = df[['control_50', 'control_100']].max(axis=1)

    df['save_100'] = (1 - df['gal_100']) * vines
    df['save_100_sum'] = df['save_100'].cumsum()

    df['save_75'] = (1 - df['gal_75']) * vines
    df['save_75_sum'] = df['save_75'].cumsum()

    df['save_50'] = (1 - df['gal_50']) * vines
    df['save_50_sum'] = df['save_50'].cumsum()

    # placeholder to view other scenarios
    df['gal_cap'] = 450 * df['eto_rain_raw'] / 231
    df['gal_max'] = 450 * df['eto_cimis'] / 231 #calculated emitter affected area
    pass
    return df


###############################################################################


def main():
    load(2018)



if __name__ == "__main__":
    main()
