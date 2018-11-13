#!/usr/bin/env python
import roslib
import rospy
import time
import heapq as hq
import numpy as np
from Node import Node
from Mapper import Mapper

#point of interest class to hold start, goals, etc
class poi:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class pathMaker:
	def __init__(self):
		rospy.init_node('pathPlanner')
		self.mapper = Mapper()
		#if rospy.get_param("robot_minDistance"):
		#	startPos = rospy.get_param("robot_minDistance")
		#	startx, starty = mapper.convertCoorToCells(startPos[0],startPos[1])
		#	start
		#else:
		#	print "Macy what about this one?"

		start = poi(100,100)
		goal = poi(333,250)

		
		startTime = time.time()
		#self.nodeChain = self.astar(start,goal)
		done = self.astar(start,goal)
		done.pn()
		print "Took",time.time() - startTime,"seconds"
	def exists(self,node, li,heap):
		if heap:
			counter = 0
			for i in li:
				if node.compare(i[2]):
					return True, counter
				counter = counter + 1
			return False, -1
		else:
			if li[node.y][node.x] == 0:
				return False
			else:
				return True		

	def astar(self,start,goal):
		#create empty priority queue
		openH = []
		hq.heapify(openH)
	
		#create an empty list to hold nodes we have been to
		closedL = np.zeros((800,1000))

		#initialize the starting node and add it to the queue
		startN = Node(start.x,start.y,None,goal)
		hq.heappush(openH,(startN.f,startN.h,startN))

		#initialize a goal node
		goalN = Node(goal.x,goal.y,None,goal)

		#hold a record for the curr node for when we're done
		curr = None

		while len(openH) != 0:
			f, h, curr = hq.heappop(openH)
			closedL[curr.y][curr.x] = 1
			
			#curr.pn()

			if curr.compare(goalN):
				break

			curr.getChildren()
			for child in curr.children:
				if self.exists(child,closedL,False) or self.mapper.checkForOccupancyInRange(child.x,child.y,True, 0.12):
					#print "we exited here at",child.x,child.y
					continue
				else:
					exist, index = self.exists(child,openH,True)

					if exist:
						#print "existed at",child.x,child.y
						if child.h < openH[index][2].h:
							openH[index] = (child.f,child.h,child)
							hq.heapify(openH)
					else:
						#print "did not exist at",child.x,child.y
						child.parent = curr
						hq.heappush(openH,(child.f,child.h,child))
		
		return curr
		curr.pn()	
		#while curr:
		#	curr.pn()
		#	parent = curr.parent
		#	curr = parent

pather = pathMaker()
