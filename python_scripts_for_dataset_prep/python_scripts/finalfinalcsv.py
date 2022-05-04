import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


print("Creating Dataframe")

videos = [1,2,3,4,5,6,7,8]

MeanValenceAll = []
MinValenceAll = []
MaxValenceAll = []
MedianValenceAll = []
MeanArousalAll = []
MinArousalAll = []
MaxArousalAll = []
MedianArousalAll = []

MeanValenceProbed = []
MinValenceProbed = []
MaxValenceProbed = []
MedianValenceProbed = []
MeanArousalProbed = []
MinArousalProbed = []
MaxArousalProbed = []
MedianArousalProbed = []


for video in videos:
#for video in range(1,2):
    directory = "final_results_5000_all/video_" + str(video)

    df = pd.read_csv(directory + '/' + 'result.csv')
    
    MeanValenceValue = np.mean(df['Mean Valence'].values) 
    MaxValenceValue = np.max(df['Max Valence'].values) 
    MinValenceValue = np.min(df['Min Valence'].values) 
    MedianValenceValue = np.median(df['Median Valence'].values) 
    MeanArousalValue = np.mean(df['Mean Arousal'].values) 
    MaxArousalValue = np.max(df['Max Arousal'].values) 
    MinArousalValue = np.min(df['Min Arousal'].values) 
    MedianArousalValue = np.median(df['Median Arousal'].values) 

    MeanValenceAll.append(MeanValenceValue)
    MinValenceAll.append(MinValenceValue)
    MaxValenceAll.append(MaxValenceValue)
    MedianValenceAll.append(MedianValenceValue)
    MeanArousalAll.append(MeanArousalValue)
    MinArousalAll.append(MinArousalValue)
    MaxArousalAll.append(MaxArousalValue)
    MedianArousalAll.append(MedianArousalValue)

    directory = "final_results_5000_probed/video_" + str(video)

    df = pd.read_csv(directory + '/' + 'result.csv')
    
    MeanValenceValue = np.mean(df['Mean Valence'].values) 
    MaxValenceValue = np.max(df['Max Valence'].values) 
    MinValenceValue = np.min(df['Min Valence'].values) 
    MedianValenceValue = np.median(df['Median Valence'].values) 
    MeanArousalValue = np.mean(df['Mean Arousal'].values) 
    MaxArousalValue = np.max(df['Max Arousal'].values) 
    MinArousalValue = np.min(df['Min Arousal'].values) 
    MedianArousalValue = np.median(df['Median Arousal'].values) 

    MeanValenceProbed.append(MeanValenceValue)
    MinValenceProbed.append(MinValenceValue)
    MaxValenceProbed.append(MaxValenceValue)
    MedianValenceProbed.append(MedianValenceValue)
    MeanArousalProbed.append(MeanArousalValue)
    MinArousalProbed.append(MinArousalValue)
    MaxArousalProbed.append(MaxArousalValue)
    MedianArousalProbed.append(MedianArousalValue)
    
import csv

with open(f'GRAPHS/arousal.csv', mode='w') as file:
    file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow([f"Video", "Mean Arousal All", "Max Arousal All", "Min Arousal All", "Median Arousal All", "Mean Arousal Probed", "Max Arousal Probed", "Min Arousal Probed", "Median Arousal Probed"])
    for i in range(len(videos)):
        file_writer.writerow([f"{videos[i]}",MeanArousalAll[i]  ,MaxArousalAll[i]  ,MinArousalAll[i]  ,MedianArousalAll[i]  ,MeanArousalProbed[i]  ,MaxArousalProbed[i]  ,MinArousalProbed[i]  ,MedianArousalProbed[i]  ])

with open(f'GRAPHS/valence.csv', mode='w') as file:
    file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow([f"Video", "Mean Valence All", "Max Valence All", "Min Valence All", "Median Valence All", "Mean Valence Probed", "Max Valence Probed", "Min Valence Probed", "Median Valence Probed"])
    for i in range(len(videos)):
        file_writer.writerow([f"{videos[i]}", MeanValenceAll[i]  ,MaxValenceAll[i]  ,MinValenceAll[i]  ,MedianValenceAll[i]  ,MeanValenceProbed[i]  ,MaxValenceProbed[i]  ,MinValenceProbed[i]  ,MedianValenceProbed[i]  ])


