#!/usr/bin/env python

import rospy
from race.msg import pid_input
from ackermann_msgs.msg import AckermannDrive

kp = 0.7
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
	## Funziona, ma ha qualche problema da sistemare:
	# 1- lo sterzo ci mette una marea di tempo ad andare in fase, ma se si cambiano troppo
	#    le costanti del PD la macchina si schianta o inverte il giro nella curva stretta
	# 2- il PD della velocità è un po improvvistato e fa un po schifo

	#scale error (non so se è quello che intendeva)
	error = data.pid_error
	if abs(error) < 0.05:
		error = 0

	#PD control per sterzo e velocità 		
	anglecorr = kp * error + kd * (prev_error - error)
	angle = prev_error - anglecorr
	prev_error = error
	vel_input = past_vel +( +0.32 - 1.45*abs(angle) -  1.4 *abs(prev_error - data.pid_error))
	#                   acc. base  frena prima delle curve   non accelera durante una curva
	
	#controllo sterzo
	if angle < -100:
		angle = -100
	elif angle > 100:
		angle = 100

	#controllo velocita
	if data.pid_vel != 0.0:
		if vel_input < 0.4:
			vel_input = 0.4
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
