import pandas as pd

config = { "00:00": 9, "01:30": 2, "01:45": 0, "02:35": 2, "04:00": 126, "04:20": 1135, "04:21": 5591, "07:00": 10968, "08:00": 7711,
    "08:05": 3287, "08:13": 2652, "08:47": 2964, "09:04": 3959, "13:00": 3293, "13:26": 2625, "15:00": 3009, "16:18": 4563, "17:37": 5853,
    "18:09": 5065, "18:36": 2537, "19:45": 1214, "20:24": 483, "22:12": 211, "23:00": 67, "23:59": 9 }

'''
index = pd.date_range('1/1/2000', periods=9, freq='min')
series = pd.Series(range(9), index=index)
'''

'''
d = {'price': [10, 11, 9, 13, 14, 18, 17, 19],
     'volume': [50, 60, 40, 100, 50, 100, 40, 50]}
df = pd.DataFrame(d)
df['week_starting'] = pd.date_range('01/01/2018',
                                    periods=8,
                                    freq='W')

df.resample('ME', on='week_starting').mean()                                    
'''

#create series by dict
d_serie = pd.Series(config)
#convert index to TimedeltaIndex
d_serie.index = pd.to_timedelta(d_serie.index.astype(str) + ':00')
#print (d_serie)

#upsampling with forward filling NaNs
s = d_serie.resample('5Min').ffill() 

upsampled = d_serie.resample('5M')
interpolated = upsampled.interpolate(method='linear')
interpolated = upsampled.interpolate(method='spline', order=2)
print(interpolated.head(32))