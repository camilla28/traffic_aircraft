from opensky_api import OpenSkyApi
import jsons
import json
import time
import datetime
import os
import threading, time
import math
import numpy as np
import pandas as pd
from datetime import datetime
from statistics import mean, stdev
from scipy.signal import butter,filtfilt
from plot_4d_dimensions import PlotData
from geopy import distance
from weather import calc_speeds

'''
ICAO_LIST_TEST_1 = ['02a1b3','3c496e','4074b2', '4075fe', '4076cc', '40799c', '461e17', 'c0637c',
                    '4692ce', '4951d6', '4b1939', '4bd183', '4cada7', '4cadf2', '4d21f2', '4d221f',
                    '4d2248', '4d22b2', '4d23fd', '503cc0', '80139d', '801431', 'a014c9', 'a1e5f8',
                    'a2401b', 'a264a4', 'a2919a', 'a3b4d6', 'a3b529', 'a41bb5', 'a4491c', 'a48dea',
                    'a4dd35', 'a4e876', 'a50119', 'a55785', 'a5ea5c', 'a6b1a3', 'a74a5a', 'a8ab3c',
                    'a8b760', 'a8c44b', 'aa76a8', 'aa777e', 'aa7fa1', 'aaaa64', 'ab3639', 'ab5f43',
                    'ab73ca', 'ab84c9', 'ac15d1', 'ac3338', 'ac4dfb', 'acef2d', 'adbb39', 'c01dcb']

'''

#ICAO_LIST_TEST_1 = ['4951d6', '4b1939', '4d23fd']
ICAO_LIST_TEST_1 = ['02a1b3', '461f64', '4b1939', '4cadbf', 'a6fea5']
ICAO_LIST_TEST_2 = ['020140', '02a1b3']
ICAO_LIST_TEST_3 = ['02a1b3']
ICAO_LIST_TEST_4 = ['020140', '02a1b3', '010244','0180a4','02006e','020073', '020095', '020104', '020112','020124','02a260','06a09a']
ICAO_LIST_TEST_5 = ['020095']
ICAO_LIST_TEST_6 = ['02a1b3', '3c6542', 'a11fc7', 'a6b3b8']
#ICAO_LIST_TEST_6 = ['a6b3b8']
ICAO_LIST_TEST_7 = ['020124']


class Trajectory:
    
    def __init__(self, datestr = None , username="Camillas97", password="PEE3028"):
        # OpenSkyApi credentials
        self.username = username
        self.password = password
        self.api = OpenSkyApi(username=username, password=password)
        if datestr is None:
            self.datestr = time.strftime("%Y%m%d")
        else:
            self.datestr = datestr


    '''
        Get States
    '''
    def __get_states(self):
         # bbox = (min latitude, max latitude, min longitude, max longitude)
        states = self.api.get_states()
        #states = self.api.get_states(bbox=(45.8389, 47.8229, 5.9962, 10.5226))
        #states = api.get_states(bbox=(-20, 60, 20, 100))
        print(states)
        for s in states.states:
            #print(states)

            icao24 = s.icao24
            # checking if the directory demo_folder 
            # exist or not.
            
            # Write in file
            datestr = time.strftime("%Y%m%d")


            if not os.path.exists("data\\"+datestr):
                
                # if the demo_folder directory is not present 
                # then create it.
                os.makedirs("data\\"+datestr)
                print("Create folder")

            #icao24 = "4b1815"
            track = jsons.dump(self.api.get_track_by_aircraft(icao24))

            if track != None:

                flights = jsons.dump(self.api.get_flights_by_aircraft(icao24,int(track['startTime'])- 86400, int(track['endTime'])+86400))
                
                if flights != None:
                    track['startTime'] = datetime.fromtimestamp(track['startTime']).strftime("%Y/%m/%d-%H:%M:%S")
                    track['endTime'] = datetime.fromtimestamp(track['endTime']).strftime("%Y/%m/%d-%H:%M:%S")

                    state = jsons.dump(s)
                    merged_dict = track
                    for key,value in state.items():
                        merged_dict[key] = value
                
                    for key,value in flights[0].items():
                            merged_dict[key] = value

                    if not os.path.exists("data\\"+datestr+"\\"+icao24):
                
                        # if the demo_folder directory is not present 
                        # then create it.
                        os.makedirs("data\\"+datestr+"\\"+icao24)
                        
                    # Write in file
                    timestr = time.strftime("%Y%m%d-%H%M%S")
                    with open("data\\"+datestr+"\\"+icao24+"\\OpenSkyTrack_"+icao24+"_"+timestr+".json", "w") as write_file:
                        json.dump(merged_dict, write_file, indent=4)
                    print("Create file")
                else:
                    print(icao24, "Sem dados de voo")
            else:
                print(icao24, "Sem trajetória")
    
     
    '''
        Read files from path and merge in a file
    '''
    def __get_state_from_files(self, only_path = False):
        # Write in file

        data_path = "data\\"+self.datestr

        dir_list = os.listdir(data_path)

        data = dict()

        for dir in dir_list:

            try:
                # Path of icao 
                path = data_path + "\\" + dir
                
                # If is directory
                if os.path.isdir(path):

                    files = os.listdir(path)
                    
                    if files != []:

                        data[dir] = list()

                        files = [f for f in files if os.path.isfile(path+'\\'+f)] #Filtering only the files.
                        
                        #If doesn't use only waypoints in track, read differents files to use information
                        if not only_path:
                            for file in files:
                                #print(path+'\\'+file)
                                with open(path+'\\'+file, "r") as read_file:
                                    
                                    data_dict = json.load(read_file)
                                    
                                    if data_dict["baro_altitude"] is None or data_dict["latitude"] is None  or data_dict["longitude"] is None:
                                        continue
                                    else:
                                        waypoint = [
                                                    data_dict["time_position"],
                                                    data_dict["latitude"],
                                                    data_dict["longitude"],
                                                    data_dict["baro_altitude"],
                                                    data_dict["true_track"],
                                                    data_dict["on_ground"],
                                                    data_dict["velocity"],
                                                    data_dict["vertical_rate"]
                                                    ]

                                        data[dir].append(waypoint)
                            
                        with open(path+'\\'+files[0], "r") as read_file:

                            data_dict = json.load(read_file)
                            
                            path_non_duplicate = []
                            [path_non_duplicate.append(item) for item in data_dict["path"] if item not in path_non_duplicate]

                            for waypoint in path_non_duplicate:
                                data[dir].append(waypoint)       
            except Exception as inst:
                print(dir)
                print(type(inst))    # the exception type
                print(inst.args)     # arguments stored in .args
                print(inst)          # __str__ allows args to be printed directly,
                print(dir)

        with open(data_path + "\\" + self.datestr + ".json", "w") as outfile:
            json.dump(data, outfile)


    '''
        Return time
    '''
    def __takeTime(self, elem):
        return elem[0]
    

    def __distance_on_geoid(self, lat1, lon1, lat2, lon2) :
    
        # Convert degrees to radians
        lat1 = lat1 * math.pi / 180.0
        lon1 = lon1 * math.pi / 180.0
        lat2 = lat2 * math.pi / 180.0
        lon2 = lon2 * math.pi / 180.0
        
        # radius of earth in metres
        r = 6378100
        
        # P
        rho1 = r * math.cos(lat1)
        z1 = r * math.sin(lat1)
        x1 = rho1 * math.cos(lon1)
        y1 = rho1 * math.sin(lon1)
        
        # Q
        rho2 = r * math.cos(lat2)
        z2 = r * math.sin(lat2)
        x2 = rho2 * math.cos(lon2)
        y2 = rho2 * math.sin(lon2)
        
        # Dot product
        dot = (x1 * x2 + y1 * y2 + z1 * z2)
        cos_theta = dot / (r * r)
        if cos_theta > 1:
            cos_theta = 1
        theta = math.acos(cos_theta)
        
        # Distance in Metres
        return r * theta

    def __remove_track_none(self, data_dict):
        index = 0
        remove_list = list()
        for item in data_dict:
            if item[4] == None:
                remove_list.append(index)
            index = index + 1
        
        remove_list.reverse()
        for i in remove_list:
            data_dict.remove(data_dict[i])

        return data_dict

    def __calc_speeds(self, waypoint, last_waypoint):

        time_diff = waypoint[0] - last_waypoint[0]

        last = (last_waypoint[1], last_waypoint[2])
        actual = (waypoint[1], waypoint[2])
        d_distante = distance.distance(last, actual).meters
        speed = d_distante / time_diff #[m/s]
        waypoint.append(speed)

        # Calculate vertical rate
        alt_diff = waypoint[3] - last_waypoint[3]
        vertical_rate = alt_diff / time_diff
        waypoint.append(vertical_rate)

        return waypoint

    '''
        Update speed using waypoints of trajectory
    '''
    def __update_speed(self):
        # Write in file

        data_path = "data\\"+self.datestr

        testFileName = data_path + "\\" + self.datestr + ".json"

        data_dict_sorted = dict()

        with open(testFileName,  "r") as read_file:
                        
            data_dict = json.load(read_file)
            icao_list = list(data_dict.keys())
            #icao = "3e7281"
            
            # icao_list = ['392aed', '151e2f', '406668', '4072ea', '471f74', '4ac9e3',
            # '4bab52', '4bb275', '4cad49', 'a3a9ff', 'a79e31', 'abd8e4']
            #icao_list = ['4072ea']
            #icao_list = ['0180a8']
            #icao_list = ['06a12f','5001db']
            #icao_list = ['5001db']
            for icao in icao_list:

                if icao == '020112':
                    print(icao)

                data_dict_sorted[icao] = sorted(data_dict[icao], key=self.__takeTime)
                data_dict_sorted[icao] = self.__remove_track_none(data_dict_sorted[icao])
                remove_list = list()

                last_waypoint = data_dict_sorted[icao][0]

                index = 1
                #print(icao)

                # if index == len(data_dict_sorted[icao]):
                #     if len(last_waypoint) < 7:
                #         last_waypoint.append(0) # Coloca zero na velocidade no primeiro index
                #         last_waypoint.append(0) # Coloca zero no vertical_rate no primeiro index
                # else:

                # for waypoint in data_dict_sorted[icao]:
                while index < len(data_dict_sorted[icao]):

                    waypoint = data_dict_sorted[icao][index]
        
                    if index != 0: 
                        # Return time difference (seconds)
                        time_diff = waypoint[0] - last_waypoint[0]

                        if time_diff !=0: 

                            if len(waypoint) < 7:
                                waypoint = self.__calc_speeds(waypoint, last_waypoint)
                            #waypoint = calc_speeds(waypoint)
                            
                            if index == 1:
                                if len(last_waypoint) < 7:
                                    last_waypoint.append(waypoint[6])  # Coloca a velocidade no primeiro index
                                    last_waypoint.append(waypoint[7]) # Coloca o vertical_rate no primeiro index
                                #last_waypoint = calc_speeds(last_waypoint)
                            
                            last_waypoint = waypoint
                            index = index + 1

                        else:
                            data_dict_sorted[icao].remove(data_dict_sorted[icao][index])
                                #remove_list.append(index)
                            # if index == 1:
                            #     if len(last_waypoint) < 7:
                            #         last_waypoint.append(waypoint[6])  # Coloca a velocidade no primeiro index
                            #         last_waypoint.append(waypoint[7]) # Coloca o vertical_rate no primeiro index
                            #     #last_waypoint = calc_speeds(last_waypoint)
                    
                if index == 1:
                    if len(last_waypoint) < 7:
                        last_waypoint.append(0) # Coloca zero na velocidade no primeiro index
                        last_waypoint.append(0) # Coloca zero no vertical_rate no primeiro index   
                    # else:
                    #     index = index + 1

                    
                        
                #     else:
                #         # Return time difference (seconds)
                #         time_diff = data_dict_sorted[icao][index+1][0] - waypoint[0]
                #         if time_diff != 0: 
                #             if len(waypoint) < 7:
                #                 waypoint = self.__calc_speeds(waypoint, data_dict_sorted[icao][index+1])
                #             waypoint = calc_speeds(waypoint)
                #         else:
                #             remove_list.append(index)

                #     index = index + 1

                # remove_list.reverse()
                # for i in remove_list:
                #     data_dict_sorted[icao].remove(data_dict_sorted[icao][i])

                        #if index !=0:    
                            
                            # Return time difference (seconds)
                            #time_diff = waypoint[0] - last_waypoint[0]

                            #if time_diff > 0 and len(waypoint) < 7:

                                # Calculate speed
                                # last = (last_waypoint[1], last_waypoint[2])
                                # actual = (waypoint[1], waypoint[2])
                                # d_distante = distance.distance(last, actual).meters
                                # speed = d_distante / time_diff #[m/s]
                                # waypoint.append(speed)

                                # # Calculate vertical rate
                                # alt_diff = waypoint[3] - last_waypoint[3]
                                # vertical_rate = alt_diff / time_diff
                                # waypoint.append(vertical_rate)
                                
                            # elif time_diff <= 0 and len(waypoint) < 7:
                            #     waypoint.append(last_waypoint[6]) #Coloca a velocidade referente ao valor anterior
                            #     waypoint.append(last_waypoint[7]) #Coloca o vertical_rate referente ao valor anterior

                            # if index == 1 and len(last_waypoint) < 7: # Se o primeiro item não tiver velocidade
                                # last_waypoint[6] = waypoint[6] # Coloca a velocidade no primeiro index
                                # last_waypoint[7] = waypoint[7] # Coloca o vertical_rate no primeiro index
                        # else:
                        #     waypoint.append(0) #speed = 0
                        #     waypoint.append(0) #vertical_rate = 0

        with open(data_path + "\\" + self.datestr + "_sorted.json", "w") as outfile:
            json.dump(data_dict_sorted, outfile)
        return data_dict_sorted


    '''
        Get dict from data
    '''
    def __get_data_dict(self):

        data_path = "data\\"+self.datestr
        
        data = dict()

        with open(data_path + "\\" + self.datestr + "_sorted.json", "r") as readfile:
            data_dict = json.load(readfile)
            icao_list = list(data_dict.keys())

            for icao in icao_list:
                data[icao] = dict()
                data[icao]['lat'] = list()
                data[icao]['lon'] = list()
                data[icao]['alt'] = list()
                data[icao]['vel_xy'] = list()
                data[icao]['vel_z'] = list()
                data[icao]['track'] = list()
                data[icao]['t'] = list()
                # data[icao]['mach'] = list()
                # data[icao]['Vtas'] = list()
                # data[icao]['Vtas_kts'] = list()
                # data[icao]['Veas'] = list()
                # data[icao]['Veas_kts'] = list()
                # data[icao]['Vcas'] = list()
                # data[icao]['Vcas_kts'] = list()

                for waypoint in data_dict[icao]:
                    try:
                        data[icao]['t'].append(waypoint[0])
                        data[icao]['lat'].append(waypoint[1])
                        data[icao]['lon'].append(waypoint[2])
                        data[icao]['alt'].append(waypoint[3])
                        data[icao]['track'].append(waypoint[4])
                        data[icao]['vel_xy'].append(waypoint[6])
                        data[icao]['vel_z'].append(waypoint[7])
                        # data[icao]['mach'].append(waypoint[8]) #-  Mach Number
                        # data[icao]['Vtas'].append(waypoint[9]) #-  Vtas/TAS True airspeed m/s
                        # data[icao]['Vtas_kts'].append(waypoint[10]) #- Vtas/TAS True airspeed knots
                        # data[icao]['Veas'].append(waypoint[11]) #- Veas/EAS Equivalent airspeed m/s
                        # data[icao]['Veas_kts'].append(waypoint[12]) #- Veas/EAS Equivalent airspeed knots
                        # data[icao]['Vcas'].append(waypoint[13]) #- Vcas/CAS Calibrated airspeed m/s
                        # data[icao]['Vcas_kts'].append(waypoint[14]) #- Vcas/CAS Calibrated airspeed knots
                    except Exception as inst:
                        print(type(inst))    # the exception type
                        print(inst.args)     # arguments stored in .args
                        print(inst)          # __str__ allows args to be printed directly,

        return data

    '''
        Function to resample data into specific time step
    '''
    def __resample_data(self, data_dict):

        data = dict()
        icao_list = list(data_dict.keys())
        #icao_list = ICAO_LIST_TEST_6

        for icao in icao_list:
            #data_dict[icao]['t'] =  pd.to_datetime(data_dict[icao]['t'])
            for i in np.arange(0, len(data_dict[icao]['t']), 1):
                data_dict[icao]['t'][i] = pd.to_datetime(datetime.fromtimestamp(data_dict[icao]['t'][i]))
            df = pd.DataFrame(data_dict[icao])
            df = df.set_index('t')
            #print(df)
            #print(df[df.index.duplicated()])

            df = df[~df.index.duplicated()] # Remove duplicated rows
            dif_data = df.index[-1]-df.index[0]
            resto = np.mod(int(dif_data.seconds/len(df.index)),60)
            if resto == 0: resto = 60
            #print(dif_data.seconds, resto)
            #upsampled = df.resample(str(resto)+'S')
            #interpolated = upsampled.interpolate(method='linear')
            old_idx = df.index
            #new_idx = pd.date_range(old_idx.min(), old_idx.max(), freq=str(resto)+'S')
            new_idx = pd.date_range(old_idx.min(), old_idx.max(), freq='60S')
            interpolated = df.reindex(old_idx.union(new_idx)).interpolate('index').reindex(new_idx)
            #interpolated = upsampled.interpolate(method='spline', order=2)
            data[icao] = interpolated
        return data


    def __remove_samples_dict(self, airplane, index_init, index_end = None):

        airplane_itens = list(airplane.keys())

        if index_end == None:
            for item in airplane_itens:
                del airplane[item][index_init]
        else:
            for item in airplane_itens:
                del airplane[item][index_init:index_end]

        return airplane


    def __remove_take_off(self, airplane, lim=None):
        
        # Get altitute data
        if isinstance(airplane, dict):
            alt = airplane["alt"]
        else:
            alt = airplane.loc[:,"alt"]
        
        window_init = 0 # A janela de take-off inicia no primeiro índice
        window_end = 0 # Inicialmente a janela de take-off acaba no primeiro índice também
        i = 1
        
        if lim == None:
            lim = 10000
        
        while i < len(alt) and alt[i] < lim:
            window_end = i 
            i = i+1   

        if window_init < window_end:
            #for i in sorted(range(window_init, window_end+1), reverse=True):
            if isinstance(airplane, dict):
                airplane = self.__remove_samples_dict(airplane, window_init, window_end+1)
            else:                
                airplane = airplane.drop(index = airplane.index[window_init:window_end+1])
        
        return airplane
    

    def __remove_landing(self, airplane, lim = None):
        
        # Get altitute data
        if isinstance(airplane, dict):
            alt = airplane["alt"]
        else:
            alt = airplane.loc[:,"alt"]
        
        window_end = len(alt) # 
        window_init = len(alt) # 
        i = window_init-1
        
        if lim == None:
            lim = 10000

        while i > -1 and alt[i] < lim:
            window_init = i 
            i = i-1

        if window_init != window_end:
#            for i in sorted(range(window_init, window_end), reverse=True):
            if isinstance(airplane, dict):
                airplane = self.__remove_samples_dict(airplane, window_init, window_end)
            else:                
                airplane = airplane.drop(index = airplane.index[window_init:window_end])

        return airplane


    '''
        Remove take off and landing of flight 
    '''
    def __get_cruise_only(self, data_dict):
        icao_list = list(data_dict.keys()) #Esse é o certo
        #icao_list = ICAO_LIST_TEST_6

        for icao in icao_list:
            airplane = data_dict[icao]['filter']
            
            # Remove take off and landing (a media da altura dos voos)
            if len(airplane.loc[:,"alt"]) > 0:
                media = mean(airplane.loc[:,"alt"])
                airplane = self.__remove_take_off(airplane, media)
                airplane = self.__remove_landing(airplane, media)
            else:
                # Remove take off and landing (10000)
                airplane = self.__remove_take_off(airplane, None)
                airplane = self.__remove_landing(airplane, None)
            
            data_dict[icao]['cruise'] = airplane
        
        return data_dict


    '''
        Separate different flights from of one icao name into two data icaos
    '''
    def __separate_flights(self, data_dict):
        icao_list = list(data_dict.keys()) #Esse é o certo
        #icao_list = ICAO_LIST_TEST_6

        data = dict()

        for icao in icao_list:
            airplane = data_dict[icao]
            data[icao] = dict()
            data[icao]['all'] = airplane

            # Remove take off and landing (10000)
            airplane = self.__remove_take_off(airplane, None)
            airplane = self.__remove_landing(airplane, None)

            
            # Get index of minimum altitude
            #print(icao)
            alt = airplane["alt"]
            if len(alt) > 0:
                alt_min = min(alt)
                last_index = len(alt)-1
                alt_min_index = alt.to_list().index(alt_min)
                
                if alt_min < 4000 and alt_min_index > 0 and alt_min_index < last_index:                

                    airplane_itens = list(airplane.keys())
                    
                    new_data = dict()
                    new_data["t"] = airplane.index[alt_min_index:last_index]
                    for item in airplane_itens:
                        new_data[item] = airplane.loc[:,item][alt_min_index:last_index]
                        
                    df = pd.DataFrame(new_data)
                    df = df.set_index('t')

                    data[icao+"_1"] = dict()
                    data[icao+"_1"]['separate'] = df
                    data[icao+"_1"]['all'] = df
                
                    update_data = dict()
                    update_data["t"] = airplane.index[0:alt_min_index]
                    for item in airplane_itens:
                        update_data[item] = airplane.loc[:,item][0:alt_min_index]

                    df = pd.DataFrame(update_data)
                    df = df.set_index('t')
                    data[icao]['separate'] = df
                else:
                    data[icao]['separate'] = airplane
            else:
                #data[icao]['separate'] = data[icao]['all'] 
                data[icao]['separate'] = airplane
        return data


    '''
        Use a butterfield filter low pass in samples 
    '''
    def butter_lowpass_filter(self, data_dict):
        
        order = 2      
        normal_cutoff = 0.13

        # Get the filter coefficients 
        b, a = butter(order, normal_cutoff, btype='low', analog=False)

        icao_list = list(data_dict.keys()) #Esse é o certo
        #icao_list = ICAO_LIST_TEST_6

        for icao in icao_list:
            airplane = data_dict[icao]["separate"]

            if len(airplane.index) > 9: # Devido ao erro:ValueError: The length of the input vector x must be greater than padlen, which is 9

                data_filter = dict()
                data_filter["t"] = airplane.index

                airplane_itens = list(airplane.keys())
                for item in airplane_itens:
                    data_filter[item] = filtfilt(b, a, airplane.loc[:,item])
                
                df = pd.DataFrame(data_filter)
                df = df.set_index('t')
                
                data_dict[icao]['filter'] = df
            else:
                data_dict[icao]['filter'] = airplane
            
        return data_dict


    def __get_samples_above_3_only(self, data):
        if len(data['filter'])>3:
            return True
        else:
            return False

    
    def __remove_samples_above_3(self, data):
        icao_list = list(data.keys()) 
        
        for icao in icao_list:
            if len(data[icao]['filter']) < 4:
                data.pop(icao)
        return data
    
    def __remove_samples_speed_above_400(self, data):
        icao_list = list(data.keys()) 
        
        for icao in icao_list:
            if abs(max(data[icao]['all']['vel_xy'])) > 400:
                data.pop(icao)
        return data

    '''
        Treat data 
    '''
    def treat_data(self, type='wr', only_path = False):
        
        # Option to new acquisition data which were not compiled
        if type == 'wr':
            # Read files from all ICAOs
            self.__get_state_from_files(only_path)
            # Update/Include speed in samples which it does not exist
            data = self.__update_speed()
        
        # Read data from file and return data into dict format
        data_dict = self.__get_data_dict()

        # Resample data to be always at same frequency
        data = self.__resample_data(data_dict)

        # Separate flights of one airplane into two icao_data
        data = self.__separate_flights(data)
        
        # Filter the data
        data = self.butter_lowpass_filter(data)

        # Remove take off and landing from data
        data = self.__get_cruise_only(data)

        # Remove samples with length below 3
        data = self.__remove_samples_above_3(data)

        # Remove samples with speed higher than 400
        # data = self.__remove_samples_speed_above_400(data)
        
        return data

    '''
        Read data from OpenSkyApi with timer 5 to 5 minutes
    '''
    def run_openskyapi_read(self):
        WAIT_TIME_SECONDS = 300 #5 minutes
        print("Read first samples")
        self.__get_states()
 
        ticker = threading.Event()
        print("Init loop")
        while not ticker.wait(WAIT_TIME_SECONDS):
            self.__get_states()