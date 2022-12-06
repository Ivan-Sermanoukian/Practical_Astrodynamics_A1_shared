# Libraries
import sys
import os
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sgp4.api import Satrec, days2mdhms, jday
from math import *

def time_tables():

    files = os.listdir(os.curdir)
    UT1_UTC_exists = 0
    LS_exists = 0
    for i in range(len(files)):
        if (files[i] == "UT1_UTC.dat"):
            UT1_UTC_exists = 1
        if (files[i] == "leap_seconds.dat"):
            LS_exists = 1

    if (UT1_UTC_exists == 0):
        url = "https://maia.usno.navy.mil/ser7/finals2000A.daily"
        UT1_UTC_data = requests.get(url, allow_redirects=True)
        open('UT1_UTC.dat', 'wb').write(UT1_UTC_data.content)
        print("UT1_UTC data correctly saved to file.")
        file = open('UT1_UTC.dat', 'r')
        file_line = file.readlines()
        time_conversion_table = np.zeros((np.size(file_line),2))
        for i in range(len(file_line)):
            time_conversion_table[i][0] = float(file_line[i][7:15])  # MJD
            time_conversion_table[i][1] = float(file_line[i][58:68]) # Time error
        np.savetxt('UT1_UTC_MJD_time.dat', time_conversion_table)
        print("UT1_UTC data correctly saved to file.")

    else:
        print("UT1_UTC data already exists in directory.")

    if (LS_exists == 0):
        url = "https://maia.usno.navy.mil/ser7/tai-utc.dat"
        LS_data = requests.get(url, allow_redirects=True)
        open('leap_seconds.dat', 'wb').write(LS_data.content)
        print("LS_data data correctly saved to file.")
        file = open('leap_seconds.dat', 'r')
        file_line = file.readlines()
        time_conversion_table = np.zeros((np.size(file_line), 4))
        for i in range(len(file_line)):
            time_conversion_table[i][0] = float(file_line[i][17:26])  # JD
            time_conversion_table[i][1] = float(file_line[i][38:49])  # Time error1
            time_conversion_table[i][2] = float(file_line[i][59:65])  # Time error2
            time_conversion_table[i][3] = float(file_line[i][70:78])  # Time error3
        np.savetxt('leap_seconds_MJD_time.dat', time_conversion_table)
        print("LS_data data correctly saved to file.")
    else:
        print("LS data already exists in directory.")

def time(argv):

    TLE_FILE = argv[2]
    data_file = open(TLE_FILE, "r")
    TLE = data_file.read()

    L1 = TLE.splitlines()[1]
    L2 = TLE.splitlines()[2]
    satellite = Satrec.twoline2rv(L1, L2)
    month, day, hour, minute, second = days2mdhms(satellite.epochyr, satellite.epochdays)
    if satellite.epochyr < 57:
        year = 2000 + satellite.epochyr
    else:
        year = 1900 + satellite.epochyr
    jd_TLE, fr_TLE = jday(year, month, day, hour, minute, second)
    mjd_TLE = jd_TLE + fr_TLE - 2400000.5

    ORBIT_FILE = argv[3]
    orbit_table = np.loadtxt(ORBIT_FILE)
    orbit_time_vector = orbit_table[:,0]

    # UTC to UT1
    TABLE_FILE = argv[4]
    UT1_UTC_table = np.loadtxt(TABLE_FILE)
    UT1_UTC = UT1_UTC_table[:,1]
    mjd = UT1_UTC_table[:,0]

    # ... data processing #

if __name__ == "__main__":

    # List of user-defined functions
    list_of_fcts = [f.__name__ for f in globals().values() if type(f) == type(lambda *args: None)]
    # print(list_of_fcts)
    if (sys.argv[1] in list_of_fcts):
        globals()[sys.argv[1]](sys.argv)
    else:
        print("Wrong input function.")
        print("Try any of the following functions :" + str(list_of_fcts))
