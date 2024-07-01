import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt


def total_area_occupied(r1, r2, d):
    # Calculate the individual areas
    A1 = math.pi * r1 ** 2
    A2 = math.pi * r2 ** 2

    if (r1+r2) <= d:
        A_overlap = 0
    else:
    # Calculate the area of overlap
        part1 = r1 ** 2 * math.acos((d ** 2 + r1 ** 2 - r2 ** 2) / (2 * d * r1))
        part2 = r2 ** 2 * math.acos((d ** 2 + r2 ** 2 - r1 ** 2) / (2 * d * r2))
        part3 = 0.5 * math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))
        A_overlap = part1 + part2 - part3
    # Calculate the total area
    A_sep = A1 + A2
    A_total = A1 + A2 - A_overlap
    print(f'diameter, {r * 2} | Area overlap, {A_overlap}')
    return A_total, A_sep

diameters = np.arange(0,26,1)

df = pd.DataFrame({'diameter':diameters})
areas =[]
areas_sep=[]

for diameter in diameters:
    r = diameter/2
    area, area_sep = total_area_occupied(r,r,12)
    areas_sep.append(area_sep)
    areas.append(area)

df['area'] = areas
df['area_sep'] = areas_sep

cap_1 = 1
cap_2 = 2

df['gal_1'] = df['area']  * cap_1 / 231
df['gal_2'] = df['area_sep']  * cap_1 / 231
df['percent1'] = (df['gal_1'] - df['gal_2']) / df['gal_1']

df['gal_3'] = df['area']  * cap_2 / 231
df['gal_4'] = df['area_sep']  * cap_2 / 231
df['percent2'] = (df['gal_3'] - df['gal_4']) / df['gal_3']

plt.figure(figsize=(12, 6))

#plt.plot(df['diameter'], df['gal_8'], label='8"', linestyle='-', color='green')
#plt.plot(df['diameter'], df['gal_4'], label='maximum', linestyle='-', color='aqua')
plt.plot(df['diameter'], df['gal_3'], label='maximum', linestyle='-', color='aqua')
#plt.plot(df['diameter'], df['gal_2'], label='minimum', linestyle='-', color='purple')
plt.plot(df['diameter'], df['gal_1'], label='minimum', linestyle='-', color='violet')


plt.axvline(x=12, color='silver', linestyle='--')  # Adding a horizontal line at y=1
#plt.text(10.75, 6.5, 'sandy', color='black', fontsize=10, va='center')
plt.axvline(x=18, color='silver', linestyle='--')  # Adding a horizontal line at y=1
#plt.text(16.75, 6.5, 'loamy', color='black', fontsize=10, va='center')
plt.axvline(x=24, color='silver', linestyle='--')  # Adding a horizontal line at y=1
#plt.text(23, 6.5, 'clay', color='black', fontsize=10, va='center')

plt.xlabel('Emitter Footprint (in)')
plt.ylabel('Retention (gallons)')
plt.title(f'Soil Water Storage Capacity')

plt.grid(axis='y', linestyle='-')
plt.legend()
plt.show()
pass








