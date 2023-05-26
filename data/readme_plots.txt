Em plots tem:

"I062/105": Data Item I062/105, Calculated Position In WGS-84 Co-ordinates. Definition : 
Calculated Position in WGS-84 Co-ordinates with a resolution of 180/(2^25) degrees. 
(Latitude) In WGS.84 in two’s complement (Range -90 ≤ latitude ≤ 90 deg). 
(Longitude) In WGS.84 in two’s complement (Range -180 ≤ longitude < 180 deg).  

"I062/136": Last valid and credible flight level used to update the track, in
two’s complement form.

"I062/185": Calculated track velocity expressed in Cartesian co-ordinates,
in two’s complement form.

"I062/200": Calculated Mode of Movement of a target.
            "trans": Transversal Acceleration :
                    = 0 Constant Course
                    = 1 Right Turn
                    = 2 Left Turn
                    = 3 Undetermined 
            "long": Longitudinal Acceleration :
                    = 0 Constant Groundspeed
                    = 1 Increasing Groundspeed
                    = 2 Decreasing Groundspeed
                    = 3 Undetermined
            "vert": Vertical Rate :
                    = 0 Level
                    = 1 Climb
                    = 2 Descent
                    = 3 Undetermined  
            "adf": Altitude Discrepancy Flag (The ADF, if set, indicates that a difference 
            has been detected in the altitude information derived from radar as compared 
            to other technologies (such as ADS-B))
                    = 0 No altitude discrepancy
                    = 1 Altitude discrepancy

"I062/220": Calculated rate of Climb/Descent of an aircraft in two’s
complement form. A positive value indicates a climb, whereas a negative value
indicates a descent.

"I062/380": Data derived directly by the aircraft. This includes data transmitted
via Mode-S and ADS-B.

    "subitem13": Barometric Vertical Rate
    {
        "baro_vert_rate": 3037.5
    },

    "subitem26": Indicated Airspeed (0 Kt ≤ Indicated Airspeed ≤ 1100 Kt)
    {
        "ias": 307
    },

    "subitem27": Mach Number (0 ≤ Mach Number ≤ 4.096 )
    {
        "mach": 0.6
    },

    "subitem3": {
        "mag_hdg": Magnetic Heading
    },

    "subitem6": The short-term vertical intent as described by either the FMS
    selected altitude, the Altitude Control Panel Selected Altitude
    (FCU/MCP), or the current aircraft altitude according to the
    aircraft's mode of flight.
    {
        "altitude": 25000, (-1300ft ≤ Altitude ≤ 100000ft 
        "sas": (SAS) = 0 No source information provided
                     = 1 Source Information provided 
        "source": (Source) = 0 Unknown
                           = 1 Aircraft Altitude
                           = 2 FCU/MCP Selected Altitude
                           = 3 FMS Selected Altitude
    },
    
    "subitem7": The vertical intent value that corresponds with the ATC cleared
    altitude, as derived from the Altitude Control Panel (FCU/MCP). 
    {
        "ah": false, (AH) Altitude Hold
                        = 0 Not active
                        = 1 Active 
        "altitude": 25000, (-1300ft ≤ Altitude ≤ 100000ft)
        "am": false, (AM) Approach Mode
                        = 0 Not active
                        = 1 Active
        "mv": false (MV) Manage Vertical Mode
                        = 0 Not active
                        = 1 Active 
    }
},
"time_of_track": "2016-10-20T11:40:02.898437"
        