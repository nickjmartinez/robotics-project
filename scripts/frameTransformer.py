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
		self.sub = rospy.Subscriber('/base_pose_ground_truth',Odometry,self.updateTruePosition)
		self.odomSub = rospy.Subscriber('/odom',Odometry,self.updateOdomPosition)
		self.listener=tf.TransformListener()
		self.m=Marker.Markers()
		self.lastx=10000;
		self.lasty=10000;

	def updateTruePosition(self,data):
		#Set up variables for info from topic
		local = data.pose.pose
		pos = local.position
		ori = local.orientation
		
		#Add the true position location and arrow
		self.m.addTruePos(pos.x,pos.y,ori.z,ori.w,"map")

		#if our new location is different than the last one we painted, paint the new one
		if((local.position.x != self.lastx) or (local.position.y != self.lasty)):
			self.lastx = local.position.x
			self.lasty = local.position.y
			self.m.addPoint(local.position.x,local.position.y,"map")
		
		#Once called method to draw to RViz
		self.m.draw()

	def updateOdomPosition(self,data):
		local = data.pose.pose
		pos = local.position
		ori = local.orientation
	
		try:
			ps = PointStamped(header=Header(stamp=rospy.Time.now(),frame_id="/odom"),point=Point(pos.x,pos.y,0))
			newp = self.listener.transformPoint("/map",ps)
			self.m.addFalsePos(newp.point.x,newp.point.y,ori.z,ori.w,"map")
			#self.m.addFalsePos(pos.x,pos.y,ori.z,ori.w,"map")
		except(tf.LookupException, tf.ExtrapolationException):
			return

optimus=transformer()
rospy.spin()
