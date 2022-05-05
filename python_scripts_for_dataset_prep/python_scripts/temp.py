path = "cdf"
import os

videos = []

for i in range(1,9):
    videos.append(str(i))

for i in videos:
    os.mkdir(path + "/" + "video_" + i)

path = "cdf/video_"
import os

videos = []

for i in range(1,9):
    videos.append(str(i))

for i in videos:
    os.mkdir(path + i + "/" + "valence")
    os.mkdir(path + i + "/" + "arousal")