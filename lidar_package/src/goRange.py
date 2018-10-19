#!/usr/bin/env python
# license removed for brevity
import rospy
from lidar_package.msg import X,Range
import serial

class RangeRot(object):
	def __init__(self):
		self.xl=X()
		self.laserS=rospy.Subscriber("/x_range", X, self.range_callback)
		#self.closestP=rospy.Publisher("/closest_point", PointStamped, queue_size=1)
		self.ser = serial.Serial('/dev/ttyACM1',57600)
		self.mylist=[]
		self.NewMax=155
		self.NewMin=105
		self.OldMax=5.6
		self.OldMin=1.95

	def range_callback (self, msg):
		self.xl=msg
	def calculatePWM(self,NewMax,NewMin,OldMax,OldMin,OldValue):
		NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
		return NewValue
	def publish_closest_obstacle(self):
		if self.xl.range.range !=0:
			xl = self.xl.range.range
			posX=self.xl.range.x
			posAngRad=self.xl.range.angRad

			self.mylist.append(xl)
			#print(len(self.mylist))
			if len(self.mylist)%10==0:
				srtArry= sorted(self.mylist, reverse=True)
			#	print (srtArry)
				srtArry.remove(srtArry[0])
				srtArry.remove(srtArry[-1])
			#	print len(srtArry)
			#	print srtArry
				del self.mylist[:]
				redcArry=reduce(lambda x,y: x+y, srtArry)/len(srtArry)
				print redcArry
				pwmRedc=self.calculatePWM(self.NewMax,self.NewMin,self.OldMax,self.OldMin,redcArry)
				print pwmRedc
				self.ser.write(str(pwmRedc))
				
			#data=str(posX)+":"+str(posAngRad)
			
			#print (data)
			
			
	
		
if __name__ == '__main__':
    try:
	rospy.init_node("go_range_data")
	r=rospy.Rate(30)
	lr=RangeRot()
	isOp=lr.ser.isOpen()
	if isOp:
		print("serialOpen")

	while not rospy.is_shutdown():
		lr.publish_closest_obstacle()
		r.sleep()
        
    except rospy.ROSInterruptException:
        pass


