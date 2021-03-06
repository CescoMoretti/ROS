#!/usr/bin/env python

import rospy
from wall_following.msg import pid_input
from geometry_msgs.msg import Point32
from std_msgs.msg import Bool
import math
global kp
global kd
global vel_input
kp = 0.75
kd = 0.17
servo_offset = 0.0	# zero correction offset in case servo is misaligned. 
prev_error = 0.0
vel_input = 0.30	
past_vel = 0.0

pub = rospy.Publisher('drive_parameters', Point32, queue_size=10)

def control(data):
	global prev_error
	global vel_input	
	global kp
	global kd	
	global past_vel

	#scale error 
	error = data.pid_error
	if abs(error) < 0.005:
		error = 0.0

	#PD control per sterzo e velocita 		
	anglecorr = kp * error # + kd * (prev_error - error)
	angle = -anglecorr + servo_offset
	#angle = prev_error - anglecorr		
	prev_error = error                  
	
	#controllo sterzo
	if angle < -0.5:
		angle = -0.5
	elif angle > 0.5:
		angle = 0.5
	
	#controllo velocita
	if data.pid_vel > 2.2:
		vel = 15000.0
	else:
		vel = 8000.0
	
	#pubblish msg
	msg = Point32()
	msg.x = vel	
	msg.y = angle
	pub.publish(msg)

if __name__ == '__main__':
	
	print("Listening to error for PID")	
	rospy.init_node('pid_controller', anonymous=True)
	rospy.Subscriber("/error", pid_input, control)
	rospy.spin()
