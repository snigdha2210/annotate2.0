import glob
import math
import matplotlib.pyplot as plt
from natsort import natsorted, ns
import pandas as pd

'''This method will return the minimum
period of time (in ms) where both the valence
and arousal of the user was same'''
def get_window_size(filename):
	original_data = pd.read_csv(filename)
	min_window_size = math.inf
	temp_valence = ""
	temp_arousal = ""
	start_time = ""
	for i in range(len(original_data['jstime'])):
		valence = original_data['valence'][i]
		arousal = original_data['arousal'][i]
		time = original_data['jstime'][i]
		if(temp_valence == "" and temp_arousal == "" and start_time == ""):
			temp_valence = valence
			temp_arousal = arousal
			start_time = time
		else:
			if(temp_valence != valence or temp_arousal != arousal):
				time_diff = time - start_time
				if(time_diff<min_window_size):
					min_window_size = time_diff
				start_time = time
				temp_valence = valence
				temp_arousal = arousal
	return min_window_size

def main():
	parent_directory = "../data/non-interpolated/annotations/"
	file_list = glob.glob(parent_directory+"*.csv")
	file_list = natsorted(file_list, key=lambda y: y.lower())
	#print(file_list)

	out_file = open("learned_window_size.txt","w+")
	window_size_list = []
	for filenames in file_list:
		print(filenames)
		window_size = get_window_size(filenames)
		print(window_size)
		window_size_list.append(window_size)
		out_file.write(filenames.split("/")[-1].split(".")[0]+","+str(window_size)+"\n")
	out_file.flush()
	out_file.close()
	
	print(window_size_list)
	#Plotting the graph	
	fig, ax = plt.subplots(figsize=(11,7))
	ax.bar(list(range(1,31)),window_size_list)
	plt.ylabel("Window Size (in ms)",fontsize=22, fontweight='bold')
	plt.xlabel("Subjects",fontsize=22, fontweight='bold')
	plt.yticks(fontsize=22, fontweight='bold')
	plt.xticks(fontsize=22, fontweight='bold')
	plt.grid()
	plt.savefig('window_size_both_change.png')

if __name__ == '__main__':
	main()