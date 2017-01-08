#Application1, Q2#
import random

def ER(n,p):
	temp = {}
	V = range(0,n)
	E = 0
	for node_i in V:
		temp[node_i] = set()
		for node_j in V:
			a = random.random()
			if node_i == node_j:
				pass
			elif a < p:
				temp[node_i].add(node_j)
	return temp 

test1 = ER(10,0.5)
print test1