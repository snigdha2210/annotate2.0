import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
# for video in [1,2,3,4,5,6,7,8]:
for video in range(8,9):
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
            tim = df['Border'].values[0]
            timeToProbe.append(tim)
        timeToProbePerSubject.append(timeToProbe)

    print(timeToProbePerSubject[0])

    print("Timestamps Found")


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

    directory = "../data/non-interpolated/physiological/Original/Original"

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

    subjects_physiological_ordered = []

    # This is done as subjects order doesn't match

    for i in range(len(subjectsOrder)):
        for j in range(len(subjects_physiological)):
            if(subjects_physiological[j]['subject'].values[0] == subjectsOrder[i]):
                subjects_physiological_ordered.append(subjects_physiological[j])

    subjects_physiological = subjects_physiological_ordered

    print(subjects_physiological[0].head())

    probedGsr = []
    probedValence = []
    probedArousal = []
    probedTime = []

    allGsrLast = []
    allTimePhysioLast = []
    allTimeAnnoLast = []
    allValenceLast = []
    allArousalLast = []

    for i in range(len(subjects_annotation)):
        timeToProbe = timeToProbePerSubject[i]

        jstime = subjects_annotation[i]['jstime'].values
        daqtime = subjects_physiological[i]['daqtime'].values

        val = []
        arou = []
        gsr_list = []
        timlist = []
        for t in timeToProbe:
            nearest_time = find_nearest(jstime, t)

            df = subjects_annotation[i][subjects_annotation[i]['jstime'] == nearest_time]

            valence = df['valence'].values[0]
            arousal = df['arousal'].values[0]

            val.append(valence)
            arou.append(arousal)
            if t == timeToProbe[len(timeToProbe) - 1]:
                allValenceLast.append(valence)
                allArousalLast.append(arousal)
            nearest_time = find_nearest(daqtime, t)

            df = subjects_physiological[i][subjects_physiological[i]['daqtime'] == nearest_time]

            gsr = df['gsr'].values[0]
            gsr_list.append(gsr)
            timlist.append(t)
        probedGsr.append(gsr_list)
        probedValence.append(val)
        probedArousal.append(arou)
        probedTime.append(timlist)
    
    allGsr = []
    allTimePhysio = []
    allTimeAnno = []
    allValence = []
    allArousal = []

    for i in range(len(subjects_annotation)):
        Gsr = []
        val = []
        arou = []

        jstime = subjects_annotation[i]['jstime'].values
        daqtime = subjects_physiological[i]['daqtime'].values
        timess = subjects_annotation[i][subjects_annotation[i]['video'] == video]['jstime'].values

        allTimeAnno.append(timess)

        allTimeAnnoLast.append(timess[len(timess) - 1])


        start = timess[0]
        end =  timess[len(timess) - 1]
        nearest_start = find_nearest(jstime, start)
        nearest_end = find_nearest(jstime, end)

        df = subjects_annotation[i][subjects_annotation[i]['jstime'].between(nearest_start, nearest_end)]

        allValence.append(df['valence'].values)
        allArousal.append(df['arousal'].values)


        timess = subjects_physiological[i][subjects_physiological[i]['video'] == video]['daqtime'].values

        allTimePhysio.append(timess)

        start = timess[0]
        end =  timess[len(timess) - 1]
        nearest_start = find_nearest(daqtime, start)
        nearest_end = find_nearest(daqtime, end)


        allTimePhysioLast.append(nearest_end)

        df = subjects_physiological[i][subjects_physiological[i]['daqtime'].between(nearest_start, nearest_end)]

        gsr = df['gsr'].values

        allGsrLast.append(gsr[len(gsr) - 1])
        allGsr.append(gsr)

    probedGsrNew = probedGsr
    probedValenceNew = probedValence
    probedArousalNew = probedArousal
    probedTimeNew = probedTime

    for i in range(len(subjects_annotation)):
        probedGsrNew[i].append(allGsrLast[i])
        probedValenceNew[i].append(allValenceLast[i])
        probedArousalNew[i].append(allArousalLast[i])
        probedTimeNew[i].append(allTimeAnnoLast[i])

    for i in range(len(subjects_annotation)):
    #for i in range(1):
        # plt.plot(allTimePhysio[i], allGsr[i], label="gsr")
        plt.plot(allTimeAnno[i], allValence[i], label="valence")
        plt.plot(probedTimeNew[i], probedValenceNew[i], 'x', markevery=range(len(probedValence[i]) - 1), linestyle='--', label='probed valence')
        # plt.plot(probedTime[i], probedGsr[i], marker='x', linestyle='--', label='probed gsr')
        plt.legend()
        plt.savefig(f"graphs_probed/valence/video_{video}sub_{subjectsOrder[i]}.png")
        plt.close()
        # plt.show()
    for i in range(len(subjects_annotation)):
        plt.plot(allTimeAnno[i], allArousal[i], label="arousal")
        plt.plot(probedTimeNew[i], probedArousalNew[i], 'x', markevery=range(len(probedArousal[i]) - 1), linestyle='--', label='probed arousal')
        plt.legend()
        plt.savefig(f"graphs_probed/arousal/video_{video}sub_{subjectsOrder[i]}.png")
        plt.close()
        # plt.show()



