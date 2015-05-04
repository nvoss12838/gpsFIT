import numpy 
from fit import *
from gps import * 
from equation_builder import *
import pickle
import sys
'''
This is the script run by pestpp in order to model the time 
series data it takes a few command line arguments in order to 
run the data to run:
python modelData.py /path/to/network.p station_name functionFile.txt
'''

network = sys.argv[1]
stationName = sys.argv[2]
functionFile = sys.argv[3]
cr = pickle.load(open(network, "rb" ))
sta = cr.get_station(stationName)
times = sta.times

funList = parseFunFile(functionFile)
data = model_tseries(times,funList)