from datetime import time
import os
from numpy.core.defchararray import index
from numpy.core.fromnumeric import mean, ptp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pointsToProbePerSubjectPerVideo = []

for video in range(1, 9):
#for video in range(7, 9):
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
    pointsToProbePerSubjectPerVideo.append(countPerSubject)

avgProbes = []
stdProbes = []

avgProbesPerVideo = []
for i in range(len(pointsToProbePerSubjectPerVideo)): #per video - 8
    numberOfProbesPerSubject = []
    for j in range(len(pointsToProbePerSubjectPerVideo[i])): # per subject - 30
        numberOfProbesPerSubject.append(int(pointsToProbePerSubjectPerVideo[i][j]))
    avgProbe = np.mean(numberOfProbesPerSubject)
    stdProbe = np.std(numberOfProbesPerSubject)
    avgProbes.append(avgProbe)
    stdProbes.append(stdProbe)

import matplotlib.pyplot as plt
import matplotlib


matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)

videos = []
count = 0
for i in range(len(pointsToProbePerSubjectPerVideo)):
    count = count + 1
    videos.append(count)

print(videos)

# #plt.bar(videos, avgProbes)
# #plt.margins(x=0)
# plt.xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
# plt.yticks([1,2,3,4,5,6], ['1','2','3','4','5','6'])
# plt.xlabel('Video', fontsize=18)
# plt.ylabel('Average number of probes', fontsize=18)
# plt.grid(axis = 'y', color = "grey", linewidth = "1.4", linestyle = "--")
# plt.bar(videos, avgProbes, yerr=stdProbes, width=0.6, capsize=6)
# plt.show()

probesPerVideo = []
for i in range(len(pointsToProbePerSubjectPerVideo)): #per video - 8
    numberOfProbesPerVideo = []
    for j in range(len(pointsToProbePerSubjectPerVideo[i])): # per subject - 30
        numberOfProbesPerVideo.append(pointsToProbePerSubjectPerVideo[i][j])
    probesPerVideo.append(numberOfProbesPerVideo)

probesPerSubject = [0]*30 # Should have lenght 30
for i in range(len(probesPerVideo)): #8
    for j in range(len(probesPerVideo[i])): #30
        probesPerSubject[j] += probesPerVideo[i][j]



avgProbesPerSubject = []
for i in range(len(probesPerSubject)):
    avgProbesPerSubject.append(probesPerSubject[i] / len(probesPerVideo))

for i in range(len(subjectsOrder)):
    subjectsOrder[i] = int(subjectsOrder[i])

yx = zip(subjectsOrder, avgProbesPerSubject)
yx = sorted(yx)
avgProbesPerSubject = [x for y, x in yx]
subjectsOrder = [y for y, x in yx]

# import matplotlib.pyplot as plt
# plt.xticks(range(1, max(subjectsOrder), 3))
# # plt.xticks(subjectsOrder)
# plt.yticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14], ['1','2','3','4','5','6','7','8','9','10','11','12','13','14'])
# plt.xlabel('User', fontsize=18)
# plt.ylabel('Number of probes', fontsize=18)
# plt.grid(axis = 'y', color = "grey", linewidth = "1.4", linestyle = "--")
# #plt.bar(subjectsOrder, avgProbesPerSubject) 

# colours = ['red', 'peru', 'orange', 'green', 'black', 'gray', 'blue', 'purple']

pointsToProbePerVideoPerSubject =[]

for i in range(len(subjectsOrder)):
    temp = []
    for j in range(len(videos)):
        temp.append(0)
    pointsToProbePerVideoPerSubject.append(temp)

for i in range(len(pointsToProbePerSubjectPerVideo)): #8
    for j in range(len(pointsToProbePerSubjectPerVideo[i])): #30
        pointsToProbePerVideoPerSubject[j][i] = pointsToProbePerSubjectPerVideo[i][j]


# def rand_jitter(arr):
#     stdev = .01 * (max(arr) - min(arr))
#     return arr + np.random.randn(len(arr)) * stdev

# def jitter(x, y, s=20, c='b', marker='o', cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, verts=None, hold=None, **kwargs):
#     return plt.scatter(x, rand_jitter(y), s=s, c=c, marker=marker, cmap=cmap, norm=norm, vmin=vmin, vmax=vmax, alpha=alpha, linewidths=linewidths, **kwargs)

# print(len(subjectsOrder))
# print(len(pointsToProbePerVideoPerSubject[i]))

# for j in range(len(videos)):
#     jitter(subjectsOrder, pointsToProbePerSubjectPerVideo[j], c=colours[j], label=f"Video {j+1}")
#     #plt.scatter(subjectsOrder, pointsToProbePerSubjectPerVideo[j], c=colours[j], label=f"Video {j+1}")
# plt.legend()

# plt.show()






import matplotlib.pyplot as plt
matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)
#plt.xticks(range(1, 9))
# plt.xticks(range(1,len(subjectsOrder)+1, 3))

fig, ax = plt.subplots()

ax.set_yticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14], ['1','2','3','4','5','6','7','8','9','10','11','12','13','14'])
ax.set_xlabel('Video', fontsize=18)
ax.set_ylabel('Number of probes', fontsize=18)
ax.grid(axis = 'y', color = "grey", linewidth = "1", linestyle = "--")

labels = []
for i in range(len(subjectsOrder)):
    labels.append(subjectsOrder[i])


bplot = ax.boxplot(pointsToProbePerSubjectPerVideo, patch_artist=True)
#bplot = ax.boxplot(pointsToProbePerVideoPerSubject, patch_artist=True)
# every_nth = 3
# for n, label in enumerate(ax.xaxis.get_ticklabels()):
#     if n % every_nth != 0:
#         label.set_visible(False)

#colors = ['lightpink', 'lightsalmon', 'lightgoldenrodyellow', 'lavender', 'lightcoral', 'lightseagreen', 'lightcyan', 'lightgreen', 'lightgray', 'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow', 'wheat', 'beige', 'lightpink', 'lightsalmon', 'lightgoldenrodyellow', 'lavender', 'lightcoral', 'lightseagreen', 'lightcyan', 'lightgreen', 'lightgray', 'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow', 'wheat', 'beige']
colors = ['lavender', 'lightcoral', 'lightcyan', 'lightgreen', 'lightgray', 'lightskyblue', 'lightslategray', 'lightsteelblue']
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

plt.tight_layout()
plt.savefig(f"../../Fig1.png")
plt.close()
#plt.show()
