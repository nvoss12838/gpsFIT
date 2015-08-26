import matplotlib.pylab as plt 
import os
import glob
import numpy as np
import pickle
import scipy.io 
from fit import *
from equation_builder import *

class timeseries(object):
      '''
      timeseries is an object for holding individual components of GPS timeseries
      Attributes:
	  component : component name i.e lat,lon, rad
	  times  :times of measurement
	  location : displacment
	  uncertainty : uncertainty
      '''
      def __init__(self,component,times,location,uncertainty):
	self.component = component
	self.times = times
	self.location = location
	self.uncertainty = uncertainty

      def get_component(self):
	return self.component

      def get_times(self,**kwargs):
	'''
	arguments = None
	kwargs : windows = starttime,endtime
	'''
	window = kwards.get('window')
	if 'window' in locals:
	  start = windows[0] 
	  end = windows [2]
	  t = []
	  for time in self.times:
	    if time > start and time < end:
	      t.append.time
	else:
	  t = self.times
	
	return t

      def get_location(self):
	return self.location
      
      def get_uncertainty(self):
	return self.uncertianty
      
      def plot(self):
	plt.errorbar(self.times, self.location, yerr= self.uncertainty)
	plt.title = self.component
	plt.show()
	return
      

class station(object):
	'''
	station is an object representing a GPS station

	Attributes:
		name : station name
		location : location of station in lon,lat
		times: time corresponding to measurment
		lat : latidudinal displacement and uncertainty
		lon : longitudinal displacement and uncertainty
		vert : vertical displacement and uncertainty
	'''
	def __init__(self,name,network,times,lat,lon,vert):
		self.name = name
		self.network = network
		self.times = times
		self.lat = lat
		self.lon = lon
		self.vert = vert 

	def get_startdate(self):
		return min(self.times)

	def get_enddate(self):
		return max(self.times)

	def get_location(self):
		return self.location

	def plot_tseries(self,**kwargs):
		'''
		plots all 3 component data
		Optional arguments: specify 3 function files for plotting as an array i.e. fun = [funX,funY,funZ]
		'''
		fun = kwargs.get('fun')
		plt.subplot(311)
		plt.title(self.name)
		plt.scatter(self.times,self.lat.location, c = 'r', label = 'Northing')
		if 'fun' in locals():
			funList = parseFunFile(fun[1])
			data = model_tseries(self.times,funList)
			plt.plot(self.times,data)
		plt.ylabel('Northing')
		plt.subplot(312)
		plt.ylabel('Easting')
		plt.scatter(self.times,self.lon.location, c = 'b', label = 'Easting')
		if 'fun' in locals():
			funList = parseFunFile(fun[0])
			data = model_tseries(self.times,funList)
			plt.plot(self.times,data)
		plt.subplot(313)
		plt.ylabel('Up')
		plt.xlabel('Time')
		plt.scatter(self.times,self.vert.location,c = 'g', label = 'Up')
		if 'fun' in locals():
			funList = parseFunFile(fun[2])
			data = model_tseries(self.times,funList)
			plt.plot(self.times,data)
		plt.savefig('station_model.jpg')
		plt.show()

class network(object):
	'''
	network is an object representing collection of gps stations
	
	Attributes:
		name : network name
		purpose : reason for network 
		organizer : orginization running network
		stations : stations in the network each is a station object
	'''
	def __init__(self,name,purpose,organizer,stations):
		self.name = name
		self.purpose = purpose
		self.organizer = organizer 
		self.stations = stations
		
	def plot_network(self):
	  #make a basemap plot of stations
	  return
	
	def get_name(self):
	  return self.name
	
	def get_organizer(self):
	  return self.organizer
	def get_station(self,station):
	  for sta in self.stations:
	    if sta.name == station:
	      return sta
	  return
	def print_stations(self):
	  print 'There are %s stations in network:' % len(self.stations)
	  index = 0
	  for station in self.stations:
	    print index, station.name
	    index += 1
	  return
	def get_stations(self):
	  print 'There are %s stations in network:' % len(self.stations)
	  stationList = []
	  index = 0
	  for station in self.stations:
	    stationList.append(station.name)
	    index += 1
	  return stationList

	def save(self):
	  pickle.dump(self,open(self.name+".p","wb"))
	  return 
	
def readData(filename):
	'''
	read in data in Decater format 
	date location uncertainty?
	'''
	#read in filename splitting into useful python arrays 
	date,loc,uncert = np.genfromtxt(filename,dtype=float,usecols = (0,1,2), unpack = True, skiprows = 1)
	dateNum = [float(d) for d in date]
	loc = [float(l) for l in loc]
	uncert = [float(x) for x in uncert]
	return dateNum,loc,uncert
      
def create_network(name,purpose,organization,networkFolder):
	'''
	create a network, and station objects for all stations in 
	networkFolder
	Inputs:
	      name : name of network
	      purpose : purpose of network
	      organization : organization running netowrk
	      networkFolder : directory containing stations in network
	
	the directory structure is /network/station/stationData
	'''
	directories = []
	for directory in os.walk('./' + networkFolder):
	    directories.append(directory)
	stations = directories[0][1]
	stationObjects = []
	for i in range(0,len(stations)):
	  latFile = glob.glob(directories[i+1][0] + '/*.lat.*.txt')[0]
	  lonFile = glob.glob(directories[i+1][0] + '/*.lon*.txt')[0]
	  radFile = glob.glob(directories[i+1][0] + '/*.rad*.txt')[0]
	  print latFile
	  t,llat,ulat =  readData(latFile)
	  lat = timeseries('Latitude',t,llat,ulat)
	  t,llon,ulon = readData(lonFile)
	  lon = timeseries('Longitude',t,llon,ulon)
	  t,lrad,urad = readData(radFile)
	  rad = timeseries('Radial',t,lrad,urad)
	  stationObjects.append(station(stations[i],name,t,lat,lon,rad))
	net = network(name,purpose,organization,stationObjects)
	return net
    
def network2Struct(network,filname,units):
    
    '''
    Takes gps python network object and converts it to matlab S structure and saves 
    as a .mat file for use with the NIF code
    
    Paramaters:
        network is a network of GPS sites
        filename is the output .m file name
        units is the units of the GPS timeseries stored in the structure
    Matlab object (S) description:
    S attributes:
        sites : cell array of Site Names (string
        decyr : cell array, one cell for every site containing array of times
        de: Cell array, one cell for every site conaining East dimension IN M
        dn:'                                             'North'             '
        du:'                                             'Up'                '
        cove:Cell array, one cell for every site containing East Covariance IN M
        covn:'                                              North            '
        covu:'                                              Up               '
        
    '''
    #create the sites array
    sites = network.get_stations()
    #create arrays to store the data
    decyr,de,dn,du,cove,covn,covu = [],[],[],[],[],[],[]
    
    #make sure the observation does not have to be scaled
    if units == 'cm':
        scale = 0.01
    if units == 'mm':
        scale  = 0.001
    if units == 'm':
        scale = 1
        
    for i in range(len(sites)):
        decyr.append(network.stations[i].times)
        de.append(scaleObs(network.stations[i].lon.location,scale))
        dn.append(scaleObs(network.stations[i].lat.location,scale))
        du.append(scaleObs(network.stations[i].vert.location,scale))
        cove.append(scaleObs(np.square(network.stations[i].lon.uncertainty),scale))
        covn.append(scaleObs(np.square(network.stations[i].lat.uncertainty),scale))
        covu.append(scaleObs(np.square(network.stations[i].vert.uncertainty),scale))
    
    S = {'Sites':sites,'DecimalYears':decyr,'EastDisplacement':de,'NorthDisplacement':dn,\
        'VerticalDisplacement':du,'EastCov':cove,'NorthCov':covn,'UpCov':covu}
    scipy.io.savemat(filname,S, oned_as = 'column')
    
    return 

def scaleObs(array,scale):
    scaled = []
    for obs in array:
        scaled.append(obs*scale)
    return scaled
    
    
    
    
    
    
    
    
    
    
    
    
