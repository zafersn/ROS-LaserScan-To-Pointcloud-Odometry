#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Point, PoseStamped, PointStamped
import serial

class subRoot(object):
	def __init__(self):
		self.datas=""
	    	self.subC=rospy.Subscriber("subCode", String, self.callback)
		self.ser = serial.Serial('/dev/ttyACM2',57600)
		
	def callback(self,data):
    		rospy.loginfo("I heard %s", data.data)
    		#self.ser.write(data.data)
		self.datas=data.data
    
	def publish_closest_obstacle(self):
		self.ser.write(self.datas)



if __name__ == '__main__':
    try:
	rospy.init_node('listener_closest', anonymous=True)
	r=rospy.Rate(30)
	lr=subRoot()
	isOp=lr.ser.isOpen()
	if isOp:
		print("serialOpen")
	while not rospy.is_shutdown():
		lr.publish_closest_obstacle()
		r.sleep()
	rospy.spinOnce()
        
    except rospy.ROSInterruptException:
        pass
