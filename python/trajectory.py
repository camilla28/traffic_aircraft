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




class Trajectory:
    
    def __init__(self, datestr = None , username="Camillas97", password="PEE3028"):
        # OpenSkyApi credentials
        self.username = username
        self.password = password
        self.api = OpenSkyApi(self.username, self.password)
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
                
            #icao24 = "4b1815"
            track = jsons.dump(self.api.get_track_by_aircraft(icao24))

            if track != None:

                flights = jsons.dump(self.api.get_flights_by_aircraft(icao24,int(track['startTime'])- 86400, int(track['endTime'])+86400))
                
                if flights != None:
                    track['startTime'] = datetime.datetime.fromtimestamp(track['startTime']).strftime("%Y/%m/%d-%H:%M:%S")
                    track['endTime'] = datetime.datetime.fromtimestamp(track['endTime']).strftime("%Y/%m/%d-%H:%M:%S")

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

            for icao in icao_list:

                data_dict_sorted[icao] = sorted(data_dict[icao], key=self.__takeTime)

                last_waypoint = data_dict_sorted[icao][0]

                index = 0

                for waypoint in data_dict_sorted[icao]:
                    
                    if index !=0:
                        # Return time difference (seconds)
                        time_diff = waypoint[0] - last_waypoint[0]
                        
                        if time_diff > 0 and len(waypoint) < 7:

                            # Calculate speed
                            lat_diff = waypoint[1] - last_waypoint[1]
                            long_diff = waypoint[2] - last_waypoint[2]
                            d_distante = self.__distance_on_geoid(last_waypoint[1], last_waypoint[2], waypoint[1], waypoint[2])
                            speed = d_distante / time_diff #[m/s]
                            waypoint.append(speed)

                            # Calculate vertical rate
                            alt_diff = waypoint[3] - last_waypoint[3]
                            vertical_rate = alt_diff / time_diff
                            waypoint.append(vertical_rate)
                        elif time_diff <= 0:
                            waypoint.append(0) #speed = 0
                            waypoint.append(0) #vertical_rate = 0
                    else:
                        waypoint.append(0) #speed = 0
                        waypoint.append(0) #vertical_rate = 0

                    index = index + 1
                    last_waypoint = waypoint
            
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

                for waypoint in data_dict[icao]:
                    data[icao]['t'].append(waypoint[0])
                    data[icao]['lat'].append(waypoint[1])
                    data[icao]['lon'].append(waypoint[2])
                    data[icao]['alt'].append(waypoint[3])
                    data[icao]['track'].append(waypoint[4])
                    data[icao]['vel_xy'].append(waypoint[6])
                    data[icao]['vel_z'].append(waypoint[7])
        
        return data

    '''
        Function to resample data into specific time step
    '''
    def __resample_data(self, data_dict):
        data = dict()
        icao_list = list(data_dict.keys())
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


    def __remove_take_off(self, airplane, lim=None):
        alt = airplane.loc[:,"alt"]
        window_init = 0 # A janela de take-off inicia no primeiro índice
        window_end = 0 # Inicialmente a janela de take-off acaba no primeiro índice também
        i = 1
        if lim == None:
            lim = 10000
        while i < len(alt) and alt[i] < lim:
            window_end = i 
            i = i+1   
        #print("Remove Take-Off: ", window_init, window_end)
        if window_init != window_end:
            for i in sorted(range(window_init, window_end+1), reverse=True):
                airplane = airplane.drop(index = airplane.index[i])
            #for i in range(window_init, window_end):
            #    airplane = airplane.drop([airplane.index[i]])
            #    print(i, airplane.index[i], airplane)
        return airplane
    

    def __remove_landing(self, airplane, lim = None):
        alt = airplane.loc[:,"alt"]
        window_end = len(alt) # 
        window_init = len(alt) # 
        i = window_init-1
        if lim == None:
            lim = 10000
        while i > -1 and alt[i] < lim:
            #print(i, alt[i])
            window_init = i 
            i = i-1   
        #print("Remove Landing: ", window_init, window_end)
        if window_init != window_end:
            for i in sorted(range(window_init, window_end), reverse=True):
                airplane = airplane.drop(index = airplane.index[i])
            #for i in range(window_init, window_end):
            #    airplane = airplane.drop([airplane.index[i]])
            #    print(i, airplane.index[i], airplane)
        return airplane


    '''
        Remove take off and landing of flight 
    '''
    def __get_cruise_only(self, data_dict):
        icao_list = list(data_dict.keys()) #Esse é o certo
        #icao_list = ['020140', '02a1b3']
        #icao_list = ['02a1b3']
        #icao_list = ['020140', '02a1b3', '010244','0180a4','02006e','020073', '020095', '020104', '020112','020124','02a260','06a09a']
        #icao_list = ['020095']

        for icao in icao_list:
            airplane = data_dict[icao]['filter']
            # Remove take off and landing (10000)
            airplane = self.__remove_take_off(airplane, None)
            airplane = self.__remove_landing(airplane, None)
            # Remove take off and landing (a media da altura dos voos)
            #airplane = self.__remove_take_off(airplane, mean(airplane.loc[:,"alt"]))
            #airplane = self.__remove_landing(airplane, mean(airplane.loc[:,"alt"]))

            data_dict[icao]['cruise'] = airplane
        return data_dict
    
    def butter_lowpass_filter(self, data):
        # Filter requirements.
        
        order = 2      
        normal_cutoff = 0.13
        # Get the filter coefficients 
        b, a = butter(order, normal_cutoff, btype='low', analog=False)

        data_dict = dict()
        icao_list = list(data.keys())
        #icao_list = ['020140', '02a1b3']
        #icao_list = ['020140', '02a1b3', '010244','0180a4','02006e','020073', '020095', '020104', '020112','020124','02a260','06a09a']
        for icao in icao_list:
            airplane = data[icao]
            if len(airplane.index) > 9: # Devido ao erro:ValueError: The length of the input vector x must be greater than padlen, which is 9

                data_dict[icao] = dict()
                data_dict[icao]['all'] = data[icao]

                data_filter = dict()
                data_filter["t"] = airplane.index
                
                data_filter["alt"] = filtfilt(b, a, airplane.loc[:,"alt"])
                data_filter["lon"] = filtfilt(b, a, airplane.loc[:,"lon"])
                data_filter["lat"] = filtfilt(b, a, airplane.loc[:,"lat"])
                data_filter["track"] = filtfilt(b, a, airplane.loc[:,"track"])
                data_filter["vel_xy"] = filtfilt(b, a, airplane.loc[:,"vel_xy"])
                data_filter["vel_z"] = filtfilt(b, a, airplane.loc[:,"vel_z"])
                
                df = pd.DataFrame(data_filter)
                df = df.set_index('t')
                
                data_dict[icao]['filter'] = df

        return data_dict

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
        
        # Filter the data
        data = self.butter_lowpass_filter(data)

        # Remove take off and landing from data
        data = self.__get_cruise_only(data)
        return data

    '''
        Read data from OpenSkyApi with timer 5 to 5 minutes
    '''
    def run_openskyapi_read(self):
        WAIT_TIME_SECONDS = 300 #5 minutes

        self.__get_states()
 
        ticker = threading.Event()
        while not ticker.wait(WAIT_TIME_SECONDS):
            self.__get_states()