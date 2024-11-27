class Conflict:
    def __init__(self, Aircraft_A_Name, Aircraft_B_Name, Conflict_Point = None, Maneuver = None):
        self.set_Aircraft_A_Name(Aircraft_A_Name)
        self.set_Aircraft_B_Name(Aircraft_B_Name)
        self.__Conflict_Point = Conflict_Point
        self.__Maneuver = Maneuver

    def set_Maneuver(self, ICAO, Initial_Point, Final_Point):
        self.__Maneuver = Maneuver(ICAO, Initial_Point, Final_Point)

    def set_Aircraft_A_Name(self, Aircraft_A_Name):
        self.__Aircraft_A_Name = Aircraft_A_Name

    def set_Aircraft_B_Name(self, Aircraft_B_Name):
        self.__Aircraft_B_Name = Aircraft_B_Name

    def set_Conflict_Point(self, time, lat, lon, alt, speed, vel_z, track):
        self.__Conflict_Point = Point(time, lat, lon, alt, speed, vel_z, track)

    def get_Maneuver(self):
        return self.__Maneuver

    def get_Aircraft_A_Name(self):
        return self.__Aircraft_A_Name

    def get_Aircraft_B_Name(self):
        return self.__Aircraft_B_Name

    def get_Conflict_Point(self):
        return self.__Conflict_Point


class Maneuver:
    
    # Type of Maneuver
    BEFORE = 1
    PATHSTEP = 2
    OVER = 3
    SEPHORIZ = 4
    FIXHPATH = 5
    FIXPATH = 6

    def __init__(self, ICAO, Type, Initial_Point = None, Final_Point= None):
        self.set_ICAO(ICAO)
        self.set_Type(Type)
        self.__Initial_Point = Initial_Point
        self.__Final_Point = Final_Point

    def set_ICAO(self, ICAO):
        self.__ICAO = ICAO

    def set_Type(self, Type):
        self.__Type = Type

    def set_Initial_Point(self, time, lat, lon, alt, speed, vel_z, track):
        self.__Initial_Point = Point(time, lat, lon, alt, speed, vel_z, track)

    def set_Final_Point(self, time, lat, lon, alt, speed, vel_z, track):
        self.__Final_Point = Point(time, lat, lon, alt, speed, vel_z, track)

    def get_ICAO(self):
        return self.__ICAO

    def set_Type(self):
        return self.__Type

    def get_Initial_Point(self):
        return self.__Initial_Point

    def get_Final_Point(self):
        return self.__Final_Point


class Point:
    def __init__(self, time, lat, lon, alt, speed, vel_z, track):
        self.set_time(time)
        self.set_latitude(lat)
        self.set_longitude(lon)
        self.set_altitude(alt)
        self.set_speed(speed)
        self.set_velZ(vel_z)
        self.set_track(track)

    def set_track(self, track):
        self.__track = track

    def set_velZ(self, vel_z):
        self.__vel_z = vel_z

    def set_speed(self, speed):
        self.__speed = speed

    def set_altitude(self, alt):
        self.__alt = alt

    def set_longitude(self, lon):
        self.__lon = lon

    def set_latitude(self, lat):
        self.__lat = lat

    def set_time(self, time):
        self.__time = time

    def get_track(self):
        return self.__track

    def get_velZ(self):
        return self.__vel_z

    def get_speed(self):
        return self.__speed

    def get_altitude(self):
        return self.__alt

    def get_longitude(self):
        return self.__lon

    def set_latitude(self):
        return self.__lat

    def set_time(self):
        return self.__time
