import os
import pandas as pd
import matplotlib.pyplot as plt
import math

directory1 = "../data/non-interpolated/physiological/Original/Floored"
directory2 = "../data/non-interpolated/annotations/Original/Floored"
directory3 = "../data/non-interpolated/physiological/Generated"
directory4 = "../data/non-interpolated/annotations/Generated"

dir1 = "../data/non-interpolated/physiological/Original/Original"
dir2 = "../data/non-interpolated/annotations/Original/Original"


# # #Uncomment to generate floored values
# # #_____________________________________________________________________________
#Change the values and floor daqtime and jstime
# files = os.listdir(dir1)
# files = sorted(files)
# f = []

# for file in files:
#     if file.endswith(".csv"):
#         f.append(file)

# print(f)

# for i in range(len(f)):
# #for i in range(1):
#     df = pd.read_csv(dir1 + '/' + f[i]) 
#     print(df.head())
#     df['daqtime'] = df['daqtime'].map(lambda times: math.floor(times))
#     print(df.head())
#     df.to_csv(directory1 + "/" + f[i], index=False ,header=True)

# files = os.listdir(dir2)
# files = sorted(files)
# f = []

# for file in files:
#     if file.endswith(".csv"):
#         f.append(file)

# print(f)

# for i in range(len(f)):
# #for i in range(1):
#     df = pd.read_csv(dir2 + '/' + f[i]) 
#     print(df.head())
#     df['jstime'] = df['jstime'].map(lambda times: math.floor(times))
#     print(df.head())
#     df.to_csv(directory2 + "/" + f[i], index=False ,header=True)

# #__________________________________________________________________________
#Generate physiological based on annotations floored

# files = os.listdir(directory1)
# files = sorted(files)
# f = []

# for file in files:
#     if file.endswith(".csv"):
#         f.append(file)

# #for i in range(1):
# for i in range(len(f)):
#     df1 = pd.read_csv(directory1 + '/' + f[i])  #Physiological
#     df2 = pd.read_csv(directory2 + '/' + f[i])  #Annotations
#     arr = df2["jstime"].values
#     #print(arr)
#     df_new = df1[df1["daqtime"].isin(arr)]
#     df_new2 = df_new.reset_index(drop=True)
#     df_new2.to_csv(directory3 + "/" + f[i], index=False ,header=True)


#_________________________________________________________________________
#Generate annotations based on generated phisiological






files = os.listdir(directory3)
files = sorted(files)
f = []

for file in files:
    if file.endswith(".csv"):
        f.append(file)

#for i in range(1):
for i in range(len(f)):
    df1 = pd.read_csv(directory3 + '/' + f[i])  #Physiological
    df2 = pd.read_csv(directory2 + '/' + f[i])  #Annotations
    arr = df1["daqtime"].values
    #print(arr)
    df_new = df2[df2["jstime"].isin(arr)]
    df_new2 = df_new.reset_index(drop=True)
    df_new2.to_csv(directory4 + "/" + f[i], index=False ,header=True)

