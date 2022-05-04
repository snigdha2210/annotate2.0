import os
from numpy.core.defchararray import index
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

directory = "1000/scores_2"

files = os.listdir(directory)
files = sorted(files)
f = []

for file in files:
    if file.endswith(".csv"):
        f.append(file)

vid2_windows_1000 = []

for i in range(len(f)):
    df = pd.read_csv(directory + '/' + f[i])
    if len(f[i]) == 16:
        name = f[i][:5]
        name = name[4:]
    if len(f[i]) == 17:
        name = f[i][:6]
        name = name[4:]
    df['subject'] = name
    vid2_windows_1000.append(df)


print(vid2_windows_1000[0].head())

subjectsOrder = []

for i in range(len(vid2_windows_1000)):
    subjectsOrder.append(vid2_windows_1000[i]["subject"].unique()[0])

print(subjectsOrder)

with open('numberOfPointsVideo2Window1000.txt', 'w') as f:
    f.write('______________________________________\n')
    f.write("____________Number Of Points______________\n")
    f.write('______________________________________\n')
    for i in range(len(vid2_windows_1000)):
        df = vid2_windows_1000[i]
        numberOfPoints = 0
        threshold = 3.5
        numberOfNewerPoints = 0

        for index, row in df.iterrows():
            if row["Score"] > threshold:
                numberOfNewerPoints += 1
            numberOfPoints += 1

        f.write(f'______________Subject {subjectsOrder[i]}_____________\n')
        f.write('______________________________________\n')
        f.write(f' Number Of points: {numberOfPoints}\n')
        f.write(f' Threshold score: {threshold}\n')
        f.write(f' Number Of points after thresholding: {numberOfNewerPoints}\n')


