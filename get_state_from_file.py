from opensky_api import OpenSkyApi
import json
import time
import os

api = OpenSkyApi(username="Camillas97", password="PEE3028")

bbox_filter = (-20, 60, 20, 100)

# Write in file
datestr = time.strftime("%Y%m%d")

data_path = "data\\"+datestr

dir_list = os.listdir(data_path)

data = dict()

for dir in dir_list:
    # Path of icao 
    path = data_path + "\\" + dir

    files = os.listdir(path)
    
    if files != []:

        data[dir] = list()

        files = [f for f in files if os.path.isfile(path+'\\'+f)] #Filtering only the files.

        for file in files:
            
            with open(path+'\\'+file, "r") as read_file:
                
                data_dict = json.load(read_file)
                
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

            for waypoint in data_dict["path"]:
                data[dir].append(waypoint)        

with open(data_path + "\\" + datestr + ".json", "w") as outfile:
    json.dump(data, outfile)

'''
with open("OpenSkyTrack_a59601_20230509-204813.json", "r") as read_file:
    data_dict = json.load(read_file)

    icao24 = data_dict["icao24"]

    vetor = [data_dict["time_position"],
             data_dict["latitude"],
             data_dict["longitude"],
             int(data_dict["baro_altitude"]),
             int(data_dict["true_track"]),
             data_dict["on_ground"]]
    
    data_dict["path"].append(vetor)

    states = api.get_states(icao24 = "a59601", bbox=bbox_filter)
    
    if states != None:
        print(states)
        for state in states.states:
            print(state)
    else:
        print(" Estado não encontrado")
'''
'''
    for waypoint in data_dict["path"]:
        
        waypoint_time = waypoint[0]
        
        states = api.get_states(time_secs=waypoint_time, icao24 = icao24, bbox=bbox_filter)
        if states != None:
            for state in states.states:
                print(state)
        else:
            print(waypoint_time, " Estado não encontrado")

'''