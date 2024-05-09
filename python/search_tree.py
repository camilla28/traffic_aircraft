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
from binarytree import build
import geopy.distance

class Search_Tree:
    def __init__(self, tree = None, data = None):
        #if tree != None:
        #    self.tree = tree
        #else:
        #    self.__create_tree(True, data = None)
        self.data = data

    def search(self, conflicts, icao):
        airplane = self.data[icao]
        icao_list = list(self.data.keys())
        icao_list.remove(icao)
        first_filter = []
        second_filter = []
        if conflicts[icao]['conflict']:
            for conflict in conflicts[icao]['man_track']:
                A_time = airplane['cruise'].index[conflict[0]]
                B_time = airplane['cruise'].index[conflict[1]]
                C_time = airplane['cruise'].index[conflict[2]]
                for icao in icao_list:
                    aircraft = self.data[icao]
                    pass
            for conflict in conflicts[icao]['man_alt']:
                A_time = airplane['cruise'].index[conflict[0]]
                B_time = airplane['cruise'].index[conflict[1]]
                A_lat = airplane['cruise'].lat[conflict[0]]
                B_lat = airplane['cruise'].lat[conflict[1]]
                A_lon = airplane['cruise'].lon[conflict[0]]
                B_lon = airplane['cruise'].lon[conflict[1]]
                A_alt = airplane['cruise'].alt[conflict[0]]
                B_alt = airplane['cruise'].alt[conflict[1]]
                
                for icao in icao_list:
                    aircraft = self.data[icao]['all']
                    time_filter = aircraft[(aircraft.index <= B_time) & (aircraft.index >=A_time)&
                                           (aircraft.lat <= max(B_lat, A_lat)) & (aircraft.lat >=min(A_lat, B_lat))&
                                           (aircraft.lon <= max(B_lon, A_lon)) & (aircraft.lon >=min(A_lon, B_lon))&(aircraft.alt <= max(B_alt, A_alt)) & (aircraft.alt >=min(A_alt, B_alt))]
                    if len(time_filter) > 0:
                        first_filter.append(icao)

                for icao in first_filter:
                    aircraft = self.data[icao]['all']
                    if A_time in aircraft.index:
                        icao_lat = aircraft.lat[A_time]
                        icao_lon = aircraft.lon[A_time]
                        icao_alt = aircraft.alt[A_time]
                    else:
                        minor = aircraft[aircraft.index < A_time]
                        major = aircraft[aircraft.index > A_time]
                        #print("Minor:", len(minor))
                        #print(minor)
                        #print("Major:", len(major))
                        #print(major)
                        if len(minor) == 0:
                            A1_time = major.index[0]
                        else:
                            A1_time = minor.index[len(minor)-1]
                        #A2_time = major.index[0]
                        icao_vel_xy = aircraft.vel_xy[A1_time]
                        icao_vel_z = aircraft.vel_z[A1_time]
                        icao_track = aircraft.track[A1_time]
                        #int(round(dtimestamp))
                        time_diff = A_time.timestamp() - A1_time.timestamp()
                        distance_xy = time_diff * icao_vel_xy
                        distance_z = time_diff * icao_vel_z
                        icao_lat = aircraft.lat[A1_time]
                        icao_lon = aircraft.lon[A1_time]
                        icao_alt = aircraft.alt[A1_time] + distance_z
                        icao_lat, icao_lon = self.__get_geoLoc_from_distance(distance_xy, icao_lat, icao_lon, icao_track)
                    
                    #print(icao, A_time, A_lat, A_lon, A_alt, icao_lat, icao_lon, icao_alt)
                    low_lim_lat, _, _ = geopy.distance.distance(nautical=5).destination((A_lat, A_lon), bearing=180)
                    high_lim_lat, _, _ = geopy.distance.distance(nautical=5).destination((A_lat, A_lon), bearing=0)
                    _, low_lim_long, _ = geopy.distance.distance(nautical=5).destination((A_lat, A_lon), bearing=270)
                    _, high_lim_long, _ = geopy.distance.distance(nautical=5).destination((A_lat, A_lon), bearing=90)
                    low_lim_alt = A_alt - 1000
                    high_lim_alt = A_alt + 1000
                    #print(low_lim_lat, high_lim_lat, low_lim_long, high_lim_long, low_lim_alt, high_lim_alt)
                    
                    if icao_lat >= low_lim_lat and icao_lat <= high_lim_lat and \
                    icao_lon >= low_lim_long and icao_lon <= high_lim_long and \
                    icao_alt >= low_lim_alt and icao_alt <= high_lim_alt:
                        second_filter.append(icao)   
                        
        return (first_filter, second_filter)
    

    def __get_geoLoc_from_distance(self, distance, lat1, lat2, track):
        lat, lon, _ = geopy.distance.distance(meters=distance).destination((lat1, lat2), bearing=track)
        return (lat, lon)
    

    def create(self, set_internal_data = False, data = None):
        if set_internal_data and data != None:
            self.data = data
        else:
            data = self.data
        self.__create_tree(data)

    def __create_tree(self, data):
        icao_list = list(data.keys())


    
    def set_data(self, data):
        self.data = data

    def set_tree(self, tree):
        self.tree = tree