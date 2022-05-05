import os
from numpy.core.defchararray import index
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

directory = "../data/non-interpolated/annotations/Generated"

files = os.listdir(directory)
files = sorted(files)
f = []

for file in files:
    if file.endswith(".csv"):
        f.append(file)

subjects_annotation = []

for i in range(len(f)):
    df = pd.read_csv(directory + '/' + f[i])
    df = df.drop(columns = ["video", "jstime"], axis=1)
    subjects_annotation.append(df)

df = subjects_annotation[0]
print(len(df))
print(df.head())

for i in range(1, len(subjects_annotation)):
    df = df.append(subjects_annotation[i])

# # USE TO GET FOR CLASSIFICATION
# def round_fn(x):
#     if(x == 5):
#         return "neutral"
#     elif(x > 5):
#         return "positive"
#     elif(x < 5):
#         return "negative"

# USE FOR REGRESSION
def round_fn(x):
    return round(x)

df['arousal'] = df['arousal'].apply(round_fn)
df['valence'] = df['valence'].apply(round_fn)

print(len(df))
print(df.head())


df.groupby(['valence']).count().plot(kind='bar')
plt.show()

df.groupby(['arousal']).count().plot(kind='bar')
plt.show()