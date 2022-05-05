from datetime import time
import os
from numpy.core.defchararray import index
from numpy.core.fromnumeric import mean, ptp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy

print("Creating Dataframe")

videos = [1,2,3,4,5,6,7,8]

for video in videos:
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


    print("Finding Actual values of valence and arousal")

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

    valencePerProbePerSubject = []
    arousalPerProbePerSubject = []

    #for i in range(2):
    for i in range(len(subjects_annotation)):
        valencePerProbe = []
        arousalPerProbe = []
        timeToProbe = timeToProbePerSubject[i]

        jstime = subjects_annotation[i]['jstime'].values

        for t in timeToProbe:
            start, end = t
            nearest_start = find_nearest(jstime, start)
            nearest_end = find_nearest(jstime, end)

            df_start = subjects_annotation[i][subjects_annotation[i]['jstime'] == nearest_start]
            df_end = subjects_annotation[i][subjects_annotation[i]['jstime'] == nearest_end]

            valence_start = df_start['valence'].values[0]
            valence_end = df_end['valence'].values[0]

            valencePerProbe.append([valence_start, valence_end])

            arousal_start = df_start['arousal'].values[0]
            arousal_end = df_end['arousal'].values[0]

            arousalPerProbe.append([arousal_start, arousal_end])
        valencePerProbePerSubject.append(valencePerProbe)
        arousalPerProbePerSubject.append(arousalPerProbe)

    allValenceDifferencePerSubject = []
    allArousalDifferencePerSubject = []

    for i in range(len(vid2_windows_5000)):
        allValenceDifference = []
        allArousalDifference = []
        for j in range(len(pointsToProbePerSubject[i])):
            allValenceDifference.append(abs(valencePerProbePerSubject[i][j][1] - valencePerProbePerSubject[i][j][0]))
            allArousalDifference.append(abs(arousalPerProbePerSubject[i][j][1] - arousalPerProbePerSubject[i][j][0]))
        allValenceDifferencePerSubject.append(allValenceDifference)
        allArousalDifferencePerSubject.append(allArousalDifference)

    for i in range(len(vid2_windows_5000)):
        sumval = np.sum(allValenceDifferencePerSubject[i])
        for j in range(len(allValenceDifferencePerSubject[i])):
            allValenceDifferencePerSubject[i][j] = allValenceDifferencePerSubject[i][j] / sumval
        allValenceDifferencePerSubject[i] = sorted(allValenceDifferencePerSubject[i])
    
    for i in range(len(vid2_windows_5000)):
        sumval = np.sum(allArousalDifferencePerSubject[i])
        for j in range(len(allArousalDifferencePerSubject[i])):
            allArousalDifferencePerSubject[i][j] = allArousalDifferencePerSubject[i][j] / sumval
        allArousalDifferencePerSubject[i] = sorted(allArousalDifferencePerSubject[i])

    #for i in range(2):
    for i in range(len(vid2_windows_5000)):
        plt.plot(range(1, len(allValenceDifferencePerSubject[i]) +1), allValenceDifferencePerSubject[i], marker="o",label="PMF")
        cdf = np.cumsum(allValenceDifferencePerSubject[i])
        plt.plot(range(1, len(cdf)+1), cdf, marker="o",label="CDF")
        plt.xlabel("Values")
        plt.xticks(range(1, len(cdf)+1))
        plt.ylabel("Difference In Valence [normalized]")
        plt.title(f"Difference In Valence for Subject {subjectsOrder[i]}")
        plt.legend()
        plt.savefig(f"cdf/video_{video}/valence/sub_{subjectsOrder[i]}.png")
        plt.close()

        plt.plot(range(1, len(allArousalDifferencePerSubject[i]) +1), allArousalDifferencePerSubject[i], marker="o",label="PMF")
        cdf = np.cumsum(allArousalDifferencePerSubject[i])
        plt.plot(range(1, len(cdf)+1), cdf, marker="o",label="CDF")
        plt.xlabel("Values")
        plt.xticks(range(1, len(cdf)+1))
        plt.ylabel("Difference In Arousal [normalized]")
        plt.title(f"Difference In Arousal for Subject {subjectsOrder[i]}")
        plt.legend()
        plt.savefig(f"cdf/video_{video}/arousal/sub_{subjectsOrder[i]}.png")
        plt.close()



