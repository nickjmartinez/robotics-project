#!/usr/bin/env python
import roslib
import rospy
import Marker
import tf
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Header
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry

class transformer:
	def __init__(self):
		rospy.init_node('transformer')
		self.sub = rospy.Subscriber('/base_pose_ground_truth',Odometry,self.callback)
		self.listener=tf.TransformListener()
		self.m=Marker.Markers()
		self.lastx=10000;
		self.lasty=10000;

	def callback(self,data):
		local = data.pose.pose
		pos = local.position
		ori = local.orientation
		try:
			self.m.addTruePos(pos.x,pos.y,ori.z,ori.w,"map")
			if((local.position.x != self.lastx) or (local.position.y != self.lasty)):
				self.lastx = local.position.x
				self.lasty = local.position.y
				self.m.addPoint(local.position.x,local.position.y,"map")

		except(tf.LookupException, tf.ExtrapolationException):
			return
		
		self.m.draw()

optimus=transformer()
rospy.spin()
