import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yaml
import json

import ETo
import weather

def load_data(data_year):
    with open('config.yaml', 'r') as file:
        config_data = yaml.safe_load(file)
    try:
        budBreak = config_data['budbreak'][f'{data_year}']
    except:
        budBreak = config_data['budbreak'][f'default']
    vines = config_data['vines']
    end_date = config_data['end_date']

    retval = 1
    retval &= ETo.fetch(data_year)
    retval &= weather.fetch(data_year)

    if retval:
        print('data updated.')
    else:
        #print('no new data')
        pass

    # This dataset doesn't need processing, load as is
    df1 = pd.read_json(f'ETo_{data_year}.json')
    df1.rename(columns={"time": "date"}, inplace=True)
    # Process 2nd dataset to extract relevant fields
    with open(f'weather_{data_year}.json', 'r') as file:
        weather_data = json.load(file)
    weather_data_processed = []
    for entry in weather_data:
        rainfall = entry["precipitation"]["total"] / 25.4  # convert mm to inch
        new_entry = {
            "date": entry["date"],
            "min_temp": entry["temperature"]["min"],
            "max_temp": entry["temperature"]["max"],
            "rainfall": rainfall,
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
    df = merged_df[(merged_df.index >= set_start_date) & (merged_df.index <= set_end_date)]
    ############################################################################
    pd.options.mode.chained_assignment = None

    # calc additional data
    df['mean_temp'] = df[['min_temp', 'max_temp']].mean(axis=1)
    df['max_temp_F'] = df['max_temp'] * 9 / 5 + 32
    df['eto_14'] = df['eto'].ewm(span=14, adjust=False).mean()
    df['eto_rain'] = df['eto'] - df['rainfall']
    df['eto_rain'] = df['eto_rain'].apply(lambda x: max(0, x))  # Replace negative values with zero
    df['eto_rain_14'] = df['eto_rain'].ewm(span=14, adjust=False).mean()
    df['dd'] = df['mean_temp'] - 10
    df['dd'] = df['dd'].apply(lambda x: max(0, x))  # Replace negative values with zero
    df['dd_sum'] = df['dd'].cumsum()
    df['kc'] = 0.87 / (1 + np.exp(-1 * ((df['dd_sum'] - 525) / 301)))

    df['gal_100'] = 4 * 6 * 144 * df['eto_rain_14'] / 231 * df['kc'] * 1
    df['gal_75'] = 4 * 6 * 144 * df['eto_rain_14'] / 231 * df['kc'] * 0.75
    df['gal_50'] = 4 * 6 * 144 * df['eto_rain_14'] / 231 * df['kc'] * 0.5

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
    df['gal_max'] = 4 * 6 * 144 * df['eto_rain_14'] / 231 * 0.7 * 1

    return df


def plot_1(data_year):
    df = load_data(data_year)

    plt.figure(figsize=(12, 6))

    plt.plot(df.index, df['gal_100'], label='100%', linestyle='-', color='aqua')
    plt.plot(df.index, df['gal_75'], label='75%', linestyle='-', color='turquoise')
    plt.plot(df.index, df['gal_50'], label='50%', linestyle='-', color='aquamarine')
    plt.axhline(y=1, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    plt.text(df.index[0], 1.03, '6-hour', color='black', fontsize=10, va='center')
    plt.axhline(y=1.333, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    plt.text(df.index[0], 1.363, '8-hour', color='black', fontsize=10, va='center')
    plt.axhline(y=2, color='silver', linestyle='--')  # Adding a horizontal line at y=1
    plt.text(df.index[0], 2.03, '12-hour Max', color='black', fontsize=10, va='center')

    plt.xlabel('Day')
    plt.ylabel('Gal/day')
    plt.title(f'Gallons/day v. % Deficit {data_year}')

    #plt.ylim(0, 1.5)  # Set the y-axis limits 
    plt.grid(axis='x', linestyle='--')
    plt.legend()
    plt.show()

    return None


def plot_2(data_year):
    df = load_data(data_year)

    plt.figure(figsize=(12, 6))

    plt.plot(df.index, df['save_100_sum'], label='100%', linestyle='-', color='aqua')
    plt.plot(df.index, df['save_75_sum'], label='75%', linestyle='-', color='turquoise')
    plt.plot(df.index, df['save_50_sum'], label='50%', linestyle='-', color='aquamarine')

    plt.xlabel('Day')
    plt.ylabel('Gallons')
    plt.title(f'Gallons Saved {data_year} Entire Vineyard')
    plt.axhline(y=0, color='silver', linestyle='--')  # Adding a horizontal line 
    plt.grid(axis='x', linestyle='--')
    plt.legend()
    plt.show()

    return None


def plot_3(data_year):
    df = load_data(data_year)

    fig, axes = plt.subplots(2, 2, figsize=(20, 10))

    axes[0, 0].plot(df.index, df['gal_max'], label='Simple', linestyle='-', color='silver')
    axes[0, 0].plot(df.index, df['gal_100'], label='100%', linestyle='-', color='aqua')
    axes[0, 0].plot(df.index, df['gal_75'], label='75%', linestyle='-', color='turquoise')
    axes[0, 0].plot(df.index, df['gal_50'], label='50%', linestyle='-', color='aquamarine')
    axes[0, 0].axhline(y=1, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    axes[0, 0].text(df.index[0], 1.03, '6-hour', color='black', fontsize=10, va='center')
    axes[0, 0].axhline(y=1.333, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    axes[0, 0].text(df.index[0], 1.363, '8-hour', color='black', fontsize=10, va='center')
    axes[0, 0].axhline(y=2, color='silver', linestyle='--')  # Adding a horizontal line at y=1
    axes[0, 0].text(df.index[0], 2.03, '12-hour Max', color='black', fontsize=10, va='center')
    axes[0, 0].set_xlabel('Day')
    axes[0, 0].set_ylabel('Gal/day')
    axes[0, 0].set_title(f'Gallons/day v. % Deficit {data_year}')
    axes[0, 0].grid(axis='x', linestyle='--')
    axes[0, 0].legend()

    axes[0, 1].plot(df.index, df['save_100_sum'], label='100%', linestyle='-', color='aqua')
    axes[0, 1].plot(df.index, df['save_75_sum'], label='75%', linestyle='-', color='turquoise')
    axes[0, 1].plot(df.index, df['save_50_sum'], label='50%', linestyle='-', color='aquamarine')
    axes[0, 1].set_xlabel('Day')
    axes[0, 1].set_ylabel('Gallons')
    axes[0, 1].set_title(f'Gallons Saved {data_year} Entire Vineyard')
    axes[0, 1].axhline(y=0, color='silver', linestyle='--')  # Adding a horizontal line
    axes[0, 1].grid(axis='x', linestyle='--')
    axes[0, 1].legend()

    axes[1, 0].plot(df.index, df['eto_14'], linestyle='-', color='aquamarine')
    #axes[1,0].plot(df.index, df['eto_rain'], linestyle='-', color='blue')
    axes[1, 0].set_xlabel('Day')
    axes[1, 0].set_ylabel('inches')
    axes[1, 0].set_title(f'ETo {data_year}')
    axes[1, 0].grid(axis='x', linestyle='--')

    axes[1, 1].plot(df.index, df['kc'], linestyle='-', color='turquoise')
    axes[1, 1].set_xlabel('Day')
    axes[1, 1].set_ylabel('%')
    axes[1, 1].set_title(f'Crop Factor {data_year}')
    axes[1, 1].grid(axis='x', linestyle='--')

    plt.tight_layout()
    plt.show()

    return None


def plot_4(data_year):
    df = load_data(data_year)

    fig, axes = plt.subplots(2, 2, figsize=(20, 10))

    axes[0, 0].plot(df.index, df['gal_max'], label='Simple', linestyle='-', color='silver')
    # axes[0, 0].plot(df.index, df['gal_100'], label='100%', linestyle='-', color='aqua')
    # axes[0, 0].plot(df.index, df['gal_75'], label='75%', linestyle='-', color='turquoise')
    # axes[0, 0].plot(df.index, df['gal_50'], label='50%', linestyle='-', color='aquamarine')
    # axes[0, 0].axhline(y=1, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    # axes[0, 0].text(df.index[0], 1.03, '6-hour', color='black', fontsize=10, va='center')
    # axes[0, 0].axhline(y=1.333, color='black', linestyle='-')  # Adding a horizontal line at y=1
    # axes[0, 0].text(df.index[0], 1.363, '8-hour', color='black', fontsize=10, va='center')
    # axes[0, 0].axhline(y=2, color='black', linestyle='-')  # Adding a horizontal line at y=1
    # axes[0, 0].text(df.index[0], 2.03, '12-hour Max', color='black', fontsize=10, va='center')
    axes[0, 0].set_xlabel('Day')
    axes[0, 0].set_ylabel('Gal/day')
    axes[0, 0].set_title(f'Gallons per Day {data_year}')
    axes[0, 0].grid(axis='x', linestyle='--')
    #axes[0, 0].legend()

    axes[0, 1].plot(df.index, df['eto_14'], linestyle='-', color='aquamarine')
    axes[0, 1].set_xlabel('Day')
    axes[0, 1].set_ylabel('inches')
    axes[0, 1].set_title(f'ETo {data_year}')
    axes[0, 1].grid(axis='x', linestyle='--')

    axes[1, 0].plot(df.index, df['kc'], linestyle='-', color='turquoise')
    axes[1, 0].set_xlabel('Day')
    axes[1, 0].set_ylabel('%')
    axes[1, 0].set_title(f'Crop Factor {data_year}')
    axes[1, 0].grid(axis='x', linestyle='--')

    axes[1, 1].plot(df.index, df['dd_sum'], linestyle='-', color='aqua')
    axes[1, 1].set_xlabel('Day')
    axes[1, 1].set_ylabel('DDs')
    axes[1, 1].set_title(f'Degree Days {data_year}')
    axes[1, 1].grid(axis='x', linestyle='--')

    plt.tight_layout()
    plt.show()

    return None


def plot_5(data_year):
    df = load_data(data_year)

    fig, ax1 = plt.subplots()

    ax1.plot(df.index, df['eto'], label='eto', linestyle='-', color='aqua')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('inches', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()  # Create a second y-axis

    ax2.plot(df.index, df['max_temp_F'], label='temp', linestyle='-', color='violet')
    ax2.set_ylabel('deg F', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    plt.title(f'ETo and Temp. {data_year}')

    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))

    plt.show()

    return None


def plot_6(data_year):
    df = load_data(data_year)

    fig, ax1 = plt.subplots()

    ax1.plot(df.index, df['eto'], label='eto', linestyle='-', color='aqua')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('inches', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()  # Create a second y-axis

    ax2.plot(df.index, df['rainfall'], label='rain', linestyle='-', color='violet')
    ax2.set_ylabel('inches', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    plt.title(f'ETo and Rain. {data_year}')

    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))

    plt.show()

    return None


def plot_7(data_year):
    df = load_data(data_year)

    plt.figure(figsize=(12, 6))

    plt.plot(df.index, df['eto_14'], label='eto', linestyle='-', color='aqua')
    plt.plot(df.index, df['eto_rain_14'], label='eto-rain', linestyle='-', color='turquoise')

    plt.xlabel('Day')
    plt.ylabel('inches')
    plt.axhline(y=0, color='silver', linestyle='--')  # Adding a horizontal line 
    plt.title(f'ETt v. -Rain {data_year}')

    plt.grid(axis='x', linestyle='--')
    plt.legend()
    plt.show()

    return None


def plot_8(data_year):
    df = load_data(data_year)

    fig, ax = plt.subplots()

    #ax.plot(df.index, df['mins_100'], label='100%', linestyle='-', color='aqua')
    ax.plot(df.index, df['mins_50'], label='actual', linestyle='-', marker='o', color='turquoise')
    ax.plot(df.index, df['control_50'], label='control', linestyle='-', color='blue')

    # ax.plot(df.index, df['mins_100'], label='actual', linestyle='-', marker='o', color='violet')
    ax.plot(df.index, df['control'], label='control', linestyle='-', color='purple')

    y_max = df['mins_100'].max()
    y_ticks = np.arange(0, y_max + 30, 10)
    ax.set_yticks(y_ticks)

    plt.xlabel('Day')
    plt.ylabel('Minutes')
    plt.title(f'Time Control {data_year}')

    #plt.grid(axis='x', linestyle='--')
    ax.grid(True)
    plt.legend()
    plt.show()

    return None


def plot_9(data_year):
    df = load_data(data_year)

    plt.figure(figsize=(12, 6))

    plt.plot(df.index, df['step_gals_50'], linestyle='-', color='aqua')

    plt.xlabel('Day')
    plt.ylabel('Gallons')
    plt.title(f'Gallons/Day {data_year}')
    plt.grid(True)

    plt.show()

    return None


def plot_10(data_year):
    df = load_data(data_year)

    plt.figure(figsize=(12, 6))

    plt.plot(df.index, df['step_gals_50_sum'], linestyle='-', color='aqua')

    plt.xlabel('Day')
    plt.ylabel('Gallons')
    plt.title(f'Gallons Total {data_year}')
    plt.grid(True)

    plt.show()

    return None


###############################################################################


def main():
    plot_1(2024)
    plot_1(2023)
    plot_1(2022)


if __name__ == "__main__":
    main()
