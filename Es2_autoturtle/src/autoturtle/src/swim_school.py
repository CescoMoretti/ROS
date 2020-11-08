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
        def teleport_absolute_client(x, y, theta):
                rospy.wait_for_service('/turtle1/teleport_absolute')    
                try:
                    teleport_absolute = rospy.ServiceProxy('/turtle1/teleport_absolute',TeleportAbsolute)
                    teleport_absolute(x, y, theta)
                    print("teleported") 
                except rospy.ServiceException,e:    
                    print "Service call failed: %s" %e
        rospy.init_node('ControlTurtlesim', anonymous=False)             
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',Pose, self.update_pose)
        rospy.loginfo(" Press CTRL+c to stop moving the Turtle")       
        rospy.on_shutdown(self.shutdown)

        self.cmd_vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=100)       
        self.pose = Pose()
        move_cmd = Twist()     

        move_cmd.linear.x = 2.0
        move_cmd.angular.z = 1.5

        #  set 1/x second	   
        x = 100
        rate = rospy.Rate(x);        
        rospy.loginfo("Set rate %dHZ",x)

        ndigits = 2
        sx =5.5
        sy=5.5
        t = time.time()
        	    
        while not rospy.is_shutdown():
            rospy.loginfo(self.pose.x)
            rospy.loginfo(sy)
                       
            if round(self.pose.theta, ndigits) == round(0.0000, ndigits) and time.time()-t > 1:
                t = time.time()
                teleport_absolute_client(sx,sy,0)                 
                move_cmd.angular.z = -1 * move_cmd.angular.z
                            
	        
            self.cmd_vel.publish(move_cmd)	        
            rate.sleep()


    def shutdown(self):        
        rospy.loginfo("Stopping the turtle")
        self.cmd_vel.publish(Twist())        
        rospy.sleep(1)

if __name__ == '__main__':
    # Try and Except.
    # If an error is encountered, a try block code execution is stopped and
    # transferred down to the except block.

    try:
        ControlTurtlesim()
    except:
        rospy.loginfo("End of the swim for this Turtle.")