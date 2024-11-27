import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd
import matplotlib.pyplot as plt
import csv
import pandas as pd
from conflict_detection import Conflict_Detection


plt.style.use('ggplot')


def plot_correlation(x, y, title, xlabel,  ylabel, fileName, parameter):
    fig, ax = plt.subplots()
    slope, intercept, r, *__ = scipy.stats.linregress(x, y)
    #line = f'Regression line: y={intercept:.2f}+{slope:.2f}x, r={r:.2f}'
    line = f'Correlation: r={r:.2f}'
    ax.plot(x, y, linewidth=0, marker='s', label='Data points')
    ax.plot(x, intercept + slope * x, label=line)
    ax.axvline(x = parameter, color = 'purple', label = 'Parameter: '+str(parameter))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(facecolor='white')
    ax.set_title(title)
    plt.savefig(fileName)
    plt.show()



conflict = Conflict_Detection()

df = pd.read_csv('dataset_3.csv')
# select columns by name
data = 'images/20230520'
data_df = df.query('Date == 20230520')

# conflict.TRACK_Maneuver_LIM
# conflict.TRACK_FRAME_INDICES
# conflict.TRACK_STD_LIM
# conflict.ALT_Maneuver_LIM 
# conflict.ALT_FRAME_INDICES 
# conflict.ALT_STD_LIM 
# conflict.SPEED_Maneuver_LIM 
# conflict.SPEED_STD_LIM 
# conflict.SPEED_FRAME_INDICES 


track_filter_df = data_df.filter(items=['TrackStdLim', 'NumManTrack'])
plot_correlation(track_filter_df['TrackStdLim'], track_filter_df['NumManTrack'], 
                 "Correlation between Conflicts Resolution by Track Maneuver \n and the Deviation of Track Reference Value", 
                 "Deviation of Track Reference Value [°]",
                 "Conflicts Resolution by Track Maneuver",
                 data+'_TrackStdLim.jpg',
                 conflict.TRACK_STD_LIM)

track_filter_df = data_df.filter(items=['TrackDeltaLim', 'NumManTrack'])
plot_correlation(track_filter_df['TrackDeltaLim'], track_filter_df['NumManTrack'], 
                 "Correlation between Conflicts Resolution by Track Maneuver \n and the Aircraft's Track Maneuver thereshold", 
                 "Aircraft's Track Maneuver thereshold [°]",
                 "Conflicts Resolution by Track Maneuver",
                 data+'_TrackDeltaLim.jpg',
                 conflict.TRACK_CHANGE_LIM)

track_filter_df = data_df.filter(items=['TrackFrameLen', 'NumManTrack'])
plot_correlation(track_filter_df['TrackFrameLen'], track_filter_df['NumManTrack'], 
                 "Correlation between Conflicts Resolution by Track Maneuver \n and the Aircraft's Trajectory frame length", 
                 "Aircraft's Trajectory frame length",
                 "Conflicts Resolution by Track Maneuver",
                 data+'_TrackFrameLen.jpg',
                 conflict.TRACK_FRAME_INDICES)


alt_filter_df = data_df.filter(items=['AltStdLim', 'NumManAlt'])
plot_correlation(alt_filter_df['AltStdLim'], alt_filter_df['NumManAlt'], 
                 "Correlation between Conflicts Resolution by Altitude Maneuver \n and the Deviation of Altitude Reference Value", 
                 "Deviation of Altitude Reference Value [m]",
                 "Conflicts Resolution by Altitude Maneuver",
                 data+'_AltStdLim.jpg',
                 conflict.ALT_STD_LIM)

alt_filter_df = data_df.filter(items=['AltDeltaLim', 'NumManAlt'])
plot_correlation(alt_filter_df['AltDeltaLim'], alt_filter_df['NumManAlt'], 
                 "Correlation between Conflicts Resolution by Altitude Maneuver \n and the Aircraft's Altitude Maneuver thereshold", 
                 "Aircraft's Altitude Maneuver thereshold [m]",
                 "Conflicts Resolution by Altitude Maneuver",
                 data+'_AltDeltaLim.jpg',
                 conflict.ALT_CHANGE_LIM)

alt_filter_df = data_df.filter(items=['AltFrameLen', 'NumManAlt'])
plot_correlation(alt_filter_df['AltFrameLen'], alt_filter_df['NumManAlt'], 
                 "Correlation between Conflicts Resolution by Altitude Maneuver \n and the Aircraft's Trajectory frame length", 
                 "Aircraft's Trajectory frame length",
                 "Conflicts Resolution by Altitude Maneuver",
                 data+'_AltFrameLen.jpg',
                 conflict.ALT_FRAME_INDICES)


speed_filter_df = data_df.filter(items=['SpeedStdLim', 'NumManSpeed'])
plot_correlation(speed_filter_df['SpeedStdLim'], speed_filter_df['NumManSpeed'], 
                 "Correlation between Conflicts Resolution by Speed Maneuver \n and the Deviation of Speed Reference Value", 
                 "Deviation of Speed Reference Value [m/s]",
                 "Conflicts Resolution by Speed Maneuver",
                 data+'_SpeedStdLim.jpg',
                 conflict.SPEED_STD_LIM)

speed_filter_df = data_df.filter(items=['SpeedDeltaLim', 'NumManSpeed'])
plot_correlation(speed_filter_df['SpeedDeltaLim'], speed_filter_df['NumManSpeed'], 
                 "Correlation between Conflicts Resolution by Speed Maneuver \n and the Aircraft's Speed Maneuver thereshold", 
                 "Aircraft's Speed Maneuver thereshold [m/s]",
                 "Conflicts Resolution by Speed Maneuver",
                 data+'_SpeedDeltaLim.jpg',
                 conflict.SPEED_CHANGE_LIM)

speed_filter_df = data_df.filter(items=['SpeedFrameLen', 'NumManSpeed'])
plot_correlation(speed_filter_df['SpeedFrameLen'], speed_filter_df['NumManSpeed'], 
                 "Correlation between Conflicts Resolution by Speed Maneuver \n and the Aircraft's trajectory frame length", 
                 "Aircraft's trajectory frame length",
                 "Conflicts Resolution by Speed Maneuver",
                 data+'_SpeedFrameLen.jpg',
                 conflict.SPEED_FRAME_INDICES)