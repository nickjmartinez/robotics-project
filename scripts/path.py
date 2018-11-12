#!/usr/bin/env python
import roslib
import rospy
import heapq as hq
from Node import Node
from Mapper import Mapper

#point of interest class to hold start, goals, etc
class poi:
	def __init__(self,x,y):
		self.x = x
		self.y = y

def exists(node, li,heap):
	if heap:
		counter = 0
		for i in li:
			if node.compare(i[1]):
				return True, counter
			counter = counter + 1
		return False, -1
	else:
		for i in li:
			if node.compare(i):
				return True
		return False		

def astar(start,goal):
	#create empty priority queue
	openH = []
	hq.heapify(openH)
	
	#create an empty list to hold nodes we have been to
	closedL = []

	#initialize the starting node and add it to the queue
	startN = Node(start.x,start.y,None,goal)
	hq.heappush(openH,(startN.f,startN))

	#initialize a goal node
	goalN = Node(goal.x,goal.y,None,goal)

	#hold a record for the curr node for when we're done
	curr = None

	while len(openH) != 0:
		f, curr = hq.heappop(openH)
		closedL.append(curr)

		if curr.compare(goalN):
			break

		curr.getChildren()
		for child in curr.children:
			if exists(child,closedL,False) or omap.checkForOccupancyInRange(child.x,child.y,True, 0.12):
				
				continue
			
			exist, index = exists(child,openH,True)

			if exist:
				if child.h < openH[index][1].h:
					openH[index][1].f = child.f
					openH[index][1].g = child.g
					openH[index][1].h = child.h
					openH[index][1].parent = curr

			if not exist:
				child.parent = curr
				hq.heappush(openH,(child.f,child))
	curr.pn()	
	while curr.parent:
		parent = curr.parent
		parent.pn()
		curr = parent
start = poi(100,100)
goal = poi(125,110)

omap = Mapper()

astar(start,goal)
