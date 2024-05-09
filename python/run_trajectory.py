from opensky_api import OpenSkyApi
from trajectory import Trajectory
from trajectory_prediction import Trajectory_Prediction
from plot_4d_dimensions import PlotData
#from conflict_detection_2 import Conflict_Detection
from conflict_detection import Conflict_Detection
from search_tree import Search_Tree
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import json
import pandas as pd
import numpy as np
from binarytree import build



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

print("Time serie")
data_time_serie = traj.treat_data(type = 'r', only_path = False)
search_tree = Search_Tree(tree=None, data=data_time_serie)

#print("Detecção!")
con_detec = Conflict_Detection(data_time_serie)
#root = build(data_time_serie)
#print(root)

plot = PlotData(data_time_serie, data_time_serie)

icao_list = list(data_time_serie.keys())
#icao_list = ['020140', '02a1b3', '010244','0180a4','02006e','020073', '020095', '020104', '020112','020124','02a260','06a09a']
#icao_list = ['020095']
#icao_list = ['02a1b3']
#icao_list = ['020140', '02a1b3']
#icao_list = ['0a009c']
f = open("conflicts.txt", "a")

for icao in icao_list:
    #print(icao)+
    #print(data_time_serie[icao])
    #plot.plot_comp_all_cruise(data_time_serie, icao)
    #plot.plot_comp_samples(data_vector, data_time_serie, icao)    

    conflicts = con_detec.search_conflicts(icao)
    if conflicts[icao]['conflict']:
        print(conflicts)
        print("There is a conflict")
        #plot.plot_icao_traj(data_time_serie, icao, conflicts)
    
    (first_filter, second_filter) = search_tree.search(conflicts, icao)
    if len(first_filter) > 0:
        print("First filter:")
        print(first_filter)
        #plot.plot_data_4_axes(data_time_serie, icao, first_filter, conflicts)
        if len(second_filter) > 0:
            print("Second filter")
            print(second_filter)
            #plot.plot_data_4_axes(data_time_serie, icao, second_filter, conflicts)

    f.write(icao+":\n")
    f.write(str(conflicts)+"\n")
    f.write("First filter:"+str(first_filter)+"\n")
    f.write("Second filter:"+str(second_filter)+"\n")
    
f.close()
   


#convert into excel
#df = pd.DataFrame(data=data_time_serie[icao])
#df.to_excel(icao+'.xlsx', index=False)


#Get Trajectory Prediction
'''traj_pred = Trajectory_Prediction(data)
data_pred = traj_pred.predict_traj(300)
print(data_pred)
'''
