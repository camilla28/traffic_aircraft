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
import plotly.express as px

class Plot:

    # Entry the data
    def __init__(self, data):
        self.__data = data
        self.search = Search_Tree(None, None)

    
    '''
        Função que plota apenas as trajetórias
    '''
    def plot_track(self, icao):
        self.plot_lon_lat_alt(icao)
        self.plot_lon_lat(icao)
        self.plot_lon_alt(icao)
        self.plot_lat_alt(icao)
        self.plot_time_lat(icao)
        self.plot_time_lon(icao)
        self.plot_time_alt(icao)
        self.plot_time_speed(icao)


    '''
        Função que plota as trajetórias com conflitos
    '''
    def plot_track_conf(self, icao, conflicts):
        self.plot_lon_lat_alt_conf(icao, conflicts)
        self.plot_lon_lat_conf(icao, conflicts)
        self.plot_lon_alt_conf(icao, conflicts)
        self.plot_lat_alt_conf(icao, conflicts)
        self.plot_time_lat_conf(icao, conflicts)
        self.plot_time_lon_conf(icao, conflicts)
        self.plot_time_alt_conf(icao, conflicts)
        self.plot_time_speed_conf(icao, conflicts)


    '''
        Função que plota as trajetórias com conflitos e trajetórias previstas
    '''
    def plot_track_conf_pred(self, icao, conflicts, track_preds):
        self.plot_lon_lat_alt_conf_pred(icao, conflicts, track_preds)
        self.plot_lon_lat_conf_pred(icao, conflicts, track_preds)
        self.plot_lon_alt_conf_pred(icao, conflicts, track_preds)
        self.plot_lat_alt_conf_pred(icao, conflicts, track_preds)
        self.plot_time_lat_conf_pred(icao, conflicts, track_preds)
        self.plot_time_lon_conf_pred(icao, conflicts, track_preds)
        self.plot_time_alt_conf_pred(icao, conflicts, track_preds)


    def plot_track_conf_pred_B_icao(self, icao, conflicts, track_preds, second_filters):
        self.plot_time_lat_conf_pred_B_icao(icao, conflicts, track_preds, second_filters)
        self.plot_time_lon_conf_pred_B_icao(icao, conflicts, track_preds, second_filters)
        self.plot_time_alt_conf_pred_B_icao(icao, conflicts, track_preds, second_filters)
       
    '''
        Função para plotar apenas a trajetória em longitude, latitude e altitude
    '''
    def plot_lon_lat_alt(self, icao):

        # Track data
        lon = self.__data[icao]['all']['lon']
        lat = self.__data[icao]['all']['lat']
        alt = self.__data[icao]['all']['alt']

        # set up a figure twice as wide as it is tall
        # plt.style.use("tableau-colorblind10")
        plt.style.use("seaborn-deep")

        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1, projection='3d')

        #Set title
        fig.suptitle('Trajectory of '+ icao, fontsize=16)

        # Set Label Name
        ax1.set_xlabel("Longitude [°]" , fontsize = 12)
        ax1.set_ylabel("Latitude [°]" , fontsize = 12)
        ax1.set_zlabel("Baro altitude [m]" , fontsize = 12)
        
        # Plot
        ax1.plot3D(lon, lat, alt, color='blue', label = icao + " track")
        # ax1.scatter3D(lon, lat, alt, color='blue', label = icao + " track")
        ax1.scatter3D(lon[0], lat[0], alt[0], s=50, label = icao + " track origin", color ='green')

        ax1.set_facecolor("white")
        ax1.legend(bbox_to_anchor=(1.1, 1.05), facecolor='white', fontsize = 12, framealpha=1)

        #plt.legend(bbox_to_anchor=(1.1, 1.05), facecolor='white', fontsize = 12, framealpha=1)
        
        plt.show()


    '''
        Função para plotar os conflitos na trajetória em longitude, latitude e altitude
    '''
    def plot_lon_lat_alt_conf(self, icao, conflicts):

        # Track data
        lon = self.__data[icao]['all']['lon']
        lat = self.__data[icao]['all']['lat']
        alt = self.__data[icao]['all']['alt']

        lon_cruise = self.__data[icao]['cruise']['lon']
        lat_cruise = self.__data[icao]['cruise']['lat']
        alt_cruise = self.__data[icao]['cruise']['alt']

        # set up a figure twice as wide as it is tall
        # plt.style.use("tableau-colorblind10")
        plt.style.use("seaborn-deep")

        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1, projection='3d')

        #Set title
        fig.suptitle('Maneuvers on the '+ icao + ' trajectory', fontsize=16)

        # Set Label Name
        ax1.set_xlabel("Longitude [°]" , fontsize = 12)
        ax1.set_ylabel("Latitude [°]" , fontsize = 12)
        ax1.set_zlabel("Baro altitude [m]" , fontsize = 12)
        
        # Plot
        ax1.plot3D(lon, lat, alt, color='blue', label = icao + " track")
        # ax1.scatter3D(lon, lat, alt, color='blue', label = icao + " track")
        ax1.scatter3D(lon[0], lat[0], alt[0], s=50, label = icao + " track origin", color ='green')

        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_lat = lat_cruise[conflict[0]]
            B_lat = lat_cruise[conflict[1]]
            A_lon = lon_cruise[conflict[0]]
            B_lon = lon_cruise[conflict[1]]
            A_alt = alt_cruise[conflict[0]]
            B_alt = alt_cruise[conflict[1]]

            ax1.scatter3D(A_lon, A_lat, A_alt, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter3D(B_lon, B_lat, B_alt, s=50, label = 'Meneuver end', color ='brown')

        ax1.set_facecolor("white")
        ax1.legend(bbox_to_anchor=(1.1, 1.05), facecolor='white', fontsize = 12, framealpha=1)

        #plt.legend(bbox_to_anchor=(1.1, 1.05), facecolor='white', fontsize = 12, framealpha=1)
        
        plt.show()


    '''
        Função para plotar os conflitos  e trajetórias previstas com trajetória em longitude, latitude e altitude
    '''
    def plot_lon_lat_alt_conf_pred(self, icao, conflicts, track_preds):

        # Track data
        lon = self.__data[icao]['all']['lon']
        lat = self.__data[icao]['all']['lat']
        alt = self.__data[icao]['all']['alt']

        lon_cruise = self.__data[icao]['cruise']['lon']
        lat_cruise = self.__data[icao]['cruise']['lat']
        alt_cruise = self.__data[icao]['cruise']['alt']

        # set up a figure twice as wide as it is tall
        # plt.style.use("tableau-colorblind10")
        plt.style.use("seaborn-deep")

        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1, projection='3d')

        #Set title
        fig.suptitle('Maneuvers and Trajectory Prediction on the '+ icao + ' trajectory', fontsize=16)

        # Set Label Name
        ax1.set_xlabel("Longitude [°]" , fontsize = 12)
        ax1.set_ylabel("Latitude [°]" , fontsize = 12)
        ax1.set_zlabel("Baro altitude [m]" , fontsize = 12)
        
        # Plot
        ax1.plot3D(lon, lat, alt, color='blue', label = icao + " track")
        # ax1.scatter3D(lon, lat, alt, color='blue', label = icao + " track")
        ax1.scatter3D(lon[0], lat[0], alt[0], s=50, label = icao + " track origin", color ='green')

        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_lat = lat_cruise[conflict[0]]
            B_lat = lat_cruise[conflict[1]]
            A_lon = lon_cruise[conflict[0]]
            B_lon = lon_cruise[conflict[1]]
            A_alt = alt_cruise[conflict[0]]
            B_alt = alt_cruise[conflict[1]]

            ax1.scatter3D(A_lon, A_lat, A_alt, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter3D(B_lon, B_lat, B_alt, s=50, label = 'Meneuver end', color ='brown')

        for track_pred in track_preds:
            pred_time = track_pred[0]
            pred_alt = track_pred[1]
            pred_lat = track_pred[2]
            pred_lon = track_pred[3]
            ax1.plot3D(pred_lon, pred_lat, pred_alt, color='blue', label = icao + " track prediction", linestyle = 'dashed')

        ax1.set_facecolor("white")
        ax1.legend(bbox_to_anchor=(1.1, 1.05), facecolor='white', fontsize = 12, framealpha=1)

        #plt.legend(bbox_to_anchor=(1.1, 1.05), facecolor='white', fontsize = 12, framealpha=1)
        
        plt.show()
 

    '''
        Função para plotar os conflitos  e trajetórias previstas com trajetória em longitude, latitude e altitude
    '''
    def plot_lon_lat_alt_conf_pred_area(self, icao, conflicts, track_preds):

        # Track data
        lon = self.__data[icao]['all']['lon']
        lat = self.__data[icao]['all']['lat']
        alt = self.__data[icao]['all']['alt']

        lon_cruise = self.__data[icao]['cruise']['lon']
        lat_cruise = self.__data[icao]['cruise']['lat']
        alt_cruise = self.__data[icao]['cruise']['alt']

        # set up a figure twice as wide as it is tall
        # plt.style.use("tableau-colorblind10")
        plt.style.use("seaborn-deep")

        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1, projection='3d')

        #Set title
        fig.suptitle('Maneuvers and Trajectory Prediction on the '+ icao + ' trajectory', fontsize=16)

        # Set Label Name
        ax1.set_xlabel("Longitude [°]" , fontsize = 12)
        ax1.set_ylabel("Latitude [°]" , fontsize = 12)
        ax1.set_zlabel("Baro altitude [m]" , fontsize = 12)
        
        # Plot
        ax1.plot3D(lon, lat, alt, color='blue', label = icao + " track")
        # ax1.scatter3D(lon, lat, alt, color='blue', label = icao + " track")
        ax1.scatter3D(lon[0], lat[0], alt[0], s=50, label = icao + " track origin", color ='green')

        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_lat = lat_cruise[conflict[0]]
            B_lat = lat_cruise[conflict[1]]
            A_lon = lon_cruise[conflict[0]]
            B_lon = lon_cruise[conflict[1]]
            A_alt = alt_cruise[conflict[0]]
            B_alt = alt_cruise[conflict[1]]

            ax1.scatter3D(A_lon, A_lat, A_alt, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter3D(B_lon, B_lat, B_alt, s=50, label = 'Meneuver end', color ='brown')

            # self.plot_area(ax1, conflict, lat_cruise, lon_cruise, alt_cruise)

        for track_pred in track_preds:
            pred_time = track_pred[0]
            pred_alt = track_pred[1]
            pred_lat = track_pred[2]
            pred_lon = track_pred[3]
            ax1.plot3D(pred_lon, pred_lat, pred_alt, color='blue', label = icao + " track prediction", linestyle = 'dashed')

            # for i in range(len(pred_alt)):
            #     self.plot_3D_cylinder(ax1, 0.083, self.search.DISTANCE_Z*2, elevation = pred_alt[i]-self.search.DISTANCE_Z, 
            #                   resolution=100, color='pink', x_center = pred_lon[i], y_center = pred_lat[i])
        
       
                    # ax2.axhline(min(pred_traj_lat)-0.083, color = 'limegreen', label = 'Lower limit', linestyle = 'dotted')

        ax1.set_facecolor("white")
        ax1.legend(bbox_to_anchor=(1.1, 1.05), facecolor='white', fontsize = 12, framealpha=1)

        #plt.legend(bbox_to_anchor=(1.1, 1.05), facecolor='white', fontsize = 12, framealpha=1)
        
        plt.show()


    def plot_area(self, ax1, conflict, lat_cruise, lon_cruise, alt_cruise):
        A_lat = lat_cruise[conflict[0]]
        B_lat = lat_cruise[conflict[1]]
        A_lon = lon_cruise[conflict[0]]
        B_lon = lon_cruise[conflict[1]]
        A_alt = alt_cruise[conflict[0]]
        B_alt = alt_cruise[conflict[1]]

        max_lat = max(B_lat, A_lat)
        max_lon = max(B_lon, A_lon)
        max_alt = max(B_alt, A_alt)

        min_lat = min(A_lat, B_lat)
        min_lon = min(A_lon, B_lon)
        min_alt = min(A_alt, B_alt)
        
        boundaries      = self.search.get_boundaries(min_lat, max_lat, min_lon, max_lon, min_alt, max_alt)
        low_lim_lat     = boundaries[0]
        high_lim_lat    = boundaries[1]
        low_lim_long    = boundaries[2]
        high_lim_long   = boundaries[3]
        low_lim_alt     = boundaries[4]
        high_lim_alt    = boundaries[5]

        ax1.axhline(high_lim_long, color = 'lime', label = 'Longitude Upper limit', linestyle = 'dotted')
        ax1.axhline(low_lim_long, color = 'limegreen', label = 'Longitude Lower limit', linestyle = 'dotted')
        ax1.axvline(high_lim_lat, color = 'darkorchid', label = 'Latitude Upper limit', linestyle = 'dotted')
        ax1.axvline(low_lim_lat, color = 'indigo', label = 'Latitude Lower limit', linestyle = 'dotted')
        ax1.azhline(high_lim_alt, color = 'deeppink', label = 'Altitude Upper limit', linestyle = 'dotted')
        ax1.azhline(low_lim_alt, color = 'hotpinnk', label = 'Altitude Lower limit', linestyle = 'dotted')
        
        # x = np.linspace(low_lim_long, high_lim_long, 200)
        # y = np.linspace(low_lim_lat, high_lim_lat, 200)
        # #x, y = np.meshgrid(x, y)
        # z = np.linspace(low_lim_alt, high_lim_alt, 200)

        # ax1.plot_trisurf(x, y, z, color='pink')

    '''
        Função para plotar apenas a trajetória em longitude e latitude
    '''
    def plot_lon_lat(self, icao):

        # Track data
        lon = self.__data[icao]['all']['lon']
        lat = self.__data[icao]['all']['lat']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Trajectory of '+ icao, fontsize=16)

        # Set Label Name
        ax1.set_xlabel("Longitude [°]" , fontsize = 12)
        ax1.set_ylabel("Latitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(lon, lat, color='blue', label = icao + " track")
        ax1.scatter(lon[0], lat[0], s=50, label = icao + " track origin", color ='green')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar conflitos a trajetória em longitude e latitude
    '''
    def plot_lon_lat_conf(self, icao, conflicts):

        # Track data
        lon = self.__data[icao]['all']['lon']
        lat = self.__data[icao]['all']['lat']

        lon_cruise = self.__data[icao]['cruise']['lon']
        lat_cruise = self.__data[icao]['cruise']['lat']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Maneuvers on the '+ icao + ' trajectory', fontsize=16)

        # Set Label Name
        ax1.set_xlabel("Longitude [°]" , fontsize = 12)
        ax1.set_ylabel("Latitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(lon, lat, color='blue', label = icao + " track")
        ax1.scatter(lon[0], lat[0], s=50, label = icao + " track origin", color ='green')

        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_lat = lat_cruise[conflict[0]]
            B_lat = lat_cruise[conflict[1]]
            A_lon = lon_cruise[conflict[0]]
            B_lon = lon_cruise[conflict[1]]

            ax1.scatter(A_lon, A_lat,  s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_lon, B_lat,  s=50, label = 'Meneuver end', color ='brown')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar conflitos e trajetórias prevista com a trajetória em longitude e latitude
    '''
    def plot_lon_lat_conf_pred(self, icao, conflicts, track_preds):

        # Track data
        lon = self.__data[icao]['all']['lon']
        lat = self.__data[icao]['all']['lat']

        lon_cruise = self.__data[icao]['cruise']['lon']
        lat_cruise = self.__data[icao]['cruise']['lat']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Maneuvers and Trajectory Prediction on the '+ icao + ' trajectory', fontsize=16)

        # Set Label Name
        ax1.set_xlabel("Longitude [°]" , fontsize = 12)
        ax1.set_ylabel("Latitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(lon, lat, color='blue', label = icao + " track")
        ax1.scatter(lon[0], lat[0], s=50, label = icao + " track origin", color ='green')

        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_lat = lat_cruise[conflict[0]]
            B_lat = lat_cruise[conflict[1]]
            A_lon = lon_cruise[conflict[0]]
            B_lon = lon_cruise[conflict[1]]

            ax1.scatter(A_lon, A_lat,  s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_lon, B_lat,  s=50, label = 'Meneuver end', color ='brown')

        for track_pred in track_preds:
            pred_lat = track_pred[2]
            pred_lon = track_pred[3]
            ax1.plot(pred_lon, pred_lat, color='blue', label = icao + " track prediction", linestyle = 'dashed')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar apenas a trajetória em longitude e altitude
    '''
    def plot_lon_alt(self, icao):

        # Track data
        lon = self.__data[icao]['all']['lon']
        alt = self.__data[icao]['all']['alt']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Trajectory of '+ icao, fontsize=16)

        # Set Label Name
        ax1.set_xlabel("Longitude [°]" , fontsize = 12)
        ax1.set_ylabel("Altitude [m]" , fontsize = 12)
        
        # Plot
        ax1.plot(lon, alt, color='blue', label = icao + " track")
        ax1.scatter(lon[0], alt[0], s=50, label = icao + " track origin", color ='green')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)

        plt.show()


    '''
        Função para plotar conflitos a trajetória em longitude e altitude
    '''
    def plot_lon_alt_conf(self, icao, conflicts):

        # Track data
        lon = self.__data[icao]['all']['lon']
        alt = self.__data[icao]['all']['alt']

        lon_cruise = self.__data[icao]['cruise']['lon']
        alt_cruise = self.__data[icao]['cruise']['alt']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Maneuvers on the '+ icao + ' trajectory', fontsize=16)

        # Set Label Name
        ax1.set_xlabel("Longitude [°]" , fontsize = 12)
        ax1.set_ylabel("Altitude [m]" , fontsize = 12)
        
        # Plot
        ax1.plot(lon, alt, color='blue', label = icao + " track")
        ax1.scatter(lon[0], alt[0], s=50, label = icao + " track origin", color ='green')
        
        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
        
            A_lon = lon_cruise[conflict[0]]
            B_lon = lon_cruise[conflict[1]]
            A_alt = alt_cruise[conflict[0]]
            B_alt = alt_cruise[conflict[1]]

            ax1.scatter(A_lon, A_alt, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_lon, B_alt, s=50, label = 'Meneuver end', color ='brown')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)

        plt.show()


    '''
        Função para plotar conflitos e trajetórias prevista com a trajetória em longitude e altitude
    '''
    def plot_lon_alt_conf_pred(self, icao, conflicts, track_preds):

        # Track data
        lon = self.__data[icao]['all']['lon']
        alt = self.__data[icao]['all']['alt']

        lon_cruise = self.__data[icao]['cruise']['lon']
        alt_cruise = self.__data[icao]['cruise']['alt']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Maneuvers and Trajectory Prediction on the '+ icao + ' trajectory', fontsize=16)

        # Set Label Name
        ax1.set_xlabel("Longitude [°]" , fontsize = 12)
        ax1.set_ylabel("Altitude [m]" , fontsize = 12)
        
        # Plot
        ax1.plot(lon, alt, color='blue', label = icao + " track")
        ax1.scatter(lon[0], alt[0], s=50, label = icao + " track origin", color ='green')
        
        # Plot conflicts
        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
        
            A_lon = lon_cruise[conflict[0]]
            B_lon = lon_cruise[conflict[1]]
            A_alt = alt_cruise[conflict[0]]
            B_alt = alt_cruise[conflict[1]]

            ax1.scatter(A_lon, A_alt, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_lon, B_alt, s=50, label = 'Meneuver end', color ='brown')

        # Plot Trajectory Prediction
        for track_pred in track_preds:
            pred_alt = track_pred[1]
            pred_lon = track_pred[3]
            ax1.plot(pred_lon, pred_alt, color='blue', label = icao + " track prediction", linestyle = 'dashed')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)

        plt.show()


    '''
        Função para plotar apenas a trajetória em latitude e altitude
    '''
    def plot_lat_alt(self, icao):

        # Track data
        lat = self.__data[icao]['all']['lat']
        alt = self.__data[icao]['all']['alt']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Trajectory of '+ icao, fontsize=16)

        # Set Label Name
        ax1.set_xlabel("Latitude [°]" , fontsize = 12)
        ax1.set_ylabel("Altitude [m]" , fontsize = 12)
        
        # Plot
        ax1.plot(lat, alt, color='blue', label = icao + " track")
        ax1.scatter(lat[0], alt[0], s=50, label = icao + " track origin", color ='green')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar conflitos em trajetória em latitude e altitude
    '''
    def plot_lat_alt_conf(self, icao, conflicts):

        # Track data
        lat = self.__data[icao]['all']['lat']
        alt = self.__data[icao]['all']['alt']

        lat_cruise = self.__data[icao]['cruise']['lat']
        alt_cruise = self.__data[icao]['cruise']['alt']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Maneuvers on the '+ icao + ' trajectory', fontsize=16)

        # Set Label Name
        ax1.set_xlabel("Latitude [°]" , fontsize = 12)
        ax1.set_ylabel("Altitude [m]" , fontsize = 12)
        
        # Plot
        ax1.plot(lat, alt, color='blue', label = icao + " track")
        ax1.scatter(lat[0], alt[0], s=50, label = icao + " track origin", color ='green')

        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_lat = lat_cruise[conflict[0]]
            B_lat = lat_cruise[conflict[1]]
            A_alt = alt_cruise[conflict[0]]
            B_alt = alt_cruise[conflict[1]]

            ax1.scatter(A_lat, A_alt, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_lat, B_alt, s=50, label = 'Meneuver end', color ='brown')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar conflitos e trajetórias prevista com a trajetória em latitude e altitude
    '''
    def plot_lat_alt_conf_pred(self, icao, conflicts, track_preds):

        # Track data
        lat = self.__data[icao]['all']['lat']
        alt = self.__data[icao]['all']['alt']

        lat_cruise = self.__data[icao]['cruise']['lat']
        alt_cruise = self.__data[icao]['cruise']['alt']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Maneuvers and Trajectory Prediction on the '+ icao + ' trajectory', fontsize=16)

        # Set Label Name
        ax1.set_xlabel("Latitude [°]" , fontsize = 12)
        ax1.set_ylabel("Altitude [m]" , fontsize = 12)
        
        # Plot
        ax1.plot(lat, alt, color='blue', label = icao + " track")
        ax1.scatter(lat[0], alt[0], s=50, label = icao + " track origin", color ='green')

        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_lat = lat_cruise[conflict[0]]
            B_lat = lat_cruise[conflict[1]]
            A_alt = alt_cruise[conflict[0]]
            B_alt = alt_cruise[conflict[1]]

            ax1.scatter(A_lat, A_alt, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_lat, B_alt, s=50, label = 'Meneuver end', color ='brown')

        for track_pred in track_preds:
            pred_alt = track_pred[1]
            pred_lat = track_pred[2]
            ax1.plot(pred_lat, pred_alt, color='blue', label = icao + " track prediction", linestyle = 'dashed')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar apenas a trajetória em tempo e latitude
    '''
    def plot_time_lat(self, icao):

        # Track data
        tempo = self.__data[icao]['all'].index
        lat = self.__data[icao]['all']['lat']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle(icao + ' latitude over time', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Latitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, lat, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], lat[0], s=50, label = icao + " track origin", color ='green')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar conflitos a trajetória em tempo e latitude
    '''
    def plot_time_lat_conf(self, icao, conflicts):

        # Track data
        tempo = self.__data[icao]['all'].index
        lat = self.__data[icao]['all']['lat']

        tempo_cruise = self.__data[icao]['cruise'].index
        lat_cruise = self.__data[icao]['cruise']['lat']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle(icao + ' latitude over time with maneuver', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Latitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, lat, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], lat[0], s=50, label = icao + " track origin", color ='green')

        
        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_time = tempo_cruise[conflict[0]]
            B_time = tempo_cruise[conflict[1]]
            A_lat = lat_cruise[conflict[0]]
            B_lat = lat_cruise[conflict[1]]

            ax1.scatter(A_time, A_lat, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_time, B_lat, s=50, label = 'Meneuver end', color ='brown')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar conflitos e trajetórias prevista com a trajetória em tempo e latitude
    '''
    def plot_time_lat_conf_pred(self, icao, conflicts, track_preds):

        # Track data
        tempo = self.__data[icao]['all'].index
        lat = self.__data[icao]['all']['lat']

        tempo_cruise = self.__data[icao]['cruise'].index
        lat_cruise = self.__data[icao]['cruise']['lat']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Maneuvers and Trajectory Prediction on the '+ icao + ' trajectory', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Latitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, lat, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], lat[0], s=50, label = icao + " track origin", color ='green')

        
        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_time = tempo_cruise[conflict[0]]
            B_time = tempo_cruise[conflict[1]]
            A_lat = lat_cruise[conflict[0]]
            B_lat = lat_cruise[conflict[1]]

            ax1.scatter(A_time, A_lat, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_time, B_lat, s=50, label = 'Meneuver end', color ='brown')

        for track_pred in track_preds:
            pred_time = track_pred[0]
            pred_lat = track_pred[2]
            ax1.plot(pred_time, pred_lat, color='blue', label = icao + " track prediction", linestyle = 'dashed')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar conflitos e trajetórias prevista com a trajetória em tempo e latitude
    '''
    def plot_time_lat_conf_pred_B_icao(self, icao, conflicts, track_preds, second_filters):

        # Track data
        tempo = self.__data[icao]['all'].index
        lat = self.__data[icao]['all']['lat']

        tempo_cruise = self.__data[icao]['cruise'].index
        lat_cruise = self.__data[icao]['cruise']['lat']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Maneuvers and Trajectory Prediction on the '+ icao + ' trajectory', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Latitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, lat, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], lat[0], s=50, label = icao + " track origin", color ='green')

        
        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_time = tempo_cruise[conflict[0]]
            B_time = tempo_cruise[conflict[1]]
            A_lat = lat_cruise[conflict[0]]
            B_lat = lat_cruise[conflict[1]]

            ax1.scatter(A_time, A_lat, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_time, B_lat, s=50, label = 'Meneuver end', color ='brown')

        i=0
        for track_pred in track_preds:
            pred_time = track_pred[0]
            pred_lat = track_pred[2]
            ax1.plot(pred_time, pred_lat, color='blue', label = icao + " track prediction", linestyle = 'dashed')
            B_icao = second_filters[i]
            B_tempo = self.__data[B_icao]['all'].index
            B_lat = self.__data[B_icao]['all']['lat']
            ax1.plot(B_tempo, B_lat, color='red', label = B_icao + " track")
            ax1.scatter(B_tempo[0], B_lat[0], s=50, label = B_icao + " track origin", color ='deeppink')
            i = i+1

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar apenas a trajetória em tempo e longitude
    '''
    def plot_time_lon(self, icao):

        # Track data
        tempo = self.__data[icao]['all'].index
        lon = self.__data[icao]['all']['lon']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle(icao + ' longitude over time', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Longitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, lon, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], lon[0], s=50, label = icao + " track origin", color ='green')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()
        

    '''
        Função para plotar conflitos a trajetória em tempo e longitude
    '''
    def plot_time_lon_conf(self, icao, conflicts):

        # Track data
        tempo = self.__data[icao]['all'].index
        lon = self.__data[icao]['all']['lon']

        tempo_cruise = self.__data[icao]['cruise'].index
        lon_cruise = self.__data[icao]['cruise']['lon']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle(icao + ' longitude over time with maneuver', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Longitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, lon, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], lon[0], s=50, label = icao + " track origin", color ='green')
        
        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_time = tempo_cruise[conflict[0]]
            B_time = tempo_cruise[conflict[1]]
            A_lon = lon_cruise[conflict[0]]
            B_lon = lon_cruise[conflict[1]]

            ax1.scatter(A_time, A_lon, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_time, B_lon, s=50, label = 'Meneuver end', color ='brown')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()
   

    '''
        Função para plotar conflitos e trajetórias prevista com a trajetória em tempo e longitude
    '''
    def plot_time_lon_conf_pred(self, icao, conflicts, track_preds):

        # Track data
        tempo = self.__data[icao]['all'].index
        lon = self.__data[icao]['all']['lon']

        tempo_cruise = self.__data[icao]['cruise'].index
        lon_cruise = self.__data[icao]['cruise']['lon']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Maneuvers and Trajectory Prediction on the '+ icao + ' trajectory', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Longitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, lon, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], lon[0], s=50, label = icao + " track origin", color ='green')
        
        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_time = tempo_cruise[conflict[0]]
            B_time = tempo_cruise[conflict[1]]
            A_lon = lon_cruise[conflict[0]]
            B_lon = lon_cruise[conflict[1]]

            ax1.scatter(A_time, A_lon, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_time, B_lon, s=50, label = 'Meneuver end', color ='brown')

        
        for track_pred in track_preds:
            pred_time = track_pred[0]
            pred_lon = track_pred[3]
            ax1.plot(pred_time, pred_lon, color='blue', label = icao + " track prediction", linestyle = 'dashed')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar conflitos e trajetórias prevista com a trajetória em tempo e longitude
    '''
    def plot_time_lon_conf_pred_B_icao(self, icao, conflicts, track_preds, second_filters):

        # Track data
        tempo = self.__data[icao]['all'].index
        lon = self.__data[icao]['all']['lon']

        tempo_cruise = self.__data[icao]['cruise'].index
        lon_cruise = self.__data[icao]['cruise']['lon']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Maneuvers and Trajectory Prediction on the '+ icao + ' trajectory', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Longitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, lon, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], lon[0], s=50, label = icao + " track origin", color ='green')
        
        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_time = tempo_cruise[conflict[0]]
            B_time = tempo_cruise[conflict[1]]
            A_lon = lon_cruise[conflict[0]]
            B_lon = lon_cruise[conflict[1]]

            ax1.scatter(A_time, A_lon, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_time, B_lon, s=50, label = 'Meneuver end', color ='brown')

        i = 0
        for track_pred in track_preds:
            pred_time = track_pred[0]
            pred_lon = track_pred[3]
            ax1.plot(pred_time, pred_lon, color='blue', label = icao + " track prediction", linestyle = 'dashed')
            B_icao = second_filters[i]
            B_tempo = self.__data[B_icao]['all'].index
            B_lon = self.__data[B_icao]['all']['lon']
            ax1.plot(B_tempo, B_lon, color='red', label = B_icao + " track")
            ax1.scatter(B_tempo[0], B_lon[0], s=50, label = B_icao + " track origin", color ='deeppink')
            i = i+1

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar apenas a trajetória em tempo e altitude
    '''
    def plot_time_alt(self, icao):

        # Track data
        tempo = self.__data[icao]['all'].index
        alt = self.__data[icao]['all']['alt']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle(icao + ' altitude over time', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Altitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, alt, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], alt[0], s=50, label = icao + " track origin", color ='green')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar conflitos a trajetória em tempo e altitude
    '''
    def plot_time_alt_conf(self, icao, conflicts):

        # Track data
        tempo = self.__data[icao]['all'].index
        alt = self.__data[icao]['all']['alt']

        tempo_cruise = self.__data[icao]['cruise'].index
        alt_cruise = self.__data[icao]['cruise']['alt']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle(icao + ' altitude over time with maneuver', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Altitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, alt, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], alt[0], s=50, label = icao + " track origin", color ='green')
        
        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_time = tempo_cruise[conflict[0]]
            B_time = tempo_cruise[conflict[1]]
            A_alt = alt_cruise[conflict[0]]
            B_alt = alt_cruise[conflict[1]]

            ax1.scatter(A_time, A_alt, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_time, B_alt, s=50, label = 'Meneuver end', color ='brown')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()


    '''
        Função para plotar conflitos a trajetória em tempo e altitude
    '''
    def plot_time_alt_conf_pred(self, icao, conflicts, track_preds):

        # Track data
        tempo = self.__data[icao]['all'].index
        alt = self.__data[icao]['all']['alt']

        tempo_cruise = self.__data[icao]['cruise'].index
        alt_cruise = self.__data[icao]['cruise']['alt']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Maneuvers and Trajectory Prediction on the '+ icao + ' trajectory', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Altitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, alt, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], alt[0], s=50, label = icao + " track origin", color ='green')
        
        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_time = tempo_cruise[conflict[0]]
            B_time = tempo_cruise[conflict[1]]
            A_alt = alt_cruise[conflict[0]]
            B_alt = alt_cruise[conflict[1]]

            ax1.scatter(A_time, A_alt, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_time, B_alt, s=50, label = 'Meneuver end', color ='brown')

        for track_pred in track_preds:
            pred_time = track_pred[0]
            pred_alt = track_pred[1]
            pred_lat = track_pred[2]
            pred_lon = track_pred[3]
            ax1.plot(pred_time, pred_alt, color='blue', label = icao + " track prediction", linestyle = 'dashed')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()

    '''
        Função para plotar conflitos a trajetória em tempo e altitude
    '''
    def plot_time_alt_conf_pred_B_icao(self, icao, conflicts, track_preds, second_filters):

        # Track data
        tempo = self.__data[icao]['all'].index
        alt = self.__data[icao]['all']['alt']

        tempo_cruise = self.__data[icao]['cruise'].index
        alt_cruise = self.__data[icao]['cruise']['alt']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle('Maneuvers and Trajectory Prediction on the '+ icao + ' trajectory', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Altitude [°]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, alt, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], alt[0], s=50, label = icao + " track origin", color ='green')
        
        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_time = tempo_cruise[conflict[0]]
            B_time = tempo_cruise[conflict[1]]
            A_alt = alt_cruise[conflict[0]]
            B_alt = alt_cruise[conflict[1]]

            ax1.scatter(A_time, A_alt, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_time, B_alt, s=50, label = 'Meneuver end', color ='brown')
        i = 0
        for track_pred in track_preds:
            pred_time = track_pred[0]
            pred_alt = track_pred[1]
            pred_lat = track_pred[2]
            pred_lon = track_pred[3]
            ax1.plot(pred_time, pred_alt, color='blue', label = icao + " track prediction", linestyle = 'dashed')
            B_icao = second_filters[i]
            B_tempo = self.__data[B_icao]['all'].index
            B_alt = self.__data[B_icao]['all']['alt']
            ax1.plot(B_tempo, B_alt, color='red', label = B_icao + " track")
            ax1.scatter(B_tempo[0], B_alt[0], s=50, label = B_icao + " track origin", color ='deeppink')
            i = i+1
            
            

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()

    '''
        Função para plotar apenas a trajetória em tempo e velocidade
    '''
    def plot_time_speed(self, icao):

        # Track data
        tempo = self.__data[icao]['all'].index
        speed = self.__data[icao]['all']['vel_xy']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle(icao + ' speed over time', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Speed [m/s]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, speed, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], speed[0], s=50, label = icao + " track origin", color ='green')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
        plt.show()
        

    '''
        Função para plotar apenas a trajetória em tempo e velocidade
    '''
    def plot_time_speed_conf(self, icao, conflicts):

        # Track data
        tempo = self.__data[icao]['all'].index
        speed = self.__data[icao]['all']['vel_xy']

        tempo_cruise = self.__data[icao]['cruise'].index
        speed_cruise = self.__data[icao]['cruise']['vel_xy']

        plt.style.use("seaborn-deep")

        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.5))

        ax1 = fig.add_subplot(1, 1, 1)

        #Set title
        fig.suptitle(icao + ' speed over time with maneuver', fontsize=16)

        # Format time axis
        format_str = '%H:%M:%S'
        format_ = mdates.DateFormatter(format_str)
        ax1.xaxis.set_major_formatter(format_)
        
        # Set Label Name
        ax1.set_xlabel("Time" , fontsize = 12)
        ax1.set_ylabel("Speed [m/s]" , fontsize = 12)
        
        # Plot
        ax1.plot(tempo, speed, color='blue', label = icao + " track")
        ax1.scatter(tempo[0], speed[0], s=50, label = icao + " track origin", color ='green')
        
        for conflict in conflicts[icao]['man_track'] + conflicts[icao]['man_alt'] + conflicts[icao]['man_speed']:
            A_time = tempo_cruise[conflict[0]]
            B_time = tempo_cruise[conflict[1]]
            A_speed = speed_cruise[conflict[0]]
            B_speed = speed_cruise[conflict[1]]

            ax1.scatter(A_time, A_speed, s=50, label = 'Meneuver begin', color ='purple')
            ax1.scatter(B_time, B_speed, s=50, label = 'Meneuver end', color ='brown')

        # ax1.set_facecolor("white")
        ax1.legend(facecolor='white', fontsize = 12, framealpha=1)
        ax1.grid(True)
        
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