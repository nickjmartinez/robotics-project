#!/usr/bin/env python
import roslib
import rospy
import time
import heapq as hq
import numpy as np
from Node import Node
from Mapper import Mapper
from Marker import MarkerMaker

#point of interest class to hold start, goals, etc
class poi:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class pathMaker:
	def __init__(self):
		#rospy.init_node('pathPlanner')
		self.mapper = Mapper()
		self.marker = MarkerMaker("/path_markers",True)
		#self.pub=rospy.Publisher(pubTopic, MarkerArray, queue_size=200,latch=latch)
		self.path = []
		

	def runAStar(self):
		start, goals = self.makePOIs()
		
		currPos = start
		currGoal = goals[0]

		print "Starting A* Algorithm"
		startTime = time.time()
		self.astar(currPos,currGoal)
		
		currPos = currGoal
		currGoal = goals[1]
		#self.astar(currPos,currGoal)

		currPos = currGoal
		currGoal = goals[3]
		#self.astar(currPos,currGoal)

		currPos = currGoal
		currGoal = goals[2]
		#self.astar(currPos,currGoal)

		print "Took",time.time() - startTime,"seconds"

		self.publishPath()

	def makePath(self,nodeChain):
		path = []
		curr = nodeChain
		counter = 0
		while curr:
			if counter%7 == 0:
				x,y = self.mapper.convertCellToCoor(curr.x,curr.y)
				path.append((round(x,2),round(y,2)))
			curr = curr.parent
			counter+= 1
			
		path.reverse()
		self.path.extend(path)

	def publishPath(self):
		for i in self.path:
			self.marker.addPathPoint(i[0],i[1],"map")
		self.marker.draw()
		print "Published path to latched /path_markers topic."

	def makePOIs(self):
		startPos = rospy.get_param("robot_start")
		goalCoors = []

		for i in range(5):
			string = "goal"
			string += str(i)
			goalCoors.append(rospy.get_param(string))
		print "Starting Point:",startPos[0],startPos[1]
		
		startx, starty = self.mapper.convertCoorToCells(startPos[0],startPos[1])
		
		goals = []
		for i,j in goalCoors:
			goalx, goaly = self.mapper.convertCoorToCells(i,j)
			goals.append(poi(goalx,goaly))
	
		start = poi(startx,starty)

		return start, goals

	def exists(self,node, li):
			if li[node.y][node.x] == 0:
				return False
			else:
				return True		

	def getIndexInHeap(self, node, heap):
		counter = 0
		for i in heap:
			if node.compare(i[2]):
				return counter
			counter = counter + 1
		return -1

	def astar(self,start,goal):
		#create empty priority queue
		openH = []
		hq.heapify(openH)
		
		#create an empty list to hold open node h values
		openL = np.zeros((self.mapper.metaData.height,self.mapper.metaData.width))

		#create an empty list to hold nodes we have been to
		closedL = np.zeros((self.mapper.metaData.height,self.mapper.metaData.width))

		#initialize the starting node and add it to the queue
		startN = Node(start.x,start.y,None,goal)
		hq.heappush(openH,(startN.f,startN.h,startN))
		openL[startN.y][startN.x] = startN.h

		#initialize a goal node
		goalN = Node(goal.x,goal.y,None,goal)

		#hold a record for the curr node for when we're done
		curr = None

		while len(openH) != 0:
			f, h, curr = hq.heappop(openH)
			openL[curr.y][curr.x] = 0
			closedL[curr.y][curr.x] = 1
			
			#curr.pn()

			if curr.compare(goalN):
				break

			curr.getChildren()
			for child in curr.children:
				if self.exists(child,closedL) or self.mapper.checkForOccupancyInRange(child.x,child.y,True, 0.12):
					#print "we exited here at",child.x,child.y
					continue
				else:
					exist = self.exists(child,openL)

					if exist:
						if child.h < openL[child.y][child.x]:
							index = self.getIndexInHeap(child, openH)
							openH[index] = (child.f,child.h,child)
							hq.heapify(openH)
							openL[child.y][child.x] = child.h
					else:
						child.parent = curr
						hq.heappush(openH,(child.f,child.h,child))
						openL[child.y][child.x] = child.h
		
		self.makePath(curr)

#pather = pathMaker()
#rospy.spin()
