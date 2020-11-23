#!/usr/bin/env python

import rospy
from race.msg import pid_input
from ackermann_msgs.msg import AckermannDrive
import math

kp = 0.64
kd = 0.17
servo_offset = 0	# zero correction offset in case servo is misaligned. 
prev_error = 0.0
vel_input = 0.30	# arbitrarily initialized. 25 is not a special value. This code can accept input desired velocity from the user.
past_vel = 0.0

pub = rospy.Publisher('/car_1/offboard/command', AckermannDrive, queue_size=10)
# setup a publisher to publish to the /car_x/offboard/command topic for your racecar.

def control(data):
	global prev_error
	global vel_input	
	global kp
	global kd	
	global past_vel
	## TODO:
	# 1- arrivo in fase dello sterzo lenta
	# 2- sistemare pid velocita in base allo sterzo nuovo

	#scale error (non so se e quello che intendeva)
	error = data.pid_error
	if abs(error) < 0.005:
		error = 0.0

	#PD control per sterzo e velocita 		
	anglecorr = kp * error + kd * (prev_error - error)
	angle = prev_error - anglecorr	
	vel_input = past_vel +( 0.022 - 1.7 * math.pow( abs(prev_error - data.pid_error),2))
	prev_error = error                  
	
	#controllo sterzo
	if angle < -100:
		angle = -100
	elif angle > 100:
		angle = 100

	#controllo velocita
	if data.pid_vel != 0.0:
		if vel_input < 0.3:
			vel_input = 0.3
	else:
		vel_input = 0
	past_vel = vel_input

	#pubblish msg
	msg = AckermannDrive()
	msg.speed = vel_input	
	msg.steering_angle = angle
	pub.publish(msg)

if __name__ == '__main__':
	global kp
	global kd
	global vel_input
	print("Listening to error for PID")
	#kp = input("Enter Kp Value: ")
	#kd = input("Enter Kd Value: ")
	#vel_input = input("Enter Velocity: ")
	rospy.init_node('pid_controller', anonymous=True)
	rospy.Subscriber("/car_1/error", pid_input, control)
	rospy.spin()
