#!/usr/bin/env python

import rospy
from race.msg import pid_input
from ackermann_msgs.msg import AckermannDrive

pub = rospy.Publisher('/car_1/offboard/command', AckermannDrive, queue_size=10)
count = 0

def control(data):
    
    global count
    count += 1
    if count > 100:
        vel_input = 0.0
        angle = 0.0
        print "stop"
    else: 
        vel_input = 0.0
        angle = 0.0

    msg = AckermannDrive()
    msg.speed = vel_input	
    msg.steering_angle = angle
    pub.publish(msg)

if __name__ == '__main__':
	global kp
	global kd
	global vel_input
	print("Listening to error for PID")
	
	#vel_input = input("Enter Velocity: ")
	rospy.init_node('pid_controller', anonymous=True)
	rospy.Subscriber("/car_1/error", pid_input, control)
	rospy.spin()