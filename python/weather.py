# Import Meteostat library and dependencies
from datetime import datetime, timedelta
from meteostat import Hourly, Point, Daily, Stations
from ADRpy import atmospheres as at
from ADRpy import unitconversions as co
import pandas as pd
import numpy as np
import math


def calc_speeds(waypoint):
    timestamp = waypoint[0]
    latitude = waypoint[1]
    longitude = waypoint[2]
    altitude = waypoint[3]
    track = waypoint[4]
    V_ground = waypoint[6]

    start = datetime.fromtimestamp(timestamp)
    end = datetime.fromtimestamp(timestamp) + timedelta(hours=1)

    point = Point(latitude, longitude, altitude)

    point.radius = 300000

    wind = Hourly(point, start, end)
    if wind.stations.empty != True:    
        wind = wind.normalize()
        wind = wind.interpolate()
        wind = wind.fetch()
    else:
        # Get wind direction and wind speed
        wdir = float('nan')
        index = 1
        stations = Stations()
        radius = 1000000
        stations1 = stations.nearby(latitude, longitude, radius)
        stations = stations1.fetch()
        print(stations)
        rows = stations.shape[0]

        while np.isnan(wdir) == True:
            print(stations.size)
            station = stations.iloc[index]
            print(station)
            print(type(station))
            station3 = stations.values[index]
            print(station3)
            station2 = stations1.fetch(1)
            print(station2)
            print(type(station2))

            station_df = pd.DataFrame(station)
            print(station_df)
            print(type(station_df))


            wind = Hourly(station_df, start, end)
            wind = wind.normalize()
            wind = wind.interpolate()
            wind = wind.fetch()

            index = index + 1
            
            # Get wind direction and wind speed
            wdir = wind.wdir[0]


    # Get wind direction and wind speed
    wdir = wind.wdir[0]
    wspd = wind.wspd[0]

    # Instantiate an atmosphere object: an off-standard ISA
    # with an offset, 25° is ISA
    ISA_temp = wind.temp[0] - 25
    isa = at.Atmosphere(offset_deg = ISA_temp)

    # Calculate true airspeed
    try:
        Vground_x = V_ground * math.cos(math.radians(track))
        Vground_y = V_ground * math.sin(math.radians(track))
    
        Vwind_x = wspd * math.cos(math.radians(wdir))
        Vwind_y = wspd * math.sin(math.radians(wdir))

        Vtas_x = Vground_x - Vwind_x
        Vtas_y = Vground_y - Vwind_y

        Vtas = math.sqrt(math.pow(Vtas_x,2) + math.pow(Vtas_x,2)) # Vtas/TAS (true airspeed) in m/s
        Vtas_kts = co.mps2kts(Vtas) # Convert speed value from m/s to knots

        Veas_kts = isa.tas2eas(Vtas_kts, altitude)  # Convert TAS to EAS at a given altitude.
        Veas = co.kts2mps(Veas_kts) # Convert speed value knots to m/s

        """ 
        kcas, mach = isa.keas2kcas(keas, altitude_m) -> Converts equivalent airspeed into calibrated airspeed.

        Parameters
        keas -> float or numpy array, equivalent airspeed in knots.
        altitude_m -> float, altitude in metres.

        Returns
        kcas -> float or numpy array, calibrated airspeed in knots.
        mach -> float, Mach number.
        """
        Vcas_kts, mach = isa.keas2kcas(Veas_kts, altitude)  # Converts equivalent airspeed into calibrated airspeed.
        Vcas = co.kts2mps(Vcas_kts) # Convert speed value knots to m/s

        waypoint.append(mach[0])    # waypoint[8] -  Mach Number
        waypoint.append(Vtas)       # waypoint[9] -  Vtas/TAS True airspeed m/s
        waypoint.append(Vtas_kts)   # waypoint[10] - Vtas/TAS True airspeed knots
        waypoint.append(Veas)       # waypoint[11] - Veas/EAS Equivalent airspeed m/s
        waypoint.append(Veas_kts)   # waypoint[12] - Veas/EAS Equivalent airspeed knots
        waypoint.append(Vcas[0])       # waypoint[13] - Vcas/CAS Calibrated airspeed m/s
        waypoint.append(Vcas_kts[0])   # waypoint[14] - Vcas/CAS Calibrated airspeed knots

    except Exception as inst:
        print(type(inst))    # the exception type
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,

    return  waypoint

# """ # Set time period
# data = datetime(2023, 12, 31, 00, 54, 20)
# start = data 
# end = data + timedelta(hours=1)

# #latitude = 49.2497
# #longitude = -123.1193

# latitude = 19.555256  
# longitude = -155.461759
# altitude_m = 10000

# stations = Stations()
# stations = stations.nearby(latitude, longitude)
# station = stations.fetch(1)

# # Print DataFrame
# print(station)

# # Get hourly data
# wind = Hourly(station, start, end)
# wind = wind.normalize()
# wind = wind.interpolate() 
# wind = wind.fetch()

# # Print DataFrame
# print(wind)
# print(wind.wdir)
# print(wind.wdir)
# print(wind.temp)

# # Get wind direction and wind speed
# wdir = wind.wdir[0]
# wspd = wind.wspd[0]

# # Instantiate an atmosphere object: an off-standard ISA
# # with a -10C offset
# ISA_temp = wind.temp[0]-25
# isa = at.Atmosphere(offset_deg=ISA_temp)

# # Query altitude
# #altitude_ft = 38000
# #altitude_m = co.feet2m(altitude_ft)

# # Query the ambient density in this model at the specified altitude
# print("ISA-10C density at", str(altitude_m), "m (geopotential):",
#     isa.airdens_kgpm3(altitude_m), "kg/m^3")

# # Query the speed of sound in this model at the specified altitude
# print("ISA-10C speed of sound at", str(altitude_m), "m (geopotential):",
#     isa.vsound_mps(altitude_m), "m/s")

# V_ground = 240
# track = 30
# #wdir = 5
# #wspd = 5

# # Calculate true airspeed
# Vground_x = V_ground*math.cos(math.radians(track))
# Vground_y = V_ground*math.sin(math.radians(track))

# Vwind_x = wspd*math.cos(math.radians(wdir))
# Vwind_y = wspd*math.sin(math.radians(wdir))

# Vtas_x = Vground_x - Vwind_x
# Vtas_y = Vground_y - Vwind_y

# Vtas = math.sqrt(math.pow(Vtas_x,2) + math.pow(Vtas_x,2)) # Vtas/TAS (true airspeed) in m/s
# Vtas_kts = co.mps2kts(Vtas) # Convert speed value from m/s to knots

# Veas_kts = isa.tas2eas(Vtas_kts, altitude_m)  # Convert TAS to EAS at a given altitude.
# Veas = co.kts2mps(Veas_kts) # Convert speed value knots to m/s

# """ 
# kcas, mach = isa.keas2kcas(keas, altitude_m) -> Converts equivalent airspeed into calibrated airspeed.

# Parameters
# keas -> float or numpy array, equivalent airspeed in knots.
# altitude_m -> float, altitude in metres.

# Returns
# kcas -> float or numpy array, calibrated airspeed in knots.
# mach -> float, Mach number.
# """
# Vcas_kts, mach = isa.keas2kcas(Veas_kts, altitude_m)  # Converts equivalent airspeed into calibrated airspeed.
# Vcas = co.kts2mps(Vcas_kts) # Convert speed value knots to m/s

# # """ 
# # tas = isa.eas2tas(eas, altitude_m)  -> Converts EAS to TAS(true airspeed) at a given altitude.

# # Parameters
# # eas -> Float or numpy array of floats. Equivalent airspeed (any unit, returned TAS value will be in the same unit).
# # altitude_m -> Float. Flight altitude in metres.

# # Returns
# # True airspeed in the same units as the EAS input.
# # """


# # tas = isa.eas2tas(eas, altitude_m)  # Converts EAS to TAS(true airspeed) at a given altitude.
# # mach = isa.mach(airspeed_mps, altitude_m=0)  # Mach number at a given speed (m/s) and altitude (m).
# # mpscas = isa.mpseas2mpscas(mpseas, altitude_m)  # Convert EAS (m/s) to CAS (m/s) at a given altitude (m).
# # vsound_kts = isa.vsound_kts(altitudes_m=0)  # Speed of sound in knots.
# # vsound_mps = isa.vsound_mps(altitudes_m=0)  # Speed of sound in m/s at an altitude given in m.

# print("Wind direction: ", wdir, "°")       # waypoint[9] -  Wind direction
# print("Wind speed: ", wspd, "m/s")       # waypoint[9] -  Wind speed m/s
# print("Ground speed: ", V_ground, "m/s")       # waypoint[9] -  Ground speed m/s
# print("Mach: ", mach[0])    # waypoint[8] -  Mach Number
# print("True airspeed: ", Vtas, "m/s")       # waypoint[9] -  Vtas/TAS True airspeed m/s
# print("True airspeed: ", Vtas_kts, "knots")   # waypoint[10] - Vtas/TAS True airspeed knots
# print("Equivalent airspeed: ", Veas, "m/s")       # waypoint[11] - Veas/EAS Equivalent airspeed m/s
# print("Equivalent airspeed: ", Veas_kts, "knots")   # waypoint[12] - Veas/EAS Equivalent airspeed knots
# print("Calibrated airspeed: ", Vcas[0], "m/s")       # waypoint[13] - Vcas/CAS Calibrated airspeed m/s
# print("Calibrated airspeed: ", Vcas_kts[0], "knots")   # waypoint[14] - Vcas/CAS Calibrated airspeed knots """