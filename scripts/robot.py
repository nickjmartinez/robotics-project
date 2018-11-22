#!/usr/bin/env python
import roslib
import rospy
import Mapper
from path import pathMaker
import numpy as np
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class robot:
	def __init__(self):
		rospy.init_node('robot')
		self.mapper = Mapper.Mapper()
		self.pm = pathMaker()
		#self.pm.testAStar()	
		self.pm.runAStar()	
		self.path = self.pm.path
		self.posInPath = 0
		self.curx = np.inf
		self.cury = np.inf
		
		self.ang = 0
		self.yaw = 0

		self.rotating = False
		self.driving = False

		self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		self.sub = rospy.Subscriber('/base_pose_ground_truth',Odometry,self.callback)
		
	
	def callback(self,data):
		if self.posInPath == len(self.path):
			return
		
		tw = Twist()
		pos = data.pose.pose.position		
		q = data.pose.pose.orientation
		
		point = self.path[self.posInPath]

		if not self.driving:
			self.ang = np.arctan2(point[1] - pos.y, point[0] - pos.x)

			siny = 2.0 * (q.w * q.z + q.x * q.y);
			cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z);  
			self.yaw = np.arctan2(siny, cosy);
		
		#if not driving, check if we are lined up
		if not self.driving:
			if abs(round(self.ang-self.yaw,1)) != 0.0:
				self.driving = False
				self.rotating = True
				tw.linear.x = 0.0
				tw.angular.z = 0.4*(self.ang-self.yaw)/abs(self.ang-self.yaw)
			else:
				tw.linear.x = 0.0
				tw.angular.z = 0.0
				self.driving = True
				self.rotating = False
				
		if not self.rotating:
			tw.angular.z=0
			if round(np.sqrt((point[0]-pos.x)**2+(point[1]-pos.y)**2),1) != 0:
				tw.linear.x = 0.5
				tw.angular.z = 0.0				
				self.driving = True
				self.rotating = False
			else:
				tw.linear.x = 0.0
				tw.angular.z = 0.0				
				self.driving = False
				self.rotating = False
				self.posInPath += 1
			
		
		self.pub.publish(tw)

try:
	rob = robot()
	rospy.spin()
except rospy.ROSInterruptException:
	pass
