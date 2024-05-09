'''
    Plot x,y,t  3d surface and z as colormap
'''

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
import json
import matplotlib.dates as dates
import pandas as pd
import datetime 


class PlotData:
    def __init__(self, data, data_pred):
        self.__data = data
        self.__data_pred = data_pred

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
    
    def plot_icao_traj(self, data, icao, conflicts = None):
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
            for conflict in conflicts[icao]['man_track']:
                indice = conflict[0]
                ax1.scatter3D(lon[indice], lat[indice], alt[indice], s=30, label = 'A', color ='red')
                indice = conflict[1]
                ax1.scatter3D(lon[indice], lat[indice], alt[indice], s=30, label = 'B', color ='black')
                indice = conflict[2]
                ax1.scatter3D(lon[indice], lat[indice], alt[indice], s=30, label = 'C', color ='green')
            for conflict in  conflicts[icao]['man_alt']:
                indice = conflict[0]
                ax1.scatter3D(lon[indice], lat[indice], alt[indice], s=30, label = 'conflict', color ='red')
                indice = conflict[1]
                ax1.scatter3D(lon[indice], lat[indice], alt[indice], s=30, label = 'conflict', color ='black')

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
        ax1.scatter3D(data_vector[icao]['lon'][0], data_vector[icao]['lat'][0], data_vector[icao]['alt'][0], s=30, label = 'origin real', color ='green')
        ax1.plot3D(data_time_serie[icao].loc[:,"lon"], data_time_serie[icao].loc[:,"lat"], data_time_serie[icao].loc[:,"alt"], label = icao + ' interpolated', color ='red')
        ax1.scatter3D(data_time_serie[icao].loc[:,"lon"][0], data_time_serie[icao].loc[:,"lat"][0], data_time_serie[icao].loc[:,"alt"][0], s=30, label = 'origin interpolated', color ='black')
        
        plt.legend()

        plt.show()

    
    def plot_comp_all_cruise(self, data, icao):
        data_cruise = data[icao]['cruise']
        data_filter = data[icao]['filter']
        data_all = data[icao]['all']
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax1 = fig.add_subplot(1, 1, 1, projection='3d')
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.set_zlabel("Baro altitude")
        
        ax1.plot3D(data_all.loc[:,"lon"], data_all.loc[:,"lat"], data_all.loc[:,"alt"], label = icao + ' complete data', color ='red')
        ax1.scatter3D(data_all.loc[:,"lon"][0], data_all.loc[:,"lat"][0], data_all.loc[:,"alt"][0], s=30, label = 'complete data', color ='black')

        ax1.plot3D(data_filter.loc[:,"lon"], data_filter.loc[:,"lat"], data_filter.loc[:,"alt"], label = icao + ' filter data', color ='purple')
        ax1.scatter3D(data_filter.loc[:,"lon"][0], data_filter.loc[:,"lat"][0], data_filter.loc[:,"alt"][0], s=30, label = 'filter data', color ='black')
        
        ax1.plot3D(data_cruise.loc[:,"lon"], data_cruise.loc[:,"lat"], data_cruise.loc[:,"alt"], label = icao + ' cruise data', color ='blue')
        ax1.scatter3D(data_cruise.loc[:,"lon"][0], data_cruise.loc[:,"lat"][0], data_cruise.loc[:,"alt"][0], s=30, label = 'cruise data', color ='green')
        
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
        ax1.scatter3D(data_all.loc[:,"lon"][0], data_all.loc[:,"lat"][0], data_all.loc[:,"alt"][0], s=30, label = icao +' P0', color ='black')
              
        for icao in icao_list:
            data_all = data[icao]['all']
            ax1.plot3D(data_all.loc[:,"lon"], data_all.loc[:,"lat"], data_all.loc[:,"alt"], label = icao)
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

        for conflict in conflicts[icao]['man_track']:
                A_time = data[icao]['cruise'].index[conflict[0]]
                B_time = data[icao]['cruise'].index[conflict[1]]
                C_time = data[icao]['cruise'].index[conflict[2]]
                for icao in icao_list:
                    aircraft = self.data[icao]
                    pass
        for conflict in conflicts[icao]['man_alt']:
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
            ax1.scatter3D(data_all.loc[:,"lon"][0], data_all.loc[:,"lat"][0], data_all.loc[:,"alt"][0], s=30, label = icao +' P0', color ='black')

            ax2.plot(data_all.index, data_all.loc[:,"lat"], label = icao)
            ax2.scatter(data_all.index, data_all.loc[:,"lat"], label = icao)
            ax2.scatter(data_all.index[0], data_all.loc[:,"lat"][0], s=30, label = icao +' P0', color ='black')

            ax3.plot(data_all.index, data_all.loc[:,"alt"], label = icao)
            ax3.scatter(data_all.index, data_all.loc[:,"alt"], label = icao)
            ax3.scatter(data_all.index[0], data_all.loc[:,"alt"][0], s=30, label = icao +' P0', color ='black')

            ax4.plot(data_all.index, data_all.loc[:,"lon"], label = icao)
            ax4.scatter(data_all.index ,data_all.loc[:,"lon"], label = icao)
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

        ax1.plot_surface(Xc, Yc, Zc, alpha=0.3)

        plt.show()

    