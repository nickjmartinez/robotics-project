#!/usr/bin/env python
import roslib
import rospy
import heapq as hq

class poi:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Node:	#class to store the values for the a* algorithm
	def __init__(self,x,y,parent):
		self.x = x
		self.y = y
		self.parent = parent
		self.f, self.g, self.h = self.calculateValues()
		self.children = []
	
	def calculateValues(self):
		if self.parent:
			if self.x != self.parent.x and self.y != self.parent.y:
				g = self.parent.g + 14
			else:
				g = self.parent.g + 10

			h = self.heuristic()
			return g+h,g,h
		else:
			return 0,0,0
	
	def heuristic(self):
		x = self.x
		y = self.y
		d = 0
		#print "goal x",goal.x,"goal y",goal.y
		while x != goal.x and y != goal.y:
			dx = (goal.x - x)/(abs(goal.x-x))
			dy = (goal.y - y)/(abs(goal.y-y))
			#print dx,dy
			x = x + dx
			y = y + dy
			#print x,y
			d = d + 14
		while x != goal.x:
			dx = (goal.x - x)/(abs(goal.x-x))
			x = x + dx
			#print "x stuff:",x,dx
			d = d + 10
		while y != goal.y:
			dy = (goal.y - y)/(abs(goal.y-y))
			y = y+ dy
			#print "y stuff:",y,dy
			d = d + 10
		#print "Done"
		return d
	
	def compare(self,node):
		return True if self.x == node.x and self.y == node.y else False

	def pn(self):
		print "Node at ("+str(self.x)+","+str(self.y)+"):		\n","f:",self.f,"g:",self.g,"h:",self.h

	def getChildren(self):
		for i in range(-1,2):
			for j in range(-1,2):
				if i == 0 and j ==0:
					continue
				node = Node(self.x+i,self.y+j,self)
				self.children.append(node)

goal = poi(-3,3)

n1 = Node(0,0,None)
n1.pn()
n1.getChildren()

for n in n1.children:
	n.pn()
