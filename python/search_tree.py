import time
import pandas as pd
import geopy.distance
import math

#from conflict import Conflict, Point, Maneuver

class Search_Tree:

    __DISTANCE_XY = 5   # 5 NM distance in xy
    DISTANCE_Z = 600 # 600 m distance in z
    __DELTA_TIME = 60   # 60 seconds is the sample time
    
    def __init__(self, tree = None, data = None):

        #if tree != None:
        #    self.tree = tree
        #else:
        #    self.__create_tree(True, data = None)
        self.data = data


    # Como o conflito não aconteceu de fato, mas sim quase aconteceu, é necessário prever a trajetória
    # Para iss mantem-se a ground speed e vertical rate constantes a partir do início da manobra
    def __trajectory_prediction(self, airplane, A_time, B_time):
        ref_time = A_time
        ref_lon = airplane['cruise'].lon[ref_time]
        ref_lat = airplane['cruise'].lat[ref_time]
        ref_alt = airplane['cruise'].alt[ref_time]
        ref_track = airplane['cruise'].track[ref_time]
        ref_vel_xy = airplane['cruise'].vel_xy[ref_time]  
        ref_vel_z = airplane['cruise'].vel_z[ref_time]   
        delta_time = pd.Timedelta(seconds = self.__DELTA_TIME)
        distance_xy = ref_vel_xy * self.__DELTA_TIME
        distance_z = ref_vel_z * self.__DELTA_TIME
        pred_alt = []
        pred_lat = []
        pred_lon = []
        pred_time = []
        while ref_time < B_time:
            pred_time.append(ref_time)
            pred_alt.append(ref_alt)
            pred_lat.append(ref_lat)
            pred_lon.append(ref_lon)
            ref_lat, ref_lon, _ = geopy.distance.distance(meters=distance_xy).destination((ref_lat, ref_lon), bearing=ref_track)
            #ref_alt = ref_alt + distance_z
            ref_time = ref_time + delta_time
        return pred_time, pred_alt, pred_lat, pred_lon 


    def __get_bearing(self, lat1, lon1, lat2, lon2):
        
        φ1 = math.radians(lat1) # φ, λ in radians
        φ2 = math.radians(lat2)
        λ1 = math.radians(lon1)
        λ2 = math.radians(lon2)
        y = math.sin(λ2-λ1) * math.cos(φ2)
        x = math.cos(φ1)*math.sin(φ2) - math.sin(φ1)*math.cos(φ2)*math.cos(λ2-λ1)
        theta = math.atan2(y, x)
        brng = (math.degrees(theta) + 360) % 360 #in degrees
        return brng


    def __trajectory_prediction_2(self, airplane, A_time, B_time):
        
        A_lon = airplane['cruise'].lon[A_time]
        A_lat = airplane['cruise'].lat[A_time]
        A_alt = airplane['cruise'].alt[A_time]
        A_vel_xy = airplane['cruise'].vel_xy[A_time]
        
        B_lon = airplane['cruise'].lon[B_time]
        B_lat = airplane['cruise'].lat[B_time]
        B_alt = airplane['cruise'].alt[B_time]

        A_point = (A_lat, A_lon)
        B_point = (B_lat, B_lon)
        dist_total = geopy.distance.distance(A_point, B_point).meters
        # duration_total = dist_total/A_vel_xy

        delta_time = pd.Timedelta(seconds = self.__DELTA_TIME)
        distance_xy = A_vel_xy * self.__DELTA_TIME
        pred_alt = []
        pred_lat = []
        pred_lon = []
        pred_time = []
        count_dist = 0
        
        delta_alt = B_alt - A_alt
        delta_tim = B_time - A_time
        # track = self.__get_bearing(A_lat, A_lon, B_lat, B_lon)
        lat = A_lat
        lon = A_lon
        ref_time = A_time
        ref_alt = A_alt

        while count_dist < dist_total:
            pred_time.append(ref_time)
            pred_lat.append(lat)
            pred_lon.append(lon)
            track = self.__get_bearing(lat, lon, B_lat, B_lon)
            (lat, lon) = self.__get_geoLoc_from_distance(distance_xy, lat, lon, track)
            count_dist = count_dist + distance_xy
            ref_time = ref_time + delta_time
        
        delta_tim = pred_time[len(pred_time)-1] - pred_time[0]
        vel_z = delta_alt/delta_tim.total_seconds()
            
        for i in range(0, len(pred_time)):
            pred_alt.append(ref_alt)
            ref_alt = ref_alt + vel_z * self.__DELTA_TIME

        # pred_time.append(B_time)
        # pred_alt.append(B_alt)
        # pred_lat.append(B_lat)
        # pred_lon.append(B_lon)
                
        return pred_time, pred_alt, pred_lat, pred_lon


    def __get_geoLoc_from_distance(self, distance, lat, lon, track):
        lat, lon, _ = geopy.distance.distance(meters=distance).destination((lat, lon), bearing=track)
        return (lat, lon)

    
    def __get_boundaries(self, min_lat, max_lat, min_lon, max_lon, min_alt, max_alt):
        low_lim_lat, _, _   = geopy.distance.distance(nautical = self.__DISTANCE_XY).destination((min_lat, min_lon), bearing=180)
        high_lim_lat, _, _  = geopy.distance.distance(nautical = self.__DISTANCE_XY).destination((max_lat, max_lon), bearing=0)
        _, low_lim_long, _  = geopy.distance.distance(nautical = self.__DISTANCE_XY).destination((min_lat, min_lon), bearing=270)
        _, high_lim_long, _ = geopy.distance.distance(nautical = self.__DISTANCE_XY).destination((max_lat, max_lon), bearing=90)
        low_lim_alt     = min_alt - self.DISTANCE_Z
        high_lim_alt    = max_alt + self.DISTANCE_Z

        return low_lim_lat, high_lim_lat, low_lim_long, high_lim_long, low_lim_alt, high_lim_alt


    def get_boundaries(self, min_lat, max_lat, min_lon, max_lon, min_alt, max_alt):
        return self.__get_boundaries(min_lat, max_lat, min_lon, max_lon, min_alt, max_alt)


    def search(self, conflicts, airplane_icao):
        airplane = self.data[airplane_icao]
        icao_list = list(self.data.keys())
        icao_list.remove(airplane_icao)
        first_filter = []
        second_filter = []
        B_conflict_point = list()
        A_conflict_point = list()
        FirstManPoint = list()
        SecondManPoint = list()
        Maneuvers = list()
        track_preds = list()

        if conflicts[airplane_icao]['conflict']:

            for conflict in conflicts[airplane_icao]['man_track'] + conflicts[airplane_icao]['man_alt'] + conflicts[airplane_icao]['man_speed']:
                
                # First point of conflict
                A_time = airplane['cruise'].index[conflict[0]]
                A_lat = airplane['cruise'].lat[conflict[0]]
                A_lon = airplane['cruise'].lon[conflict[0]]
                A_alt = airplane['cruise'].alt[conflict[0]]
                A_track = airplane['cruise'].track[conflict[0]]
                A_velxy = airplane['cruise'].vel_xy[conflict[0]]
                A_velz = airplane['cruise'].vel_z[conflict[0]]
                
                # Second point of conflict
                B_time = airplane['cruise'].index[conflict[1]]
                B_lat = airplane['cruise'].lat[conflict[1]]
                B_lon = airplane['cruise'].lon[conflict[1]]
                B_alt = airplane['cruise'].alt[conflict[1]]
                B_track = airplane['cruise'].track[conflict[1]]
                B_velxy = airplane['cruise'].vel_xy[conflict[1]]
                B_velz = airplane['cruise'].vel_z[conflict[1]]

                if len(conflicts[airplane_icao]['man_track'])> 0:
                    Maneuver_Type = "track"
                if len(conflicts[airplane_icao]['man_alt']) > 0:
                    Maneuver_Type = "alt"
                if len(conflicts[airplane_icao]['man_speed']) > 0:
                    Maneuver_Type = "speed"
                
                Maneuver_Act = conflict[2]
                
                # Search for the other(s) airplanes in conflict
                for icao in icao_list:

                    # Deve considerar todo o dado do outro avião
                    aircraft = self.data[icao]['all']

                    # Para determinar os limites do setor onde acontece o conflito, pega os valores maximos e mínimos de latitude, 
                    # longitude e altitude determinados pelos dois pontos de conflito
                    max_lat = max(B_lat, A_lat)
                    max_lon = max(B_lon, A_lon)
                    max_alt = max(B_alt, A_alt)

                    min_lat = min(A_lat, B_lat)
                    min_lon = min(A_lon, B_lon)
                    min_alt = min(A_alt, B_alt)
                    
                    # Com esses valores, incluir os limites da norma de 5 NM e 1000 (máximo)
                    boundaries      = self.__get_boundaries(min_lat, max_lat, min_lon, max_lon, min_alt, max_alt)
                    low_lim_lat     = boundaries[0]
                    high_lim_lat    = boundaries[1]
                    low_lim_long    = boundaries[2]
                    high_lim_long   = boundaries[3]
                    low_lim_alt     = boundaries[4]
                    high_lim_alt    = boundaries[5]

                    # Filtra as aeronaves que passam naquele instante, por aquele setor
                    time_filter = aircraft[(aircraft.index <= B_time) & (aircraft.index >=A_time) &
                                           (aircraft.lat <= high_lim_lat) & (aircraft.lat >= low_lim_lat) &
                                           (aircraft.lon <= high_lim_long) & (aircraft.lon >= low_lim_long) &
                                           (aircraft.alt <= high_lim_alt) & (aircraft.alt >= low_lim_alt)]
                    if len(time_filter) > 0:
                        first_filter.append(icao)

                first_filter = list(set(first_filter))
                
                # Faz a projeção da trajetória considerando velocidade constante
                # track_pred = self.__trajectory_prediction(airplane, A_time, B_time)
                track_pred = self.__trajectory_prediction_2(airplane, A_time, B_time)
                track_preds.append(track_pred)
                
                # Not found the airplane yet
                found = False

                # Verifica se a cada ponto da trajetória predita, ele está em conflito com uma outra aeronave
                for i in range(len(track_pred[0])):
                    ref_time = track_pred[0][i]
                    ref_alt = track_pred[1][i]
                    ref_lat = track_pred[2][i]
                    ref_lon = track_pred[3][i]
                    
                    for icao in first_filter: # Icao -> Aircraft B
                        aircraft = self.data[icao]['all']
                        # se a outra aeronave tiver aquele mesmo tempo, pega ele próprio para comparar
                        if ref_time in aircraft.index:
                            A1_time = ref_time
                            icao_lat = aircraft.lat[ref_time]
                            icao_lon = aircraft.lon[ref_time]
                            icao_alt = aircraft.alt[ref_time]
                            icao_vel_xy = aircraft.vel_xy[ref_time]
                            icao_vel_z = aircraft.vel_z[ref_time]
                            icao_track = aircraft.track[ref_time]
                        # Caso contrário, interpola
                        else:
                            minor = aircraft[aircraft.index < ref_time]
                            major = aircraft[aircraft.index > ref_time]
                            if len(minor) == 0:
                                A1_time = major.index[0]
                            else:
                                A1_time = minor.index[len(minor)-1]
                            icao_vel_xy = aircraft.vel_xy[A1_time]
                            icao_vel_z = aircraft.vel_z[A1_time]
                            icao_track = aircraft.track[A1_time]
                            time_diff = ref_time.timestamp() - A1_time.timestamp()
                            distance_xy = time_diff * icao_vel_xy
                            distance_z = time_diff * icao_vel_z
                            icao_lat = aircraft.lat[A1_time]
                            icao_lon = aircraft.lon[A1_time]
                            icao_alt = aircraft.alt[A1_time] #+ distance_z
                            
                            # icao_lat, icao_lon = self.__get_geoLoc_from_distance(distance_xy, icao_lat, icao_lon, icao_track)
                        
                        # Verifica se tem conflito entre o ponto da trajetória prevista e a aeronve a ser avaliada 
                        boundaries      = self.__get_boundaries(ref_lat, ref_lat, ref_lon, ref_lon, A_alt, A_alt)
                        low_lim_lat     = boundaries[0]
                        high_lim_lat    = boundaries[1]
                        low_lim_long    = boundaries[2]
                        high_lim_long   = boundaries[3]
                        low_lim_alt     = boundaries[4]
                        high_lim_alt    = boundaries[5]
                        
                        if (icao_lat >= low_lim_lat and icao_lat <= high_lim_lat and \
                           icao_lon >= low_lim_long and icao_lon <= high_lim_long) and \
                           icao_alt >= low_lim_alt and icao_alt <= high_lim_alt:

                            if icao not in airplane_icao and airplane_icao not in icao:
                                second_filter.append(icao)
                                found = True

                                A_dict = dict()
                                A_dict['time'] = ref_time
                                A_dict['lat'] = ref_lat
                                A_dict['lon'] = ref_lon
                                A_dict['alt'] = ref_alt
                                A_dict['vel_xy'] = airplane['cruise'].vel_xy[ref_time]
                                A_dict['vel_z'] = airplane['cruise'].vel_z[ref_time]
                                A_dict['track'] = airplane['cruise'].track[ref_time] 
                                A_conflict_point.append(A_dict)

                                B_dict = dict()
                                B_dict['time'] = A1_time
                                B_dict['lat'] = icao_lat
                                B_dict['lon'] = icao_lon
                                B_dict['alt'] = icao_alt
                                B_dict['vel_xy'] = icao_vel_xy
                                B_dict['vel_z'] = icao_vel_z
                                B_dict['track'] = icao_track
                                B_conflict_point.append(B_dict)

                                A_point = dict()
                                A_point['time'] = A_time
                                A_point['lat'] = A_lat
                                A_point['lon'] = A_lon
                                A_point['alt'] = A_alt
                                A_point['vel_xy'] = A_velxy
                                A_point['vel_z'] = A_velz
                                A_point['track'] = A_track
                                FirstManPoint.append(A_point)

                                B_point = dict()
                                B_point['time'] = B_time
                                B_point['lat'] = B_lat
                                B_point['lon'] = B_lon
                                B_point['alt'] = B_alt
                                B_point['vel_xy'] = B_velxy
                                B_point['vel_z'] = B_velz
                                B_point['track'] = B_track
                                SecondManPoint.append(B_point)
                                
                                Maneuver = dict()
                                Maneuver["Maneuver_Type"] = Maneuver_Type
                                Maneuver["Maneuver_Act"] = Maneuver_Act
                                Maneuvers.append(Maneuver)
                                break
                    
                    if found is True:
                        break
                        
        return (second_filter, first_filter, FirstManPoint, SecondManPoint, Maneuvers, A_conflict_point, B_conflict_point, track_preds)
