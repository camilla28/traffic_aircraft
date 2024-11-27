from trajectory import Trajectory
from plot_4d_dimensions import PlotData
import csv

def __plot_test(datestr):
    datestr = "20230727"
    traj = Trajectory(datestr)

    print("Time serie")
    data_time_serie = traj.treat_data(type = 'r', only_path = False)

    plot = PlotData(data_time_serie, data_time_serie)


    #plot.plot_by_file(datestr)

    # icao_list = ['392aed', '151e2f', '406668', '4072ea', '471f74', '4ac9e3',
    #             '4bab52', '4bb275', '4cad49', 'a3a9ff', 'a79e31', 'abd8e4']

    #icao_list = ['4072ea']
    icao_list = list(data_time_serie.keys())

    # icao_list = ['0101be', '010206', '01022f', '02007d', '020095', '02010d', '020124',
    #              '020140', '020176', '02a1a4', '02a1b1', '02a1b3', '04008c', '060040',
    #              '06a099', '06a0b0', '06a13c', '06a1e6', '06a1eb', '06a2e5', '06a30c',
    #              '0a0021', '0a0077', '0a007a', '0a0084', '0a008f', '0a009c', '0d08f3',
    #              '0d09a9', '0d0a3a', '0d0abd', '0d0acd', '0d0b16', '0d0c92', '0d0ce0',
    #              '0d0cfd', '0d839c', '15063a', '151da0', '151dad', '151e0b', '151e12',
    #              '151e14']

    #icao_list = ['020140', '02a1b3']
    for icao in icao_list:
    #    plot.plot_comp_all_speed(data_time_serie, icao, None)
        plot.plot_icao_traj_without_alt(data_time_serie, icao, None, None)
        # plot.plot_comp_all_cruise(data_time_serie, icao)

def __plot_by_Date():
    
    # Para cada conflito:
    # fileName = 'dataset_' + str(date) + '.csv'
    fileName = 'dataset.csv'
    date = ""
    with open(fileName, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Date"] != date:
                date = row["Date"]
                traj = Trajectory(date)
                print("Read trajectory file of data: "+ date)
                data_time_serie = traj.treat_data(type = 'r', only_path = False)
                plot = PlotData(data_time_serie, data_time_serie)
            print(row["Date"])
            plot.plot_conflict(data_time_serie, row)
            
    
# def __plot_by_Date(date):
    
#     traj = Trajectory(date)
#     print("Read trajectory file of data: "+ date)
#     data_time_serie = traj.treat_data(type = 'r', only_path = False)
#     plot = PlotData(data_time_serie, data_time_serie)

#     # Para cada conflito:
#     # fileName = 'dataset_' + str(date) + '.csv'
#     fileName = 'dataset.csv'
#     date = ""
#     with open(fileName, newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             plot.plot_conflict(data_time_serie, row)

__plot_by_Date()
# __plot_by_Date("20230727")