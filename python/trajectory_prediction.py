
'''
    Trajectory Prediction
'''
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
import json
import math
import geopy
from geopy.distance import geodesic, great_circle


class Trajectory_Prediction:
    
    def __init__(self, data):
        self.data = data


    def __get_point_at_distance(self, t, velxy, lat1, lon1, track, alt, velz):
        """
        lat: initial latitude, in degrees
        lon: initial longitude, in degrees
        t: delta time in seconds
        velxy: velocity in m/s
        d: target distance from initial
        track: (true) heading in degrees
        R: optional radius of sphere, defaults to mean radius of earth

        Returns new lat/lon coordinate {d}km from initial, in degrees
        """

        '''
        R=6371
        d = (velxy * t)/1000 # distance em km
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        a = math.radians(track)
        lat2 = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1) * math.sin(d/R) * math.cos(a))
        lon2 = lon1 + math.atan2(
            math.sin(a) * math.sin(d/R) * math.cos(lat1),
            math.cos(d/R) - math.sin(lat1) * math.sin(lat2)
        )
        return (math.degrees(lat2), math.degrees(lon2),)

        '''

        alt_diff = velz*t
        alt = alt + alt_diff
            
        # given: lat1, lon1, b = bearing in degrees, d = distance in kilometers

        d = (velxy * t)/1000 # distance em km
        #a = math.radians(track)
        origin = geopy.Point(lat1, lon1)
        destination = great_circle(kilometers=d).destination(origin, track)

        lat2, lon2 = destination.latitude, destination.longitude
        return(lat2, lon2, alt)
        


    def predict_traj(self, delta_t):
        data_predict = dict()

        for icao in self.data.keys():
            data_predict[icao] = list()
            index = 0
            print(icao)

            for waypoint in self.data[icao]:

                if index != 0:
                    waypoint_predict = list()
                    lat=waypoint[1]
                    lon=waypoint[2]
                    alt=waypoint[3]
                    track=waypoint[4]
                    vel_xy=waypoint[6]
                    vel_z=waypoint[7]
                    new_waypoint = self.__get_point_at_distance(delta_t, vel_xy, lat, lon, track, alt, vel_z)
                    new_time = waypoint[0]+delta_t
                    print(new_time, new_waypoint)
                    waypoint_predict.append(new_time)

                index = index + 1

            data_predict[icao].append(waypoint_predict)