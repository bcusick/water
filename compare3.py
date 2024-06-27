import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

import plotly.graph_objs as go
import plotly.offline as pyo

from sklearn.linear_model import LinearRegression

first = 1992
last = 2023
years = np.arange(first, last + 1)

# Create a list to hold the plotly traces
traces = []

final_cumsum_values = []
valid_years = []
for data_year in years:
    pd.options.mode.chained_assignment = None
    # Skip the year 2019
    if data_year == 2019:
        continue

    file_path = f'weather_data/CIMIS_{data_year}.json'

    df = pd.read_json(file_path)
    df.set_index('date', inplace=True)
    df.index = pd.to_datetime(df.index)

    cumsum = df['rainfall'].cumsum()

    # Extract the final value of the cumulative sum
    final_cumsum_value = cumsum.iloc[-1]
    final_cumsum_values.append(final_cumsum_value)
    valid_years.append(data_year)

# Create a trace for the final cumulative sum values
trace = go.Scatter(
    x=valid_years,
    y=final_cumsum_values,
    mode='markers+lines',
    name='Final Cumulative Sum'
)

# Fit a linear regression model to add a trendline
X = np.array(valid_years).reshape(-1, 1)
y = np.array(final_cumsum_values)
model = LinearRegression().fit(X, y)
trendline = model.predict(X)

# Create a trace for the trendline
trendline_trace = go.Scatter(
    x=valid_years,
    y=trendline,
    mode='lines',
    name='Trendline',
    line=dict(dash='dash')
)

# Define the layout
layout = go.Layout(
    title='Final Cumulative Sum of ETO CIMIS over Years',
    xaxis=dict(title='Year'),
    yaxis=dict(title='Final Cumulative Sum of ETO CIMIS')
)

# Create a figure
fig = go.Figure(data=[trace, trendline_trace], layout=layout)

# Save the plot as an HTML file
pyo.plot(fig, filename='final_cumsum_trendline_plot.html')

# Optionally display the plot in the notebook (uncomment if running in a Jupyter notebook)
# pyo.iplot(fig)

