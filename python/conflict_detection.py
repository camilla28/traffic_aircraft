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
from geopy import distance



class Conflict_Detection:

    TRACK_CHANGE_LIM = 15 #5° de mudança de direção pode determinar a
    TRACK_FRAME_INDICES = 5 # É o tamanho do frame que é avaliado se houve a mudança de rumo (10)
    TRACK_STD_LIM = 2 # É o std limite para avaliação
    ALT_CHANGE_LIM = 600 # 650 m de mudança de altitude (houve uma mudança de altitude de 650 m)
    ALT_FRAME_INDICES = 10 # É o tamanho do frame que é avaliado se houve a mudança de altitude (7)
    ALT_STD_LIM = 50 # É o tamanho do frame que é avaliado se houve a mudança de altitude (7)
    SPEED_CHANGE_LIM = 100 #30 m/s de mudança de velocidade (houve uma mudança de velocidade de 30 m/s)
    SPEED_STD_LIM = 10 # Determina o range de speed para indicação do fim da manobra valor da velocidde, velocidade +/-10 é o range
    SPEED_FRAME_INDICES = 6 # É o tamanho do frame que é avaliado se houve a mudança de altitude 
    __SPEED_STD_FILTER = 45 # As amostras que continham umm std maior do que 45, tinham uma variação nã natural (Coletar esse caso)
    __SPEED_LIM_MAX = 400 # Filtra pela velocidade, não faz sentido as amostras terem uma velocidade acima de 400 m/s
    #ALT_FRAME_INDICES = 10 # É o índice que utilizado para estabelecer o limite para std
    
    def __init__(self, data= None):
        self.data = data
    
    
    def analysis_filters(self, icao_list):
        high_spd_filter = 0
        std_spd_filter = 0
        response = dict()

        for icao in icao_list:
            airplane = self.data[icao]['cruise']

            if len(airplane.loc[:,"vel_xy"]) > 0 and abs(max(airplane.loc[:,"vel_xy"])) > self.__SPEED_LIM_MAX:
                high_spd_filter = high_spd_filter + 1
    
            # if len(airplane.loc[:,"vel_xy"]) > 2 and stdev(airplane.loc[:,"vel_xy"])> self.__SPEED_STD_FILTER:
            #     std_spd_filter = std_spd_filter + 1

        response['high_spd_filter'] = high_spd_filter
        response['std_spd_filter'] = std_spd_filter
        
        return response

    def __search_conflicts(self, icao, response, args):
        airplane = self.data[icao]['cruise']
        response[icao] = dict()
        
        alt_frame_indices = self.ALT_FRAME_INDICES if args['alt_frame_indices'] == None else args['alt_frame_indices'] 
        alt_change_lim = self.ALT_CHANGE_LIM if args['alt_change_lim'] == None else args['alt_change_lim']
        alt_std_lim = self.ALT_STD_LIM if args['alt_std_lim'] == None else args['alt_std_lim']

        track_frame_indices = self.TRACK_FRAME_INDICES if args['track_frame_indices'] == None else args['track_frame_indices'] 
        track_change_lim = self.TRACK_CHANGE_LIM if args['track_change_lim'] == None else args['track_change_lim']
        track_std_lim = self.TRACK_STD_LIM if args['track_std_lim'] == None else args['track_std_lim']
        
        speed_frame_indices = self.SPEED_FRAME_INDICES if args['speed_frame_indices'] == None else args['speed_frame_indices'] 
        speed_change_lim = self.SPEED_CHANGE_LIM if args['speed_change_lim'] == None else args['speed_change_lim']
        speed_std_lim = self.SPEED_STD_LIM if args['speed_std_lim'] == None else args['speed_std_lim']
        

        # Apenas com velocidades menores que 400 m/s      
        if len(airplane.loc[:,"vel_xy"]) > 0 and abs(max(airplane.loc[:,"vel_xy"])) < self.__SPEED_LIM_MAX:              
            response[icao]['man_alt'] = self.det_maneuver_alt(airplane.loc[:,"alt"], alt_frame_indices, alt_change_lim, alt_std_lim)
            response[icao]['man_speed'] = self.det_maneuver_speed(airplane.loc[:,"vel_xy"], speed_frame_indices, speed_change_lim, speed_std_lim)
            response[icao]['man_track'] = self.det_maneuver_track(airplane.loc[:,"track"], track_frame_indices, track_change_lim, track_std_lim)
            
            if len(response[icao]['man_track'])!=0 or len(response[icao]['man_alt'])!=0 or len(response[icao]['man_speed'])!=0:
                response[icao]['conflict'] = True
            else:
                response[icao]['conflict'] = False

        else:
            response[icao]['man_alt'] = []
            response[icao]['man_speed'] = []
            response[icao]['man_track'] = []
            response[icao]['conflict'] = False

        return response   


    def search_conflicts(self, args, icao = None):
        response = dict()

        if icao != None:
            response = self.__search_conflicts(icao, response, args)
        else:
            icao_list = list(self.data.keys())
            for icao in icao_list:
                response = self.__search_conflicts(icao, response, args)
        return response
    

    def __check_change_speed(self, speed, indice, speed_frame_indices, speed_change_lim):
        # if indice >= len(speed):
        #     return -1
        spd = speed[speed.index[indice]]
        #print(indice, t, ant_t)
        response = -1

        # Se o indice for maior do que o tamanho da janela de avaliação, pega só a janela e o que está dentro dela
        if indice >= speed_frame_indices:
            begin = indice - speed_frame_indices
        # Se o indice for menor do que o tamanho da janela de avaliação, pega desde a posição zero e o
        # que vem depois dele até o indice atual
        else:
            begin = 0

        # Verifica se tem diferença em relação a todo 
        for i in range(begin, indice):
            ant_spd = speed[speed.index[i]]
            if abs(spd-ant_spd) >= speed_change_lim:
                response = i
                break

        return response
    

    def __check_change_alt(self, alt, indice, alt_frame_indices, alt_change_lim):
        # if indice >= len(alt):
        #     return -1
        altitude = alt[alt.index[indice]]
        #print(indice, t, ant_t)
        response = -1

        # Se o indice for maior do que o tamanho da janela de avaliação, pega só a janela e o que está dentro dela
        if indice >= alt_frame_indices:
            begin = indice - alt_frame_indices
        # Se o indice for menor do que o tamanho da janela de avaliação, pega desde a posição zero e o
        # que vem depois dele até o indice atual
        else:
            begin = 0

        # Verifica se tem diferença em relação a todo 
        for i in range(begin, indice):
            ant_altitude = alt[alt.index[i]]
            if abs(altitude - ant_altitude) >= alt_change_lim:
                response = i
                break

        return response
        


    def __check_change_track(self, track, indice, track_frame_indices, track_change_lim):
        # if indice >= len(track):
        #     return -1
        ref_track = track[track.index[indice]]
        #print(indice, t, ant_t)
        response = -1

        # Se o indice for maior do que o tamanho da janela de avaliação, pega só a janela e o que está dentro dela
        if indice >= track_frame_indices:
            begin = indice - track_frame_indices
        # Se o indice for menor do que o tamanho da janela de avaliação, pega desde a posição zero e o
        # que vem depois dele até o indice atual
        else:
            begin = 0

        # Verifica se tem diferença em relação a todo 
        for i in range(begin, indice):
            ant_track = track[track.index[i]]
            if abs(ref_track-ant_track) >= track_change_lim:
                response = i
                break

        return response



    def __update_indice(self, indice, response, length, frame_len):
        if response == -1:
            indice = indice + 1
        else:
            if indice < length - frame_len:
                indice = indice + frame_len # talvez deveria ser response + frame_len
            elif indice == length - 1:
                indice = indice +1
            else:
                indice = length - 1
        return indice



    def det_maneuver_alt(self, alt, alt_frame_indices, alt_change_lim, alt_std_lim):  
        A = -1
        B = -1
        man_conflict = []        
        indice = 1

        while indice < len(alt):
            if A == -1 and B == -1: # Verifica o primeiro ponto
                A = self.__check_change_alt(alt, indice, alt_frame_indices, alt_change_lim)
                indice = self.__update_indice(indice, A, len(alt), alt_frame_indices)
                alt_ref = alt[alt.index[A]]
            elif A != -1 and B == -1: # Verifica o segundo ponto
                if alt[alt.index[indice]] <= alt_ref + alt_std_lim and \
                   alt[alt.index[indice]] >= alt_ref - alt_std_lim:
                    B = indice
                # Update indice
                indice = self.__update_indice(indice, B, len(alt), alt_frame_indices)
            else:
                A = -1
                B = -1
                indice = indice + 1
            # Verifica se encontrou os dois pontos
            if A != -1 and B != -1: 
                if A !=0 and B < len(alt)-1:
                    # Verifica se o começo da resolução do conflito é positivo ou não 
                    if alt[A+1] - alt[A] > 0:
                        resp = (A, B, 1)
                    else:
                        resp = (A, B, -1)

                    man_conflict.append(resp)
                A = -1
                B = -1
        return man_conflict    



    def det_maneuver_speed(self, speed, speed_frame_indices, speed_change_lim, speed_std_lim):  
        A = -1
        B = -1
        man_conflict = []        
        indice = 1

        # Filtra pela velocidade, não faz sentido as amostras terem uma velocidade acima de 400 m/s
        if len(speed) > 0 and abs(max(speed)) > self.__SPEED_LIM_MAX: # Precisa deixar isso no tratamentodo dado, não na obtenção do conflito
            return man_conflict
        # Filtra pelo desvio... quando tem muita variação a amostra não faz mt sentido (pegar quanto por cento das amostras caem aqui)
        # Verifica se o tamanho é maior que 2 para poder obter utilizar o stdev
        # if len(speed) > 2 and stdev(speed)> self.__SPEED_STD_FILTER: 
        #     return man_conflict
        
        while indice < len(speed):
            # Verifica o primeiro ponto
            if A == -1 and B == -1: 
                A = self.__check_change_speed(speed, indice, speed_frame_indices, speed_change_lim)
                indice = self.__update_indice(indice, A, len(speed), speed_frame_indices)
                speed_ref = speed[speed.index[A]]
            # Verifica o segundo ponto, se a velocidade for próxima da última velocidade dentro de uma faixa
            elif A != -1 and B == -1: 
                if speed[speed.index[indice]] <= speed_ref + speed_std_lim and \
                speed[speed.index[indice]] >= speed_ref - speed_std_lim:
                    B = indice
                # Update indice
                indice = self.__update_indice(indice, B, len(speed), speed_frame_indices)
            else:
                A = -1
                B = -1
                indice = indice + 1
            # Verifica se encontrou os dois pontos
            if A != -1 and B != -1: 
                if A !=0 and B < len(speed)-1:
                    resp = (A, B)
                    # Verifica se o começo da resolução do conflito é positivo ou não 
                    if speed[A+1] - speed[A] > 0:
                        resp = (A, B, 1)
                    else:
                        resp = (A, B, -1)

                    man_conflict.append(resp)
                A = -1
                B = -1
        return man_conflict 


    def det_maneuver_track(self, track, track_frame_indices, track_change_lim, track_std_lim):  
        A = -1
        B = -1
        man_conflict = []        
        indice = 1

        while indice < len(track):
            # Verifica o primeiro ponto
            if A == -1 and B == -1: 
                A = self.__check_change_track(track, indice, track_frame_indices, track_change_lim)
                track_ref = track[track.index[indice]]
                indice = self.__update_indice(indice, A, len(track), track_frame_indices)
            # Verifica o segundo ponto, se a velocidade for próxima da última velocidade dentro de uma faixa
            elif A != -1 and B == -1: 
                if track[track.index[indice]] <= track_ref + track_std_lim and \
                track[track.index[indice]] >= track_ref - track_std_lim:
                    B = indice
                # Update indice
                indice = self.__update_indice(indice, B, len(track), track_frame_indices)
            else:
                A = -1
                B = -1
                indice = indice + 1
            # Verifica se encontrou os dois pontos
            if A != -1 and B != -1: 
                if A !=0 and B < len(track)-1:
                    # Verifica se o começo da resolução do conflito é positivo ou não 
                    # Left -> 1
                    # Right -> -1
                    if track[A+1] - track[A] > 0:
                        resp = (A, B, 1)
                    else:
                        resp = (A, B, -1)
                    man_conflict.append(resp)
                A = -1
                B = -1
        # i = 0
        # for i in len(man_conflict):
        #     if
        return man_conflict 



    def __update_indice_track(self, indice, response, len):
        if response == -1:
            indice = indice + 1
        else:
            if indice < len - self.__TRACK_STD_INDICES:
                indice = indice + self.__TRACK_STD_INDICES
            elif indice == len-1:
                indice = indice +1
            else:
                indice = len-1
        return indice
    


    # def detect_maneuver_track(self, track):
    #     indice = 0
    #     change_track_detected = []
    #     second_point_found = False
    #     up = []
    #     down = []
    #     #print(track)
    #     for t in track:
    #         if indice !=0:
    #             # Verifica se entre o waypoint anterior e esse houve mudança de direção maior ou igual a
    #             # TRACK_CHANGE_LIM = 25
    #             if abs(ant_t-t)>=self.TRACK_CHANGE_LIM: # ou se uma sucessão dos últimos valores forem
                    
    #                 # É utilizado uma janela para calculo do valor de referência para o track do primeiro ponto
    #                 # do conflito e o desvio das amostras. Essa janela é determinada pela variável __TRACK_STD_INDICES 
    #                 # que é igual 6, utiliza-se sempre essa janela para determinar a média dos últimos valores 
    #                 # e o desvio variação dessa medida
    #                 if indice > self.__TRACK_STD_INDICES:
    #                     last_track = mean(track[track.index[indice-self.__TRACK_STD_INDICES:indice-1]])
    #                     last_track_std = stdev(track[track.index[indice-self.__TRACK_STD_INDICES:indice-1]])

    #                 # Se o indice for menor do que essa janela, então deve pegar desde o início dos dados 
    #                 # (índice =0)
    #                 else:
    #                     # Se o índice for 1 não é necessário fazer a média, apenas pegar o valor.
    #                     # E o desvio é o desvio padrão declarado.
    #                     if indice == 1:
    #                         last_track = track[track.index[0]]
    #                         last_track_std = self.TRACK_STD_LIM
    #                     # Se o indice for maior que 1 então é necessário fazer a média até o primeiro indice.
    #                     # E o desvio é obtido a partir das mesmas amostras.
    #                     else:
    #                         last_track = mean(track[track.index[0]:track.index[indice-1]])
    #                         last_track_std = stdev(track[track.index[0]:track.index[indice-1]])
                    
    #                 # Para encontrar o segundo ponto, percorre-se os dados a partir da próxima posição que ainda 
    #                 # não foi endereçada 
    #                 for i in np.arange(indice+1, len(track)-1, 1):
    #                     # Verifica qual valor "volta" para o rumo "track" anterior a manobra do primeiro ponto:
    #                     # verificando se a diferença entre os tranks é inferior ao desvio das amostras ou do 
    #                     # desvio Default. No caso de ser verdadeiro, encontra-se o segundo ponto e salva-se o 
    #                     # primeiro e último ponto do desvio
    #                     if abs(last_track-track[track.index[i]])<=last_track_std or \
    #                         abs(last_track-track[track.index[i]])<=self.TRACK_CHANGE_LIM_BACK :
    #                         change_track_detected.append((indice, i))
    #                         second_point_found = True
    #                         break
    #                 # Caso não encontra o segundo ponto, salva um None no lugar.
    #                 if second_point_found == False:
    #                     change_track_detected.append((indice, None))

    #             # No caso em que não encontrou diferença entre um amostra e sua anterior direta, utiliza-se uma 
    #             # janela de verificação, a fim de verificar se houve uma manobra realizada durante consecutivas amostras.
                
    #             # Neste primeiro caso o indice é maior do que o número de amostras analisadas em cada verificação 
    #             # (número definido por __TRACK_STD_INDICES) E o desvio entre a primeira amostra da janela e a última
    #             # for maior que o desvio default E a diferença entre a primeira amostra da janela e a última for 
    #             # maior que a mudança de rumo(track) limite.
    #             elif indice > self.__TRACK_STD_INDICES and \
    #                  stdev(track[track.index[indice-self.__TRACK_STD_INDICES]:track.index[indice]]) > self.TRACK_STD_LIM \
    #                  and abs(track[track.index[indice]]-track[track.index[indice-self.__TRACK_STD_INDICES]])> self.TRACK_CHANGE_LIM:

    #                 # Caso a variação seja positiva, o primeiro ponto da janela é considerada como primeiro 
    #                 # ponto do conflito, ou seja, o ponto onde começou a manobra.  
    #                 if track[track.index[indice]]-track[track.index[indice-self.__TRACK_STD_INDICES]] > self.TRACK_CHANGE_LIM:
    #                     # Se a lista de primeiro pontos estiver maior do que de segundo pontos, quer dizer que não foi obtido
    #                     # um segundo ponto do conflito para o último conflito identificado e então deve ser armazenado o None
    #                     # nessa posição.
    #                     if len(up) > len(down):
    #                         down.append(None)
    #                     up.append(indice-self.__TRACK_STD_INDICES)
    #                 # Caso a variação seja negativa, o primeiro ponto da janela é considerada como segundo 
    #                 # ponto do conflito, ou seja, o ponto onde terminou a manobra.  
    #                 elif track[track.index[indice]]-track[track.index[indice-self.__TRACK_STD_INDICES]] < -1*self.TRACK_CHANGE_LIM:
    #                     # Se a lista de segundos pontos estiver maior do que de primeiros pontos, quer dizer que não foi obtido
    #                     # um primeiro ponto do conflito para o último conflito identificado e então deve ser armazenado o None
    #                     # nessa posição.
    #                     if len(down) > len(up):
    #                         up.append(None)
    #                     down.append(indice-self.__TRACK_STD_INDICES)
    #             else:
    #                 # Se o indice for inferior ao tamanho da janela e maior que 1 e desvio entre as amostras 
    #                 # é maior do que o desvio default e a diferença entre o primeiro e segundo ponto é maior que 
    #                 # a mudança de rumo limite
    #                 if indice <= self.__TRACK_STD_INDICES and indice > 1 \
    #                     and stdev(track[track.index[0]:track.index[indice]]) > self.TRACK_STD_LIM:
    #                     # and abs(track[indice]-track[indice-self.__TRACK_STD_INDICES])> self.TRACK_CHANGE_LIM
                        
    #                     # Caso a diferença seja maior que a mudança de rumo limite, o primeiro ponto é o indice 0
    #                     if track[track.index[indice]]-track[track.index[0]] > self.TRACK_CHANGE_LIM:
    #                         up.append(0)

    #                     # Caso contrário o segundo ponto é igual do indice 0
    #                     elif track[track.index[indice]]-track[track.index[0]]< -1*self.TRACK_CHANGE_LIM:
    #                         down.append(0)
    #                 #else:
    #                 #    up.append(indice)
            
    #         else:
    #             up.append(indice)

    #         ant_t = t
    #         indice = indice+1
        
    #     while len(up) > len(down):
    #         down.append(None)
    #     while len(down) > len(up):
    #         up.append(None)

    #     # A mudança de rumo é identificada pelos dois pontos
    #     for i in range(0,len(up)):
    #         change_track_detected.append((up[i],down[i]))

    #     # Não é interessante ter qualquer um dos dados incluindo None, portanto essas mudanças de rumo são excluídas
    #     none_len =[x for x, y in enumerate(change_track_detected) if y[1] == None or y[0] == None]
    #     for i in sorted(none_len, reverse=True):
    #         del change_track_detected[i]

    #     return change_track_detected
    


    # def det_maneuver_track(self, track, lat, lon):
    #     man_conflict = []        
    #     indice = self.__TRACK_STD_INDICES
    #     while indice < len(track):
    #         exit_point = indice 
    #         entry_point = exit_point - self.__TRACK_STD_INDICES
    #         delta = math.atan2(lat[exit_point]-lat[entry_point],lon[exit_point]-lon[entry_point])
    #         if delta >= 0:
    #             course = delta
    #         else:
    #             course = 2*math.pi + delta
    #         delta_course = course - track[entry_point]

    #         if abs(delta_course) > self.TRACK_CHANGE_LIM:
    #             resp = (entry_point, exit_point)
    #             man_conflict.append(resp)
    #             indice = self.__update_indice(indice, exit_point, len(track), self.TRACK_FRAME_INDICES)
    #             # indice = self.__update_indice_track(indice, exit_point, len(track))
            
    #         else:
    #             indice = self.__update_indice(indice, -1, len(track), self.TRACK_FRAME_INDICES)
    #             # indice = self.__update_indice_track(indice, -1, len(track))
        
    #     return man_conflict


    # def det_maneuver_alt_old(self, alt):  
    #     A = -1
    #     B = -1
    #     man_conflict = []        
    #     indice = 1
    #     while indice < len(alt):
    #         if A == -1 and B == -1: # Verifica o primeiro ponto
    #             A = self.__check_change_alt(alt, indice)
    #             indice = self.__update_indice( indice, A, len(alt))
    #         elif A != -1 and B == -1: # Verifica o segundo ponto
    #             B = self.__check_change_alt(alt, indice)
    #             # Identifica segundo ponto do conflito
    #             if B != -1:
    #                 B = indice
    #             # Update indice
    #             indice = self.__update_indice( indice, B, len(alt))
    #         else:
    #             A = -1
    #             B = -1
    #             indice = indice + 1
    #         # Verifica se encontrou os dois pontos
    #         if A != -1 and B != -1: 
    #             resp = (A, B)
    #             if A !=0 and B < len(alt)-1:
    #                 man_conflict.append(resp)
    #             A = -1
    #             B = -1
    #     return man_conflict 


    # def det_maneuver_speed_2(self, speed, lat, lon):  
    #     A = -1
    #     B = -1
    #     man_conflict = []        
    #     indice = 0
    #     #high_speed = speed[speed>1000]
    #     high_speed = list(filter(lambda x: x > 400, speed))

    #     if len(high_speed) > 0:
    #         return man_conflict
    #     elif len(speed)>2 and stdev(speed)>45:
    #         return man_conflict

    #     ref_speed = 0

    #     while indice < len(speed)-5:
            
    #         travel_time = 5 # 5 minutes

    #         entry = (lat[indice], lon[indice])
    #         exit = (lat[indice+5-1], lon[indice+5-1])
    #         travel_dist = distance.distance(entry, exit).meters

    #         Max_GSpeed = 2*travel_dist/travel_time - speed[indice]
    #         Gspeed_Rate = (Max_GSpeed - speed[indice])/travel_time/60

    #         if abs(Gspeed_Rate) > 0.017:
    #             A = indice
    #             ref_speed = speed[indice]

    #             B_indice = indice + 5
    #             while B_indice < len(speed):

    #                 if speed[B_indice] < ref_speed + 10 and speed[B_indice] > ref_speed - 10:
    #                     B = B_indice
    #                     resp = (A, B)
    #                     man_conflict.append(resp)
    #                     indice = B_indice -1
    #                     break

    #                 B_indice = B_indice + 1

    #         # Update indice
    #         indice = indice + 1

    #     return man_conflict 

    

    # def __check_change_track(self, track, indice):
    #     t = track[track.index[indice]]
    #     ant_t = track[track.index[indice-1]]
    #     #print(indice, t, ant_t)
    #     response = -1

    #     if abs(ant_t-t) >= self.TRACK_CHANGE_LIM:
    #         response = indice-1

    #     elif indice > self.__TRACK_STD_INDICES and \
    #         abs(t-track[track.index[indice-self.__TRACK_STD_INDICES]]) >= self.TRACK_CHANGE_LIM:
    #         response = indice-self.__TRACK_STD_INDICES

    #     elif indice <= self.__TRACK_STD_INDICES and \
    #         abs(t-track[track.index[0]]) >= self.TRACK_CHANGE_LIM:
    #         response = 0
    #     return response


    # def det_maneuver_track(self, track):    
    #     A = -1
    #     B = -1
    #     C = -1
    #     man_conflict = []        
    #     for indice in range(1, len(track)):
    #         if A == -1 and B == -1 and C == -1: # Verifica o primeiro ponto
    #             A = self.__check_change_track(track, indice)
    #         elif A != -1 and B == -1 and C == -1: # Verifica o segundo ponto
    #             B = self.__check_change_track(track, indice)
    #         elif A != -1 and B != -1 and C == -1: # Verifica o terceiro e último ponto
    #             C = self.__check_change_track(track, indice)
    #         elif A != -1 and B != -1 and C != -1:
    #             resp = (A, B, C)
    #             man_conflict.append(resp)
    #             A = -1
    #             B = -1
    #             C = -1
    #         else:
    #             A = -1
    #             B = -1
    #             C = -1
    #     return man_conflict