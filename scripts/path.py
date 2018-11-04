#!/usr/bin/env python
import roslib
import rospy
import heapq

class Node:	#class to store the values for the a* algorithm
	def __init__(self,f,g,h):
		self.f = f
		self.g = g
		self.h = h
	def tuple(self):
		return [self.f,self.g,self.h]
	

