#!/usr/bin/env python

import rospy				
from math import pow, atan2, sqrt
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist




class ControlTurtlesim():
    def update_pose(self, data):        
        self.pose = data  
    def eucl_dist(self, goal):           
        return sqrt(pow((goal.x - self.pose.x), 2)+pow((goal.y - self.pose.y), 2))
    def angle(self ,goal):
        return atan2(goal.y - round(self.pose.y,2), goal.x - round(self.pose.x,2))

    def __init__(self):              

        
        #implement pose
        rospy.init_node('ControlTurtlesim', anonymous=False)             
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',Pose, self.update_pose)
        self.pose = Pose()
        #shutdown
        rospy.loginfo(" Press CTRL+c to stop moving the Turtle")       
        rospy.on_shutdown(self.shutdown)        
        #msg publisher
        self.cmd_vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)        
        move_cmd = Twist()
        #starting data
        print("insert the coordinates")
        goal = Pose()
        goal.x = input("x: ")        
        goal.y = input("y: ") 
        tollerance = input("set the tollerance: ")       
        
        # set frequency to 1/x second	   
        x = 10
        rate = rospy.Rate(x);        
        rospy.loginfo("Set rate %dHZ",x)
        #data utils
        costL = 1.5
        costA = 4.0
              
        #cycle	    
        while not rospy.is_shutdown() and self.eucl_dist(goal) >= tollerance: 
            rospy.loginfo(self.pose.x)  
            rospy.loginfo(self.pose.y) 
            rospy.loginfo("%f\n",move_cmd.angular.z)         

            move_cmd.linear.x = costL * self.eucl_dist(goal)
            move_cmd.linear.y = 0
            move_cmd.linear.z = 0
            move_cmd.angular.z = costA * (self.angle(goal)-self.pose.theta)  
            move_cmd.angular.x = 0
            move_cmd.angular.y = 0                

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