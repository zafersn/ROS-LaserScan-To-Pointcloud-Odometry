#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point, PoseStamped, PointStamped
from lidar_package.msg import X,Range
from std_msgs.msg import String
import tf2_ros
import PyKDL
import tf2_geometry_msgs
from math import cos,sin


class LaserRot(object):
	def __init__(self):
		self.laser=LaserScan()
		self.laserS=rospy.Subscriber("/scan", LaserScan, self.laser_callback)
		self.closestP=rospy.Publisher("/closest_point", PointStamped, queue_size=1)
		self.pub = rospy.Publisher('subCode', String, queue_size=10)
		self.rangeLs=rospy.Publisher("/x_range", X, queue_size=1)
		self.tf_buffer=tf2_ros.Buffer(rospy.Duration(1200.0))
		self.tf_listener=tf2_ros.TransformListener(self.tf_buffer)
		self.get_transform()
		self.OldMin=0.5
		self.now=0

	def get_transform(self):
		try:
			self.transform = self.tf_buffer.lookup_transform("laser", "laser", rospy.Time(0), rospy.Duration(1.0))
		except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
			#rospy.logerror("Error getting transform")
			print "Error"
   
	def laser_callback (self, msg):
		self.laser=msg
		self.get_transform()

	def publish_closest_obstacle(self):
		laser = self.laser.ranges
		shortest_laser = 1.2
		mintest_laser=self.OldMin
		point=Point()
		rangeL=Range()

		
		for i in range(len(laser)):
			if laser[i] < shortest_laser and laser[i]>mintest_laser:
				angle=self.laser.angle_min + i*self.laser.angle_increment
				x=laser[i]*cos(angle)

				#if angle>0.2:
				#	shotest_laser=laser[i]
				#	point.x=x
				#	point.y=shortest_laser*sin(angle)

				if (angle>1.2 and angle <2.0) or (angle<-1.2 and angle>-2.0) :
					shortest_laser=laser[i]
					point.x=x
					point.y=shortest_laser*sin(angle)
					print ("laser: ",laser[i]," angleDeg: ",angle*57.2958," rad: ",angle)
					self.pub.publish("1")
					rangeL.range=shortest_laser
					rangeL.x=x
					rangeL.y=shortest_laser*sin(angle)
					rangeL.angRad=angle
					self.now = rospy.get_time()
					#print "time111",self.now
				else:
					ifTime=rospy.get_time()
					#print "time222",ifTime," cik: ",ifTime-self.now
#					print "elsee"
					if(ifTime-self.now>0.6):
						self.pub.publish("0")
			
					
		pose=PoseStamped()
		xL=X()
		xL.header=self.laser.header
		pose.header=self.laser.header
		point.z=0.0
		rangeL.z=0.0
		xL.range=rangeL
		pose.pose.position=point
		#print(point)

		pose_transformed= tf2_geometry_msgs.do_transform_pose(pose, self.transform)
		point_transformed=PointStamped()	
		point_transformed.header=pose_transformed.header
		point_transformed.point = pose_transformed.pose.position
		self.closestP.publish(point_transformed)

		
		self.rangeLs.publish(xL)

rospy.init_node("compute_closest_obstcl")
r=rospy.Rate(30)
lr=LaserRot()

while not rospy.is_shutdown():
	lr.publish_closest_obstacle()
	r.sleep()
