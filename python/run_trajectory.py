from opensky_api import OpenSkyApi
from trajectory import Trajectory
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))

datestr = "20230601"

traj = Trajectory(datestr)

#traj.run_openskyapi_read()

data = traj.treat_data()
for icao in data.keys():

    for index in range(len(data[icao])-1):
        print(data[icao]['lon'][index])
        print(data[icao]['lat'][index])
        print(data[icao]['vel_xy'][index])
        print(data[icao]['track'][index])
        
        track = math.radians(data[icao]['track'][index])
        vel = data[icao]['vel_xy'][index]
        vel_x = math.cos(track)*vel
        vel_y = math.sin(track)*vel
        delta_t = data[icao]['t'][index+1] - data[icao]['t'][index]
        
        print(delta_t)
        print(data[icao]['lon'][index]+vel_x*delta_t)
        print(data[icao]['lat'][index]+vel_y*delta_t)