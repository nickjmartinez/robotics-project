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
		self.pm.runAStar()		
		self.path = self.pm.path
		self.curx = np.inf
		self.cury = np.inf

		#self.sub = rospy.Subscriber('/base_pose_ground_truth',Odometry,self.callback)
		
	
	#def callback(self,data):
		
try:
	rob = robot()
	rospy.spin()
except rospy.ROSInterruptException:
	pass
