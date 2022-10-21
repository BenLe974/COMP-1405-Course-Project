

import math


def mult_scalar(matrix, scale):
	new_matrix = []
	for row in range(len(matrix)):
		new_matrix.append([])
		for column in range(len(matrix[row])):
			new_matrix[row].append(matrix[row][column] * scale)
	return new_matrix

def mult_matrix(a, b):
	new_matrix = []
	if len(a) == len(b):
		#for m in range(len(a)): #iterates over the rows of a 
			for p in range(len(b[0])): #iterates over the columns of b
				sum = 0
				for n in range(len(a)): #iterates over the columns of a
					sum = sum + a[n]*b[n][p] #used notation from mathisfun.com directly
				new_matrix.append(sum)
	else:
		return None

	return new_matrix
	
def euclidean_dist(a,b):
	sum = 0
	if len(a) == len(b):
		for i in range(len(a)):
			calc = (a[i] - b[i])**2
			sum = calc + sum
		dist = math.sqrt(sum)
	else:
		return None
	return dist
