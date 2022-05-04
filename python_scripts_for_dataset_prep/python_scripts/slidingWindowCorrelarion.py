import os
from numpy.core.defchararray import index
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas.io.stata import ValueLabelTypeMismatch

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
    if len(f[i]) == 9:
        name = f[i][:5]
        name = name[4:]
    if len(f[i]) == 10:
        name = f[i][:6]
        name = name[4:]
    df['subject'] = name
    subjects_annotation.append(df)

directory = "../data/non-interpolated/physiological/Generated"

files = os.listdir(directory)
files = sorted(files)
f = []

for file in files:
    if file.endswith(".csv"):
        f.append(file)

subjects_physiological = []

for i in range(len(f)):
    df = pd.read_csv(directory + '/' + f[i])
    if len(f[i]) == 9:
        name = f[i][:5]
        name = name[4:]
    if len(f[i]) == 10:
        name = f[i][:6]
        name = name[4:]
    df['subject'] = name
    subjects_physiological.append(df)


remove_vids = [10,11,12]


for i in remove_vids:
    for j in range(len(subjects_annotation)):
        subset = subjects_annotation[j][(subjects_annotation[j]["video"] != i)]
        subjects_annotation[j] = subset

for i in remove_vids:
    for j in range(len(subjects_physiological)):
        subset = subjects_physiological[j][(subjects_physiological[j]["video"] != i)]
        subjects_physiological[j] = subset

subjectsOrder = []

for i in range(len(subjects_annotation)):
    subjectsOrder.append(subjects_annotation[i]["subject"].unique()[0])

for i in range(len(subjects_annotation)):
    listOfPhysiologialIndex = subjects_physiological[i]["daqtime"].values
    listOfArousalIndex = subjects_annotation[i]["jstime"].values
    listOfDifference = np.setdiff1d(listOfArousalIndex, listOfPhysiologialIndex)

    for val in listOfDifference:
        subjects_annotation[i] = subjects_annotation[i][subjects_annotation[i]["jstime"] != val]
        subjects_physiological[i] = subjects_physiological[i][subjects_physiological[i]["daqtime"] != val]
    

    listOfPhysiologialIndex = subjects_physiological[i]["daqtime"].values
    listOfArousalIndex = subjects_annotation[i]["jstime"].values
    listOfDifference = np.setdiff1d(listOfPhysiologialIndex, listOfArousalIndex)

    for val in listOfDifference:
        subjects_annotation[i] = subjects_annotation[i][subjects_annotation[i]["jstime"] != val]
        subjects_physiological[i] = subjects_physiological[i][subjects_physiological[i]["daqtime"] != val]


corr_valence = []
corr_arousal = []


for i in range(len(subjects_annotation)):
#for i in range(1):
    subject_annotation = subjects_annotation[i]
    subject_physiological = subjects_physiological[i]

    subject_valence = subject_annotation.drop(["jstime", "video", "subject", "arousal"], axis=1)
    subject_arousal = subject_annotation.drop(["jstime", "video", "subject", "valence"], axis=1)
    subject_physio = subject_physiological.drop(["daqtime", "video", "subject"], axis=1)

    n = 1000  #chunk row size
    list_subject_arousal = [subject_arousal[i:i+n] for i in range(0,subject_arousal.shape[0],n)]
    list_subject_valence = [subject_valence[i:i+n] for i in range(0,subject_valence.shape[0],n)]
    list_subject_physio = [subject_physio[i:i+n] for i in range(0,subject_physio.shape[0],n)]


    list_corr_vals_valence = []
    for i in range(len(list_subject_physio)):
        corr_vals_valence = []
        for name, values in list_subject_physio[i].iteritems():
            corr_vals_valence.append(list_subject_valence[i]["valence"].corr(list_subject_physio[i][str(name)]))
        list_corr_vals_valence.append(corr_vals_valence)
    corr_valence.append(list_corr_vals_valence)

    list_corr_vals_arousal = []
    for i in range(len(list_subject_physio)):
        corr_vals_arousal = []
        for name, values in list_subject_physio[i].iteritems():
            corr_vals_arousal.append(list_subject_arousal[i]['arousal'].corr(list_subject_physio[i][str(name)], method='pearson'))
        list_corr_vals_arousal.append(corr_vals_arousal)
    corr_arousal.append(list_corr_vals_arousal)

listOfNames = []

for name, values in subjects_physiological[0].drop(["daqtime", "video", "subject"], axis=1).iteritems():
    listOfNames.append(name)


with open('plots/sliding_correlation.txt', 'w') as f:
    f.write('______________________________________\n')
    f.write("_________Sliding_Correlation 5000__________\n")
    f.write('______________________________________\n')
    for j in range(len(subjectsOrder)):
        f.write('______________________________________\n')
        f.write(f"___________Subject {subjectsOrder[j]}________________\n")
        f.write('______________________________________\n')
        for i in range(len(corr_arousal[j])):
        #for i in range(1):
            listOfNamesCopy = listOfNames.copy()
            f.write(f"_____________Chunk {i}_________________\n")
            f.write('________________________________________\n')
            sortedVals, sortedNames = zip(*sorted(zip(corr_arousal[j][i], listOfNamesCopy), reverse=True))
            f.write("Valence\n \n")
            for k in range(5):
                f.write(f"{sortedNames[k]}:  {sortedVals[k]}")
                f.write("\n")
            f.write('______________________________________\n')
            listOfNamesCopy = listOfNames.copy()
            sortedVals, sortedNames = zip(*sorted(zip(corr_valence[j][i], listOfNamesCopy), reverse=True))
            f.write("Arousal\n \n")
            for k in range(5):
                f.write(f"{sortedNames[k]}:  {sortedVals[k]}")
                f.write("\n")
            f.write('______________________________________\n')
            f.write('______________________________________\n')