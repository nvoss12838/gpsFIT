import numpy 
from fit import *
from equation_builder import *
import sys
'''
This is the script run by pestpp in order to model the time 
series data it takes a few command line arguments in order to 
run the data to run:
python modelData.py dataFile.txt functionFile.txt
'''

datafile = sys.argv[1]
functionFile = sys.argv[2]

times,location,uncertainty = readData(datafile)
funList = parseFunFile(functionFile)
model_tseries(times,funList)