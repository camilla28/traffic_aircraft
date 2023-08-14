from opensky_api import OpenSkyApi
from trajectory import Trajectory
from trajectory_prediction import Trajectory_Prediction
from plot_4d_dimensions import PlotData
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

# set up a figure twice as wide as it is tall
#fig = plt.figure(figsize=plt.figaspect(0.5))

# Read data
'''
traj = Trajectory()
traj.run_openskyapi_read()
'''

# Get trajectory
datestr = "20230727"
traj = Trajectory(datestr)
data = traj.treat_data(type = 'waypoint')

#Get Trajectory Prediction
'''traj_pred = Trajectory_Prediction(data)
data_pred = traj_pred.predict_traj(300)
print(data_pred)
'''
#Plot trajectory
plot = PlotData(data, data)
plot.plot_data(data)
