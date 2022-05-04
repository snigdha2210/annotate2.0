import os
import pandas as pd
import matplotlib.pyplot as plt

directory1 = "../data/interpolated/physiological/Original"
directory2 = "../data/interpolated/annotations"
directory3 = "../data/interpolated/physiological/Generated"

files = os.listdir(directory1)
files = sorted(files)
f = []

for file in files:
    if file.endswith(".csv"):
        f.append(file)

#for i in range(1):
for i in range(len(f)):
    df1 = pd.read_csv(directory1 + '/' + f[i])  #Physiological
    df2 = pd.read_csv(directory2 + '/' + f[i])  #Annotations
    arr = df2["jstime"].values
    #print(arr)
    df_new = df1[df1["daqtime"].isin(arr)]
    df_new2 = df_new.reset_index(drop=True)
    df_new2.to_csv(directory3 + "/" + f[i], index=False ,header=True)