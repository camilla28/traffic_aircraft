'''
    Conflict Detection
'''
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
import json
import math
import geopy
from geopy.distance import geodesic, great_circle
from statistics import mean, stdev
from operator import itemgetter


class Conflict_Detection:

    __TRACK_CHANGE_LIM = 25 #25° de mudança de direção pode determinar a
    __TRACK_CHANGE_LIM_BACK = 4 # 2°
    __TRACK_STD_INDICES = 6 # É o índice que utilizado para estabelecer o limite para std
    __TRACK_STD_LIM = 10 # É o std limite para avaliação
    __ALT_CHANGE_LIM = 500 # 1000 m de mudança de altitude
    __ALT_CHANGE_LIM_BACK = 100 # 200 m de limite para indicar um retorno à altitude de antes
    __ALT_STD_INDICES = 6 # É o índice que utilizado para estabelecer o limite para std
    __ALT_STD_LIM = 500 # É o std limite para avaliação
    
    def __init__(self, data):
        self.data = data
    

    def __search_conflicts(self, icao, response):
        airplane = self.data[icao]
        response[icao] = dict()
        response[icao]['man_track'] = self.detect_maneuver_track(airplane['track'])
        response[icao]['man_alt'] = self.detect_maneuver_alt(airplane['alt'], airplane['vel_z'])
        if len(response[icao]['man_track'])!=0 or len(response[icao]['man_alt'])!=0:
            response[icao]['conflict'] = True
        else:
            response[icao]['conflict'] = False
        return response


    def search_conflicts(self, icao = None):
        response = dict()
        if icao != None:
            response = self.__search_conflicts(icao, response)
        else:
            icao_list = list(self.data.keys())
            for icao in icao_list:
                response = self.__search_conflicts(icao, response)
        return response
    

    def detect_maneuver_track(self, track):
        indice = 0
        change_track_detected = []
        second_point_found = False
        up = []
        down = []
        for t in track:
            if indice !=0:
                # Verifica se entre o waypoint anterior e esse houve mudança de direção maior ou igual do que
                # __TRACK_CHANGE_LIM = 25
                if abs(ant_t-t)>=self.__TRACK_CHANGE_LIM: # ou se uma sucessão dos últimos valores forem
                    
                    # É utilizado uma janela para calculo, que é determinada pela variável __TRACK_STD_INDICES 
                    # que é igual 6, utiliza-se sempre essa janela para determinar a média dos últimos valores 
                    # e o desvio variação dessa medida
                    if indice > self.__TRACK_STD_INDICES:
                        last_track = mean(track[indice-self.__TRACK_STD_INDICES:indice-1])
                        last_track_std = stdev(track[indice-self.__TRACK_STD_INDICES:indice-1])

                    # Se o indice for menor do que essa janela, então deve pegar desde o início dos dados 
                    # (índice =0)
                    
                    elif indice-1 == 0:
                        last_track = track[0]
                        last_track_std = self.__TRACK_STD_LIM
                    else:
                        last_track = mean(track[0:indice-1])
                        if  indice-2 > 0:
                            last_track_std = stdev(track[0:indice-1])
                        else:
                            last_track_std = self.__TRACK_STD_LIM
                    # É utilizado então o último valor utilizado 
                    for i in np.arange(indice+1, len(track)-1, 1):

                        if abs(last_track-track[i])<=last_track_std or \
                            abs(last_track-track[i])<=self.__TRACK_CHANGE_LIM_BACK :
                            change_track_detected.append((indice, i))
                            second_point_found = True
                            break

                    if second_point_found == False:
                        change_track_detected.append((indice, None))
            ant_t = t
            indice = indice+1

        none_len =[x for x, y in enumerate(change_track_detected) if y[1] == None or y[0] == None]

        for i in sorted(none_len, reverse=True):
            del change_track_detected[i]
        
        return change_track_detected


    def detect_maneuver_alt(self, alt, vertical_rate):
        indice = 0
        change_alt_detected = []
        second_point_found = False 
        up = []
        down = []
        print(vertical_rate)
        for t in alt:
            if indice !=0:
                if abs(ant_t-t)>=self.__ALT_CHANGE_LIM and \
                    (vertical_rate[indice]>20 or vertical_rate[indice]<-20):

                    if indice > 3:
                        last_alt = mean(alt[indice-3:indice-1])
                        last_alt_std = stdev(alt[indice-3:indice-1])

                    elif indice-1 == 0:
                        last_alt = alt[0]
                        last_alt_std = self.__ALT_STD_LIM
                    else:
                        last_alt = mean(alt[0:indice-1])
                        if  indice-2 > 0:
                            last_alt_std = stdev(alt[0:indice-1])
                        else:
                            last_alt_std = self.__ALT_STD_LIM

                    for i in np.arange(indice+1, len(alt)-1, 1):

                        if (abs(last_alt-alt[i])<=last_alt_std or \
                            abs(last_alt-alt[i])<=self.__ALT_CHANGE_LIM_BACK) and \
                            (vertical_rate[i]>20 or vertical_rate[i]<-20):
                            second_point_found = True                        
                            change_alt_detected.append((indice, i))
                            break

                    if second_point_found == False:
                        change_alt_detected.append((indice, None))


            ant_t = t
            indice = indice+1

        none_len =[x for x, y in enumerate(change_alt_detected) if y[1] == None or y[0] == None]
       
        for i in sorted(none_len, reverse=True):
            del change_alt_detected[i]

        return change_alt_detected