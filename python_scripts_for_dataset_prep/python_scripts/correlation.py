import os
from numpy.core.defchararray import index
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

corr_valence = []
corr_arousal = []

subjectsOrder = []

for i in range(len(subjects_annotation)):
    subjectsOrder.append(subjects_annotation[i]["subject"].unique()[0])

for i in range(len(subjects_annotation)):
#for i in range(1):
    subject_annotation = subjects_annotation[i]
    subject_physiological = subjects_physiological[i]

    subject_valence = subject_annotation.drop(["jstime", "video", "subject", "arousal"], axis=1)
    subject_arousal = subject_annotation.drop(["jstime", "video", "subject", "valence"], axis=1)
    subject_physio = subject_physiological.drop(["daqtime", "video", "subject"], axis=1)

    corr_vals_valence = []
    for name, values in subject_physio.iteritems():
        corr_vals_valence.append([str(name) , subject_valence['valence'].corr(subject_physio[str(name)], method='pearson')])
    corr_valence.append(corr_vals_valence)

    corr_vals_arousal = []
    for name, values in subject_physio.iteritems():
        corr_vals_arousal.append([str(name) , subject_arousal['arousal'].corr(subject_physio[str(name)], method='pearson')])
    corr_arousal.append(corr_vals_arousal)

corr_valence = np.array(corr_valence)
corr_arousal = np.array(corr_arousal)

sum1 = [0,0,0,0,0,0,0,0]
for i in range(len(corr_valence)):
    for j in range(len(sum1)):
        sum1[j] += float(corr_valence[i][j][1])

avg1 = sum1.copy()
for i in range(len(avg1)):
    avg1[i] = avg1[i] / len(subjectsOrder)

sum2 = [0,0,0,0,0,0,0,0]
for i in range(len(corr_arousal)):
    for j in range(len(sum2)):
        sum2[j] += float(corr_arousal[i][j][1])

avg2 = sum2.copy()
for i in range(len(avg2)):
    avg2[i] = avg2[i] / len(subjectsOrder)


listOfNames1 = []
listOfNames2 = []

for i in range(1):
    for j in range(len(sum1)):
        listOfNames1.append(corr_valence[i][j][0])

listOfNames2 = listOfNames1.copy()
listOfNames = listOfNames1.copy()

sorted1, sortedNames1 = zip(*sorted(zip(avg1, listOfNames1), reverse=True))
sorted2, sortedNames2 = zip(*sorted(zip(avg2, listOfNames2), reverse=True))

corr_valence = []
corr_arousal = []

for i in range(len(subjects_annotation)):
#for i in range(1):
    subject_annotation = subjects_annotation[i]
    subject_physiological = subjects_physiological[i]

    subject_valence = subject_annotation.drop(["jstime", "video", "subject", "arousal"], axis=1)
    subject_arousal = subject_annotation.drop(["jstime", "video", "subject", "valence"], axis=1)
    subject_physio = subject_physiological.drop(["daqtime", "subject", "video"], axis=1)

    corr_vals_valence = []
    for name, values in subject_physio.iteritems():
        if name != "subject":
            corr_vals_valence.append(subject_valence['valence'].corr(subject_physio[str(name)], method='pearson'))
    corr_valence.append(corr_vals_valence)

    corr_vals_arousal = []
    for name, values in subject_physio.iteritems():
        if name != "subject":
            corr_vals_arousal.append(subject_arousal['arousal'].corr(subject_physio[str(name)], method='pearson'))
    corr_arousal.append(corr_vals_arousal)

# Save to .txt
with open('plots/correlation.txt', 'w') as f:
    f.write('______________________________________\n')
    f.write("_____________Correlation______________\n")
    f.write('______________________________________\n')
    f.write("\n")
    f.write("Average Valence\n \n")
    for i in range(5):
        f.write(f"{sortedNames1[i]}:  {sorted1[i]}")
        f.write("\n")
    f.write('______________________________________\n \n')
    f.write("Average Arousal\n \n")
    for i in range(5):
        f.write(f"{sortedNames2[i]}:  {sorted2[i]}")
        f.write("\n")
    f.write('______________________________________\n')

    for i in range(len(subjectsOrder)):
        listOfNamesCopy = listOfNames.copy()
        f.write(f"_____________Subject {subjectsOrder[i]}______________\n")
        f.write('______________________________________\n')
        sortedVals, sortedNames = zip(*sorted(zip(corr_arousal[i], listOfNamesCopy), reverse=True))
        f.write("Valence\n \n")
        for j in range(5):
            f.write(f"{sortedNames[j]}:  {sortedVals[j]}")
            f.write("\n")
        f.write('______________________________________\n')
        listOfNamesCopy = listOfNames.copy()
        sortedVals, sortedNames = zip(*sorted(zip(corr_valence[i], listOfNamesCopy), reverse=True))
        f.write("Arousal\n \n")
        for j in range(5):
            f.write(f"{sortedNames[j]}:  {sortedVals[j]}")
            f.write("\n")
        f.write('______________________________________\n')
        f.write('______________________________________\n')

# # save to .csv file

# sortedValsArousal = []
# sortedNamesArousal = []
# sortedValsValence = []
# sortedNamesValence = []

# for i in range(len(corr_arousal)):
#     listOfNamesCopy = listOfNames.copy()
#     sortedVals, sortedNames = zip(*sorted(zip(corr_arousal[i], listOfNamesCopy), reverse=True))
#     sortedNamesArousal.append(sortedNames)
#     sortedValsArousal.append(sortedVals)
#     listOfNamesCopy = listOfNames.copy()
#     sortedVals, sortedNames = zip(*sorted(zip(corr_valence[i], listOfNamesCopy), reverse=True))
#     sortedNamesValence.append(sortedNames)
#     sortedValsValence.append(sortedVals)

# Arousal = [sortedNamesArousal, sortedValsArousal]
# Valence = [sortedNamesValence, sortedValsValence]

# Arousal = np.array(Arousal)
# Valence = np.array(Valence)

# #print(Arousal[0-1]) list of ordered signal names or values
# #print(Arousal[0][0-29]) list of ordered signal names per subject
# #print(Arousal[1][0-29]) list of ordered signal values per subject
# #print(Arousal[0][0-29][0-7]) individual value of correlation

# dictionary_arousal = {
#     "Subject":[],
#     "1st most correlated name":[],
#     "1st most correlated val":[],
#     "2nd most correlated name":[],
#     "2nd most correlated val":[],
#     "3rd most correlated name":[],
#     "3rd most correlated val":[],
#     "4th most correlated name":[],
#     "4th most correlated val":[],
#     "5th most correlated name":[],
#     "5th most correlated val":[],
#     "6th most correlated name":[],
#     "6th most correlated val":[],
#     "7th most correlated name":[],
#     "7th most correlated val":[],
#     "8th most correlated name":[],
#     "8th most correlated val":[]
# }

# for i in range(len(Arousal[0])):
#     dictionary_arousal["Subject"].append(subjectsOrder[i])
#     dictionary_arousal["1st most correlated name"].append(Arousal[0][i][0])
#     dictionary_arousal["1st most correlated val"].append(Arousal[1][i][0])
#     dictionary_arousal["2nd most correlated name"].append(Arousal[0][i][1])
#     dictionary_arousal["2nd most correlated val"].append(Arousal[1][i][1])
#     dictionary_arousal["3rd most correlated name"].append(Arousal[0][i][2])
#     dictionary_arousal["3rd most correlated val"].append(Arousal[1][i][2])
#     dictionary_arousal["4th most correlated name"].append(Arousal[0][i][3])
#     dictionary_arousal["4th most correlated val"].append(Arousal[1][i][3])
#     dictionary_arousal["5th most correlated name"].append(Arousal[0][i][4])
#     dictionary_arousal["5th most correlated val"].append(Arousal[1][i][4])
#     dictionary_arousal["6th most correlated name"].append(Arousal[0][i][5])
#     dictionary_arousal["6th most correlated val"].append(Arousal[1][i][5])
#     dictionary_arousal["7th most correlated name"].append(Arousal[0][i][6])
#     dictionary_arousal["7th most correlated val"].append(Arousal[1][i][6])
#     dictionary_arousal["8th most correlated name"].append(Arousal[0][i][7])
#     dictionary_arousal["8th most correlated val"].append(Arousal[1][i][7])


# df = pd.DataFrame(dictionary_arousal)
# df.to_csv("corr_arousal.csv")



# dictionary_valence = {
#     "Subject":[],
#     "1st most correlated name":[],
#     "1st most correlated val":[],
#     "2nd most correlated name":[],
#     "2nd most correlated val":[],
#     "3rd most correlated name":[],
#     "3rd most correlated val":[],
#     "4th most correlated name":[],
#     "4th most correlated val":[],
#     "5th most correlated name":[],
#     "5th most correlated val":[],
#     "6th most correlated name":[],
#     "6th most correlated val":[],
#     "7th most correlated name":[],
#     "7th most correlated val":[],
#     "8th most correlated name":[],
#     "8th most correlated val":[]
# }

# for i in range(len(Valence[0])):
#     dictionary_valence["Subject"].append(subjectsOrder[i])
#     dictionary_valence["1st most correlated name"].append(Valence[0][i][0])
#     dictionary_valence["1st most correlated val"].append(Valence[1][i][0])
#     dictionary_valence["2nd most correlated name"].append(Valence[0][i][1])
#     dictionary_valence["2nd most correlated val"].append(Valence[1][i][1])
#     dictionary_valence["3rd most correlated name"].append(Valence[0][i][2])
#     dictionary_valence["3rd most correlated val"].append(Valence[1][i][2])
#     dictionary_valence["4th most correlated name"].append(Valence[0][i][3])
#     dictionary_valence["4th most correlated val"].append(Valence[1][i][3])
#     dictionary_valence["5th most correlated name"].append(Valence[0][i][4])
#     dictionary_valence["5th most correlated val"].append(Valence[1][i][4])
#     dictionary_valence["6th most correlated name"].append(Valence[0][i][5])
#     dictionary_valence["6th most correlated val"].append(Valence[1][i][5])
#     dictionary_valence["7th most correlated name"].append(Valence[0][i][6])
#     dictionary_valence["7th most correlated val"].append(Valence[1][i][6])
#     dictionary_valence["8th most correlated name"].append(Valence[0][i][7])
#     dictionary_valence["8th most correlated val"].append(Valence[1][i][7])


# df = pd.DataFrame(dictionary_valence)
# df.to_csv("corr_valence.csv")


# Save to plots
## Arousal

def normalize(x):
    x = np.array(x)
    x = x/sum(x)
    return x.tolist()

ArousalListOfSensors = []

for i in range(len(subjectsOrder)):
    listOfNamesCopy = listOfNames.copy()
    sortedVals, sortedNames = zip(*sorted(zip(corr_arousal[i], listOfNamesCopy), reverse=True))
    ArousalListOfSensors.append(sortedNames[0])

#for i in range(1):
for i in range(len(ArousalListOfSensors)):
    subject_annotation = subjects_annotation[i]
    subject_arousal = subject_annotation.drop(["subject", "video", "valence"], axis=1)
    subject_physiological = subjects_physiological[i]
    subject_physiological = subject_physiological.drop(["subject", "video"], axis=1)
    
    listOfPhysiologialIndex = subject_physiological["daqtime"].values
    listOfArousalIndex = subject_arousal["jstime"].values
    listOfDifference = np.setdiff1d(listOfArousalIndex, listOfPhysiologialIndex)

    for val in listOfDifference:
        subject_arousal = subject_arousal[subject_arousal["jstime"] != val]
        subject_physiological = subject_physiological[subject_physiological["daqtime"] != val]
    

    listOfPhysiologialIndex = subject_physiological["daqtime"].values
    listOfArousalIndex = subject_arousal["jstime"].values
    listOfDifference = np.setdiff1d(listOfPhysiologialIndex, listOfArousalIndex)
    
    for val in listOfDifference:
        subject_arousal = subject_arousal[subject_arousal["jstime"] != val]
        subject_physiological = subject_physiological[subject_physiological["daqtime"] != val]

    y1 = subject_arousal["arousal"].values
    y1 = normalize(y1)

    y2 = subject_physiological[ArousalListOfSensors[i]].values
    y2 = normalize(y2)

    x = subject_arousal["jstime"].values
    x = x/1000
    
    plt.xlabel = "time"
    plt.plot(x, y1, label="Arousal")
    plt.plot(x, y2, label=ArousalListOfSensors[i], linewidth=0.5)
    plt.legend()
    plt.savefig(f"plots/Arousal/Subject{subjectsOrder[i]}.png")
    plt.close()

# # Save to plots
# ## Valence
# def normalize(x):
#     x = np.array(x)
#     x = x/sum(x)
#     return x.tolist()

# ValenceListOfSensors = []

# for i in range(len(subjectsOrder)):
#     listOfNamesCopy = listOfNames.copy()
#     sortedVals, sortedNames = zip(*sorted(zip(corr_valence[i], listOfNamesCopy), reverse=True))
#     ValenceListOfSensors.append(sortedNames[0])

# #for i in range(1):
# for i in range(len(ValenceListOfSensors)):
#     subject_annotation = subjects_annotation[i]
#     subject_valence = subject_annotation.drop(["subject", "video", "arousal"], axis=1)
#     subject_physiological = subjects_physiological[i]
#     subject_physiological = subject_physiological.drop(["subject", "video"], axis=1)
    
#     listOfPhysiologialIndex = subject_physiological["daqtime"].values
#     listOfValenceIndex = subject_valence["jstime"].values
#     listOfDifference = np.setdiff1d(listOfValenceIndex, listOfPhysiologialIndex)

#     for val in listOfDifference:
#         subject_valence = subject_valence[subject_valence["jstime"] != val]
#         subject_physiological = subject_physiological[subject_physiological["daqtime"] != val]
    

#     listOfPhysiologialIndex = subject_physiological["daqtime"].values
#     listOfValenceIndex = subject_valence["jstime"].values
#     listOfDifference = np.setdiff1d(listOfPhysiologialIndex, listOfValenceIndex)
    
#     for val in listOfDifference:
#         subject_valence = subject_valence[subject_valence["jstime"] != val]
#         subject_physiological = subject_physiological[subject_physiological["daqtime"] != val]

#     y1 = subject_valence["valence"].values
#     y1 = normalize(y1)

#     y2 = subject_physiological[ValenceListOfSensors[i]].values
#     y2 = normalize(y2)

#     x = subject_valence["jstime"].values
#     x = x/1000
    
#     plt.xlabel = "time"
#     plt.plot(x, y1, label="Valence")
#     plt.plot(x, y2, label=ValenceListOfSensors[i], linewidth=0.5)
#     plt.legend()
#     plt.savefig(f"plots/Valence/Subject{subjectsOrder[i]}.png")
#     plt.close()