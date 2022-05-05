import numpy as np
import glob
import matplotlib.pyplot as plt
from natsort import natsorted,ns
import pandas as pd
from scipy.stats import kendalltau
import seaborn as sns

def get_inter_annotator_score(annotator_1_score,annotator_2_score):
	return kendalltau(annotator_1_score,annotator_2_score)[0]

def get_windowed_data(dataframe,window_size=1000,behavior_type='valence'):
	temp_time = -1
	windowed_data = []
	temp_data = []
	for i in range(len(dataframe['jstime'])):
		curr_time = dataframe['jstime'].iat[i]
		if(temp_time==-1):
			temp_time = curr_time 
			temp_data.append(dataframe[behavior_type].iat[i])
		elif((curr_time-temp_time)<=window_size):
			temp_data.append(dataframe[behavior_type].iat[i])
		elif((curr_time-temp_time)>window_size):
			temp_time = curr_time
			windowed_data.append(np.mean(temp_data))
			temp_data = []

	return windowed_data


def main(video_id):
	annotator_directory = "../data/non-interpolated/annotations/"
	annotation_filelist = natsorted(glob.glob(annotator_directory+"*.csv"))

	n = len(annotation_filelist)
	annotation_array = np.ones([n,n])
	subjects = []
	for i in range(len(annotation_filelist)):
		#print(annotation_filelist[i])
		subject_1 = annotation_filelist[i].split("/")[-1].split(".")[0]
		subjects.append(subject_1)
		annotations_1 = pd.read_csv(annotation_filelist[i])
		annotations_1 = annotations_1[annotations_1['video']==video_id]
		#print(annotations_1.shape)
		annotations_1 = get_windowed_data(annotations_1)
		print("Checking correlation for: "+subject_1)
		annotation_array[i][i] = 1
		for j in range(len(annotation_filelist)):
			if(i!=j):
				subject_2 = annotation_filelist[j].split("/")[-1].split(".")[0]
				annotations_2 = pd.read_csv(annotation_filelist[j])
				annotations_2 = annotations_2[annotations_2['video']==video_id]
				#print(annotations_2.shape)
				annotations_2 = get_windowed_data(annotations_2)
				print("with: "+subject_2)
				
				#print(len(annotations_1))
				#print(len(annotations_2))
				#assert ((len(annotations_1) == len(annotations_2)-1) or (len(annotations_1)-1 == len(annotations_2)) or (len(annotations_1) == len(annotations_2)))

				annotations_1 = annotations_1[:min(len(annotations_1),len(annotations_2))]
				annotations_2 = annotations_2[:min(len(annotations_1),len(annotations_2))]
				#print(get_inter_annotator_score(annotations_1,annotations_2)) 
				annotation_array[i,j] = get_inter_annotator_score(annotations_1,annotations_2)

	print(annotation_array)
	fig, ax = plt.subplots(figsize=(12,7))
	ax = sns.heatmap(annotation_array,linewidths=.6)
	ax.set_xticklabels(list(range(1,31)))
	ax.set_yticklabels(list(range(1,31)))
	plt.savefig('annotation_agreement_'+str(video_id)+'.png')

if __name__ == '__main__':
	video_list = [1,2,3,4,5,6,7,8,10,11,12]
	for video_id in video_list:
		main(video_id)