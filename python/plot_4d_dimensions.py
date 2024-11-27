'''
    Plot x,y,t  3d surface and z as colormap
'''

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
import json
import matplotlib.dates as dates
import pandas as pd
from datetime import datetime
import seaborn as sns
import statistics
from statistics import mean, stdev
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.patches import Circle
from search_tree import Search_Tree




class PlotData:
    def __init__(self, data, data_pred):
        self.__data = data
        self.__data_pred = data_pred
        self.search = Search_Tree(None, None)

    def plot_data_comp(self):
        icao_list = list(self.__data.keys())
        for icao in icao_list:
            lat = list()
            lon = list()
            alt = list()
            vel_xy = list()
            vel_z = list()
            track = list()
            t = list()
            for waypoint in self.__data[icao]:
                t.append(waypoint[0])
                lat.append(waypoint[1])
                lon.append(waypoint[2])
                alt.append(waypoint[3])
                track.append(waypoint[4])
                vel_xy.append(waypoint[6])
                vel_z.append(waypoint[7])

            lat_pred = list()
            lon_pred = list()
            alt_pred = list()
            vel_xy_pred = list()
            vel_z_pred = list()
            track_pred = list()
            t_pred = list()
            for waypoint in self.__data_pred[icao]:
                t_pred.append(waypoint[0])
                lat_pred.append(waypoint[1])
                lon_pred.append(waypoint[2])
                alt_pred.append(waypoint[3])
                track_pred.append(waypoint[4])
                vel_xy_pred.append(waypoint[6])
                vel_z_pred.append(waypoint[7])
            
             # set up a figure twice as wide as it is tall
            fig = plt.figure(figsize=plt.figaspect(0.5))

             #ax1 = fig.add_subplot(2, 2, 1, projection='3d')
            ax1 = fig.add_subplot(1, 1, 1, projection='3d')
            ax1.set_xlabel("Longitude")
            ax1.set_ylabel("Latitude")
            ax1.set_zlabel("Baro altitude")
            ax1.plot3D(lon, lat, alt, label = 'Real')
            ax1.scatter3D(lon, lat, alt, label = 'Real')
            ax1.plot3D(lon_pred, lat_pred, alt_pred, label = 'Prediction')
            ax1.scatter3D(lon_pred, lat_pred, alt_pred, label = 'Prediction')
            ax1.scatter3D(lon[0], lat[0], alt[0], label = 'Origin point')

            plt.legend()

            plt.show()


    def plot_data(self, data):
        icao_list = list(data.keys())
        for icao in icao_list:
            # set up a figure twice as wide as it is tall
            fig = plt.figure(figsize=plt.figaspect(0.5))


    def plot_data(self, data):
        icao_list = list(data.keys())
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

            for waypoint in data[icao]:
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
            ax1.plot3D(lon, lat, alt, label = icao)
            ax1.scatter3D(lon, lat, alt, label = icao)
            ax1.scatter3D(lon[0], lat[0], alt[0], label = 'origin')
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

    def plot_by_file(self, datestr):
        '''
            Código teste
        '''
        #datestr = time.strftime("%Y%m%d")
        #datestr = "20230601"
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
                ax1.plot3D(lon, lat, alt, label = icao)
                ax1.scatter3D(lon, lat, alt, label = icao)
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
    

    def plot_icao_traj_without_alt(self, data, icao, conflicts = None, pred_traj = None):
         #Plot trajectory
        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        if isinstance(data[icao]['cruise'], list):
            lon = data[icao]['cruise']['lon']
            lat = data[icao]['cruise']['lat']
        elif isinstance(data[icao]['cruise'], pd.DataFrame):
            lon = data[icao]['cruise'].loc[:,"lon"]
            lat = data[icao]['cruise'].loc[:,"lat"]

        ax1.plot(lon, lat, label = icao)
        ax1.scatter(lon, lat, s=5,  label = icao, color ='blue')
        if len(lon) > 0 and len(lat) > 0:
            ax1.scatter(lon[0], lat[0],  s=30, label = 'origin', color ='green')
    
        if conflicts != None and conflicts[icao]['conflict'] == True:
            for conflict in  conflicts[icao]['man_alt']+conflicts[icao]['man_track']:
                indice = conflict[0]
                ax1.scatter(lon[indice], lat[indice], s=30, label = 'conflict', color ='red')
                indice = conflict[1]
                ax1.scatter(lon[indice], lat[indice], s=30, label = 'conflict', color ='black')

        if pred_traj != None:
            ax1.plot(pred_traj[3], pred_traj[2], label = icao, color = 'green')
            ax1.scatter(pred_traj[3], pred_traj[2], s=5,  label = icao, color ='green')
            ax1.scatter(pred_traj[3][0], pred_traj[2][0], s=30, label = 'origin', color ='purple')
            ax1.scatter(pred_traj[3][len(pred_traj[0])-1], pred_traj[2][len(pred_traj[0])-1], s=30, label = 'end', color ='green')

        plt.legend()

        plt.show()

    def plot_conflict(self, data, row):
        A_icao            = row['Aircraft A'] 
        A_Ini_Man_Time    = mdates.date2num(datetime.strptime(row['Aircraft A Ini Man Time'], '%Y-%m-%d %H:%M:%S'))
        A_Ini_Man_Lat     = float(row['Aircraft A Ini Man Lat']) 
        A_Ini_Man_Lon     = float(row['Aircraft A Ini Man Lon'])
        A_Ini_Man_Alt     = float(row['Aircraft A Ini Man Alt'])
        A_Ini_Man_VelXY   = float(row['Aircraft A Ini Man Vel_xy'])
        A_Ini_Man_VelZ    = float(row['Aircraft A Ini Man Vel_z']) 
        A_Ini_Man_Track   = float(row['Aircraft A Ini Man Track'])
        SpeedManeuver     = row['Speed Maneuver'] 
        AltManeuver       = row['Altitude Maneuver']
        TrackManeuver     = row['Track Maneuver'] 
        A_End_Man_Time    = mdates.date2num(datetime.strptime(row['Aircraft A End Man Time'], '%Y-%m-%d %H:%M:%S'))
        A_End_Man_Lat     = float(row['Aircraft A End Man Lat'])
        A_End_Man_Lon     = float(row['Aircraft A End Man Lon'])
        A_End_Man_Alt     = float(row['Aircraft A End Man Alt'])
        A_End_Man_VelXY   = float(row['Aircraft A End Man Vel_xy'])
        A_End_Man_VelZ    = float(row['Aircraft A End Man Vel_z'])
        A_End_Man_Track   = float(row['Aircraft A End Man Track'])
        A_Conflict_Time   = matplotlib.dates.datestr2num(row['Aircraft A Conflict Time'])
        A_Conflict_Lat    = float(row['Aircraft A Conflict Lat'])
        A_Conflict_Lon    = float(row['Aircraft A Conflict Lon'])
        A_Conflict_Alt    = float(row['Aircraft A Conflict Alt'])
        A_Conflict_VelXY  = float(row['Aircraft A Conflict Vel_xy']) 
        A_Conflict_VelZ   = float(row['Aircraft A Conflict Vel_z'])
        A_Conflict_Track  = float(row['Aircraft A Conflict Track'])
        B_icao            = row['Aircraft B'] 
        B_Conflict_Time   = matplotlib.dates.datestr2num(row['Aircraft B Conflict Time'])
        B_Conflict_Lat    = float(row['Aircraft B Conflict Lat'])
        B_Conflict_Lon    = float(row['Aircraft B Conflict Lon'])
        B_Conflict_Alt    = float(row['Aircraft B Conflict Alt'])
        B_Conflict_VelXY  = float(row['Aircraft B Conflict Vel_xy']) 
        B_Conflict_VelZ   = float(row['Aircraft B Conflict Vel_z'])
        B_Conflict_Track  = float(row['Aircraft B Conflict Track'])

        # Get trajectory of Aircraft A
        A_time = mdates.date2num(data[A_icao]['cruise'].index)
        A_lon = data[A_icao]['cruise'].loc[:,"lon"]
        A_lat = data[A_icao]['cruise'].loc[:,"lat"]
        A_alt = data[A_icao]['cruise'].loc[:,"alt"]
        A_vel_xy = data[A_icao]['cruise'].loc[:,"vel_xy"]
        A_vel_z = data[A_icao]['cruise'].loc[:,"vel_z"]

        # Get trajectory of Aircraft B 
        B_time = data[B_icao]['cruise'].index
        B_lon = data[B_icao]['cruise'].loc[:,"lon"]
        B_lat = data[B_icao]['cruise'].loc[:,"lat"]
        B_alt = data[B_icao]['cruise'].loc[:,"alt"]
        B_vel_xy = data[B_icao]['cruise'].loc[:,"vel_xy"]
        B_vel_z = data[B_icao]['cruise'].loc[:,"vel_z"]

        plt.style.use('ggplot')

        # First figure Plot 3D (x,y,z)
        fig = plt.figure(figsize=plt.figaspect(0.5))
        fig.suptitle('Trajectory', fontsize=16)
        ax1 = fig.add_subplot(1, 1, 1, projection='3d')
        ax1.plot3D(A_lon, A_lat, A_alt, label = A_icao)
        ax1.scatter3D(A_lon, A_lat, A_alt, s=5,  label = A_icao, color ='blue')
        ax1.scatter3D(A_lon[0], A_lat[0], A_alt[0], s=30, label = 'origin', color ='green')
        ax1.set_title("Trajectory (Lon, Lat, Alt)")
        ax1.set_xlabel("Longitude [°]")
        ax1.set_ylabel("Latitude [°]")
        ax1.set_zlabel("Baro altitude [m]")
        ax1.legend(facecolor='white')

        fig2 = plt.figure(figsize=plt.figaspect(0.5))
        fig2.suptitle('Trajectory', fontsize=16)
        ax2 = fig2.add_subplot(1, 1, 1)
        ax2.plot(A_lon, A_lat, label = A_icao)
        ax2.scatter(A_lon, A_lat, s=5,  label = A_icao, color ='blue')
        ax2.scatter(A_lon[0], A_lat[0], s=30, label = 'origin', color ='green')
        ax2.set_title("Trajectory (Lon, Lat)")
        ax2.set_xlabel("Longitude [°]")
        ax2.set_ylabel("Latitude [°]")
        ax2.legend(facecolor='white')

        # Second figure Plot Speed
        fig5 = plt.figure(figsize=plt.figaspect(0.5))
        fig5.suptitle('Speed', fontsize=16)
        ax1 = fig5.add_subplot(1, 1, 1)
        ax1.plot(A_time, A_vel_xy, label = A_icao+ " - Ground speed", color = 'blue')
        ax1.set_title("Ground Speed ")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Ground Speed [m/s]")
        ax1.legend(facecolor='white')

        fig6 = plt.figure(figsize=plt.figaspect(0.5))
        fig6.suptitle('Vertical Rate', fontsize=16)
        ax2 = fig6.add_subplot(1, 1, 1)
        ax2.plot(A_time, A_vel_z, label = A_icao+ " - Vertical rate", color = 'blue')
        ax2.set_title("Vertical rate")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Vertical rate [m/s]")
        ax2.legend(facecolor='white')

        latMin = min(A_Ini_Man_Lat, A_End_Man_Lat, A_Conflict_Lat,B_Conflict_Lat)
        latMax = max(A_Ini_Man_Lat, A_End_Man_Lat, A_Conflict_Lat,B_Conflict_Lat)
        lonMin = min(A_Ini_Man_Lon, A_End_Man_Lon, A_Conflict_Lon,B_Conflict_Lon)
        lonMax = max(A_Ini_Man_Lon, A_End_Man_Lon, A_Conflict_Lon,B_Conflict_Lon)

        # Third figure Plot 3D (x,y,z)
        fig7 = plt.figure(figsize=plt.figaspect(0.5))
        fig7.suptitle('Conflict - 3D', fontsize=16)
        #ax1 = fig7.add_subplot(1, 1, 1, projection='3d')
        #ax1 = fig12.add_subplot(1, 1, 1)
        ax1 = Axes3D(fig7, azim=30, elev=30)
        ax1.plot3D(A_lon, A_lat, A_alt, label = A_icao, color = 'blue')
        ax1.plot3D(B_lon, B_lat, B_alt, label = B_icao, color = 'red')
        ax1.scatter3D(A_Ini_Man_Lon, A_Ini_Man_Lat, A_Ini_Man_Alt, s=30, label = A_icao+ '- Maneuver begin', color ='green')
        ax1.scatter3D(A_End_Man_Lon, A_End_Man_Lat, A_End_Man_Alt, s=30, label = A_icao+ '- Maneuver end', color ='purple')
        ax1.scatter3D(A_Conflict_Lon, A_Conflict_Lat, A_Conflict_Alt, s=30, label = A_icao+ '- Predict Conflict', color ='brown')
        ax1.scatter3D(B_Conflict_Lon, B_Conflict_Lat, B_Conflict_Alt, s=30, label = B_icao+ '- Predict Conflict', color ='black')
        self.plot_3D_cylinder(ax1, 0.083, self.search.DISTANCE_Z*2, elevation = B_Conflict_Alt-self.search.DISTANCE_Z, 
                              resolution=100, color='b', x_center = B_Conflict_Lon, y_center = B_Conflict_Lat)

        ax1.set_title("Conflict (Lon, Lat, Alt)")
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.set_zlabel("Baro altitude")
        ax1.legend(facecolor='white')
        
        # Third figure Plot 3D (x,y,z)
        fig8 = plt.figure(figsize=plt.figaspect(0.5))
        fig8.suptitle('Conflict - 3D', fontsize=16)
        #ax1 = fig7.add_subplot(1, 1, 1, projection='3d')
        #ax1 = fig12.add_subplot(1, 1, 1)
        ax1 = Axes3D(fig8, azim=30, elev=30)
        ax1.plot3D(A_lon, A_lat, A_alt, label = A_icao, color = 'blue')
        ax1.plot3D(B_lon, B_lat, B_alt, label = B_icao, color = 'red')
        ax1.scatter3D(A_Ini_Man_Lon, A_Ini_Man_Lat, A_Ini_Man_Alt, s=30, label = A_icao+ '- Maneuver begin', color ='green')
        ax1.scatter3D(A_End_Man_Lon, A_End_Man_Lat, A_End_Man_Alt, s=30, label = A_icao+ '- Maneuver end', color ='purple')
        ax1.scatter3D(A_Conflict_Lon, A_Conflict_Lat, A_Conflict_Alt, s=30, label = A_icao+ '- Predict Conflict', color ='brown')
        ax1.scatter3D(B_Conflict_Lon, B_Conflict_Lat, B_Conflict_Alt, s=30, label = B_icao+ '- Predict Conflict', color ='black')
        ax1.set_xlim([lonMin, lonMax])
        ax1.set_ylim([latMin, latMax])
        self.plot_3D_cylinder(ax1, 0.083, self.search.DISTANCE_Z*2, elevation = B_Conflict_Alt-self.search.DISTANCE_Z, 
                              resolution=100, color='b', x_center = B_Conflict_Lon, y_center = B_Conflict_Lat)
        ax1.set_title("Conflict (Lon, Lat, Alt)")
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.set_zlabel("Baro altitude")
        ax1.legend(facecolor='white')

        fig9 = plt.figure(figsize=plt.figaspect(0.5))
        fig9.suptitle('Conflict - 2D', fontsize=16)
        ax2 = fig9.add_subplot(1, 1, 1)
        ax2.plot(A_lon, A_lat, label = A_icao, color = 'blue')
        ax2.plot(B_lon, B_lat, label = B_icao, color = 'red')
        ax2.scatter(A_Ini_Man_Lon, A_Ini_Man_Lat, s=30, label = A_icao+ '- Maneuver begin', color ='green')
        ax2.scatter(A_End_Man_Lon, A_End_Man_Lat, s=30, label = A_icao+ '- Maneuver end', color ='purple')
        ax2.scatter(A_Conflict_Lon, A_Conflict_Lat, s=30, label = A_icao+ '- Point of Predict Conflict', color ='brown')
        ax2.scatter(B_Conflict_Lon, B_Conflict_Lat, s=30, label = B_icao+ '- Point of Predict Conflict', color ='black')
        circle1 = plt.Circle((B_Conflict_Lon, B_Conflict_Lat),  0.083, color='b', alpha=0.5)
        ax2.add_patch(circle1)
        ax2.set_xlim([lonMin, lonMax])
        ax2.set_ylim([latMin, latMax])
        ax2.set_title("Trajectory (Lon, Lat)")
        ax2.set_xlabel("Longitude")
        ax2.set_ylabel("Latitude")
        ax2.legend(facecolor='white')

        fig10 = plt.figure(figsize=plt.figaspect(0.5))
        fig10.suptitle('Conflict - 2D', fontsize=16)
        ax2 = fig10.add_subplot(1, 1, 1)
        ax2.plot(A_lon, A_lat, label = A_icao, color = 'blue')
        ax2.plot(B_lon, B_lat, label = B_icao, color = 'red')
        ax2.scatter(A_Ini_Man_Lon, A_Ini_Man_Lat, s=30, label = A_icao+ '- Maneuver begin', color ='green')
        ax2.scatter(A_End_Man_Lon, A_End_Man_Lat, s=30, label = A_icao+ '- Maneuver end', color ='purple')
        ax2.scatter(A_Conflict_Lon, A_Conflict_Lat, s=30, label = A_icao+ '- Point of Predict Conflict', color ='brown')
        ax2.scatter(B_Conflict_Lon, B_Conflict_Lat, s=30, label = B_icao+ '- Point of Predict Conflict', color ='black')
        circle1 = plt.Circle((B_Conflict_Lon, B_Conflict_Lat),  0.083, color='b', alpha=0.5)
        ax2.add_patch(circle1)
        ax2.set_title("Trajectory (Lon, Lat)")
        ax2.set_xlabel("Longitude")
        ax2.set_ylabel("Latitude")
        ax2.legend(facecolor='white')

        # Second figure Plot Speed
        fig11 = plt.figure(figsize=plt.figaspect(0.5))
        fig11.suptitle('Speed  - Conflict', fontsize=16)
        ax1 = fig11.add_subplot(1, 1, 1)
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        ax1.plot(A_time, A_vel_xy, label = A_icao+ " - Ground speed", color = 'blue')
        # ax1.plot(B_time.values.astype("float64"), B_vel_xy, label = A_icao+ " - Ground speed", color = 'red')
        ax1.scatter(A_Ini_Man_Time, A_vel_xy[datetime.strptime(row['Aircraft A Ini Man Time'], '%Y-%m-%d %H:%M:%S')],  s=30, label = A_icao+ '- Maneuver begin', color ='green')
        ax1.scatter(A_End_Man_Time, A_vel_xy[datetime.strptime(row['Aircraft A End Man Time'], '%Y-%m-%d %H:%M:%S')],  s=30, label = A_icao+ '- Maneuver end', color ='purple')
        # ax1.scatter(A_Conflict_Time, A_Conflict_VelXY,  s=30, label = A_icao+ '- Predict Conflict', color ='brown')
        # ax1.scatter(B_Conflict_Time, B_Conflict_VelXY,  s=30, label = B_icao+ '- Predict Conflict', color ='black')
        ax1.set_title("Ground Speed ")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Ground Speed [m/s]")
        ax1.legend(facecolor='white')

        fig12 = plt.figure(figsize=plt.figaspect(0.5))
        fig12.suptitle('Vertical Rate - Conflict', fontsize=16)
        ax1 = fig12.add_subplot(1, 1, 1)
        print(A_time)
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        ax1.plot(A_time, A_vel_z, label = A_icao+ " - Vertical rate", color = 'blue')
        # ax1.plot(B_time.values.astype("float64"), B_vel_z, label = A_icao+ " - Vertical rate", color = 'red')
        ax1.scatter(A_Ini_Man_Time, A_vel_z[datetime.strptime(row['Aircraft A Ini Man Time'], '%Y-%m-%d %H:%M:%S')],  s=30, label = A_icao+ '- Maneuver begin', color ='green')
        ax1.scatter(A_End_Man_Time, A_vel_z[datetime.strptime(row['Aircraft A End Man Time'], '%Y-%m-%d %H:%M:%S')],  s=30, label = A_icao+ '- Maneuver end', color ='purple')
        # ax1.scatter(A_Conflict_Time, A_Conflict_VelZ,  s=30, label = A_icao+ '- Predict Conflict', color ='brown')
        # ax1.scatter(B_Conflict_Time, B_Conflict_VelZ,  s=30, label = B_icao+ '- Predict Conflict', color ='black')
        ax1.set_title("Vertical rate")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Vertical rate [m/s]")
        ax1.legend(facecolor='white')

        print("Aircraft A: ", A_icao, "\tAircraft B:", B_icao)
        print("SpeedManeuver: ", SpeedManeuver)
        print("AltManeuver: ", AltManeuver)
        print("TrackManeuver: ", TrackManeuver)

        plt.legend()

        plt.show()


    def plot_icao_traj(self, data, icao, conflicts = None, pred_traj = None):
         #Plot trajectory
        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax1 = fig.add_subplot(1, 1, 1, projection='3d')
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.set_zlabel("Baro altitude")
        if isinstance(data[icao]['cruise'], list):
            lon = data[icao]['cruise']['lon']
            lat = data[icao]['cruise']['lat']
            alt = data[icao]['cruise']['alt']
        elif isinstance(data[icao]['cruise'], pd.DataFrame):
            lon = data[icao]['cruise'].loc[:,"lon"]
            lat = data[icao]['cruise'].loc[:,"lat"]
            alt = data[icao]['cruise'].loc[:,"alt"]

        ax1.plot3D(lon, lat, alt, label = icao)
        ax1.scatter3D(lon, lat, alt, s=5,  label = icao, color ='blue')
        ax1.scatter3D(lon[0], lat[0], alt[0], s=30, label = 'origin', color ='green')
        if conflicts != None and conflicts[icao]['conflict'] == True:
            # for conflict in conflicts[icao]['man_track']:
            #     indice = conflict[0]
            #     ax1.scatter3D(lon[indice], lat[indice], alt[indice], s=30, label = 'A', color ='red')
            #     indice = conflict[1]
            #     ax1.scatter3D(lon[indice], lat[indice], alt[indice], s=30, label = 'B', color ='black')
            #     indice = conflict[2]
            #     ax1.scatter3D(lon[indice], lat[indice], alt[indice], s=30, label = 'C', color ='green')
            for conflict in  conflicts[icao]['man_alt'] + conflicts[icao]['man_track'] + conflicts[icao]['man_speed']:
                indice = conflict[0]
                ax1.scatter3D(lon[indice], lat[indice], alt[indice], s=30, label = 'conflict', color ='red')
                indice = conflict[1]
                ax1.scatter3D(lon[indice], lat[indice], alt[indice], s=30, label = 'conflict', color ='black')

        if pred_traj != None:
            ax1.plot3D(pred_traj[3], pred_traj[2], pred_traj[1], label = icao, color = 'green')
            ax1.scatter3D(pred_traj[3], pred_traj[2], pred_traj[1], s=5,  label = icao, color ='green')
            ax1.scatter3D(pred_traj[3][0], pred_traj[2][0], pred_traj[1][0], s=30, label = 'origin', color ='green')
            ax1.scatter3D(pred_traj[3][len(pred_traj[0])-1], pred_traj[2][len(pred_traj[0])-1], pred_traj[1][len(pred_traj[0])-1], s=30, label = 'end', color ='green')

        plt.legend()

        plt.show()


    def plot_comp_samples(self, data_vector, data_time_serie, icao):
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax1 = fig.add_subplot(1, 1, 1, projection='3d')
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.set_zlabel("Baro altitude")
        ax1.plot3D(data_vector[icao]['lon'], data_vector[icao]['lat'], data_vector[icao]['alt'], label = icao + ' real', color ='blue')
        #ax1.scatter3D(data_vector[icao]['lon'], data_vector[icao]['lat'], data_vector[icao]['alt'], s=5,  label = icao, color ='blue')
        if len(data_time_serie[icao].loc[:,"lon"]) > 0:
            ax1.scatter3D(data_vector[icao]['lon'][0], data_vector[icao]['lat'][0], data_vector[icao]['alt'][0], s=30, label = 'origin real', color ='green')
        ax1.plot3D(data_time_serie[icao].loc[:,"lon"], data_time_serie[icao].loc[:,"lat"], data_time_serie[icao].loc[:,"alt"], label = icao + ' interpolated', color ='red')
        if len(data_time_serie[icao].loc[:,"lon"]) > 0:
            ax1.scatter3D(data_time_serie[icao].loc[:,"lon"][0], data_time_serie[icao].loc[:,"lat"][0], data_time_serie[icao].loc[:,"alt"][0], s=30, label = 'origin interpolated', color ='black')
        
        plt.legend()

        plt.show()


    def plot_compare(self, data, icao):
        data_separate = data[icao]['separate']
        data_all = data[icao]['all']        
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax1 = fig.add_subplot(1, 1, 1, projection='3d')
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.set_zlabel("Baro altitude")
        
        ax1.plot3D(data_all.loc[:,"lon"], data_all.loc[:,"lat"], data_all.loc[:,"alt"], label = icao + ' complete data', color ='red')
        if len(data_separate.loc[:,"lon"]) > 0:
            ax1.scatter3D(data_all.loc[:,"lon"][180], data_all.loc[:,"lat"][180], data_all.loc[:,"alt"][180], s=30, label = 'complete data', color ='black')
            print(icao, data_all.loc[:,"alt"][180], data_all["alt"][180])
        
        ax1.plot3D(data_separate.loc[:,"lon"], data_separate.loc[:,"lat"], data_separate.loc[:,"alt"], label = icao + ' separate data', color ='green')
        if len(data_separate.loc[:,"lon"]) > 0:
            ax1.scatter3D(data_separate.loc[:,"lon"][0], data_separate.loc[:,"lat"][0], data_separate.loc[:,"alt"][0], s=30, label = 'separate data', color ='green')
        
        print("------------------------------------------------------------------------------")
        plt.legend()

        plt.show()
        

    def plot_comp_all_cruise(self, data, icao):
        data_cruise = data[icao]['cruise']
        data_filter = data[icao]['filter']
        data_separate = data[icao]['separate']
        data_all = data[icao]['all']
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax1 = fig.add_subplot(1, 1, 1, projection='3d')
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.set_zlabel("Baro altitude")
        
        ax1.plot3D(data_all.loc[:,"lon"], data_all.loc[:,"lat"], data_all.loc[:,"alt"], label = icao + ' complete data', color ='red')
        if len(data_all.loc[:,"lon"]) > 0:
            ax1.scatter3D(data_all.loc[:,"lon"][0], data_all.loc[:,"lat"][0], data_all.loc[:,"alt"][0], s=30, label = 'complete data', color ='black')
        
        ax1.plot3D(data_separate.loc[:,"lon"], data_separate.loc[:,"lat"], data_separate.loc[:,"alt"], label = icao + ' separate data', color ='green')
        if len(data_separate.loc[:,"lon"]) > 0:
            ax1.scatter3D(data_separate.loc[:,"lon"][0], data_separate.loc[:,"lat"][0], data_separate.loc[:,"alt"][0], s=30, label = 'separate data', color ='green')
        
        ax1.plot3D(data_filter.loc[:,"lon"], data_filter.loc[:,"lat"], data_filter.loc[:,"alt"], label = icao + ' filter data', color ='purple')
        if len(data_filter.loc[:,"lon"]) > 0:
            ax1.scatter3D(data_filter.loc[:,"lon"][0], data_filter.loc[:,"lat"][0], data_filter.loc[:,"alt"][0], s=30, label = 'filter data', color ='green')
        
        ax1.plot3D(data_cruise.loc[:,"lon"], data_cruise.loc[:,"lat"], data_cruise.loc[:,"alt"], label = icao + ' cruise data', color ='blue')
        if len(data_cruise.loc[:,"lon"]) > 0:
            ax1.scatter3D(data_cruise.loc[:,"lon"][0], data_cruise.loc[:,"lat"][0], data_cruise.loc[:,"alt"][0], s=30, label = 'cruise data', color ='green')
        
        plt.legend()

        plt.show()


    def plot_comp_all_speed(self, data, icao, conflicts = None):
        print(icao)
        data_all = data[icao]['cruise']
        
        # Ground Speed and Mach
        fig = plt.figure(figsize=plt.figaspect(0.5))
        # Ground Speed
        #ax1 = fig.add_subplot(2, 1, 1)
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Ground Speed [m/s]")

        removed_outliers = data_all[data_all.loc[:,"vel_xy"]<375]
        
        ax1.plot(data_all.index, data_all.loc[:,"vel_xy"], label = icao + ' ground speed', color ='red')
        ax1.scatter(data_all.index, data_all.loc[:,"vel_xy"], s=5, label = icao + ' ground speed', color ='red')

        #ax1.plot(removed_outliers.index, removed_outliers.loc[:,"vel_xy"], label = icao + ' removed outliers', color ='blue')
        if len(data_all.loc[:,"vel_xy"]) > 2:
            ax1.axhline(y=float(statistics.mean(data_all.loc[:,"vel_xy"])), color ='blue')
            print(mean(data_all.loc[:,"vel_xy"]), stdev(data_all.loc[:,"vel_xy"]))

        
        if conflicts != None and conflicts[icao]['conflict'] == True:
            for conflict in  conflicts[icao]['man_speed']:
                indice = conflict[0]
                ax1.scatter(data_all.index[indice], data_all.loc[:,"vel_xy"][indice], s=30, label = 'conflict', color ='blue')
                indice = conflict[1]
                ax1.scatter(data_all.index[indice], data_all.loc[:,"vel_xy"][indice], s=30, label = 'conflict', color ='black')

        # ax2 = fig.add_subplot(2, 1, 2)
        # ax2.set_xlabel("Time")
        # ax2.set_ylabel("Mach")
        # ax2.plot(data_all.index, data_all.loc[:,"mach"], label = icao + ' mach', color ='red')
        # ax2.axhline(y=float(statistics.mean(data_all.loc[:,"mach"])))

        # if len(data_all.index) > 0:
        #     ax1.scatter(data_all.index, data_all.loc[:,"vel_xy"],  label = 'ground speed', color ='red')
        #     ax1.scatter(removed_outliers.index, removed_outliers.loc[:,"vel_xy"], label = 'removed outliers', color ='blue')
        #     ax2.scatter(data_all.index, data_all.loc[:,"mach"],  label = 'mach', color ='red')

        # ######### Vtas and Vtas_kts #############
        # fig2 = plt.figure(figsize=plt.figaspect(0.5))

        # # Vtas [m/s]
        # ax1 = fig2.add_subplot(2, 1, 1)
        # ax1.set_xlabel("Time")
        # ax1.set_ylabel("Vtas [m/s]")
        
        # ax1.plot(data_all.index, data_all.loc[:,"Vtas"], label = icao + ' Vtas', color ='red')
        # ax1.axhline(y=float(statistics.mean(data_all.loc[:,"Vtas"])))
        # print(mean(data_all.loc[:,"Vtas"]), stdev(data_all.loc[:,"Vtas"]))

        # # Vtas [kts]
        # ax2 = fig2.add_subplot(2, 1, 2)
        # ax2.set_xlabel("Time")
        # ax2.set_ylabel("Vtas [knots]")
        # ax2.plot(data_all.index, data_all.loc[:,"Vtas_kts"], label = icao + ' Vtas_kts', color ='red')
        # ax2.axhline(y=float(statistics.mean(data_all.loc[:,"Vtas_kts"])))

        # if len(data_all.index) > 0:
        #     ax1.scatter(data_all.index, data_all.loc[:,"Vtas"],  label = 'Vtas', color ='red')
        #     ax2.scatter(data_all.index, data_all.loc[:,"Vtas_kts"],  label = 'Vtas_kts', color ='red')
        
        # ##### Veas and Veas_kts ######
        # fig3 = plt.figure(figsize=plt.figaspect(0.5))

        # # Veas [m/s]
        # ax1 = fig3.add_subplot(2, 1, 1)
        # ax1.set_xlabel("Time")
        # ax1.set_ylabel("Veas [m/s]")
        
        # ax1.plot(data_all.index, data_all.loc[:,"Veas"], label = icao + ' Veas', color ='red')
        # ax1.axhline(y=float(statistics.mean(data_all.loc[:,"Veas"])))
        # print(mean(data_all.loc[:,"Veas"]), stdev(data_all.loc[:,"Veas"]))

        # # Veas [kts]
        # ax2 = fig3.add_subplot(2, 1, 2)
        # ax2.set_xlabel("Time")
        # ax2.set_ylabel("Veas [knots]")
        # ax2.plot(data_all.index, data_all.loc[:,"Veas_kts"], label = icao + ' Veas_kts', color ='red')
        # ax2.axhline(y=float(statistics.mean(data_all.loc[:,"Veas_kts"])))

        # if len(data_all.index) > 0:
        #     ax1.scatter(data_all.index, data_all.loc[:,"Veas"],  label = 'Veas', color ='red')
        #     ax2.scatter(data_all.index, data_all.loc[:,"Veas_kts"],  label = 'Veas_kts', color ='red')

        # ##### Vcas and Vcas_kts ######
        # fig4 = plt.figure(figsize=plt.figaspect(0.5))

        # # Vcas [m/s]
        # ax1 = fig4.add_subplot(2, 1, 1)
        # ax1.set_xlabel("Vcas")
        # ax1.set_ylabel("Vcas [m/s]")
        
        # ax1.plot(data_all.index, data_all.loc[:,"Vcas"], label = icao + ' Vcas', color ='red')
        # ax1.axhline(y=float(statistics.mean(data_all.loc[:,"Vcas"])))
        # print(mean(data_all.loc[:,"Vcas"]), stdev(data_all.loc[:,"Vcas"]))

        # # Vcas [kts]
        # ax2 = fig4.add_subplot(2, 1, 2)
        # ax2.set_xlabel("Time")
        # ax2.set_ylabel("Vcas [knots]")
        # ax2.plot(data_all.index, data_all.loc[:,"Vcas_kts"], label = icao + ' Vcas_kts', color ='red')
        # ax2.axhline(y=float(statistics.mean(data_all.loc[:,"Vcas_kts"])))

        # if len(data_all.index) > 0:
        #     ax1.scatter(data_all.index, data_all.loc[:,"Vcas"],  label = 'Vcas', color ='red')
        #     ax2.scatter(data_all.index, data_all.loc[:,"Vcas_kts"],  label = 'Vcas_kts', color ='red')
        # #sns.boxplot(data_all.loc[:,"vel_xy"])

        plt.legend()
        plt.show()



    def plot_icao_list(self, data, icao, icao_list):
        data_cruise = data[icao]['cruise']
        data_all = data[icao]['all']
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax1 = fig.add_subplot(1, 1, 1, projection='3d')
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.set_zlabel("Baro altitude")
        
        ax1.plot3D(data_all.loc[:,"lon"], data_all.loc[:,"lat"], data_all.loc[:,"alt"], label = icao, color ='red')
        if len(data_all.loc[:,"lon"]) > 0:
            ax1.scatter3D(data_all.loc[:,"lon"][0], data_all.loc[:,"lat"][0], data_all.loc[:,"alt"][0], s=30, label = icao +' P0', color ='black')
              
        for icao in icao_list:
            data_all = data[icao]['all']
            ax1.plot3D(data_all.loc[:,"lon"], data_all.loc[:,"lat"], data_all.loc[:,"alt"], label = icao)
            if len(data_all.loc[:,"lon"]) > 0:
                ax1.scatter3D(data_all.loc[:,"lon"][0], data_all.loc[:,"lat"][0], data_all.loc[:,"alt"][0], s=30, label = icao +' P0', color ='black')

        plt.legend()
        plt.show()
    

    def data_for_cylinder_along_z(self, center_x, center_y, radius, height_z):
        z = np.linspace(0, height_z, 50)
        theta = np.linspace(0, 2*np.pi, 50)
        theta_grid, z_grid=np.meshgrid(theta, z)
        x_grid = radius*np.cos(theta_grid) + center_x
        y_grid = radius*np.sin(theta_grid) + center_y
        return x_grid,y_grid,z_grid
    

    def plot_data_4_axes(self, data, icao, icao_list, conflicts):
        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_time = data[icao]['cruise'].index[conflict[0]] - datetime.timedelta(minutes=5)
            B_time = data[icao]['cruise'].index[conflict[1]] + datetime.timedelta(minutes=5)
            A_lat = min(data[icao]['cruise'].lat[conflict[0]:conflict[1]])-0.4
            B_lat = max(data[icao]['cruise'].lat[conflict[0]:conflict[1]])+0.4
            A_lon = min(data[icao]['cruise'].lon[conflict[0]:conflict[1]])-0.4
            B_lon = max(data[icao]['cruise'].lon[conflict[0]:conflict[1]])+0.4
            A_alt = 8000
            B_alt = 12000
            #A_alt = min(data[icao]['cruise'].alt[conflict[0]-2:conflict[1]])-1000
            #_alt = max(data[icao]['cruise'].alt[conflict[0]-2:conflict[1]])+1000
            conflict_lat = data[icao]['cruise'].lat[conflict[0]]
            conflict_lon = data[icao]['cruise'].lon[conflict[0]]
            conflict_alt = data[icao]['cruise'].alt[conflict[0]]
        

        data_all = data[icao]['all']
        lon_min = min(data_all.loc[:,"lon"])-1
        lon_max = max(data_all.loc[:,"lon"])+1
        lat_min = min(data_all.loc[:,"lat"])-1
        lat_max = max(data_all.loc[:,"lat"])+1
        alt_min = min(data_all.loc[:,"alt"])-100
        alt_max = max(data_all.loc[:,"alt"])+100

        time_min = min(data_all.index) - datetime.timedelta(minutes=5)
        time_max = max(data_all.index) + datetime.timedelta(minutes=5)
        
        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1, projection='3d')
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.set_zlabel("Baro altitude")
        ax1.set_xlim([lon_min, lon_max])
        ax1.set_ylim([lat_min, lat_max])
        ax1.set_zlim([alt_min, alt_max])
        
        
        ax1.plot3D(data_all.loc[:,"lon"], data_all.loc[:,"lat"], data_all.loc[:,"alt"], label = icao, color ='red')
        ax1.scatter3D(data_all.loc[:,"lon"], data_all.loc[:,"lat"], data_all.loc[:,"alt"], s=5, label = icao, color ='red')
        if len(data_all.loc[:,"lon"]) > 0:
            ax1.scatter3D(data_all.loc[:,"lon"][0], data_all.loc[:,"lat"][0], data_all.loc[:,"alt"][0], s=30, label = icao +' P0', color ='black')
        
        # set up a figure twice as wide as it is tall
        fig2 = plt.figure(figsize=plt.figaspect(0.5))
        
        ax2 = fig2.add_subplot(3, 1, 1)
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Latitude")
        ax2.set_xlim([A_time, B_time])
        ax2.set_ylim([A_lat, B_lat])
        ax2.plot(data_all.index, data_all.loc[:,"lat"], label = icao, color ='red')
        ax2.scatter(data_all.index, data_all.loc[:,"lat"], label = icao, color ='red')
        #ax2.scatter(data_all.index[0], data_all.loc[:,"lat"][0], s=30, label = icao +' P0', color ='black')
        ax2.axvline(x = data[icao]['cruise'].index[conflict[0]], color = 'black', label = 'Conflict begin')
        ax2.axvline(x = data[icao]['cruise'].index[conflict[1]], color = 'black', label = 'Conflict end')
        ax2.axhline(y = data[icao]['cruise'].lat[conflict[0]] + 0.083, color = 'black', label = 'Lim above')
        ax2.axhline(y = data[icao]['cruise'].lat[conflict[0]] - 0.083, color = 'black', label = 'Lim bellow')

        ax3 = fig2.add_subplot(3, 1, 2)
        ax3.set_xlabel("Time")
        ax3.set_ylabel("Baro altitude")
        ax3.set_xlim([A_time, B_time])
        ax3.set_ylim([A_alt, B_alt])
        ax3.plot(data_all.index, data_all.loc[:,"alt"], label = icao, color ='red')
        ax3.scatter(data_all.index, data_all.loc[:,"alt"], label = icao, color ='red')
        #ax3.scatter(data_all.index[0], data_all.loc[:,"alt"][0], s=30, label = icao +' P0', color ='black')
        ax3.axvline(x = data[icao]['cruise'].index[conflict[0]], color = 'black', label = 'Conflict begin')
        ax3.axvline(x = data[icao]['cruise'].index[conflict[1]], color = 'black', label = 'Conflict end')

        ax3.axhline(y = data[icao]['cruise'].alt[conflict[0]] + 1000, color = 'black', label = 'Lim above')
        ax3.axhline(y = data[icao]['cruise'].alt[conflict[0]] - 1000, color = 'black', label = 'Lim bellow')

        ax4 = fig2.add_subplot(3, 1, 3)
        ax4.set_xlabel("Time")
        ax4.set_ylabel("Longitude")
        ax4.set_xlim([A_time, B_time])
        ax4.set_ylim([A_lon, B_lon])
        ax4.plot(data_all.index, data_all.loc[:,"lon"], label = icao, color ='red')
        ax4.scatter(data_all.index ,data_all.loc[:,"lon"], label = icao, color ='red')
        #ax4.scatter(data_all.index[0], data_all.loc[:,"lon"][0], s=30, label = icao +' P0', color ='black')
        ax4.axvline(x = data[icao]['cruise'].index[conflict[0]], color = 'black', label = 'Conflict begin')
        ax4.axvline(x = data[icao]['cruise'].index[conflict[1]], color = 'black', label = 'Conflict end')

        ax4.axhline(y = data[icao]['cruise'].lon[conflict[0]] + 0.083, color = 'black', label = 'Lim above')
        ax4.axhline(y = data[icao]['cruise'].lon[conflict[0]] - 0.083, color = 'black', label = 'Lim bellow')

        for icao in icao_list:
            data_all = data[icao]['all']
            
            ax1.plot3D(data_all.loc[:,"lon"], data_all.loc[:,"lat"], data_all.loc[:,"alt"], label = icao)
            ax1.scatter3D(data_all.loc[:,"lon"], data_all.loc[:,"lat"], data_all.loc[:,"alt"], s=5, label = icao)
            if len(data_all.loc[:,"lon"]) > 0:
                ax1.scatter3D(data_all.loc[:,"lon"][0], data_all.loc[:,"lat"][0], data_all.loc[:,"alt"][0], s=30, label = icao +' P0', color ='black')

            ax2.plot(data_all.index, data_all.loc[:,"lat"], label = icao)
            ax2.scatter(data_all.index, data_all.loc[:,"lat"], label = icao)
            if len(data_all.loc[:,"lon"]) > 0:
                ax2.scatter(data_all.index[0], data_all.loc[:,"lat"][0], s=30, label = icao +' P0', color ='black')

            ax3.plot(data_all.index, data_all.loc[:,"alt"], label = icao)
            ax3.scatter(data_all.index, data_all.loc[:,"alt"], label = icao)
            if len(data_all.loc[:,"lon"]) > 0:
                ax3.scatter(data_all.index[0], data_all.loc[:,"alt"][0], s=30, label = icao +' P0', color ='black')

            ax4.plot(data_all.index, data_all.loc[:,"lon"], label = icao)
            ax4.scatter(data_all.index ,data_all.loc[:,"lon"], label = icao)
            if len(data_all.loc[:,"lon"]) > 0:
                ax4.scatter(data_all.index[0], data_all.loc[:,"lon"][0], s=30, label = icao +' P0', color ='black')

        fig.legend()
        plt.legend()

        plt.grid()
        ax2.grid()
        ax3.grid()
        ax4.grid()


        # set up a figure twice as wide as it is tall
        #fig = plt.figure(figsize=plt.figaspect(0.5))

        #ax1 = fig.add_subplot(1, 1, 1, projection='3d')

        Xc,Yc,Zc = self.data_for_cylinder_along_z(conflict_lat,
                                                  conflict_lon,
                                                  0.083,
                                                  conflict_alt+1000)
        #print(Xc,Yc,Zc)

        #ax1.plot_surface(Xc, Yc, Zc, alpha=0.3)

        plt.show()

    def plot_3D_cylinder(self, ax, radius, height, elevation=0, resolution=100, color='b', x_center = 0, y_center = 0):
       

        x = np.linspace(x_center-radius, x_center+radius, resolution)
        z = np.linspace(elevation, elevation+height, resolution)
        X, Z = np.meshgrid(x, z)

        Y = np.sqrt(radius**2 - (X - x_center)**2) + y_center # Pythagorean theorem

        ax.plot_surface(X, Y, Z, color=color, alpha=0.5)
        ax.plot_surface(X, (2*y_center-Y), Z, color=color, alpha=0.5)

        floor = Circle((x_center, y_center), radius, color=color)
        ax.add_patch(floor)
        art3d.pathpatch_2d_to_3d(floor, z=elevation, zdir="z")

        ceiling = Circle((x_center, y_center), radius, color=color)
        ax.add_patch(ceiling)
        art3d.pathpatch_2d_to_3d(ceiling, z=elevation+height, zdir="z")

        return ax
    