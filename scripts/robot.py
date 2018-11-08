#!/usr/bin/env python
import roslib
import rospy
import Mapper
import numpy as np
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class robot:
	def __init__(self):
		rospy.init_node('robot')
		self.mapper = Mapper.Mapper()
		#self.minD = float(rospy.get_param("robot_minDistance"))
		self.minD = 0.12
		self.curx = np.inf
		self.cury = np.inf

		self.sub = rospy.Subscriber('/base_pose_ground_truth',Odometry,self.callback)
		
	
	def callback(self,data):
		local = data.pose.pose
		pos = local.position
		ori = local.orientation
	
		if((pos.x != self.curx) or (pos.y != self.cury)):
			self.curx = pos.x
			self.cury = pos.y
			
		if self.mapper.checkForOccupancyInRange(pos.x,pos.y,self.minD):
			print "Within range of an obstable!! Time:",rospy.Time.now()
try:
	rob = robot()
	rospy.spin()
except rospy.ROSInterruptException:
	pass
