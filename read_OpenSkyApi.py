# Installation
'''
conda create -n traffic -c conda-forge python=3.10 traffic
conda activate traffic

from traffic.data.samples import belevingsvlucht
from rich.pretty import pprint
from traffic.data.samples import quickstart
'''

from opensky_api import OpenSkyApi
import jsons
import json
import time
import datetime
import os
import threading, time

api = OpenSkyApi(username="Camillas97", password="PEE3028")

def get_states():
    # bbox = (min latitude, max latitude, min longitude, max longitude)
    states = api.get_states(bbox=(45.8389, 47.8229, 5.9962, 10.5226))
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
        track = jsons.dump(api.get_track_by_aircraft(icao24))

        if track != None:

            flights = jsons.dump(api.get_flights_by_aircraft(icao24,int(track['startTime'])- 86400, int(track['endTime'])+86400))
            
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

WAIT_TIME_SECONDS = 300 #5 minutes

get_states()
 
ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    get_states()