import numpy as np
import matplotlib.pylab as plt
import inspect 
from fit import *

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

def compute(fun):
  value = 0
  for i in range(len(fun.equation)):
    method = getattr(fun.equation[i],inspect.getmembers(fun.equation[i],predicate=inspect.ismethod)[1][0])
    value += method()
  return value
 
def model_tseries(times,funList):
  modeledData = []
  for t in times:
      for fun in funList:
	  fun.t = t 
      fun = function(funList)
      modeledData.append(compute(fun))
  return modeledData

def parseFunFile(functionFile):
    funList = []
    lines = [line.strip() for line in open(functionFile)]
    print lines
    for line in lines:
      functiontxt = line.split(' ')
      function = functiontxt[0]
      print function
      args = [float(item) for item in functiontxt[1:]]
      print args
      funList.append(eval(function)(*args))
    return funList
    
