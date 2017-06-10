#!/usr/bin/env python

import time
import os
from sys import argv
from multiprocessing import Process

# nQueen backtracking
if len(argv) != 4:
	print "Utilisation de la commande : python nQueen.py <taille> <premiere colonne> <dernier colonne>"
	exit(len(argv))

size = int(argv[1])
firstCol = int(argv[2])
lastCol = int(argv[3])


nbSolution = 0
S = [0]*size

def isFree(S, row, col):
	r = 0
	c = 0
	ok = True
	while r < row:
		c = S[r]
		ok = ok & (abs(row-r) != abs(col-c)) & (col != c)
		r = r+1
	return ok

def placeQueen(row, startCol):
	global S
	global nbSolution
	if row == 0:
		S[row] = startCol
		try:
			placeQueen(row+1, 0)
		except MemoryError:
			exit(2)
	else:
		if row >= size:
			# print(S)
			nbSolution += 1
		else:
			col = 0
			while col < size:
				if isFree(S,row,col):
					S[row] = col
					placeQueen(row+1, 0)
					S[row] = 0
				col += 1

if __name__ == '__main__':
	debut = time.time()

	for i in range(firstCol, lastCol):
		placeQueen(0, i)

	fin = time.time()
	#print("Nombre de solutions calculees : " + str(nbSolution))
	
	#print("Temps d'execution = " + str(fin - debut) + " secondes")
	temps=round(fin - debut, 2)
	print str(nbSolution) + ":" + str(temps)
	exit(0)

