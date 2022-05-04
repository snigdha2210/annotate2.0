import glob
import matplotlib.pyplot as plt
import os
import pandas as pd
import sys

def remove_extension(filename):
	return (filename.split("/")[len(filename.split("/"))-1].split(".")[0])

def plot_emotion_annotations(parent_directory):
	list_input_files = glob.glob(parent_directory+"*.csv")
	for filenames in list_input_files:
		input_file = pd.read_csv(filenames)
		fig, ax = plt.subplots()
		plt.plot(input_file['jstime']/1000.0,input_file['valence'],'r-',label="Valence")
		plt.plot(input_file['jstime']/1000.0,input_file['arousal'],'g--',label="Arousal")
		plt.grid()
		ax.legend()
		ax.set_ylabel("Annotation Scores")
		ax.set_xlabel("Time (in secs)")
		plt.savefig(parent_directory+remove_extension(filenames)+".png")

def main():
	parent_directory = ""
	if(len(sys.argv)<=1):
		print("Provide arguments")
		print("--i\tTo plot the emotion annotations from the interpolated directory of the initially processed data")
		print("--u\tTo plot the emotion annotations from the interpolated directory of the initially processed data")
		sys.exit(1)
	elif(sys.argv[1]=="--i"):
		parent_directory = "../data/interpolated/annotations/"
	elif(sys.argv[1]=="--u"):
		parent_directory = "../data/non-interpolated/annotations/"
	else:
		print("Provide correct arguments")
		print("--i\tTo plot the emotion annotations from the interpolated directory of the initially processed data")
		print("--u\tTo plot the emotion annotations from the interpolated directory of the initially processed data")
		sys.exit(2)
	
	plot_emotion_annotations(parent_directory)

if __name__ == '__main__':
	main()

