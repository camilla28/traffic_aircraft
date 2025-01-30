# Traffic Aircraft Project

## Dataset
Each conflict is composed of the following information in this order:

**Date:** Is the date in format YYYYMMDD. The value can be 20230511, 20230520, 20230522, 20230526, 20230527, 20230528, 20230529, 20230530, 20230724, 20230727, 20230821, 20240528, 20240529, 20240603, 20240604, 20240605, 20240607, 20240611, 20240612, 20240614, 20240615

**NumAeronaves:** Is the number of aircraft per day

**Aircraft A:** ICAO identification of aircraft A

**Aircraft A Ini Man Time:** Time in initial waypoint of maneuver executed by aircraft A

**Aircraft A Ini Man Lat:** Latitude in initial waypoint of maneuver executed by aircraft A

**Aircraft A Ini Man Lon:** Longitude in initial waypoint of maneuver executed by aircraft A

**Aircraft A Ini Man Alt:** Altitude in initial waypoint of maneuver executed by aircraft A im meters

**Aircraft A Ini Man Vel_xy:** Ground speed in initial waypoint of maneuver executed by aircraft A in m/s

**Aircraft A Ini Man Vel_z:** Vertical rate in initial waypoint of maneuver executed by aircraft A in m/s

**Aircraft A Ini Man Track:** Track in initial waypoint of maneuver executed by aircraft A in degrees

**Speed Maneuver:** Classification of maneuver. Can be -1, 1, or 0.

**Altitude Maneuver:** Classification of maneuver. Can be -1, 1, or 0.

**Track Maneuver:** Classification of maneuver. Can be -1, ,1 or 0.

**Aircraft A End Man Time:** Time in end waypoint of maneuver executed by aircraft A

**Aircraft A End Man Lat:** Latitude in end waypoint of maneuver executed by aircraft A

**Aircraft A End Man Lon:** Longitude in end waypoint of maneuver executed by aircraft A

**Aircraft A End Man Alt:** Altitude in end waypoint of maneuver executed by aircraft A im meters

**Aircraft A End Man Vel_xy:** Ground speed in end waypoint of maneuver executed by aircraft A in m/s

**Aircraft A End Man Vel_z:** Vertical rate in end waypoint of maneuver executed by aircraft A in m/s

**Aircraft A End Man Track:** Track in end waypoint of maneuver executed by aircraft A in degrees

**Aircraft A Conflict Time:** Time in end waypoint of conflict identified by aircraft A

**Aircraft A Conflict Lat:** Latitude in end waypoint of conflict identified by aircraft A

**Aircraft A Conflict Lon:** Longitude in end waypoint of conflict identified by aircraft A

**Aircraft A Conflict Alt:** Altitude in end waypoint of conflict identified by aircraft A in meters

**Aircraft A Conflict Vel_xy:** Ground speed in end waypoint of conflict identified by aircraft A in m/s

**Aircraft A Conflict Vel_z:** Vertical rate in end waypoint of conflict identified by aircraft A in m/s

**Aircraft A Conflict Track:** Track in end waypoint of conflict identified by aircraft A in degrees

**Aircraft B:** ICAO identification of aircraft B (the second aircraft in conflict)

**Aircraft B Conflict Time:** Time in end waypoint of conflict identified by aircraft B

**Aircraft B Conflict Lat:** Latitude in end waypoint of conflict identified by aircraft B

**Aircraft B Conflict Lon:** Longitude in end waypoint of conflict identified by aircraft B

**Aircraft B Conflict Alt:** Altitude in end waypoint of conflict identified by aircraft B in meters

**Aircraft B Conflict Vel_xy:** Ground speed in end waypoint of conflict identified by aircraft B in m/s

**Aircraft B Conflict Vel_z:** Vertical rate in end waypoint of conflict identified by aircraft B in m/s

**Aircraft B Conflict Track:** Track in end waypoint of conflict identified by aircraft B in degrees


## Function

To use the plot function just navigate to the python level and write the following code in the prompt. If there is no argument, all the days in dataset conflicts are plotted:
```
python run_plot.py
```
But days can be used as arguments. Only the days informed as argument are plotted: 
```
python run_plot.py 20230727 20240612
```
