#!/usr/bin/env python
import roslib
import rospy
import Mapper
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class robot:
	def __init__(self):
		rospy.init_node('robot')
		self.sub = rospy.Subscriber('/base_pose_ground_truth',Odometry,self.callback)
		self.mapper = Mapper.Mapper()
		self.minD = float(rospy.get_param("robot_minDistance"))
	
	def callback(self,data):
		local = data.pose.pose
		pos = local.position
		ori = local.orientation
	
		

try:
	rob = robot()
except rospy.ROSInterruptException:
	pass
