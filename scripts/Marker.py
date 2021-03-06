#!/usr/bin/env python
import roslib
import rospy
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

class MarkerMaker:
	def __init__(self,pubTopic,latch):
		self.i=0
		self.markers=[]
		self.pub=rospy.Publisher(pubTopic, MarkerArray, queue_size=200,latch=latch)
		
	def addPoint(self,x,y,frame):
		mr=Marker()
		sx, sy, sz = 0.05, 0.05, 0.05
		sr, sg, sb = 0, 0, 1.0
		self.addMarker(mr,frame,self.i,mr.SPHERE,mr.ADD,x,y,0.0,0.0,sx,sy,sz,sr,sg,sb)
		self.i+=1
	
	def addPathPoint(self,x,y,frame):
		mr=Marker()
		px, py, pz = 0.05, 0.05, 0.05
		pr, pg, pb = 1.0, 0, 0
		self.addMarker(mr,frame,self.i,mr.CUBE,mr.ADD,x,y,0.0,0.0,px,py,pz,pr,pg,pb)
		self.i+=1

	def addGoalPoint(self,x,y,frame):
		mr=Marker()
		px, py, pz = 0.10, 0.10, 0.10
		pr, pg, pb = 0, 1.0, 0
		self.addMarker(mr,frame,self.i,mr.CUBE,mr.ADD,x,y,0.0,0.0,px,py,pz,pr,pg,pb)
		self.i+=1

	def addMarker(self,mr,frame,i,shape,action,x,y,z,w,sx,sy,sz,r,g,b):
		mr.header.frame_id=frame
		mr.ns="basic"
		mr.id= i
		mr.type=shape
		mr.action=action
		mr.pose.position.x=x
		mr.pose.position.y=y
		mr.pose.orientation.z=z
		mr.pose.orientation.w=w
		mr.scale.x=sx
		mr.scale.y=sy
		mr.scale.z=sz
		mr.color.r=r
		mr.color.g=g
		mr.color.b=b
		mr.color.a=1.0
		self.markers.append(mr)

	def draw(self):
		markerArray = MarkerArray()
		for m in self.markers:
			markerArray.markers.append(m)
		self.pub.publish(markerArray)
