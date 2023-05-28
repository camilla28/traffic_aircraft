
'''
    Plot x,y,t  3d surface and z as colormap
'''
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
import json



'''
    Código teste
'''
datestr = time.strftime("%Y%m%d")

data_path = "data\\"+datestr

with open(data_path + "\\" + datestr + "_sorted.json", "r") as readfile:
    data_dict = json.load(readfile)
    icao_list = list(data_dict.keys())


    '''fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_title('Track')
    ax.set_ylabel("Latitude")
    ax.set_xlabel("Longitude")
    ax.set_zlabel("Baro altitude")
    '''

    for icao in icao_list:
        lat = list()
        lon = list()
        alt = list()
        vel_xy = list()
        vel_z = list()
        track = list()
        t = list()
        
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.set_title('Track')
        ax.set_ylabel("Latitude")
        ax.set_xlabel("Longitude")
        ax.set_zlabel("Baro altitude")

        for waypoint in data_dict[icao]:
            t.append(waypoint[0])
            lat.append(waypoint[1])
            lon.append(waypoint[2])
            alt.append(waypoint[3])
            track.append(waypoint[4])
            vel_xy.append(waypoint[6])
            vel_z.append(waypoint[7])

        
        ax.plot3D(lon, lat, alt, label = icao)
        ax.scatter3D(lon, lat, alt, label = icao)
        
        plt.legend()

        plt.show()
    



