
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
datestr = "20230601"
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
        
        
        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        for waypoint in data_dict[icao]:
            t.append(waypoint[0])
            lat.append(waypoint[1])
            lon.append(waypoint[2])
            alt.append(waypoint[3])
            track.append(waypoint[4])
            vel_xy.append(waypoint[6])
            vel_z.append(waypoint[7])

        
        #ax1 = fig.add_subplot(2, 2, 1, projection='3d')
        ax1 = fig.add_subplot(1, 1, 1, projection='3d')
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.set_zlabel("Baro altitude")
        ax1.plot3D(lon, lat, alt, cmap = t, label = icao)
        ax1.scatter3D(lon, lat, alt, cmap = t, label = icao)
        '''
        ax2 = fig.add_subplot(2, 2, 2, projection='3d')
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Latitude")
        ax2.set_zlabel("Baro altitude")
        ax2.plot3D(t, lat, alt, label = icao)
        ax2.scatter3D(t, lat, alt, label = icao)

        ax3 = fig.add_subplot(2, 2, 3, projection='3d')
        ax3.set_xlabel("Longitude")
        ax3.set_ylabel("Time")
        ax3.set_zlabel("Baro altitude")
        ax3.plot3D(lon, t, alt, label = icao)
        ax3.scatter3D(lon, t, alt, label = icao)

        ax4 = fig.add_subplot(2, 2, 4, projection='3d')
        ax4.set_xlabel("Longitude")
        ax4.set_ylabel("Latitude")
        ax4.set_zlabel("Time")
        ax4.plot3D(lon, lat, t, label = icao)
        ax4.scatter3D(lon, lat, t, label = icao)
        '''
        
        plt.legend()

        plt.show()
    



