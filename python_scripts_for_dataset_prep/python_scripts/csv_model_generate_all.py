import os
from numpy.core.defchararray import index
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

#for video in range(1, 9):
for video in range(7, 9):
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


    allScores = []

    for i in range(len(vid2_windows_5000)):
        allScores.append(vid2_windows_5000[i]["Score"].values)

    print("Scores Extracted")
    #print(allScores[0])
    
    
    print("Finding timestamps corresponding to these points")

    timeToAllPerSubject = []
    for i in range(len(vid2_windows_5000)):
        timeToProbe = []
        #for j in range(1,2):
        for j in range(len(allScores[i])):
            df = vid2_windows_5000[i][vid2_windows_5000[i]['Score'] == allScores[i][j]]
            tim = df['Border'].values[0]
            timstart = df['Start'].values[0]
            timend = df['End'].values[0]
            timeToProbe.append([tim, timstart, timend])
        timeToAllPerSubject.append(timeToProbe)

    #print(timeToAllPerSubject[0])

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

    print("Annotations Extracted")

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

    print(subjects_physiological[0])

    print("Physiological Extracted")

    #print(subjects_annotation[0])

    print("Finding values corresponding to these timesteps")

    allValence = []
    allArousal = []
    allValenceDiff = []
    allArousalDiff = []
    allTime = []
    allPhysiologicalDiff = []

    for i in range(len(subjects_annotation)):
        timeToProbe = timeToAllPerSubject[i]

        jstime = subjects_annotation[i]['jstime'].values
        daqtime = subjects_physiological[i]['daqtime'].values

        val = []
        arou = []

        bvp_list = []
        gsr_list = []
        rsp_list = []
        skt_list = []
        emg_zygo_list = []
        emg_coru_list = []
        emg_trap_list = []

        allPhysioDiff = []

        timlist = []
        valDiff = []
        arouDiff = []
        for t in timeToProbe:

            # Find closest timestamp direct value
            nearest_time = find_nearest(jstime, t[0])

            df = subjects_annotation[i][subjects_annotation[i]['jstime'] == nearest_time]

            valence = df['valence'].values[0]
            arousal = df['arousal'].values[0]

            val.append(valence)
            arou.append(arousal)
            
            nearest_time = find_nearest(daqtime, t[0])

            df = subjects_physiological[i][subjects_physiological[i]['daqtime'] == nearest_time]

            gsr = df['gsr'].values[0]
            gsr_list.append(gsr)

            bvp = df['bvp'].values[0]
            bvp_list.append(bvp)

            rsp = df['rsp'].values[0]
            rsp_list.append(rsp)

            skt = df['skt'].values[0]
            skt_list.append(skt)

            emg_zygo = df['emg_zygo'].values[0]
            emg_zygo_list.append(emg_zygo)

            emg_coru = df['emg_coru'].values[0]
            emg_coru_list.append(emg_coru)

            emg_trap = df['emg_trap'].values[0]
            emg_trap_list.append(emg_trap)

            timlist.append(t[0])

            # Find closest timestamp difference value

            nearest_time_start = find_nearest(jstime, t[1])
            nearest_time_end = find_nearest(jstime, t[2])

            df_start = subjects_annotation[i][subjects_annotation[i]['jstime'] == nearest_time_start]
            df_end = subjects_annotation[i][subjects_annotation[i]['jstime'] == nearest_time_end]

            valence_start = df_start['valence'].values[0]
            valence_end = df_end['valence'].values[0]

            arousal_start = df_start['arousal'].values[0]
            arousal_end = df_end['arousal'].values[0]

            valence_diff = abs(valence_end - valence_start)
            arousal_diff = abs(arousal_end - arousal_start)

            valDiff.append(valence_diff)
            arouDiff.append(arousal_diff)

            nearest_time_start = find_nearest(daqtime, t[1])
            nearest_time_end = find_nearest(daqtime, t[2])

            df_start = subjects_physiological[i][subjects_physiological[i]['daqtime'] == nearest_time_start]
            df_end = subjects_physiological[i][subjects_physiological[i]['daqtime'] == nearest_time_end]

            gsr_start = df_start['gsr'].values[0]
            gsr_end = df_end['gsr'].values[0]

            bvp_start = df_start['bvp'].values[0]
            bvp_end = df_end['bvp'].values[0]

            rsp_start = df_start['rsp'].values[0]
            rsp_end = df_end['rsp'].values[0]

            skt_start = df_start['skt'].values[0]
            skt_end = df_end['skt'].values[0]

            emg_zygo_start = df_start['emg_zygo'].values[0]
            emg_zygo_end = df_end['emg_zygo'].values[0]

            emg_coru_start = df_start['emg_coru'].values[0]
            emg_coru_end = df_end['emg_coru'].values[0]

            emg_trap_start = df_start['emg_trap'].values[0]
            emg_trap_end = df_end['emg_trap'].values[0]

            gsr_diff = abs(gsr_end - gsr_start)
            bvp_diff = abs(bvp_end - bvp_start)
            rsp_diff = abs(rsp_end - rsp_start)
            skt_diff = abs(skt_end - skt_start)
            emg_zygo_diff = abs(emg_zygo_end - emg_zygo_start)
            emg_coru_diff = abs(emg_coru_end - emg_coru_start)
            emg_trap_diff = abs(emg_trap_end - emg_trap_start)

            allPhysioDiff.append([gsr_diff, bvp_diff, rsp_diff, skt_diff, emg_zygo_diff, emg_coru_diff, emg_trap_diff])






        #probedGsr.append(gsr_list)
        
        allValence.append(val)
        allArousal.append(arou)
        allTime.append(timlist)
        allValenceDiff.append(valDiff)
        allArousalDiff.append(arouDiff)
        allPhysiologicalDiff.append(allPhysioDiff)

    
    print("Values Found")
    print(allValenceDiff[0])

    print("Saving Data")

    for i in range(len(allValence)):
        with open(f'5000_added/scores_{video}/sub_{subjectsOrder[i]}_scores.csv', mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Start', 'Border', 'End', 'Valence', 'Arousal', 'Valence Diff', 'Arousal Diff', 'Score', 'GSR_Diff', 'BVP_Diff', 'RSP_Diff', 'SKT_Diff', 'EMG_ZYGO_Diff', 'EMG_CORU_Diff', 'EMG_TRAP_Diff'])
            for j in range(len(allValence[i])):
                writer.writerow([timeToAllPerSubject[i][j][1], timeToAllPerSubject[i][j][0], timeToAllPerSubject[i][j][2], allValence[i][j], allArousal[i][j], allValenceDiff[i][j], allArousalDiff[i][j], allScores[i][j], allPhysiologicalDiff[i][j][0], allPhysiologicalDiff[i][j][1], allPhysiologicalDiff[i][j][2], allPhysiologicalDiff[i][j][3], allPhysiologicalDiff[i][j][4], allPhysiologicalDiff[i][j][5], allPhysiologicalDiff[i][j][6]])
            