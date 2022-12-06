# Routines that read and download the leap-second and time correction tables 

## How it works

The time_conversions.py script provides a way to read and download the time correction tables between different time standards.

The `time_tables()` function checks whether the tables are already in your current directory and, if that is not the case, they are downloaded as a text file.

Regarding UT1-UTC the following reference is used: [FINALS2000A.daily](https://maia.usno.navy.mil/ser7/finals2000A.daily)

Regarding leap seconds the following reference is used: [TAI-UTC](https://maia.usno.navy.mil/ser7/tai-utc.dat)

# How to use

In order to use each function, go to the CLI and use the following commands:

* python main.py time_tables
* python main.py time TLE.dat TLEorbit.dat UT1_UTC_MJD_time.dat leap_seconds_MJD_time.dat
