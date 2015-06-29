#!/usr/bin/env python

import random
import math

class Polygon(object):

	originLocation = [] 

	def __init__(self):
		for x in range(0,2):
			self.originLocation[x] = random.randint(0,100) 		

	def pointinPolygon(self,point):
		pass



class regularOctagon(Polygon):

	__poly_length = 0 
	__square_length = 0

	def __init__(self, length):
		self.__poly_length = length
		self.__square_length = 2.414*length
		super(regularOctagon,self).__init__()

	#changes regualrOctagon size
	def morphing (self, length):
		self.__poly_length = length
		self.__square_length = 2.414*length
		
	#Sees if the point lies within the regualrOctagon
	def pointinPolygon(self,point):
		if (point[0] > self.domain(0)) and (point[0] <  self.domain(1)):
			if (point[1] > self.range(0)) and (point[1] < self.range(1)):
				if point[0] < (self.domain(0) + (self.__square_length/(math.sqrt(2)*2.414))):
					if (point[1] > point[0]) and (point[1] < (self.range(0) + point[0])): 
						return "Not Within Octagon"
				elif point[0] > (self.domain(1) - (self.__square_length/(math.sqrt(2)*2.414))):
					if (point[1] > point[0]) and (point[1] < (self.range(0) + point[0])): 
						return "Not Within Octagon"
				elif (True):
					return "Within Octagon"
		return "Not within Octagon"

	def domain (self, z):
		if z == 0:
			return (self.originLocation[0] - (self.__square_length/2))
		else:
			return (self.originLocation[0] + (self.__square_length/2))

	def range (self, z):
		if z == 0:
			return (self.originLocation[1] - (self.__square_length/2))
		else:
			return (self.originLocation[1] + (self.__square_length/2))

		
