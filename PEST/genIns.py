import numpy as np 
import pickle

network = '../Data/Costa_Rica.p'
stationName = 'pne2'
cr = pickle.load(open(network, "rb" ))
sta = cr.get_station(stationName)
times = sta.times
f = open('/home/nvoss/Geodesy/CR_2014/model.ins', 'w')
f.write('pif @ \n')
f.write('@model@\n')
#f.write('l1 w !obs1! \n')
for i in range(len(times)):
	f.write(' l1 w !obs' + str(i+1) + '!\n')
f.close()
