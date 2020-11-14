#!/usr/bin/env python

import rospy				
import math
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute
import time



class ControlTurtlesim():
    def update_pose(self, data):        
        self.pose = data  
    def __init__(self):      

        #implement teleport
        def teleport_absolute_client(x, y, theta):
                rospy.wait_for_service('/turtle1/teleport_absolute')    
                try:
                    teleport_absolute = rospy.ServiceProxy('/turtle1/teleport_absolute',TeleportAbsolute)
                    teleport_absolute(x, y, theta)                    
                except rospy.ServiceException,e:    
                    print "Service call failed: %s" %e

        #implement pose
        rospy.init_node('ControlTurtlesim', anonymous=False)             
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',Pose, self.update_pose)
        self.pose = Pose()
        #shutdown
        rospy.loginfo(" Press CTRL+c to stop moving the Turtle")       
        rospy.on_shutdown(self.shutdown)
        
        #msg publisher
        self.cmd_vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=100)        
        move_cmd = Twist()

        #starting data  
        print("Insert data\n")
        move_cmd.linear.x = input("linear velocity:")
        move_cmd.angular.z = input("angular velocity:")

        # set frequency to 1/x second	   
        x = 100
        rate = rospy.Rate(x);        
        rospy.loginfo("Set rate %dHZ",x)

        #data utils
        ndigits = 1
        sx =5.5
        sy=5.5
        t = time.time()
        #cycle	    
        while not rospy.is_shutdown():
            if round(self.pose.theta, ndigits) == round(0.0000, ndigits) and time.time()-t > 1:
                t = time.time()
                teleport_absolute_client(sx,sy,0)                 
                move_cmd.angular.z = -1 * move_cmd.angular.z        
            self.cmd_vel.publish(move_cmd)	        
            rate.sleep()
    #shutdown function
    def shutdown(self):        
        rospy.loginfo("Stopping the turtle")
        self.cmd_vel.publish(Twist())        
        rospy.sleep(1)
#launch for node
if __name__ == '__main__':
    try:
        ControlTurtlesim()
    except:
        rospy.loginfo("End of the swim for this Turtle.")