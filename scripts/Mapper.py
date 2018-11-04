#!/usr/bin/env python
import roslib
import rospy
from nav_msgs.msg import OccupancyGrid

class Mapper:
	def __init__(self):
		rospy.init_node('Mapper')
		#in order to guarentee we have received map info, wait for the message
		msg = rospy.wait_for_message('/map', OccupancyGrid, timeout=None)
		#store the occupancy grid and map meta data
		self.grid = msg.data
		self.metaData = msg.info
		
	def checkForOccupancy(self,x,y):#take in an xy point and return if it is occupied
		origin = self.metaData.origin.position
		res = self.metaData.resolution

		#get the x and y cell positions as specified in the map.yaml
		x_cell = int((x-origin.x)/res)
		y_cell = int((y-origin.y)/res)

		#convert the cell coordinates to an index in the occupancy grid
		gridIndex = x_cell + y_cell*self.metaData.width
		
		#if the grid has a value other than zero, lets assume it is occupied
		if self.grid[gridIndex] != 0:
			return True 	#occupied
		else:
			return False	#not

mappy = Mapper()
print "Occupancy in 0,0: ", mappy.checkForOccupancy(0,0)
print "Occupancy in 2,-1: ", mappy.checkForOccupancy(2,-1)
print "Occupancy in 0,4: ", mappy.checkForOccupancy(0,4)

