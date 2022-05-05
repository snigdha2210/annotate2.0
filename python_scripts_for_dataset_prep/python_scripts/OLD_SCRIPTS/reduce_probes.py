import glob
from natsort import natsorted,ns
import pandas as pd

def reduce_probes(video_id=1,max_limit=10):
	parent_directory = "1000/scores_"+str(video_id)+"/"
	filelist = natsorted(glob.glob(parent_directory+".csv"))
	for files in filelist:
		print(files)
		in_file = pd.read_csv(files)
		i = 0
		j = 0
		while(i<len(in_file['Start'])):
			

def main():
	video_id = 1
	reduce_probes(video_id=1,max_limit=10)

if __name__ == '__main__':
	main()