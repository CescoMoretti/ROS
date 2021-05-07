#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from wall_following.msg import pid_input
# Import whatever else you think is necessary

# Some useful variable declarations.
angle_range = 0		# sensor angle range of the lidar
car_length = 1.5	# distance (in m) that we project the car forward for correcting the error. You may want to play with this. 
desired_trajectory = 1	# distance from the wall (left or right - we cad define..but this is defined for right). You should try different values
vel = 20 		# this vel variable is not really used here.
error = 0.0

pub = rospy.Publisher('/error', pid_input, queue_size=10)
# change the value of x to your team number.

##	Input: 	data: Lidar scan data
##			theta: The angle at which the distance is requried
##	OUTPUT: distance of scan at angle theta

def getRange(data,theta):
	ind = theta * (len(data.ranges)/270)
	data.ranges[int(ind)]

	'''
	if data.ranges[int(ind)] != "nan":
		return data.ranges[int(ind)]
	else:
		return 10.0
	'''
# Find the index of the arary that corresponds to angle theta.
# Return the lidar scan value at that index
# Do some error checking for NaN and ubsurd values
	return 

def callback(data):
	theta = 40
	a0 = 40
	a1 = a0 + theta
	vel = 1
	a = getRange(data,a1)
	print a 
	b = getRange(data,a0)	
	swing = math.radians(theta)	
	
	AC = 1.0
	## Your code goes here to compute alpha, AB, and CD..and finally the error.
	alpha = math.atan2(a* math.cos(swing)-b, a*math.sin(swing))
	AB = b* math.cos(alpha)
	CD = AB + AC * math.sin(alpha)
	error = 0.5- CD
	
	#collision avoidance
	if getRange(data,130) < 0.5:
		vel=0

	#publish msg
	msg = pid_input()
	msg.pid_error = error		
	msg.pid_vel = vel		
	pub.publish(msg)
	

if __name__ == '__main__':
	print("Laser node started")
	rospy.init_node('dist_finder',anonymous = True)
	rospy.Subscriber("/scan",LaserScan,callback)
	# subscribe to the correct /car_x/scan topic for your car..
	rospy.spin()
