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

	def callback(self,data):
		local = data.pose.pose
		try:
			#print "Points: " + str(local.position.x) + str(local.position.y)
			#ps=PointStamped(header=Header(stamp=rospy.Time.now(),frame_id="/odom"),point=Point(local.position.x,local.position.y,0))
			#p = self.listener.transformPoint(ps,"/map")
			#print "P Point: " + str(p.point.x) + str(p.point.y)
			self.m.add(local.position.x,local.position.y,local.orientation.z,local.orientation.w,"map")
		except(tf.LookupException, tf.ExtrapolationException):
			return
		
		self.m.draw()

optimus=transformer()
rospy.spin()
