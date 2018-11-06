#!/usr/bin/env python
import roslib
import rospy
from geometry_msgs.msg import Twist

class robot:
	def __init__(self):
		rospy.init_node('robot')
		pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
		rate = rospy.Rate(5)
		while not rospy.is_shutdown():
			tw=Twist()
			tw.linear.x=0.5
			tw.angular.z=0.5
			pub.publish(tw)
			rate.sleep()

try:
	rob = robot()
except rospy.ROSInterruptException:
	pass
