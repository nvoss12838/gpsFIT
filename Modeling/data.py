
class station(object):
	'''
	station is an object representing a GPS station

	Attributes:
		name : station name
		location : location of station in lon,lat
		times: time corresponding to measurment
		lat : latidudinal displacement
		lon : longitudinal displacement
		vert : vertical displacement
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
