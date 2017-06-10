#!/usr/bin/env python

import time
import os
from sys import argv
from multiprocessing import Process

# nQueen backtracking
N = int(argv[1]) # taille du tableau
# rowInit = int(argv[2]) # colone de depart
nbSolution = 0
S = [0]*N

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
		if row >= N:
			# print(S)
			nbSolution += 1
		else:
			col = 0
			while col < N:
				if isFree(S,row,col):
					S[row] = col
					placeQueen(row+1, 0)
					S[row] = 0
				col += 1


	

def main():
	if len(argv) != 3:
		exit(1)

	debut = time.time()
	placeQueen(0, N)
	print("Nombre de slutions calculees : " + str(nbSolution))
	fin = time.time()
	print("Temps d'execution = " + str(fin - debut) + " secondes")
	exit(0)

if __name__ == '__main__':

	main()

