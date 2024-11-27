
from trajectory import Trajectory
#from opensky_api import OpenSkyApi



# set up a figure twice as wide as it is tall
#fig = plt.figure(figsize=plt.figaspect(0.5))

# Read data

traj = Trajectory()
traj.run_openskyapi_read()
