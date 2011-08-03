#!/usr/bin/env python
import argparse
import shutil
import os
import sys
import csv
import makepar
from math import cos, sin, sqrt

k=123.4567901
delL=0.1

def rollup(x,a):
	return a(1)+a(2)*tanh(a(3)*x+a(4))

def sqrtk(L):
	# Frac of length
	temp=L/(128*delL)
	a=[1.006370764,0.9640900469, 0.3349204039, -6.217212044]
	return sqrt(rollup(x,a))

def genmatrix():
	fID=open('qmat.csv','w')
	csv.register_dialect('csv',delimiter=',',skipinitialspace=True)
	wrtr=csv.writer(fID,dialect='csv')
	wrtr.writerow(['','Occurence','L','R11','R33','R12','R34','R21','R43','R22','R44'])
	for i in range(1,129):
		effrtk=sqrtk(delL*(i-1))
		r11=cos(effrtk*delL)
		r12=sin(effrtk*delL)/effrtk
		r21=-effrtk*sin(effrtk*delL)
		r22=cos(effrtk*delL)
		row=['Q',i,delL,r11,r11,r12,r12,r21,r21,r22,r22]
		wrtr.writerow(row)
	fID.close()
	makepar.makepar('qmat.csv','qmat.par',False)

if __name__ == '__main__':
	parser=argparse.ArgumentParser(description=
			'Generates matrix file for many-quad simulation of plasma lensing.')
	parser.add_argument('-V',action='version',version='%(prog)s v0.1')
	parser.add_argument('-v','--verbose',action='store_true',
			help='Verbose mode.')
	# parser.add_argument('inputfile',
	#                 help='Yuri\'s lattice.')
	# parser.add_argument('outputfile',
	#                 help='Output filename for concatenated lattice.')
	arg=parser.parse_args()

	genmatrix()
