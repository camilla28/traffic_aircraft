from opensky_api import OpenSkyApi
from trajectory import Trajectory
from trajectory_prediction import Trajectory_Prediction
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

data = traj.treat_data(type = 'waypoint')
traj_pred = Trajectory_Prediction(data)


traj_pred.predict_traj(300)