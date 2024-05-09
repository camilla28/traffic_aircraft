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

    __TRACK_CHANGE_LIM = 15 #5° de mudança de direção pode determinar a
    __TRACK_CHANGE_LIM_BACK = 4 # 2°
    __TRACK_STD_INDICES = 6 # É o índice que utilizado para estabelecer o limite para std
    __TRACK_STD_LIM = 10 # É o std limite para avaliação
    __ALT_CHANGE_LIM = 650 # 1000 m de mudança de altitude
    __ALT_CHANGE_LIM_BACK = 100 # 200 m de limite para indicar um retorno à altitude de antes
    __ALT_STD_INDICES = 10 # É o índice que utilizado para estabelecer o limite para std
    __ALT_STD_LIM = 500 # É o std limite para avaliação
    
    def __init__(self, data):
        self.data = data
    

    def __search_conflicts(self, icao, response):
        airplane = self.data[icao]['cruise']

        response[icao] = dict()
        #response[icao]['man_track'] = self.det_maneuver_track(airplane.loc[:,"track"])
        response[icao]['man_track'] = []
        response[icao]['man_alt'] = self.det_maneuver_alt(airplane.loc[:,"alt"])
        #response[icao]['man_alt'] = self.detect_maneuver_alt(airplane.loc[:,"alt"], airplane.loc[:,"vel_z"])
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
    

    def __check_change_track(self, track, indice):
        t = track[track.index[indice]]
        ant_t = track[track.index[indice-1]]
        #print(indice, t, ant_t)
        response = -1

        if abs(ant_t-t) >= self.__TRACK_CHANGE_LIM:
            response = indice-1

        elif indice > self.__TRACK_STD_INDICES and \
            abs(t-track[track.index[indice-self.__TRACK_STD_INDICES]]) >= self.__TRACK_CHANGE_LIM:
            response = indice-self.__TRACK_STD_INDICES

        elif indice <= self.__TRACK_STD_INDICES and \
            abs(t-track[track.index[0]]) >= self.__TRACK_CHANGE_LIM:
            response = 0
        return response


    def det_maneuver_track(self, track):    
        A = -1
        B = -1
        C = -1
        man_conflict = []        
        for indice in range(1, len(track)):
            if A == -1 and B == -1 and C == -1: # Verifica o primeiro ponto
                A = self.__check_change_track(track, indice)
            elif A != -1 and B == -1 and C == -1: # Verifica o segundo ponto
                B = self.__check_change_track(track, indice)
            elif A != -1 and B != -1 and C == -1: # Verifica o terceiro e último ponto
                C = self.__check_change_track(track, indice)
            elif A != -1 and B != -1 and C != -1:
                resp = (A, B, C)
                man_conflict.append(resp)
                A = -1
                B = -1
                C = -1
            else:
                A = -1
                B = -1
                C = -1
        return man_conflict


    def __check_change_alt(self, alt, indice):
        if indice >= len(alt):
            return -1
        t = alt[alt.index[indice]]
        #print(indice, t, ant_t)
        response = -1

        # Se o indice for maior do que o tamanho da janela de avaliação, pega só a janela e o que está dentro dela
        if indice >= self.__ALT_STD_INDICES:
            begin = indice-self.__ALT_STD_INDICES
        # Se o indice for menor do que o tamanho da janela de avaliação, pega desde a posição zero e o
        # que vem depois dele até o indice atual
        else:
            begin = 0

        # Verifica se tem diferença em relação a todo 
        for i in range(begin, indice):
            ant_t = alt[alt.index[i]]
            if abs(t-ant_t) >= self.__ALT_CHANGE_LIM:
                response = i
                break

        return response


    def __update_indice(self, indice, response, len):
        if response == -1:
            indice = indice + 1
        else:
            if indice < len - self.__ALT_STD_INDICES:
                indice = indice + self.__ALT_STD_INDICES
            elif indice == len-1:
                indice = indice +1
            else:
                indice = len-1
        return indice


    def det_maneuver_alt(self, alt):  
        A = -1
        B = -1
        man_conflict = []        
        indice = 1
        while indice < len(alt):
            if A == -1 and B == -1: # Verifica o primeiro ponto
                A = self.__check_change_alt(alt, indice)
                indice = self.__update_indice( indice, A, len(alt))
            elif A != -1 and B == -1: # Verifica o segundo ponto
                B = self.__check_change_alt(alt, indice)
                # Identifica segundo ponto do conflito
                if B != -1:
                    B = indice
                # Update indice
                indice = self.__update_indice( indice, B, len(alt))
            else:
                A = -1
                B = -1
                indice = indice + 1
            # Verifica se encontrou os dois pontos
            if A != -1 and B != -1: 
                resp = (A, B)
                if A !=0 and B < len(alt)-1:
                    man_conflict.append(resp)
                A = -1
                B = -1
        return man_conflict    


    def detect_maneuver_track(self, track):
        indice = 0
        change_track_detected = []
        second_point_found = False
        up = []
        down = []
        print(track)
        for t in track:
            if indice !=0:
                # Verifica se entre o waypoint anterior e esse houve mudança de direção maior ou igual a
                # __TRACK_CHANGE_LIM = 25
                if abs(ant_t-t)>=self.__TRACK_CHANGE_LIM: # ou se uma sucessão dos últimos valores forem
                    
                    # É utilizado uma janela para calculo do valor de referência para o track do primeiro ponto
                    # do conflito e o desvio das amostras. Essa janela é determinada pela variável __TRACK_STD_INDICES 
                    # que é igual 6, utiliza-se sempre essa janela para determinar a média dos últimos valores 
                    # e o desvio variação dessa medida
                    if indice > self.__TRACK_STD_INDICES:
                        last_track = mean(track[track.index[indice-self.__TRACK_STD_INDICES:indice-1]])
                        last_track_std = stdev(track[track.index[indice-self.__TRACK_STD_INDICES:indice-1]])

                    # Se o indice for menor do que essa janela, então deve pegar desde o início dos dados 
                    # (índice =0)
                    else:
                        # Se o índice for 1 não é necessário fazer a média, apenas pegar o valor.
                        # E o desvio é o desvio padrão declarado.
                        if indice == 1:
                            last_track = track[track.index[0]]
                            last_track_std = self.__TRACK_STD_LIM
                        # Se o indice for maior que 1 então é necessário fazer a média até o primeiro indice.
                        # E o desvio é obtido a partir das mesmas amostras.
                        else:
                            last_track = mean(track[track.index[0]:track.index[indice-1]])
                            last_track_std = stdev(track[track.index[0]:track.index[indice-1]])
                    
                    # Para encontrar o segundo ponto, percorre-se os dados a partir da próxima posição que ainda 
                    # não foi endereçada 
                    for i in np.arange(indice+1, len(track)-1, 1):
                        # Verifica qual valor "volta" para o rumo "track" anterior a manobra do primeiro ponto:
                        # verificando se a diferença entre os tranks é inferior ao desvio das amostras ou do 
                        # desvio Default. No caso de ser verdadeiro, encontra-se o segundo ponto e salva-se o 
                        # primeiro e último ponto do desvio
                        if abs(last_track-track[track.index[i]])<=last_track_std or \
                            abs(last_track-track[track.index[i]])<=self.__TRACK_CHANGE_LIM_BACK :
                            change_track_detected.append((indice, i))
                            second_point_found = True
                            break
                    # Caso não encontra o segundo ponto, salva um None no lugar.
                    if second_point_found == False:
                        change_track_detected.append((indice, None))

                # No caso em que não encontrou diferença entre um amostra e sua anterior direta, utiliza-se uma 
                # janela de verificação, a fim de verificar se houve uma manobra realizada durante consecutivas amostras.
                
                # Neste primeiro caso o indice é maior do que o número de amostras analisadas em cada verificação 
                # (número definido por __TRACK_STD_INDICES) E o desvio entre a primeira amostra da janela e a última
                # for maior que o desvio default E a diferença entre a primeira amostra da janela e a última for 
                # maior que a mudança de rumo(track) limite.
                elif indice > self.__TRACK_STD_INDICES and \
                     stdev(track[track.index[indice-self.__TRACK_STD_INDICES]:track.index[indice]]) > self.__TRACK_STD_LIM \
                     and abs(track[track.index[indice]]-track[track.index[indice-self.__TRACK_STD_INDICES]])> self.__TRACK_CHANGE_LIM:

                    # Caso a variação seja positiva, o primeiro ponto da janela é considerada como primeiro 
                    # ponto do conflito, ou seja, o ponto onde começou a manobra.  
                    if track[track.index[indice]]-track[track.index[indice-self.__TRACK_STD_INDICES]] > self.__TRACK_CHANGE_LIM:
                        # Se a lista de primeiro pontos estiver maior do que de segundo pontos, quer dizer que não foi obtido
                        # um segundo ponto do conflito para o último conflito identificado e então deve ser armazenado o None
                        # nessa posição.
                        if len(up) > len(down):
                            down.append(None)
                        up.append(indice-self.__TRACK_STD_INDICES)
                    # Caso a variação seja negativa, o primeiro ponto da janela é considerada como segundo 
                    # ponto do conflito, ou seja, o ponto onde terminou a manobra.  
                    elif track[track.index[indice]]-track[track.index[indice-self.__TRACK_STD_INDICES]] < -1*self.__TRACK_CHANGE_LIM:
                        # Se a lista de segundos pontos estiver maior do que de primeiros pontos, quer dizer que não foi obtido
                        # um primeiro ponto do conflito para o último conflito identificado e então deve ser armazenado o None
                        # nessa posição.
                        if len(down) > len(up):
                            up.append(None)
                        down.append(indice-self.__TRACK_STD_INDICES)
                else:
                    # Se o indice for inferior ao tamanho da janela e maior que 1 e desvio entre as amostras 
                    # é maior do que o desvio default e a diferença entre o primeiro e segundo ponto é maior que 
                    # a mudança de rumo limite
                    if indice <= self.__TRACK_STD_INDICES and indice > 1 \
                        and stdev(track[track.index[0]:track.index[indice]]) > self.__TRACK_STD_LIM:
                        # and abs(track[indice]-track[indice-self.__TRACK_STD_INDICES])> self.__TRACK_CHANGE_LIM
                        
                        # Caso a diferença seja maior que a mudança de rumo limite, o primeiro ponto é o indice 0
                        if track[track.index[indice]]-track[track.index[0]] > self.__TRACK_CHANGE_LIM:
                            up.append(0)

                        # Caso contrário o segundo ponto é igual do indice 0
                        elif track[track.index[indice]]-track[track.index[0]]< -1*self.__TRACK_CHANGE_LIM:
                            down.append(0)
                    #else:
                    #    up.append(indice)
            
            else:
                up.append(indice)

            ant_t = t
            indice = indice+1
        
        while len(up) > len(down):
            down.append(None)
        while len(down) > len(up):
            up.append(None)

        # A mudança de rumo é identificada pelos dois pontos
        for i in range(0,len(up)):
            change_track_detected.append((up[i],down[i]))

        # Não é interessante ter qualquer um dos dados incluindo None, portanto essas mudanças de rumo são excluídas
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
        #print(vertical_rate)
        for t in alt:
            if indice !=0:
                if abs(ant_t-t)>=self.__ALT_CHANGE_LIM and \
                    (vertical_rate[alt.index[indice]]>20 or vertical_rate[alt.index[indice]]<-20):

                    if indice > 3:
                        last_alt = mean(alt[alt.index[indice-3:indice-1]])
                        last_alt_std = stdev(alt[alt.index[indice-3:indice-1]])

                    else:
                        last_alt = mean(alt[alt.index[0:indice-1]])
                        last_alt_std = stdev(alt[alt.index[0:indice-1]])

                    for i in np.arange(indice+1, len(alt)-1, 1):

                        if (abs(last_alt-alt[alt.index[i]])<=last_alt_std or \
                            abs(last_alt-alt[alt.index[i]])<=self.__ALT_CHANGE_LIM_BACK) and \
                            (vertical_rate[alt.index[i]]>20 or vertical_rate[alt.index[i]]<-20):
                            second_point_found = True                        
                            change_alt_detected.append((indice, i))
                            break

                    if second_point_found == False:
                        change_alt_detected.append((indice, None))

                elif indice > self.__ALT_STD_INDICES and \
                     stdev(alt[alt.index[indice-self.__ALT_STD_INDICES:indice]]) > self.__ALT_STD_LIM:
                    
                    if alt[alt.index[indice]]-alt[alt.index[indice-self.__ALT_STD_INDICES]] > self.__ALT_CHANGE_LIM:
                        while len(up) > len(down):
                            down.append(None)
                        up.append(indice-self.__ALT_STD_INDICES)

                    elif alt[alt.index[indice]]-alt[alt.index[indice-self.__ALT_STD_INDICES]] < -1*self.__ALT_CHANGE_LIM:
                        while len(down) > len(up):
                            up.append(None)
                        down.append(indice-self.__ALT_STD_INDICES)

                else:
                    if indice <= self.__ALT_STD_INDICES and indice > 1 \
                        and stdev(alt[alt.index[0:indice]]) > self.__ALT_STD_LIM:

                        if alt[alt.index[indice]]-alt[alt.index[0]] > self.__ALT_CHANGE_LIM:
                            up.append(0)

                        elif alt[alt.index[indice]]-alt[alt.index[0]]< -1*self.__ALT_CHANGE_LIM:
                            down.append(0)
                
            ant_t = t
            indice = indice+1

        while len(up) > len(down):
            down.append(None)
        while len(down) > len(up):
            up.append(None)

        for i in range(0,len(up)):
            change_alt_detected.append((up[i],down[i]))

        none_len =[x for x, y in enumerate(change_alt_detected) if y[1] == None or y[0] == None]
       
        for i in sorted(none_len, reverse=True):
            del change_alt_detected[i]

        return change_alt_detected