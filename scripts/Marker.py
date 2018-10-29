#!/usr/bin/env python
import roslib
import rospy
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

class Markers:
	def __init__(self):
		self.trueArrowId = 0
		self.trueCubeId = 1
		self.falseArrowId = 2
		self.falseCubeId = 3
		self.i=4
		self.markers=[]
		self.pub=rospy.Publisher("/real_robot_pose", MarkerArray, queue_size=200)

	
	def addTruePos(self,x,y,z,w,frame):
		#True Arrow RGB Values
		ar, ag, ab = 1.0, 0, 0
		#True Cube RGB Values
		cr, cg, cb = 1.0, 0, 0
		self.addArrow(self.trueArrowId,x,y,z,w,frame,ar,ag,ab)
		self.addCube(self.trueCubeId,x,y,z,w,frame,cr,cg,cb)
		
	
	def addArrow(self,i,x,y,z,w,frame,ar,ag,ab):
		mr = Marker()
		#Arrow XYZ Scale
		ax, ay, az = 0.5, 0.05, 0.05
		#Add the Arrow to RViz
		self.addMarker(mr,frame,i,mr.ARROW,mr.ADD,x,y,z,w,ax,ay,az,ar,ag,ab,False)

	def addCube(self,i,x,y,z,w,frame,cr,cg,cb):
		mr= Marker()
		#Cube XYZ Scale
		cx,cy,cz = 0.05, 0.05, 0.05
		#Add the Cube to RViz
	 	self.addMarker(mr,frame,i,mr.CUBE,mr.ADD,x,y,z,w,cx,cy,cz,cr,cg,cb,False)
		
	def addPoint(self,x,y,frame):
		mr=Marker()
		sx, sy, sz = 0.05, 0.05, 0.05
		sr, sg, sb = 0, 0, 1.0
		self.addMarker(mr,frame,self.i,mr.SPHERE,mr.ADD,x,y,0.0,0.0,sx,sy,sz,sr,sg,sb,True)

	def addMarker(self,mr,frame,i,shape,action,x,y,z,w,sx,sy,sz,r,g,b,changeI):
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
		if(changeI):
			self.i+=1
		self.markers.append(mr)

	def draw(self):
		markerArray=MarkerArray()
		for m in self.markers:
			markerArray.markers.append(m)
		self.pub.publish(markerArray)
