import matplotlib.pyplot as plt
import numpy as np

import data

def plot_A(data_year):
    df = data.load(data_year)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['eto_14'], linestyle='-', color='aquamarine')

    plt.xlabel('Day')
    plt.ylabel('Inches')
    plt.title(f'ETo {data_year}')

    #plt.ylim(0, 1.5)  # Set the y-axis limits
    plt.grid(axis='x', linestyle='--')
    #plt.legend()
    plt.show()

    return None


def plot_B(data_year):
    df = data.load(data_year)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['gal_max'], label='Simple', linestyle='-', color='silver')

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
    # plt.legend()
    plt.show()

    return None


def plot_C(data_year):
    df = data.load(data_year)

    fig, axes = plt.subplots(2, 2, figsize=(20, 10))

    axes[0, 0].plot(df.index, df['gal_max'], label='Simple', linestyle='-', color='silver')
    axes[0, 0].plot(df.index, df['gal_100'], label='100%', linestyle='-', color='aqua')
    axes[0, 0].plot(df.index, df['gal_75'], label='75%', linestyle='-', color='turquoise')
    axes[0, 0].plot(df.index, df['gal_50'], label='50%', linestyle='-', color='aquamarine')
    axes[0, 0].axhline(y=1, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    axes[0, 0].text(df.index[0], 1.03, '6-hour', color='black', fontsize=10, va='center')
    axes[0, 0].axhline(y=1.333, color='black', linestyle='-')  # Adding a horizontal line at y=1
    axes[0, 0].text(df.index[0], 1.363, '8-hour', color='black', fontsize=10, va='center')
    axes[0, 0].axhline(y=2, color='black', linestyle='-')  # Adding a horizontal line at y=1
    axes[0, 0].text(df.index[0], 2.03, '12-hour Max', color='black', fontsize=10, va='center')
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

def plot_D(data_year):
    df = data.load(data_year)

    plt.figure(figsize=(12, 6))
    #plt.plot(df.index, df['gal_max'], label='Simple', linestyle='-', color='silver')
    #plt.plot(df.index, df['gal_100'], label='100%', linestyle='-', color='aqua')
    #plt.plot(df.index, df['gal_75'], label='75%', linestyle='-', color='turquoise')
    plt.plot(df.index, df['gal_50_daily'], label='daily', linestyle='-', color='turquoise')
    plt.plot(df.index, df['gal_50'], label='2week avg', linestyle='-', color='aquamarine')

    plt.axhline(y=0.83, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    plt.text(df.index[0], 0.86, '5-hour', color='black', fontsize=10, va='center')

    plt.axhline(y=1, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    plt.text(df.index[0], 1.03, '6-hour', color='black', fontsize=10, va='center')



    plt.axhline(y=1.17, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    plt.text(df.index[0], 1.2, '7-hour', color='black', fontsize=10, va='center')

    plt.axhline(y=1.333, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    plt.text(df.index[0], 1.363, '8-hour', color='black', fontsize=10, va='center')

    plt.axhline(y=1.5, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    plt.text(df.index[0], 1.53, '9-hour', color='black', fontsize=10, va='center')

    plt.axhline(y=2, color='silver', linestyle='--')  # Adding a horizontal line at y=1
    plt.text(df.index[0], 2.03, '12-hour Max', color='black', fontsize=10, va='center')

    plt.xlabel('Day')
    plt.ylabel('Gal/day')
    plt.title(f'Gallons/day {data_year}')

    #plt.ylim(0, 1.5)  # Set the y-axis limits
    plt.grid(axis='x', linestyle='--')
    plt.legend()
    plt.show()

    return None

def plot_E(data_year):
    df = data.load(data_year)

    fig, ax1 = plt.subplots(figsize=(20, 10))

    ax1.plot(df.index, df['eto_cimis'], label='eto', linestyle='-', color='aqua')
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

def plot_F(data_year):
    df = data.load(data_year)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['save_50_sum'], linestyle='-', color='aquamarine')

    plt.xlabel('Day')
    plt.ylabel('Inches')
    plt.title(f'ETo {data_year}')

    #plt.ylim(0, 1.5)  # Set the y-axis limits
    plt.grid(axis='x', linestyle='--')
    #plt.legend()
    plt.show()

    return None

def plot_G(data_year):
    df = data.load(data_year)

    plt.figure(figsize=(12, 6))

    plt.plot(df.index, df['def_min'], label='min', linestyle='-', color='turquoise')
    plt.plot(df.index, df['def_max'], label='max', linestyle='-', color='aquamarine')
    plt.axhline(y=75, color='silver', linestyle='--')  # Adding a horizontal line at y=1
    plt.axhline(y=50, color='silver', linestyle='--')  # Adding a horizontal line at y=1
    plt.axhline(y=40, color='silver', linestyle='--')  # Adding a horizontal line at y=1
    plt.axhline(y=30, color='silver', linestyle='--')  # Adding a horizontal line at y=1
    plt.axhline(y=20, color='silver', linestyle='--')  # Adding a horizontal line at y=1
    plt.axhline(y=10, color='silver', linestyle='--')  # Adding a horizontal line at y=1


    plt.xlabel('Day')
    plt.ylabel('% Actual')
    plt.title(f'% Deficit at Soil Capacity {data_year}')

    #plt.ylim(0, 1.5)  # Set the y-axis limits
    plt.grid(axis='x', linestyle='--')
    plt.legend()
    plt.show()

    return None

def plot_Comp(years):
    # Create a plot
    fig, ax = plt.subplots(figsize=(12, 6))
    #ax.plot(x, y)
    for year in years:
        df = data.load(year)
        ax.plot(df['day_of_year'], df['gal_50'], label=f'{year}', linestyle='-')
    # Add a horizontal band
    ax.axhspan(ymin=0.333, ymax=0.666, facecolor='lightgray', alpha=0.25, hatch='/')

    ax.axhline(y=0.83, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    ax.text(2, 0.86, '5-hour', color='black', fontsize=10, va='center')

    ax.axhline(y=1, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    ax.text(2, 1.03, '6-hour', color='black', fontsize=10, va='center')

    ax.axhline(y=1.17, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    ax.text(2, 1.2, '7-hour', color='black', fontsize=10, va='center')

    ax.axhline(y=1.333, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    ax.text(2, 1.363, '8-hour', color='black', fontsize=10, va='center')

    ax.axhline(y=1.5, color='silver', linestyle='-')  # Adding a horizontal line at y=1
    ax.text(2, 1.53, '9-hour', color='black', fontsize=10, va='center')

    ax.axhline(y=2, color='silver', linestyle='--')  # Adding a horizontal line at y=1
    ax.text(2, 2.03, '12-hour Max', color='black', fontsize=10, va='center')

    ax.set_xlabel('Day of Year')
    ax.set_ylabel('Gal/day')
    ax.set_title(f'Yearly Water Requirements')

    #plt.ylim(0, 1.5)  # Set the y-axis limits
    ax.grid(axis='x', linestyle='--')
    ax.legend()
    plt.show()
###############################################################################


def main():
    first = 2020
    last = 2024
    years = np.arange(first, last + 1)
    #plot_Comp(years)

    plot_D(2024)
    #plot_E(2024)

if __name__ == "__main__":
    main()