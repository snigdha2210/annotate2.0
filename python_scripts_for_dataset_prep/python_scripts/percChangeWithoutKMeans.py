from datetime import time
import os
from numpy.core.defchararray import index
from numpy.core.fromnumeric import mean, ptp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import copy

print("Creating Dataframe")

#PARAMS
videos = [1,2,3,4,5,6,7,8]
thresholds = [0.5, 1, 1.5]

#initialize csv


with open(f'changePerc/changePercThresholdArousalWithoutKMeans.csv', 'w') as file:
    file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['Video', 'User', 'Threshold', 'Number of changes'])

with open(f'changePerc/changePercThresholdValenceWithoutKMeans.csv', 'w') as file:
    file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['Video', 'User', 'Threshold', 'Number of changes'])

with open(f'changePerc/changePercThresholdWithoutKMeans.csv', 'w') as file:
    file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['Video', 'User', 'Threshold', 'Number of changes'])

# videos = [2]
# thresholds = [0.5]
for video in videos:
    for threshold in thresholds:
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


        # outliers = []

        # def detect_outlier(data):
        #     data_mean, data_std = np.mean(data), np.std(data)
        #     data = list(data)
        #     datacpy = data.copy()
        #     cut_off = data_std * 3
        #     upper = data_mean + cut_off
        #     lower = data_mean - cut_off
        #     outliers = []
        #     valid_outliers = []
        #     for j in range(len(data)):
        #         if data[j] > upper:
        #             #outliers.append(data[j])
        #             #datacpy.remove(data[j])
        #             valid_outliers.append(data[j])
        #     for j in range(len(data)):
        #         if data[j] < lower:
        #             datacpy.remove(data[j])
        #             outliers.append(data[j])
        #     return outliers, datacpy, valid_outliers

        # outliers_per_subject = []

        # vid2_windows_5000_for_kmeans = []

        # #for i in range(1):
        # for i in range(len(vid2_windows_5000)):
        #     scores = vid2_windows_5000[i]['Score'].values
        #     outliers, scores, valid_outliers = detect_outlier(scores)
        #     outliers_per_subject.append(valid_outliers)

        #     idx_drop = []
        #     idx_drop_kmeans = []

        #     for j in range(len(vid2_windows_5000[i]['Score'].values)):
        #         for k in range(len(outliers)):
        #             if(round(vid2_windows_5000[i]['Score'].values[j], 4) == round(outliers[k], 4)):
        #                 val = vid2_windows_5000[i][round(vid2_windows_5000[i]['Score'],4) == round(outliers[k],4)]
        #                 idxl = val.index.tolist()
        #                 idx = idxl[0]
        #                 idx_drop.append(idx)
        #     for j in range(len(vid2_windows_5000[i]['Score'].values)):
        #         for k in range(len(valid_outliers)):
        #             if(round(vid2_windows_5000[i]['Score'].values[j], 4) == round(valid_outliers[k], 4)):
        #                 val = vid2_windows_5000[i][round(vid2_windows_5000[i]['Score'],4) == round(valid_outliers[k],4)]
        #                 idxl = val.index.tolist()
        #                 idx = idxl[0]
        #                 idx_drop_kmeans.append(idx)
        #     vid2_windows_5000[i] = vid2_windows_5000[i].drop(idx_drop)
        #     vid2_windows_5000_for_kmeans.append(vid2_windows_5000[i].drop(idx_drop_kmeans))



        # print("Outliers Detected")

        # # print(outliers_per_subject)
        # # print(len(outliers_per_subject))

        # print("K Means Clustering")

        # from sklearn.cluster import KMeans

        # centroids = []

        # #for i in range(1):
        # for i in range(len(vid2_windows_5000_for_kmeans)):
        #     X = vid2_windows_5000_for_kmeans[i]['Score'].values
        #     kmeans = KMeans(n_clusters=2).fit(X.reshape(-1,1))
        #     a = kmeans.cluster_centers_
        #     choosen_centroid = np.max(a)
        #     #print(choosen_centroid)
        #     centroids.append(choosen_centroid)

        # # print(centroids)
        # # print(len(centroids))

        # print("K Means Clustering Done")
        print("Finding number of points above centroid")

        countPerSubject = []
        pointsToProbePerSubject = []

        for i in range(len(vid2_windows_5000)):
            count = 0
            pointsToProbe = []
            scores = vid2_windows_5000[i]['Score'].values
            for j in range(len(scores)):
                if(scores[j] > 0):
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

        valenceDifferenceSubject = []
        arousalDifferenceSubject = []
        scoreDifferenceSubject = []

        for i in range(len(vid2_windows_5000)):
            valenceDifference = []
            arousalDifference = []
            scoreDifference = []
            for j in range(len(pointsToProbePerSubject[i])):
                valenceDifference.append(abs(valencePerProbePerSubject[i][j][1] - valencePerProbePerSubject[i][j][0]))
                arousalDifference.append(abs(arousalPerProbePerSubject[i][j][1] - arousalPerProbePerSubject[i][j][0]))
                scoreDifference.append(abs(pointsToProbePerSubject[i][j]))
            valenceDifferenceSubject.append(valenceDifference)
            arousalDifferenceSubject.append(arousalDifference)
            scoreDifferenceSubject.append(scoreDifference)

        numberArousalDifferencePerSubject = []
        numberValenceDifferencePerSubject = []
        numberScoreDifferencePerSubject = []
        total = 0
        for i in range(len(pointsToProbePerSubject)):
            numtemp1 = 0
            numtemp2 = 0
            numtemp3 = 0
            for j in range(len(pointsToProbePerSubject[i])):
                if(pointsToProbePerSubject[i][j] > threshold):
                    numtemp3 += 1
                if(valenceDifferenceSubject[i][j] > threshold):
                    numtemp2 += 1
                if(arousalDifferenceSubject[i][j] > threshold):
                    numtemp1 += 1
                total += 1
            numberArousalDifferencePerSubject.append(numtemp1)
            numberValenceDifferencePerSubject.append(numtemp2)
            numberScoreDifferencePerSubject.append(numtemp3)


        # print("Dumping Data to txt file")

        # with open(f'changePerc/changePercThreshold{threshold}.txt', 'a') as f:
        #     f.write('______________________________________\n')
        #     f.write(f"____________Video {video}______________\n")
        #     f.write('______________________________________\n')
        #     f.write(f'Change in Arousal Percentage = {(numberArousalDifference)*100/total}\n')
        #     f.write(f'Change in Valence Percentage = {(numberValenceDifference)*100/total}\n')
        #     f.write(f'Change in Either Percentage = {(eitherChange)*100/total}\n')

        print("Dumping Data to csv file")

        for i in range(len(vid2_windows_5000)):
            with open(f'changePerc/changePercThresholdArousalWithoutKMeans.csv', 'a') as file:
                file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                file_writer.writerow([video, subjectsOrder[i], threshold, numberArousalDifferencePerSubject[i]])

        for i in range(len(vid2_windows_5000)):
            with open(f'changePerc/changePercThresholdValenceWithoutKMeans.csv', 'a') as file:
                file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                file_writer.writerow([video, subjectsOrder[i], threshold, numberValenceDifferencePerSubject[i]])
        
        for i in range(len(vid2_windows_5000)):
            with open(f'changePerc/changePercThresholdWithoutKMeans.csv', 'a') as file:
                file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                file_writer.writerow([video, subjectsOrder[i], threshold, numberScoreDifferencePerSubject[i]])



        print("Data Dumped")