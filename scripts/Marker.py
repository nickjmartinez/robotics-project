#!/usr/bin/env python
import roslib
import rospy
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

class Markers:
	def __init__(self):
		self.i=0
		self.markers=[]
		self.pub=rospy.Publisher("/real_robot_pose", MarkerArray, queue_size=200)
		
	def add(self,x,y,z,w,frame):
		mr=Marker()
		mr.header.frame_id=frame
		mr.ns="basic"
		mr.id=self.i
		mr.type=mr.ARROW
		mr.action=mr.ADD
		mr.pose.position.x=x
		mr.pose.position.y=y
		mr.pose.orientation.z=z
		mr.pose.orientation.w=w
		mr.scale.x=1
		mr.scale.y=0.05
		mr.scale.z=0.05
		mr.color.r=0
		mr.color.g=0
		mr.color.b=1.0
		mr.color.a=1.0
		self.markers.append(mr)
		self.i+=1

	def draw(self):
		markerArray=MarkerArray()
		for m in self.markers:
			markerArray.markers.append(m)
		self.pub.publish(markerArray)
		self.i=0
