
from opensky_api import OpenSkyApi
import json
import time
import math

def takeTime(elem):
    return elem[0]

def distance_on_geoid(lat1, lon1, lat2, lon2) :
    
    # Convert degrees to radians
    lat1 = lat1 * math.pi / 180.0
    lon1 = lon1 * math.pi / 180.0
    lat2 = lat2 * math.pi / 180.0
    lon2 = lon2 * math.pi / 180.0
    
    # radius of earth in metres
    r = 6378100
    
    # P
    rho1 = r * math.cos(lat1)
    z1 = r * math.sin(lat1)
    x1 = rho1 * math.cos(lon1)
    y1 = rho1 * math.sin(lon1)
    
    # Q
    rho2 = r * math.cos(lat2)
    z2 = r * math.sin(lat2)
    x2 = rho2 * math.cos(lon2)
    y2 = rho2 * math.sin(lon2)
    
    # Dot product
    dot = (x1 * x2 + y1 * y2 + z1 * z2)
    cos_theta = dot / (r * r)
    theta = math.acos(cos_theta)
    
    # Distance in Metres
    return r * theta


# Write in file
datestr = time.strftime("%Y%m%d")

data_path = "data\\"+datestr

testFileName = data_path + "\\" + datestr + ".json"

data_dict_sorted = dict()

with open(testFileName,  "r") as read_file:
                
    data_dict = json.load(read_file)
    icao_list = list(data_dict.keys())

    for icao in icao_list:

        data_dict_sorted[icao] = sorted(data_dict[icao], key=takeTime)

        last_waypoint = data_dict_sorted[icao][0]

        index = 0
        for waypoint in data_dict_sorted[icao]:
            
            if index !=0:
                # Return time difference (seconds)
                time_diff = waypoint[0] - last_waypoint[0]
                
                if time_diff > 0 and len(waypoint) < 7:

                    # Calculate speed
                    lat_diff = waypoint[1] - last_waypoint[1]
                    long_diff = waypoint[2] - last_waypoint[2]
                    d_distante = distance_on_geoid(last_waypoint[1], last_waypoint[2], waypoint[1], waypoint[2])
                    speed = d_distante/time_diff
                    waypoint.append(speed)

                    # Calculate vertical rate
                    alt_diff = waypoint[3] - last_waypoint[3]
                    vertical_rate = alt_diff / time_diff
                    waypoint.append(vertical_rate)

            index = index + 1
            last_waypoint = waypoint
    
with open(data_path + "\\" + datestr + "_sorted.json", "w") as outfile:
    json.dump(data_dict_sorted, outfile)