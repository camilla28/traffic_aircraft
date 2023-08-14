from opensky_api import OpenSkyApi
import jsons
import json
import time
import datetime
import os
import threading, time
import math


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
    def __get_state_from_files(self):
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

                    for file in files:
                        
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
                            speed = d_distante/time_diff #[m/s]
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
        Read data from OpenSkyApi with timer 5 to 5 minutes
    '''
    def run_openskyapi_read(self):
        WAIT_TIME_SECONDS = 300 #5 minutes

        self.__get_states()
 
        ticker = threading.Event()
        while not ticker.wait(WAIT_TIME_SECONDS):
            self.__get_states()


    '''
        Treta data 
    '''
    def treat_data(self, type='vector'):
        self.__get_state_from_files()
        data = self.__update_speed()
        if type == 'vector':
            data = self.__get_data_dict()
        return data
