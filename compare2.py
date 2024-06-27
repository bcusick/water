import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.offline as pyo

# Initialize the range of years
first = 1990
last = 2023
years = np.arange(first, last + 1)

# Create a list to hold the plotly traces
traces = []

# Loop through each year
for data_year in years:
    # Define file path
    file_path = f'weather_data/CIMIS_{data_year}.json'

    # Filter DataFrame based on date range
    set_start_date = pd.to_datetime(f'{data_year}-01-01')
    set_end_date = pd.to_datetime(f'{data_year}-10-31')

    # Read JSON file into a DataFrame
    df = pd.read_json(file_path)

    # Set index to 'date' column and convert to DateTime index
    df.set_index('date', inplace=True)
    df.index = pd.to_datetime(df.index)

    df2 = df[(df.index >= set_start_date) & (df.index <= set_end_date)]
    # Extract 'eto_cimis' column
    eto = df2['eto_cimis'].ewm(span=21, adjust=False).mean()

    # Convert index to day of the year
    days_of_year = df.index.dayofyear

    # Create a trace for the current year
    trace = go.Scatter(
        x=days_of_year,
        y=eto,
        mode='lines',
        name=str(data_year)
    )

    # Add the trace to the list
    traces.append(trace)

# Define the layout
layout = go.Layout(
    title='ETO CIMIS over Years',
    xaxis=dict(title='Day of Year'),
    yaxis=dict(title='ETO CIMIS')
)

# Create a figure
fig = go.Figure(data=traces, layout=layout)

# Save the plot as an HTML file
pyo.plot(fig, filename='eto_cimis_plot.html')

# Optionally display the plot in the notebook (uncomment if running in a Jupyter notebook)
# pyo.iplot(fig)
