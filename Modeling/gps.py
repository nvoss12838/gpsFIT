import matplotlib.pylab as plt 

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
	def __init__(self,name,location,times,lat,lon,vert):
		self.name = name
		self.location = location
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
