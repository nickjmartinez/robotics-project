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
		self.origin = self.metaData.origin.position
		self.res = self.metaData.resolution		

	def checkForOccupancy(self,x,y):#take in an xy point and return if it is occupied
		origin = self.metaData.origin.position
		res = self.metaData.resolution

		#get the x and y cell positions as specified in the map.yaml
		x_cell = int((x-self.origin.x)/self.res)
		y_cell = int((y-self.origin.y)/self.res)

		return self.checkGridValue(x_cell,y_cell)
		
#shape of the box to check, center dot is the point we want
		# # # # #
		#		#
		#	.	#
		#		#
		# # # # #
	def checkForOccupancyInRange(self,_x,_y,areCells,off):
		#cell offset value from center
		offset = int(off/self.res)
		
		#x and y cell positions
		if areCells:
			x_cell = _x
			y_cell = _y
		else:
			x_cell = int((_x-self.origin.x)/self.res)
			y_cell = int((_y-self.origin.y)/self.res)
		
		#print "My x coor is:",_x," and my y coor is:",_y
		#print "My x cell is:",x_cell," and my y cell is:",y_cell

		occupied = False
		#top and top rows, lock y +- offset, cycle through x-+ offset
		for x in range(x_cell - offset, x_cell + offset + 1):
			if occupied:
				break
			if self.checkGridValue(x,y_cell+offset) or self.checkGridValue(x,y_cell-offset):
				occupied = True
		#side rows, lock x +- offset, cycle through y-+ offset
		for y in range(y_cell - offset, y_cell + offset + 1):
			if occupied:
				break
			if self.checkGridValue(x_cell+offset,y) or self.checkGridValue(x_cell-offset,y):
				occupied = True
	
		return occupied

	def checkGridValue(self, x_cell,y_cell):
		#convert the cell coordinates to an index in the occupancy grid
		gridIndex = x_cell + y_cell*self.metaData.width
		
		#if the grid has a value other than zero, lets assume it is occupied
		return True if self.grid[gridIndex] == 100 else False

if __name__ == "__main__":
	mappy = Mapper()
	print "Occupancy in 0,0: ", mappy.checkForOccupancy(0,0)
	print "Occupancy in 2,-1: ", mappy.checkForOccupancy(2,-1)
	print "Occupancy in 0,4: ", mappy.checkForOccupancy(0,4)

