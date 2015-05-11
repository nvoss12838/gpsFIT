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
  '''
  computes a function at the value t specified in the function class 
  '''
  value = 0
  for i in range(len(fun.equation)):
    method = getattr(fun.equation[i],inspect.getmembers(fun.equation[i],predicate=inspect.ismethod)[1][0])
    value += method()
  return value

def writeModelData(times,modeledData):
   f = open('modelTseries.txt','w')
   f.write('model \n')
   for i in range(len(times)):
     f.write('%s	%s\n' % (times[i],modeledData[i]))
   return
 
def model_tseries(times,funList):
  '''
  takes in measurement times and computes the value of the function at those times
  '''
  modeledData = []
  for t in times:
      for fun in funList:
	  fun.t = t
	  if fun.name == 'trend' or fun.name == 'periodAnn' or fun.name == 'periodSemiAnn':
	    fun.t0 = min(times)
	    
      fun = function(funList)
      modeledData.append(compute(fun))
  writeModelData(times,modeledData)
  return modeledData

def parseFunFile(functionFile):
    ''' 
    parse the function file to return the wanted function and their arguments
    '''
    funList = []
    lines = [line.strip() for line in open(functionFile)]
    for line in lines:
      functiontxt = line.split(' ')
      function = functiontxt[0]
      if function != '#':
        args = [float(item) for item in functiontxt[1:]]
        args.insert(0,0)
        if function == 'trend' or function == 'periodAnn' or function == 'periodSemiAnn':
          args.insert(0,0)
        funList.append(eval(function)(*args))
    return funList
    
