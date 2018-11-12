#!/usr/bin/env python

#class to store the values for the a* algorithm
class Node:
	def __init__(self,x,y,parent,goal):
		self.x = x
		self.y = y
		self.parent = parent
		self.goal = goal
		self.f, self.g, self.h = self.calculateValues()
		self.children = []

	#calculate the g,h, and then f values for this node
	def calculateValues(self):
		#if a parent exists, calculate values using it
		if self.parent:
			#if we are diagonal from our parent, our distance is 14 + their distance
			if self.x != self.parent.x and self.y != self.parent.y:
				g = self.parent.g + 14
			#if we are level with them, our distance is 10 + their distance			
			else:
				g = self.parent.g + 10
			#calculate the heuristic distance from the goal
			h = self.heuristic()
			#return g and h, as well as their sum f
			return g+h,g,h
		else:
			#if we had no parent(starting node), return 0 for all
			return 0,0,0
	
	def heuristic(self):
		x = self.x
		y = self.y
		d = 0
		#while our x and y are not equal to the goal, incriment them until one is
		while x != self.goal.x and y != self.goal.y:
			#get a 1 or -1 to add to our coordinates
			dx = (self.goal.x - x)/(abs(self.goal.x-x))
			dy = (self.goal.y - y)/(abs(self.goal.y-y))
			#update positions
			x = x + dx
			y = y + dy
			#since we moved diagonally, add 14 to distance
			d = d + 14
		#while our x or y is not equal to the goal, incriment until at goal
		#since for these we are moving in a straight line, add 10 to distance
		while x != self.goal.x:
			dx = (self.goal.x - x)/(abs(self.goal.x-x))
			x = x + dx
			d = d + 10
		while y != self.goal.y:
			dy = (self.goal.y - y)/(abs(self.goal.y-y))
			y = y+ dy
			d = d + 10
		#reached goal, return distance there
		return d
	
	#comparative function for nodes
	def compare(self,node):
		return True if self.x == node.x and self.y == node.y else False
	
	#print info for node
	def pn(self):
		print "Node at ("+str(self.x)+","+str(self.y)+"):\n","f:",self.f,"g:",self.g,"h:",self.h
	
	#get the children of this node
	def getChildren(self):
		for i in range(-1,2):
			for j in range(-1,2):
				if i == 0 and j ==0:
					continue
				node = Node(self.x+i,self.y+j,self,self.goal)
				self.children.append(node)
