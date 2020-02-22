import numpy as np
from math import atan2, atan
from functools import reduce
from random import randint


def ccw(a, b, c):
		return (b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0])

def polar_angle(a, b):
	return atan2(b[1] - a[1], b[0] - a[0])



class ConvexHull:
	# It is assumed the points are in general position

	@staticmethod
	def MonotoneChain(points): # Andrew's algorithm (vertical line sweep)
		lower, upper = [], []
		points = sorted(points)
		for p in points:
			while len(lower) > 1 and ccw(lower[-2], lower[-1], p) <= 0: lower.pop()
			while len(upper) > 1 and ccw(upper[-2], upper[-1], p) >= 0: upper.pop()
			lower.append(p)
			upper.append(p)
		return lower + upper[-2:0:-1]


	@staticmethod
	def GrahamScan(points): # Radial line sweep
		p0 = min(points)
		points = sorted(points, key=lambda x: polar_angle(p0, x))
		hull = [ p0 ]
		for p in points:
			while len(hull) > 1 and ccw(hull[-2], hull[-1], p) <= 0: hull.pop()
			hull.append(p)
		return hull


	@staticmethod
	def QuickHull(points): # Divide and conquer
		def FindHull(S, p, q):
			if not S:
				return []
			c = max(S, key=lambda x: abs(ccw(x, p, q)))
			S1 = list(filter(lambda x: ccw(x, p, c) < 0, S))
			S2 = list(filter(lambda x: ccw(x, c, q) < 0, S))
			return FindHull(S1, p, c) + [c] + FindHull(S2, c, q)

		a, b = min(points), max(points)
		S1 = list(filter(lambda x: ccw(x, a, b) < 0, points))
		S2 = list(set(points) - set(S1))
		return [a] + FindHull(S1, a, b) + [b] + FindHull(S2, b, a)


	@staticmethod
	def JarvisMarch(points): # Gift wrapping algorithm
		hull  = [ min(points) ] # p0
		while True:
			nPoint = reduce(lambda x,y: y if (x == hull[-1] or ccw(y, hull[-1], x) < 0) else x, points)
			if nPoint == hull[0]:
				break
			hull.append(nPoint)
		return hull


	@staticmethod
	def QuickElimination(points): # Eliminate redundant points
		def QuadContains(Q, p):
			return (ccw(Q[0], Q[1], p) >= 0 and ccw(Q[1], Q[2], p) >= 0 and
					ccw(Q[2], Q[3], p) >= 0 and ccw(Q[3], Q[0], p) >= 0)
		
		a = min(points, key=lambda x: x[0] + x[1])
		b = max(points, key=lambda x: x[0] - x[1])
		c = max(points, key=lambda x: x[0] + x[1])
		d = min(points, key=lambda x: x[0] - x[1])
		Q = [a, b, c, d]
		newSet = list(filter(lambda x: not QuadContains(Q, x), points))
		return ConvexHull.GrahamScan(newSet)



@profile
def main():
	for i in range(10):
		N = randint(30, 10**4)
		points = list(map(tuple, (1e4*np.random.random((N,2))).tolist()))

		ConvexHull.MonotoneChain(points)
		ConvexHull.JarvisMarch(points)
		ConvexHull.QuickHull(points)
		ConvexHull.GrahamScan(points)
		ConvexHull.QuickElimination(points)

"""
def main():
	n = int(input())
	points = [tuple(map(int, input().split(' '))) for i in range(n)]

	result = ConvexHull.GrahamScan(points)
	print("Convex hull of points using GrahamScan algorithm:")
	print(*result, sep='\n')
"""

if __name__ == "__main__":
    main()

