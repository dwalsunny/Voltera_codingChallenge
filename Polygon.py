#!/usr/bin/env python

import random
import math

class Polygon(object):

	originLocation = [0,0] #member


	#This is the constructor. A constructor is a method.  It is a special a method, and it builds the object.  An object is a instance of the class. 
	def __init__(self):
		for x in range(0,2):
			self.originLocation[x] = random.randint(0,100) 		

	def printsomething(self): #testing method
		print self.originLocation

	def pointinPolygon(self,point):
		pass



class regularOctagon(Polygon):

	__length = 0 #member
	#__domain = [(originLocation[0] - (__length/2)), (originLocation[0] + (__length/2))]
	#__range = [(originLocation[1] - (__length/2)), (originLocation[1] + (__length/2))]


	def __init__(self, length):
		self.__length = length
		super(regularOctagon,self).__init__()



	def morphing (self, length):
		self.__length = length

	def pointinPolygon(self,point):
		if (point[0] > self.domain(0)) and (point[0] <  self.domain(1)):
			if (point[1] > self.range(0)) and (point[1] < self.range(1)):
				if point[0] < (self.domain(0) + (self.__length/(math.sqrt(2)*2.414))):
					if (point[1] > point[0]) and (point[1] < (self.range(0) + point[0])): 
						return "Not Within Octagon"
				elif point[0] > (self.domain(1) - (self.__length/(math.sqrt(2)*2.414))):
					if (point[1] > point[0]) and (point[1] < (self.range(0) + point[0])): 
						return "Not Within Octagon"
				elif (True):
					return "Within Octagon"
		return "Not within Octagon"

	def domain (self, z):
		if z == 0:
			return (self.originLocation[0] - (self.__length/2))
		else:
			return (self.originLocation[0] + (self.__length/2))
	def range (self, z):
		if z == 0:
			return (self.originLocation[1] - (self.__length/2))
		else:
			return (self.originLocation[1] + (self.__length/2))

		

Angela = regularOctagon (10)

Angela.printsomething()

print (Angela.pointinPolygon([50,50]))
