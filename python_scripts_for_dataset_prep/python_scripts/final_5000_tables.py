from datetime import time
import os
from numpy.core.defchararray import index
from numpy.core.fromnumeric import mean, ptp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy

videos = [1,2,3,4,5,6,7,8]

for video in videos:

    print("Creating Dataframe")

    directory = "5000/scores_" + str(video)

    files = os.listdir(directory)
    files = sorted(files)
    f = []

    for file in files:
        if file.endswith(".csv"):
            f.append(file)


    vid2_windows_5000 = []

    for i in range(len(f)):
        df = pd.read_csv(directory + '/' + f[i])
        if len(f[i]) == 16:
            name = f[i][:5]
            name = name[4:]
        if len(f[i]) == 17:
            name = f[i][:6]
            name = name[4:]
        df['subject'] = name
        vid2_windows_5000.append(df)


    subjectsOrder = []

    for i in range(len(vid2_windows_5000)):
        subjectsOrder.append(vid2_windows_5000[i]["subject"].unique()[0])

    print("Dataframe Created")
    print("Detecting Outliers")


    outliers = []

    def detect_outlier(data):
        data_mean, data_std = np.mean(data), np.std(data)
        data = list(data)
        datacpy = data.copy()
        cut_off = data_std * 3
        upper = data_mean + cut_off
        lower = data_mean - cut_off
        outliers = []
        valid_outliers = []
        for j in range(len(data)):
            if data[j] > upper:
                #outliers.append(data[j])
                #datacpy.remove(data[j])
                valid_outliers.append(data[j])
        for j in range(len(data)):
            if data[j] < lower:
                datacpy.remove(data[j])
                outliers.append(data[j])
        return outliers, datacpy, valid_outliers

    outliers_per_subject = []

    vid2_windows_5000_for_kmeans = []

    #for i in range(1):
    for i in range(len(vid2_windows_5000)):
        scores = vid2_windows_5000[i]['Score'].values
        outliers, scores, valid_outliers = detect_outlier(scores)
        outliers_per_subject.append(valid_outliers)

        idx_drop = []
        idx_drop_kmeans = []

        for j in range(len(vid2_windows_5000[i]['Score'].values)):
            for k in range(len(outliers)):
                if(round(vid2_windows_5000[i]['Score'].values[j], 4) == round(outliers[k], 4)):
                    val = vid2_windows_5000[i][round(vid2_windows_5000[i]['Score'],4) == round(outliers[k],4)]
                    idxl = val.index.tolist()
                    idx = idxl[0]
                    idx_drop.append(idx)
        for j in range(len(vid2_windows_5000[i]['Score'].values)):
            for k in range(len(valid_outliers)):
                if(round(vid2_windows_5000[i]['Score'].values[j], 4) == round(valid_outliers[k], 4)):
                    val = vid2_windows_5000[i][round(vid2_windows_5000[i]['Score'],4) == round(valid_outliers[k],4)]
                    idxl = val.index.tolist()
                    idx = idxl[0]
                    idx_drop_kmeans.append(idx)
        vid2_windows_5000[i] = vid2_windows_5000[i].drop(idx_drop)
        vid2_windows_5000_for_kmeans.append(vid2_windows_5000[i].drop(idx_drop_kmeans))



    print("Outliers Detected")

    # print(outliers_per_subject)
    # print(len(outliers_per_subject))

    print("K Means Clustering")

    from sklearn.cluster import KMeans

    centroids = []

    #for i in range(1):
    for i in range(len(vid2_windows_5000_for_kmeans)):
        X = vid2_windows_5000_for_kmeans[i]['Score'].values
        kmeans = KMeans(n_clusters=2).fit(X.reshape(-1,1))
        a,b = kmeans.cluster_centers_
        a = a[0]
        b = b[0]
        choosen_centroid = max(a,b)
        #print(choosen_centroid)
        centroids.append(choosen_centroid)

    # print(centroids)
    # print(len(centroids))

    print("K Means Clustering Done")
    print("Finding number of points above centroid")

    countPerSubject = []
    pointsToProbePerSubject = []

    for i in range(len(vid2_windows_5000)):
        count = 0
        pointsToProbe = []
        scores = vid2_windows_5000[i]['Score'].values
        for j in range(len(scores)):
            if(scores[j] > centroids[i]):
                count = count+1
                pointsToProbe.append(scores[j])

        countPerSubject.append(count)
        pointsToProbePerSubject.append(pointsToProbe)

    print(countPerSubject)

    print("Number of points above centroid calculated")
    print("Finding timestamps corresponding to these points")

    timeToProbePerSubject = []
    for i in range(len(vid2_windows_5000)):
        timeToProbe = []
        #for j in range(1,2):
        for j in range(len(pointsToProbePerSubject[i])):
            df = vid2_windows_5000[i][vid2_windows_5000[i]['Score'] == pointsToProbePerSubject[i][j]]
            left_time = df['Start'].values[0]
            right_time = df['End'].values[0]
            tim = [left_time, right_time]
            timeToProbe.append(tim)
        timeToProbePerSubject.append(timeToProbe)

    print(timeToProbePerSubject[0])

    print("Timestamps Found")



    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    directory = "../data/non-interpolated/annotations/Original/Original"

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

    subjects_annotation_ordered = []

    # This is done as subjects order doesn't match

    for i in range(len(subjectsOrder)):
        for j in range(len(subjects_annotation)):
            if(subjects_annotation[j]['subject'].values[0] == subjectsOrder[i]):
                subjects_annotation_ordered.append(subjects_annotation[j])

    subjects_annotation = subjects_annotation_ordered

    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    print("Finding Actual values of valence and arousal for ALL")

    meanValenceWindowPerSubject = []
    medianValenceWindowPerSubject = []
    minValenceWindowPerSubject = []
    maxValenceWindowPerSubject = []

    meanArousalWindowPerSubject = []
    medianArousalWindowPerSubject = []
    minArousalWindowPerSubject = []
    maxArousalWindowPerSubject = []

    #for i in range(1):
    for i in range(len(subjects_annotation)):
        meanValenceWindow = []
        medianValenceWindow = []
        minValenceWindow = []
        maxValenceWindow = []


        meanArousalWindow = []
        medianArousalWindow = []
        minArousalWindow = []
        maxArousalWindow = []
        jstime = subjects_annotation[i][subjects_annotation[i]['video'] == video]['jstime'].values

        for t in range(0, len(jstime), 100):
            start = int(jstime[t])
            end = int(start) + 4999
            nearest_start = find_nearest(jstime, start)
            nearest_end = find_nearest(jstime, end)

            df = subjects_annotation[i][subjects_annotation[i]['jstime'].between(nearest_start, nearest_end)]

            valence = df['valence'].values
            arousal = df['arousal'].values

            meanArousalWindow.append(np.mean(arousal))
            minArousalWindow.append(np.min(arousal))
            maxArousalWindow.append(np.max(arousal))
            medianArousalWindow.append(np.median(arousal))

            meanValenceWindow.append(np.mean(valence))
            minValenceWindow.append(np.min(valence))
            maxValenceWindow.append(np.max(valence))
            medianValenceWindow.append(np.median(valence))
        
        meanArousalWindowPerSubject.append(meanArousalWindow)
        minArousalWindowPerSubject.append(minArousalWindow)
        maxArousalWindowPerSubject.append(maxArousalWindow)
        medianArousalWindowPerSubject.append(medianArousalWindow)

        meanValenceWindowPerSubject.append(meanValenceWindow)
        minValenceWindowPerSubject.append(minValenceWindow)
        maxValenceWindowPerSubject.append(maxValenceWindow)
        medianValenceWindowPerSubject.append(medianValenceWindow)



    print("Dumping All Data to csv file")

    import csv

    for i in range(len(subjectsOrder)):
        with open(f'final_results_5000_all/video_{video}/sub_{subjectsOrder[i]}.csv', mode='w') as file:
            file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow([f"Window", "Mean Valence", "Max Valence", "Min Valence", "Median Valence", "Mean Arousal", "Max Arousal", "Min Arousal", "Median Arousal"])
            for j in range(len(meanValenceWindowPerSubject[i])):
                file_writer.writerow([f"{j + 1}", meanValenceWindowPerSubject[i][j], maxValenceWindowPerSubject[i][j],  minValenceWindowPerSubject[i][j], medianValenceWindowPerSubject[i][j], meanArousalWindowPerSubject[i][j], maxArousalWindowPerSubject[i][j],  minArousalWindowPerSubject[i][j], medianArousalWindowPerSubject[i][j]])

    print("Finding Actual values of valence and arousal for PROBED")

    meanValenceProbeWindowPerSubject = []
    medianValenceProbeWindowPerSubject = []
    minValenceProbeWindowPerSubject = []
    maxValenceProbeWindowPerSubject = []

    meanArousalProbeWindowPerSubject = []
    medianArousalProbeWindowPerSubject = []
    minArousalProbeWindowPerSubject = []
    maxArousalProbeWindowPerSubject = []

    #for i in range(2):
    for i in range(len(subjects_annotation)):
        meanValenceProbeWindow = []
        medianValenceProbeWindow = []
        minValenceProbeWindow = []
        maxValenceProbeWindow = []


        meanArousalProbeWindow = []
        medianArousalProbeWindow = []
        minArousalProbeWindow = []
        maxArousalProbeWindow = []

        timeToProbe = timeToProbePerSubject[i]

        jstime = subjects_annotation[i]['jstime'].values

        for t in timeToProbe:
            start, end = t
            nearest_start = find_nearest(jstime, start)
            nearest_end = find_nearest(jstime, end)

            df = subjects_annotation[i][subjects_annotation[i]['jstime'].between(nearest_start, nearest_end)]

            valence = df['valence'].values
            arousal = df['arousal'].values

            meanArousalProbeWindow.append(np.mean(arousal))
            minArousalProbeWindow.append(np.min(arousal))
            maxArousalProbeWindow.append(np.max(arousal))
            medianArousalProbeWindow.append(np.median(arousal))

            meanValenceProbeWindow.append(np.mean(valence))
            minValenceProbeWindow.append(np.min(valence))
            maxValenceProbeWindow.append(np.max(valence))
            medianValenceProbeWindow.append(np.median(valence))
            
        meanArousalProbeWindowPerSubject.append(meanArousalProbeWindow)
        minArousalProbeWindowPerSubject.append(minArousalProbeWindow)
        maxArousalProbeWindowPerSubject.append(maxArousalProbeWindow)
        medianArousalProbeWindowPerSubject.append(medianArousalProbeWindow)

        meanValenceProbeWindowPerSubject.append(meanValenceProbeWindow)
        minValenceProbeWindowPerSubject.append(minValenceProbeWindow)
        maxValenceProbeWindowPerSubject.append(maxValenceProbeWindow)
        medianValenceProbeWindowPerSubject.append(medianValenceProbeWindow)



    print("Dumping Probed Data")

    import csv

    for i in range(len(subjectsOrder)):
        with open(f'final_results_5000_probed/video_{video}/sub_{subjectsOrder[i]}.csv', mode='w') as file:
            file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow([f"Window", "Mean Valence", "Max Valence", "Min Valence", "Median Valence", "Mean Arousal", "Max Arousal", "Min Arousal", "Median Arousal"])
            for j in range(len(meanValenceProbeWindowPerSubject[i])):
                file_writer.writerow([f"{j + 1}", meanValenceProbeWindowPerSubject[i][j], maxValenceProbeWindowPerSubject[i][j],  minValenceProbeWindowPerSubject[i][j], medianValenceProbeWindowPerSubject[i][j], meanArousalProbeWindowPerSubject[i][j], maxArousalProbeWindowPerSubject[i][j],  minArousalProbeWindowPerSubject[i][j], medianArousalProbeWindowPerSubject[i][j]])

    print("Data Dumped")

    print("Results.csv ALL")

    directory = "final_results_5000_all/video_" + str(video)

    files = os.listdir(directory)
    files = sorted(files)
    f = []

    for file in files:
        if file.endswith(".csv"):
            f.append(file)


    final_csv_5000_all = []

    for i in range(len(f)):
        df = pd.read_csv(directory + '/' + f[i])
        if len(f[i]) == 9:
            name = f[i][:5]
            name = name[4:]
        if len(f[i]) == 10:
            name = f[i][:6]
            name = name[4:]
        df['subject'] = name
        final_csv_5000_all.append(df)

    subjectsOrderAll = []

    for i in range(len(final_csv_5000_all)):
        subjectsOrderAll.append(final_csv_5000_all[i]["subject"].unique()[0])


    print("Dataframe Created")
    print("Calculating for All Windows")

    meanValenceAveragePerSubject = [] 
    maxValenceAveragePerSubject = []
    minValenceAveragePerSubject = []
    medianValenceAveragePerSubject = []
    meanArousalAveragePerSubject = []
    maxArousalAveragePerSubject = []
    minArousalAveragePerSubject = []
    medianArousalAveragePerSubject = []

    for i in range(len(subjectsOrderAll)):
        meanValenceAveragePerSubject.append(np.mean(final_csv_5000_all[i]['Mean Valence'].values)) 
        maxValenceAveragePerSubject.append(np.max(final_csv_5000_all[i]['Max Valence'].values))
        minValenceAveragePerSubject.append(np.min(final_csv_5000_all[i]['Min Valence'].values))
        medianValenceAveragePerSubject.append(np.median(final_csv_5000_all[i]['Median Valence'].values))
        meanArousalAveragePerSubject.append(np.mean(final_csv_5000_all[i]['Mean Arousal'].values))
        maxArousalAveragePerSubject.append(np.max(final_csv_5000_all[i]['Max Arousal'].values))
        minArousalAveragePerSubject.append(np.min(final_csv_5000_all[i]['Min Arousal'].values))
        medianArousalAveragePerSubject.append(np.median(final_csv_5000_all[i]['Median Arousal'].values))


    print("Calculation complete")
    print("Dumping Data for all windows")

    import csv

    with open(f'final_results_5000_all/video_{video}/result.csv', mode='w') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(["Subject", "Mean Valence", "Max Valence", "Min Valence", "Median Valence", "Mean Arousal", "Max Arousal", "Min Arousal", "Median Arousal"])
        for i in range(len(subjectsOrderAll)):
                file_writer.writerow([subjectsOrderAll[i], meanValenceAveragePerSubject[i], maxValenceAveragePerSubject[i], minValenceAveragePerSubject[i], medianValenceAveragePerSubject[i], meanArousalAveragePerSubject[i], maxArousalAveragePerSubject[i], minArousalAveragePerSubject[i], medianArousalAveragePerSubject[i]])

    print("Data Dumped")
    print("Resulst.csv Probed")

    directory = "final_results_5000_probed/video_" + str(video)

    files = os.listdir(directory)
    files = sorted(files)
    f = []

    for file in files:
        if file.endswith(".csv"):
            f.append(file)


    final_csv_5000_probed = []

    for i in range(len(f)):
        df = pd.read_csv(directory + '/' + f[i])
        if len(f[i]) == 9:
            name = f[i][:5]
            name = name[4:]
        if len(f[i]) == 10:
            name = f[i][:6]
            name = name[4:]
        df['subject'] = name
        final_csv_5000_probed.append(df)

    subjectsOrderProbed = []

    for i in range(len(final_csv_5000_probed)):
        subjectsOrderProbed.append(final_csv_5000_probed[i]["subject"].unique()[0])

    # print(subjectsOrderProbed)
    # print(subjectsOrderAll)
    # print(final_csv_5000_probed[0].head())


    print("Calculating for Probed Windows")

    meanValenceAveragePerSubject = [] 
    maxValenceAveragePerSubject = []
    minValenceAveragePerSubject = []
    medianValenceAveragePerSubject = []
    meanArousalAveragePerSubject = []
    maxArousalAveragePerSubject = []
    minArousalAveragePerSubject = []
    medianArousalAveragePerSubject = []

    print(final_csv_5000_probed[0].head())

    for i in range(len(subjectsOrderProbed)):
        meanValenceAveragePerSubject.append(np.mean(final_csv_5000_probed[i]['Mean Valence'].values)) 
        maxValenceAveragePerSubject.append(np.max(final_csv_5000_probed[i]['Max Valence'].values))
        minValenceAveragePerSubject.append(np.min(final_csv_5000_probed[i]['Min Valence'].values))
        medianValenceAveragePerSubject.append(np.median(final_csv_5000_probed[i]['Median Valence'].values))
        meanArousalAveragePerSubject.append(np.mean(final_csv_5000_probed[i]['Mean Arousal'].values))
        maxArousalAveragePerSubject.append(np.max(final_csv_5000_probed[i]['Max Arousal'].values))
        minArousalAveragePerSubject.append(np.min(final_csv_5000_probed[i]['Min Arousal'].values))
        medianArousalAveragePerSubject.append(np.median(final_csv_5000_probed[i]['Median Arousal'].values))


    print("Calculation complete")

    print(subjectsOrderProbed)

    print("Dumping Data for probed windows")

    import csv

    with open(f'final_results_5000_probed/video_{video}/result.csv', mode='w') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(["Subject", "Mean Valence", "Max Valence", "Min Valence", "Median Valence", "Mean Arousal", "Max Arousal", "Min Arousal", "Median Arousal"])
        for i in range(len(subjectsOrderProbed)):
                file_writer.writerow([subjectsOrderProbed[i], meanValenceAveragePerSubject[i], maxValenceAveragePerSubject[i], minValenceAveragePerSubject[i], medianValenceAveragePerSubject[i], meanArousalAveragePerSubject[i], maxArousalAveragePerSubject[i], minArousalAveragePerSubject[i], medianArousalAveragePerSubject[i]])

    print("Data Dumped")