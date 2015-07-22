import numpy as np 

def par2fun(parFile,funFile):
	data = np.genfromtxt(parFile,skiprows = 1, dtype = None)
	f = open(funFile,'w')
	f.write('trend %s %s \n' % ((data[0][1]*data[0][2]),(data[1][1]*data[1][2])))
	f.write('periodAnn %s %s \n' % (data[2][1],data[3][1]))
	f.write('periodSemiAnn %s %s \n'% (data[4][1],data[5][1]))
	f.write('jump %s %s \n' % ((data[8][1]*data[8][2]),(data[6][1]*data[6][2])))
	f.write('jump %s %s \n' % ((data[9][1]*data[9][2]),(data[7][1]*data[7][2])))
	f.write('exponential %s %s %s \n' % ((data[10][1]*data[10][2]),(data[8][1]*data[8][2]),(data[11][1]*data[11][2])))
	f.write('exponential %s %s %s \n' % ((data[12][1]*data[12][2]),(data[8][1]*data[8][2]),(data[13][1]*data[13][2])))
	f.write('exponential %s %s %s \n' % ((data[14][1]*data[14][2]),(data[8][1]*data[8][2]),(data[15][1]*data[15][2])))
	f.write('sse %s %s %s \n' % ((data[16][1]*data[16][2]),(data[17][1]*data[17][2]),(data[18][1]*data[18][2])))
	f.write('sse %s %s %s \n' % ((data[19][1]*data[19][2]),(data[20][1]*data[20][2]),(data[21][1]*data[21][2])))
	f.write('sse %s %s %s \n' % ((data[22][1]*data[22][2]),(data[23][1]*data[23][2]),(data[24][1]*data[24][2])))
	f.write('sse %s %s %s \n' % ((data[25][1]*data[25][2]),(data[26][1]*data[26][2]),(data[27][1]*data[27][2]))) 
	f.write('sse %s %s %s \n' % ((data[28][1]*data[28][2]),(data[29][1]*data[29][2]),(data[30][1]*data[30][2])))
	f.write('sse %s %s %s \n' % ((data[31][1]*data[31][2]),(data[32][1]*data[32][2]),(data[33][1]*data[33][2])))
	f.write('sse %s %s %s \n' % ((data[34][1]*data[34][2]),(data[35][1]*data[35][2]),(data[36][1]*data[36][2])))
	f.write('sse %s %s %s \n' % ((data[37][1]*data[37][2]),(data[38][1]*data[38][2]),(data[39][1]*data[39][2])))
	f.write('sse %s %s %s \n' % ((data[40][1]*data[40][2]),(data[41][1]*data[41][2]),(data[42][1]*data[42][2])))
	return

