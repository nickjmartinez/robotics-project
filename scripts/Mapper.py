#!/usr/bin/env python
import roslib
import rospy
from nav_msgs.msg import OccupancyGrid

class Mapper:
	def __init__(self):
		#this line is only required if mapper is by itself, not attached to a node
		#rospy.init_node('Mapper')

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
		x_cell, y_cell = self.convertCoorToCells(x,y)

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
			x_cell, y_cell = _x,_y
		else: 
			x_cell, y_cell = self.convertCoorToCells(_x,_y)
		
		#print "My x coor is:",_x," and my y coor is:",_y
		#print "My x cell is:",x_cell," and my y cell is:",y_cell

		occupied = False
		#top and bottom rows, lock y +- offset, cycle through x-+ offset
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
	
	def convertCoorToCells(self,x_coor,y_coor):
		x_cell = int((x_coor-self.origin.x)/self.res)
		y_cell = int((y_coor-self.origin.y)/self.res)
		return x_cell, y_cell

	def convertCellToCoor(self,x_cell,y_cell):
		x_coor = round(x_cell * self.res + self.origin.x,2)
		y_coor = round(y_cell * self.res + self.origin.y,2)
		return x_coor,y_coor

if __name__ == "__main__":
	mappy = Mapper()
	print "Occupancy in 0,0: ", mappy.checkForOccupancy(0,0)
	print "Occupancy in 2,-1: ", mappy.checkForOccupancy(2,-1)
	print "Occupancy in 0,4: ", mappy.checkForOccupancy(0,4)

