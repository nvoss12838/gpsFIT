import numpy as np
import sys
import os 
import matplotlib.pylab as plt

def heavy(t,t0):
   if t<t0:
	 x=0
   else:
	 x = 1
   return x 
def heavyInv(t,t0):
	if t>t0:
	 	x=0
   	else:
	 	x = 1
	return x 
def trend(t,m,b):
    #fit trend : y = mx+b 
    y = m*t + b #m = trend and b is the bias 
    return y
def periodAnn(t,A1,A2):
    #annual periods trend should be removed first
    y = A1*np.cos(2.0*np.pi*t) + A2*np.sin(2.0*np.pi*t)
    return y 
def periodSemiAnn(t,A3,A4):
    #semi-annual periods trend should be removed first
    y = A3*np.cos((4.0*np.pi*t)) + A4*np.sin((4.0*np.pi*t))
    return y 

def jump(t,t0,G):
    #fit for jump (either antenna change or earthquake
    y = G*heavy(t,t0)
    return y 
def exponential(t,C,eqt,tau):
    #fit the postsiesmic deformation
    #we could also do a logLarithmic (aught to implement in future)
    y = C*(1.0-np.exp(-(t-eqt)/(tau/365.0)))
    return y 
def sse(t,t0,tau,U):
    #fit arctan as approximation for sse from Holtkamp and Brudzinski 2008
    #t01 is the median time of the sse
    #tau is the period over which the sse takes place. 
    y = 0.5*U*((np.tanh((t-t0)/tau))-1)
    return y 

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
def fun(t,b,A1,A2,A3,A4,G,H,C,D,E,t04,t4,U4,t01,t1,U1,m):
    y = []
    #fit arctan as approximation for sse from Holtkamp and Brudzinski 2008
    #t01 is the median time of the sse
    #tau is the period over which the sse takes place.
    eqt1 = 2012.6817
    eqt2 = 2012.8159
    ant = 2010.07
    
    #m =  -1.26
    #t01 = 2003 + (254/365.0) + (30/(2.0*365.0)) 
    t02 = 2005 + (198/365.01) + (30/(2.0*365.0))
    t03 = 2007 + (140/365.0) + (33/(2.0*365.0))
    t05 = 2009 + (-80.0/365.01) + (180/(2.0*365.0))
    t06 = 2011 + (170/365.01) + (20/(2.0*365.0))
    

    #t1 = (30/(2*365.0))
    t2 = (30.0/(2*365.0))
    t3 = (30.0/(2*365.0))
    t5 = (180.0/(2*365.0))
    t6 = (20.0/(2*365.0))
    #U1 = -0.65
    U2 = -.66
    U3 = -0.13
    U5 = 0.44
    U6 = -0.08
    tau = 7.0
    tau2 = 70.0
    tau3 = 420.0

    for i in range(len(t)):
      #y.append(trend((t[i]-t[0]),m,b) + (periodAnn(t[i]-t[0],A1,A2) + periodSemiAnn(t[i]-t[0],A3,A4)) +\
       # sse(t[i],t06,t6,U6)+sse(t[i],t02,t2,U2)+sse(t[i],t03,t3,U3)+sse(t[i],t04,(t4/(2.0*365.0)),U4)+\
        #+jump(t[i],eqt1,G)+jump(t[i],eqt2,H)  + exponential(t[i],C,eqt1,tau)*heavy(t[i],eqt1)\
        #+exponential(t[i],D,eqt1,tau2)*heavy(t[i],eqt1)+exponential(t[i],E,eqt1,tau3)*heavy(t[i],eqt1))
      #sse(t[i],t01,t1,U1)+sse(t[i],t02,t2,U2
      y.append(trend((t[i]-t[0]),m,b) + (periodAnn(t[i]-t[0],A1,A2) + periodSemiAnn(t[i]-t[0],A3,A4)) +\
        +sse(t[i],t01,t1,U1)+sse(t[i],t04,(t4/(2.0*365.0)),U4)+\
        +jump(t[i],eqt1,G)+jump(t[i],eqt2,H) + exponential(t[i],C,eqt1,tau)*heavy(t[i],eqt1)\
        +exponential(t[i],D,eqt1,tau2)*heavy(t[i],eqt1)+exponential(t[i],E,eqt1,tau3)*heavy(t[i],eqt1))
      #above is trend Annual period semiAnnual period 
      #2007 sse 2009 sse 2011 sse.   #add in 2012 sse?e
      #Mainshock aftershock 3 exponentials and 
      #2014 sse 
    return y
def writeFile(time,model,uncert):	
	f = open('model.txt', 'w')
	f.write('model\n')
	for i in range(len(time)):
		f.write(str(time[i]) + ' ' + str(model[i]) + ' ' + str(uncert[i]) + ' \n')
	f.close()
def writeNoiseFile(tsf,time,model,loc,uncert):
	noise = np.array(loc) - np.array(model)
	plt.scatter(time,noise)
	plt.show()
	fil = tsf.split('/')[1]
	os.chdir('noise')
	f = open((fil + '.noise.txt'), 'w')
	for i in range(len(time)):
		f.write(str(time[i]) + ' ' + str(noise[i]) + ' ' + str(uncert[i]) + ' \n')
	f.close()
	os.chdir('..')
#file for the time series    
timeSeriesFile = sys.argv[1]
#read the data into arrays
time,loc,uncert = readData(timeSeriesFile)
#load the parameters from the text file
paramaterFile = sys.argv[2]
b,A1,A2,A3,A4,G,H,C,D,E,t04,t4,U4,t01,t1,U1,m= np.loadtxt(paramaterFile,usecols = [1], skiprows = 1 )

#compute the new array:

model = fun(time,b,A1,A2,A3,A4,G,H,C,D,E,t04,t4,U4,t01,t1,U1,m)

#write new file wth model data

writeFile(time,model,uncert)

#writeNoiseFile(timeSeriesFile,time,model,loc,uncert)
import matplotlib.pylab as plt
plt.plot(time,model, c= 'r', label = 'Model')
plt.scatter(time,loc, c = 'b', label = 'Position')
plt.legend(loc = 3)
plt.xlabel('Time')
plt.ylabel('Position (cm)')
plt.title('IND1 Longitude')
plt.show()
