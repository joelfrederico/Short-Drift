#!/usr/bin/env python
import argparse
import shutil
import os
import sys
import csv
import makepar

from math import cos, sin, sqrt, tan

# Defines division length
delL=0.1


# Returns sqrt(k) where k is the focusing,
# as a function of s-coordinate.
def k(L):
	# Frac of length
	temp=L/(128*delL)
	# This defines k at s
	return L*(1-temp)

def genmatrix():
	# Open and determine how to write to file
	fID=open('qmat.csv','w')
	csv.register_dialect('csv',delimiter=',',skipinitialspace=True)
	wrtr=csv.writer(fID,dialect='csv')

	# Header row for parameters to be written
	wrtr.writerow(['','Occurence','L','R11','R33','R12','R34','R21','R43','R22','R44'])

	for i in range(1,129):
		# Current s coordinate
		currentL = delL*(i-1)

		# Effective square root of focusing
		# to be used in current section, k:
		# x'' = k(s) x
		effrtk   = math.sqrt(k(currentL))

		# Thick lens matrix elements.
		# Note: r(1:2,1:2)=r(3:4,3:4)
		r11 = math.cos(effrtk*delL)
		r12 = math.sin(effrtk*delL)/effrtk
		r21 = -effrtk*math.sin(effrtk*delL)
		r22 = math.cos(effrtk*delL)

		# Row of parameter values to be written to CSV
		# (for tranlation to .par)
		row=['Q',i,delL,r11,r11,r12,r12,r21,r21,r22,r22]

		# Write to file
		wrtr.writerow(row)

	# Close up file
	fID.close()

	# Translate file to .par
	makepar.makepar('qmat.csv','qmat.par',False)

# Executed when called from command line
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
