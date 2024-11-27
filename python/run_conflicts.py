from trajectory import Trajectory, ICAO_LIST_TEST_1, ICAO_LIST_TEST_2, ICAO_LIST_TEST_3, ICAO_LIST_TEST_4, ICAO_LIST_TEST_5, ICAO_LIST_TEST_6, ICAO_LIST_TEST_7
from plot_4d_dimensions import PlotData
#from conflict_detection_2 import Conflict_Detection
from conflict_detection import Conflict_Detection
from search_tree import Search_Tree
import numpy as np
from datetime import datetime
import os
import csv


__WRITE_FILE = False
__PLOT_DATA  = True
__LOG_DATA   = True


def __create_specific_conflict_file(date):

    fileName = 'dataset_' + str(date) + '.csv'

     #Initiate all the instances
    traj = Trajectory(date)
    #Read all the data
    data_time_serie = traj.treat_data(type = 'wr', only_path = False)
    search_tree = Search_Tree(tree=None, data=data_time_serie)
    con_detec = Conflict_Detection(data_time_serie)
    plot = PlotData(data_time_serie, data_time_serie)    
    icao_list = list(data_time_serie.keys())
    NumAeronaves = len(icao_list)


    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = ['NumAeronaves','Aircraft A', 'Aircraft A Ini Man Time', 'Aircraft A Ini Man Lat', 'Aircraft A Ini Man Lon', 
        'Aircraft A Ini Man Alt', 'Aircraft A Ini Man Vel_xy', 'Aircraft A Ini Man Vel_z', 'Aircraft A Ini Man Track',
        'Speed Maneuver', 'Altitude Maneuver', 'Track Maneuver',
        'Aircraft A End Man Time', 'Aircraft A End Man Lat', 'Aircraft A End Man Lon', 
        'Aircraft A End Man Alt', 'Aircraft A End Man Vel_xy', 'Aircraft A End Man Vel_z', 'Aircraft A End Man Track',
        'Aircraft A Conflict Time', 'Aircraft A Conflict Lat', 'Aircraft A Conflict Lon', 
        'Aircraft A Conflict Alt', 'Aircraft A Conflict Vel_xy', 'Aircraft A Conflict Vel_z', 'Aircraft A Conflict Track',
        'Aircraft B', 'Aircraft B Conflict Time', 'Aircraft B Conflict Lat', 'Aircraft B Conflict Lon', 
        'Aircraft B Conflict Alt', 'Aircraft B Conflict Vel_xy', 'Aircraft B Conflict Vel_z', 'Aircraft B Conflict Track']

        print("Create file")
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        args = dict()
        args['alt_frame_indices'] = None
        args['alt_change_lim'] = None
        args['alt_std_lim'] = None

        args['track_frame_indices'] = None
        args['track_change_lim'] = None
        args['track_std_lim'] = None
        
        args['speed_frame_indices'] = None
        args['speed_change_lim'] = None
        args['speed_std_lim'] = None

        conflicts = con_detec.search_conflicts(args)
        NumManSpeed = 0
        NumManAlt = 0
        NumManTrack = 0
        
        for icao in icao_list:
            if conflicts[icao]['conflict']:
                (second_filter, FirstPoint, SecondPoint, Maneuvers, A_conflict, B_conflict) = search_tree.search(conflicts, icao)

                for i in range(len(second_filter)):

                    TrackManeuver   = Maneuvers[i]["Maneuver_Act"] if Maneuvers[i]["Maneuver_Type"] == "track" else 0 
                    AltManeuver     = Maneuvers[i]["Maneuver_Act"] if Maneuvers[i]["Maneuver_Type"] == "alt" else 0 
                    SpeedManeuver   = Maneuvers[i]["Maneuver_Act"] if Maneuvers[i]["Maneuver_Type"] == "speed" else 0

                    A_Ini_Man_Time = FirstPoint[i]['time']
                    A_Ini_Man_Lat = FirstPoint[i]['lat']
                    A_Ini_Man_Lon = FirstPoint[i]['lon']
                    A_Ini_Man_Alt = FirstPoint[i]['alt']
                    A_Ini_Man_VelXY = FirstPoint[i]['vel_xy']
                    A_Ini_Man_VelZ = FirstPoint[i]['vel_z']
                    A_Ini_Man_Track = FirstPoint[i]['track']
                    
                    A_End_Man_Time = SecondPoint[i]['time']
                    A_End_Man_Lat = SecondPoint[i]['lat']
                    A_End_Man_Lon = SecondPoint[i]['lon']
                    A_End_Man_Alt = SecondPoint[i]['alt']
                    A_End_Man_VelXY = SecondPoint[i]['vel_xy']
                    A_End_Man_VelZ = SecondPoint[i]['vel_z']
                    A_End_Man_Track = SecondPoint[i]['track']

                    A_Conflict_Time = A_conflict[i]['time']
                    A_Conflict_Lat = A_conflict[i]['lat']
                    A_Conflict_Lon = A_conflict[i]['lon']
                    A_Conflict_Alt = A_conflict[i]['alt']
                    A_Conflict_VelXY = A_conflict[i]['vel_xy']
                    A_Conflict_VelZ = A_conflict[i]['vel_z']
                    A_Conflict_Track = A_conflict[i]['track']

                    B_Conflict_Time = B_conflict[i]['time']
                    B_Conflict_Lat = B_conflict[i]['lat']
                    B_Conflict_Lon = B_conflict[i]['lon']
                    B_Conflict_Alt = B_conflict[i]['alt']
                    B_Conflict_VelXY = B_conflict[i]['vel_xy']
                    B_Conflict_VelZ = B_conflict[i]['vel_z']
                    B_Conflict_Track = B_conflict[i]['track']

                    writer.writerow(
                        {
                            'NumAeronaves': str(NumAeronaves),
                            'Aircraft A': str(icao), 
                            'Aircraft A Ini Man Time': str(A_Ini_Man_Time), 
                            'Aircraft A Ini Man Lat': str(A_Ini_Man_Lat), 
                            'Aircraft A Ini Man Lon': str(A_Ini_Man_Lon), 
                            'Aircraft A Ini Man Alt': str(A_Ini_Man_Alt), 
                            'Aircraft A Ini Man Vel_xy': str(A_Ini_Man_VelXY), 
                            'Aircraft A Ini Man Vel_z': str(A_Ini_Man_VelZ), 
                            'Aircraft A Ini Man Track': str(A_Ini_Man_Track),
                            'Speed Maneuver': str(SpeedManeuver), 
                            'Altitude Maneuver': str(AltManeuver), 
                            'Track Maneuver': str(TrackManeuver),
                            'Aircraft A End Man Time': str(A_End_Man_Time), 
                            'Aircraft A End Man Lat': str(A_End_Man_Lat), 
                            'Aircraft A End Man Lon': str(A_End_Man_Lon), 
                            'Aircraft A End Man Alt': str(A_End_Man_Alt), 
                            'Aircraft A End Man Vel_xy': str(A_End_Man_VelXY), 
                            'Aircraft A End Man Vel_z': str(A_End_Man_VelZ), 
                            'Aircraft A End Man Track': str(A_End_Man_Track),
                            'Aircraft A Conflict Time': str(A_Conflict_Time), 
                            'Aircraft A Conflict Lat': str(A_Conflict_Lat), 
                            'Aircraft A Conflict Lon': str(A_Conflict_Lon), 
                            'Aircraft A Conflict Alt': str(A_Conflict_Alt), 
                            'Aircraft A Conflict Vel_xy': str(A_Conflict_VelXY), 
                            'Aircraft A Conflict Vel_z': str(B_Conflict_VelZ), 
                            'Aircraft A Conflict Track': str(A_Conflict_Track),
                            'Aircraft B': str(second_filter[i]), 
                            'Aircraft B Conflict Time': str(B_Conflict_Time), 
                            'Aircraft B Conflict Lat': str(B_Conflict_Lat), 
                            'Aircraft B Conflict Lon': str(B_Conflict_Lon), 
                            'Aircraft B Conflict Alt': str(B_Conflict_Alt), 
                            'Aircraft B Conflict Vel_xy': str(B_Conflict_VelXY), 
                            'Aircraft B Conflict Vel_z': str(B_Conflict_VelZ), 
                            'Aircraft B Conflict Track': str(B_Conflict_Track)
                        }
                    )
                    print("Write row")




def __create_conflicts_file():
    subfolders = [f.path for f in os.scandir("data") if f.is_dir()]
    
    # Create file 
    with open('dataset_3.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date', 'NumAeronaves', 'NumManSpeed', 'SpeedFrameLen', 'SpeedDeltaLim', 'SpeedStdLim',
        'NumManTrack', 'TrackFrameLen', 'TrackDeltaLim', 'TrackStdLim','NumManAlt', 'AltFrameLen', 'AltDeltaLim', 'AltStdLim']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        SpeedFrameLen = [1, 3, 5, 6, 7, 10, 15]
        SpeedDeltaLim = [10, 30, 60, 99, 100, 105]
        SpeedStdLim = [2, 5, 9, 10, 11, 15]

        TrackFrameLen = [1, 3, 4, 5, 6, 10, 15]
        TrackDeltaLim = [5, 14, 15, 16, 20, 30]
        TrackStdLim = [2, 5, 9, 10, 11, 15]

        AltFrameLen = [1, 5, 9, 10, 11, 17, 30]
        AltDeltaLim = [300, 590, 600, 610, 900, 1000]
        AltStdLim = [10, 20, 49, 50, 55, 100]

        for folder in subfolders:
            #Initiate all the instances
            Date = folder.replace('data\\', '')

            print("Begin data: " + Date)
            traj = Trajectory(Date)
            #Read all the data
            data_time_serie = traj.treat_data(type = 'r', only_path = False)
            search_tree = Search_Tree(tree=None, data=data_time_serie)
            con_detec = Conflict_Detection(data_time_serie)
            plot = PlotData(data_time_serie, data_time_serie)    
            icao_list = list(data_time_serie.keys())
            NumAeronaves = len(icao_list)

            for i in range(len(SpeedFrameLen)):

                for j in range(len(SpeedDeltaLim)):

                    for k in range(len(SpeedStdLim)):

                        args = dict()
                        args['alt_frame_indices'] = AltFrameLen[i]
                        args['alt_change_lim'] = AltDeltaLim[j]
                        args['alt_std_lim'] = AltStdLim[k]

                        args['track_frame_indices'] = TrackFrameLen[i]
                        args['track_change_lim'] = TrackDeltaLim[j]
                        args['track_std_lim'] = TrackStdLim[k]
                        
                        args['speed_frame_indices'] = SpeedFrameLen[i]
                        args['speed_change_lim'] = SpeedDeltaLim[j]
                        args['speed_std_lim'] = SpeedStdLim[k]
                        
                        conflicts = con_detec.search_conflicts(args)
                        NumManSpeed = 0
                        NumManAlt = 0
                        NumManTrack = 0
                        
                        for icao in icao_list:
                            if conflicts[icao]['conflict']:

                                (second_filter, FirstPoint, SecondPoint, Maneuvers, A, B) = search_tree.search(conflicts, icao)

                                for index in range(len(second_filter)):

                                    if Maneuvers[index]["Maneuver_Type"] == "track":
                                        NumManTrack = NumManTrack + 1
                                    elif Maneuvers[index]["Maneuver_Type"] == "alt":
                                        NumManAlt = NumManAlt + 1
                                    elif Maneuvers[index]["Maneuver_Type"] == "speed":
                                        NumManSpeed = NumManSpeed + 1


                        writer.writerow({'Date': Date, 
                                        'NumAeronaves': str(NumAeronaves),
                                        'NumManSpeed': str(NumManSpeed),
                                        'SpeedFrameLen': str(SpeedFrameLen[i]),
                                        'SpeedDeltaLim': str(SpeedDeltaLim[j]),
                                        'SpeedStdLim': str(SpeedStdLim[k]),
                                        'NumManTrack': str(NumManTrack),
                                        'TrackFrameLen': str(TrackFrameLen[i]),
                                        'TrackDeltaLim': str(TrackDeltaLim[j]),
                                        'TrackStdLim': str(TrackStdLim[k]),
                                        'NumManAlt': str(NumManAlt),
                                        'AltFrameLen': str(AltFrameLen[i]),
                                        'AltDeltaLim': str(AltDeltaLim[j]),
                                        'AltStdLim': str(AltStdLim[k])})
                                 
                        print("Write row")


def __test_run_conflict():

    print("Time serie")
    # Get trajectory
    datestr = "20230727"
    traj = Trajectory(datestr)
    data_time_serie = traj.treat_data(type = 'r', only_path = False)
    search_tree = Search_Tree(tree=None, data=data_time_serie)
    con_detec = Conflict_Detection(data_time_serie)
    plot = PlotData(data_time_serie, data_time_serie)


    icao_list = list(data_time_serie.keys())

    # icao_list = ['151e2f', '461f9e']

    # icao_list = ['06a1eb', '151e2f', '3453c3', '3c6542', '406668', '40688d', '4072ea',
    #              '461f9e', '485788', '4ac9e3', '8964a7', 'a1d76b', 'a5d623', 'a79e31',
    #              'a7b0c4']

    # icao_list = ['06a1eb', '06a2e9', '0d0a19', '151e2f', '151e6b', '3453c3', '392aed',
    #              '3c6542', '406668', '40688d', '4072ea', '407c0b', '461f9e', '485788',
    #              '4864ee', '4a2aac', '4ac9e3', '4b1807', '4bb275', '4bc841', '4cad49',
    #              '7380c3', '7cadac', '80073d', '888169', '89618a', '896411', '8964a7', 
    #              '8964ff', 'a1d76b', 'a1fb1a', 'a5d623', 'a79e31', 'a7b0c4', 'a8021d',
    #              'c060bc']

    # icao_list = ['06a074', '0d085c', '0d0a08', '151dad', '151e12', '151e2f', '345611',
    #              '3c670b', '3c7421', '3c78e2', '4007f9', '400afb', '405638', '406250',
    #              '406668', '406a92', '4070ed', '40769f', '407b54', '407cb2', '407e5f',
    #              '43c39d', '440053', '4400ec', '440667', '4841a5', '48c22f', '495212',
    #              '495216', '4a1921', '4ac9f5', '4ba9e4', '4bb28a', '4bb4e3', '4bc841']

    # Make analysis 
    # icao_list = ['020140', '02a1b3']
    # icao_list = ['010161','0101be','010206','01022f','0180a4','02007d','020095','0200ae',
    #             '020124','020140','020176','02a1a4','02a1b1','02a1b3']
    # icao_list =['010161', '0a0084', '0a009c', '020140', '151e12', '151e2f']
    response = con_detec.analysis_filters(icao_list)

    if __WRITE_FILE is True:
        f = open("conflicts_38.txt", "w")
        # f.write("Speed Lim:100\tSpeed frames:6\tAlt Lim:600\tAlt frames:10\tTrajectory Prediction considering also the vertical rate\n")
        f.write("Speed Lim:90\tSpeed frames:6\tAlt Lim:600\tAlt frames:10\t Track lim: 5 \t track frames: 5\tTrajectory Prediction considering only the ground speed "+ 
        "const and vertical rate equal to zero\n")
        
        f.write("Aeronaves filtradas pela alta velocidade: "+str(float(response['high_spd_filter']/len(icao_list)))+", "+str(response['high_spd_filter'])+"\n") 
        f.write("Aeronaves filtradas pela desvio: "+str(float(response['std_spd_filter']/len(icao_list)))+", "+str(response['std_spd_filter'])+"\n") 
        f.write("Total de aeronaves: "+str(len(icao_list))+"\n") 

    if __LOG_DATA is True:
        print("Speed Lim:100\tSpeed frames:6\tAlt Lim:600\tAlt frames:10\tTrajectory Prediction considering also the vertical rate\n")
        print("Aeronaves filtradas pela alta velocidade: ", float(response['high_spd_filter']/len(icao_list)), response['high_spd_filter'])    
        print("Aeronaves filtradas pela desvio: ", float(response['std_spd_filter']/len(icao_list)), response['std_spd_filter'])    
        print("Total de aeronaves: ", len(icao_list))  

    count_conflicts = 0
    maneuver_speed = 0
    maneuver_alt = 0
    maneuver_track = 0

    initial_time = datetime.now()

    if __WRITE_FILE is True:
        f.write("Initial Time: "+initial_time.strftime("%Y/%m/%d %H:%M:%S")+"\n")

    if __LOG_DATA is True:
        print(initial_time)

    for icao in icao_list:

        # Search for conflicts
        conflicts = con_detec.search_conflicts(icao)

        if conflicts[icao]['conflict']:
            # plot.plot_icao_traj(data_time_serie, icao, conflicts, None)
            # plot.plot_icao_traj_without_alt(data_time_serie, icao, conflicts, None)

            # Search for the second airplane in conflict
            (first_filter, second_filter, track_pred) = search_tree.search(conflicts, icao)

            if len(first_filter) > 0:

                if len(second_filter) > 0:

                    if __WRITE_FILE is True:
                        f.write(icao+":\n")
                        f.write(str(conflicts)+"\n")
                        f.write("First filter:"+str(first_filter)+"\n")
                        f.write("Second filter:"+str(second_filter)+"\n")

                    if __LOG_DATA is True:
                        print(icao)
                        print("There is a conflict")
                        print(conflicts)

                    if __PLOT_DATA is True:
                        plot.plot_data_4_axes(data_time_serie, icao, second_filter, conflicts)
                        plot.plot_icao_traj(data_time_serie, icao, conflicts, track_pred)
                        plot.plot_icao_traj_without_alt(data_time_serie, icao, conflicts, track_pred)
                        plot.plot_comp_all_speed(data_time_serie, icao, conflicts)

                    if len(conflicts[icao]['man_speed']) > 0:
                        maneuver_speed = maneuver_speed + 1
                    if len(conflicts[icao]['man_alt']) > 0:
                        maneuver_alt = maneuver_alt + 1
                    if len(conflicts[icao]['man_track']) > 0:
                        maneuver_track = maneuver_track + 1
                    count_conflicts = count_conflicts + 1


    final_time = datetime.now()
    diference_time = final_time - initial_time


    if __WRITE_FILE is True:
        f.write("Final Time: "+final_time.strftime("%Y/%m/%d %H:%M:%S")+"\n")
        f.write("Test Duration: "+str(diference_time)+"\n")

        f.write("Conflitos resolvidos por velocidade e altitude: "+str(float(count_conflicts/len(icao_list))*100)+"%\n") 
        f.write("Conflitos resolvidos por velocidade: "+str(float(maneuver_speed/len(icao_list))*100)+"%, "+str(maneuver_speed)+"\n")  
        f.write("Conflitos resolvidos por altitude: "+str(float(maneuver_alt/len(icao_list))*100)+"%, "+str(maneuver_alt)+"\n")  
        f.write("Conflitos resolvidos por rumo: "+str(float(maneuver_track/len(icao_list))*100)+"%, "+str(maneuver_track)+"\n")  

        f.close()

    if __LOG_DATA is True:
        print(final_time)
        print(diference_time)

        print("Conflitos resolvidos por velocidade e altitude: ", float(count_conflicts/len(icao_list))*100,"%" ) 
        print("Conflitos resolvidos por velocidade: ", float(maneuver_speed/len(icao_list))*100,"%, " ,maneuver_speed)  
        print("Conflitos resolvidos por altitude: ", float(maneuver_alt/len(icao_list))*100,"%, " , maneuver_alt)    
        print("Conflitos resolvidos por rumo: ", float(maneuver_track/len(icao_list))*100,"%, " , maneuver_track)  


# def get_database_sensibility(self, data):

# dataList = ["20230511", "20230520", "20230522", "20230526", "20230527", "20230528", "20230529", 
#             "20230530", "20230724", "20240528", "20240529"]
dataList = ["20230821","20240528", "20240529"]

for data in dataList:
    initial_time = datetime.now()
    print(initial_time)

    # __create_conflicts_file()
    print(data)
    __create_specific_conflict_file(data)

    final_time = datetime.now()
    diference_time = final_time - initial_time
    print(final_time)
    print(diference_time)

