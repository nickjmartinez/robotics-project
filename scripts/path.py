#!/usr/bin/env python
import roslib
import rospy
import heapq as hq
from Node import Node

#point of interest class to hold start, goals, etc
class poi:
	def __init__(self,x,y):
		self.x = x
		self.y = y

goal = poi(-3,3)

n1 = Node(0,0,None,goal)
n1.getChildren()
n1.pn()

for n in n1.children:
	n.pn()


