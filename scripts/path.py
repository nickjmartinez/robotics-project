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
		self.path = []
		self.timer = 0

		self.minD = 0.07
		self.numOfPoints = 5
		#self.runAStar()

	def testAStar(self):
		start, goals = self.makePOIs()

		start = poi(750,400)
		
		print "Starting Testing A* Algorithm"
		self.timer = time.time()
		self.astar(start,goals[4])
		print "A* finished in",round(time.time() - self.timer,2),"seconds"

		self.publishPath()

	def runAStar(self):
		start, goals = self.makePOIs()
		numG = len(goals)

		print "Starting A* Algorithm"
		self.timer = time.time()
		currPos = start
		while len(goals) > 0:
			print "Making Path to Goal #"+str(numG-len(goals)+1)+", Elapsed Time:",round(time.time()-self.timer,2)
			dmin = np.inf
			minGoalIndex = 0
			counter = 0
			for goal in goals:
				d = np.sqrt((currPos.x-goal.x)**2 + (currPos.y-goal.y)**2)
				if d < dmin:
					dmin = d
					minGoalIndex = counter
				counter = counter + 1
			
			target = goals[minGoalIndex]
			self.astar(currPos,target)
			
			currPos = target
			goals.pop(minGoalIndex)
			#break#remove when ready to vist all goals
			self.publishPath()
			
		print "A* finished in",round(time.time() - self.timer,2),"seconds"

		

	def makePath(self,nodeChain):
		path = []
		curr = nodeChain
		counter = 0
		while curr:
			if counter%self.numOfPoints == 0:
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
		#print "Published path to latched /path_markers topic."

	def makePOIs(self):
		startPos = rospy.get_param("robot_start")
		goalCoors = []

		for i in range(5):
			string = "goal"
			string += str(i)
			goalCoors.append(rospy.get_param(string))
		print "Starting Point:",startPos[0],startPos[1]
		
		startx, starty = self.mapper.convertCoorToCells(startPos[0],startPos[1])
		self.marker.addGoalPoint(startPos[0],startPos[1],"map")		

		goals = []
		for i,j in goalCoors:
			self.marker.addGoalPoint(i,j,"map")
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
		
		#create an empty list to hold open node g values
		openL = np.zeros((self.mapper.metaData.height,self.mapper.metaData.width))

		#create an empty list to hold nodes we have been to
		closedL = np.zeros((self.mapper.metaData.height,self.mapper.metaData.width))

		#initialize the starting node and add it to the queue
		startN = Node(start.x,start.y,None,goal)
		hq.heappush(openH,(startN.f,startN.h,startN))
		openL[startN.y][startN.x] = -1

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
				if child.x > 800 and child.y > 400:
					self.minD = 0.07
				else:
					self.minD = 0.10
				if self.exists(child,closedL) or self.mapper.checkForOccupancyInRange(child.x,child.y,True,self.minD):
					#print "we exited here at",child.x,child.y
					continue
				else:
					inOpenL = self.exists(child,openL)

					if not inOpenL or child.g < openL[child.y][child.x]:
						
						
						child.parent = curr
						if not inOpenL:
							hq.heappush(openH,(child.f,child.h,child))
							openL[child.y][child.x] = child.g
						else:
							index = self.getIndexInHeap(child, openH)
							openH[index] = (child.f,child.h,child)
							hq.heapify(openH)
							openL[child.y][child.x] = child.g
					
						
		
		self.makePath(curr)
