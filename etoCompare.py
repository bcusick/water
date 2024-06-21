import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yaml
import json

data_year = 2023

df1 = pd.read_json(f'ETo_{data_year}.json')
df1.rename(columns={"time": "date"}, inplace=True)



df2 = pd.read_json(f'cimis_{data_year}_77.json')


df3 = pd.read_json(f'cimis_{data_year}_158.json')


# Set the data column as the index
df1.set_index('date', inplace=True)
df2.set_index('date', inplace=True)
df3.set_index('date', inplace=True)

# ensure correct format
df1.index = pd.to_datetime(df1.index)
df2.index = pd.to_datetime(df2.index)
df3.index = pd.to_datetime(df3.index)

columns_from_df2 = df2[['eto_cimis']].rename(columns={'eto_cimis': 'eto_cimis_77'})
columns_from_df3 = df3[['eto_cimis']].rename(columns={'eto_cimis': 'eto_cimis_158'})

# Concatenating columns to df3
merged_df = pd.concat([df1, columns_from_df2, columns_from_df3], axis=1)

set_start_date = pd.to_datetime(f'{data_year}-5-1')
set_end_date = pd.to_datetime(f'{data_year}-9-30')
df = merged_df[(merged_df.index >= set_start_date) & (merged_df.index <= set_end_date)]


pass