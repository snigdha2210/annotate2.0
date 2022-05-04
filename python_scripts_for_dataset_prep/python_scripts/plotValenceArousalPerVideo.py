import os
import pandas as pd
import matplotlib.pyplot as plt

directory = "../data/non-interpolated/annotations/Original/Original"

files = os.listdir(directory)
files = sorted(files)
f = []

for file in files:
    if file.endswith(".csv"):
        f.append(file)

subjects = []

for i in range(len(f)):
    df = pd.read_csv(directory + '/' + f[i])
    if len(f[i]) == 9:
        name = f[i][:5]
        name = name[4:]
    if len(f[i]) == 10:
        name = f[i][:6]
        name = name[4:]
    df['subject'] = name
    subjects.append(df)

video_nums = [1,2,3,4,5,6,7,8,10,11,12]

for vnum in video_nums:
#for vnum in range(1,3):
    df = pd.DataFrame()
    for i in range(len(subjects)):
    #for i in range(1):
        df1 = subjects[i].loc[subjects[i]['video'] == vnum]
        temp = df1.iloc[0]['jstime']

        for index, row in df1.iterrows():
            df1.loc[index, 'jstime'] -= temp

        df = df.append(df1, ignore_index=True)

        X = df1['jstime']
        Y = df1['valence']
        Z = df1['arousal']

        plt.plot(X, Y, label="valence")
        plt.plot(X, Z, label="arousal")
        plt.legend()
        plt.title(f"Subject {df1.iloc[0]['subject']} ; Video {vnum}")
        plt.show()

    print(df) 