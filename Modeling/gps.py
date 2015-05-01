import matplotlib.pylab as plt 
import os
import glob
import numpy as np
import pickle

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

      def get_times(self):
	return self.times

      def get_location(self):
	return self.location
      
      def get_uncertainty(self):
	return self.unvertianty
      
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

	def plot_tseries(self):
		plt.subplot(311)
		plt.title(self.name)
		plt.scatter(self.times,self.lat, c = 'r', label = 'Northing')
		plt.ylabel('Northing')
		plt.subplot(312)
		plt.ylabel('Easting')
		plt.scatter(self.times,self.lon, c = 'b', label = 'Easting')
		plt.subplot(313)
		plt.ylabel('Up')
		plt.xlabel('Time')
		plt.scatter(self.times,self.vert,c = 'g', label = 'Up')
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
	def save(self):
	  pickle.dump(self,open(self.name+".p","wb"))
	  return 
	
def readData(filename):
	'''
	read in data in Decater format 
	date location uncertainty?
	'''
	#read in filename splitting into useful python arrays 
	date,loc,uncert = np.genfromtxt(filename,dtype=float,usecols = (0,1,2), unpack = True)
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
	for i in range(1,len(stations)):
	  latFile = glob.glob(directories[i][0] + '/*.lat')[0]
	  lonFile = glob.glob(directories[i][0] + '/*.lon')[0]
	  radFile = glob.glob(directories[i][0] + '/*.rad')[0]
	  t,llat,ulat =  readData(latFile)
	  lat = timeseries('Latitude',t,llat,ulat)
	  t,llon,ulon = readData(lonFile)
	  lon = timeseries('Longitude',t,llon,ulon)
	  t,lrad,urad = readData(radFile)
	  rad = timeseries('Radial',t,lrad,urad)
	  stationObjects.append(station(stations[i],name,t,lat,lon,rad))
	net = network(name,purpose,organization,stationObjects)
	return net
    
		