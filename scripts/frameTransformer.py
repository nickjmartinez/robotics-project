#!/usr/bin/env python
import roslib
import rospy
import Marker
import tf
import numpy as np
from nav_msgs.msg import Odometry

class transformer:
	def __init__(self):
		rospy.init_node('transformer')
		self.sub = rospy.Subscriber('/base_pose_ground_truth',Odometry,self.updateTruePosition)
		self.br = tf.TransformBroadcaster()
		
		self.m=Marker.Markers()
		self.curx=np.inf;
		self.cury=np.inf;

	def updateTruePosition(self,data):
		#Set up variables for info from topic
		local = data.pose.pose
		pos = local.position
		ori = local.orientation
		
		#update the real_robot_pose frame
		self.br.sendTransform((pos.x,pos.y,pos.z),(ori.x,ori.y,ori.z,ori.w),rospy.Time.now(),"real_robot_pose","map")
	
		#Add the true position location and arrow
		#self.m.addTruePos(0,0,0,1,"real_robot_pose")

		#if our new location is different than the last one we painted, paint the new one
		if((pos.x != self.curx) or (pos.y != self.cury)):
			self.curx = pos.x
			self.cury = pos.y
			self.m.addPoint(pos.x,pos.y,"map")
		
		#Once called method to draw to RViz
		self.m.draw()

optimus=transformer()
rospy.spin()
