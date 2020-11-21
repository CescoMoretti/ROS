#!/usr/bin/env python

import rospy				
import math
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import SetPen
from std_srvs.srv import Empty
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
                print "Teleport: Service call failed: %s" %e
        #implement set pen
        def set_pen(flag):
            rospy.wait_for_service('/turtle1/set_pen')
            try:
                set_pen = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
                set_pen(250,230,250,3,flag)
            except rospy.ServiceException,e:    
                print "Set pen color: Service call failed: %s" %e
        #implement change color of background
        def change_background(r,g,b):
            rospy.wait_for_service('/clear')
            try: 
                print "test"
                rospy.set_param('/turtlesim/background_r', r)
                rospy.set_param('/turtlesim/background_g', g)
                rospy.set_param('/turtlesim/background_b', b)                
                change_background_color = rospy.ServiceProxy('/clear', Empty)
                change_background_color()
                
            except rospy.ServiceException,e:
                print "Change background color: Service call failed : %s" %e


        #implement pose
        rospy.init_node('ControlTurtlesim', anonymous=False)             
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',Pose, self.update_pose)
        self.pose = Pose()
        #shutdown
        rospy.loginfo(" Press CTRL+c to stop moving the Turtle")       
        rospy.on_shutdown(self.shutdown)        
        #msg publisher
        self.cmd_vel = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=40)        
        move_cmd = Twist()
        #starting data 
        l = input("insert square lenght: ")        
        change_background(255,70,70)        
 
        # set frequency to 1/x second	   
        x = 20
        rate = rospy.Rate(x);        
        rospy.loginfo("Set rate %dHZ",x)
        #data utils
        cycleFlag = True
        lastFlag = False
        ndigits = 1
        

        set_pen(True)
        teleport_absolute_client(1,1,0)
        move_cmd.linear.x = 1.5
        move_cmd.linear.y = 0
        move_cmd.linear.z = 0        
        set_pen(False)
        #cycle	    
        while cycleFlag and not rospy.is_shutdown():
            #al posto del teleport si possono cambiare le velocità per fargli fare gli angoli,
            #ma mi piaceva di piu con la tartaruga che si gira, l'unica cosa è che facendo cosi 
            #sporca un po gli spigoli
            if round(self.pose.x,ndigits) == 1.0+l and round(self.pose.y,ndigits) ==1.0:                
                teleport_absolute_client(self.pose.x,self.pose.y,math.pi/2)

            if round(self.pose.x,ndigits) == 1.0+l and round(self.pose.y,ndigits) ==1.0+l:                
                teleport_absolute_client(self.pose.x,self.pose.y,math.pi)              
            
            if round(self.pose.x,ndigits) == 1.0 and round(self.pose.y,ndigits) ==1.0+l:                
                teleport_absolute_client(self.pose.x,self.pose.y,(math.pi/2)*3)
                lastFlag = True	        
            
            if round(self.pose.x,ndigits) == 1.0 and round(self.pose.y,ndigits) ==1.0 and lastFlag:                
                teleport_absolute_client(self.pose.x,self.pose.y,math.pi*2)
                cycleFlag = False
            
            self.cmd_vel.publish(move_cmd)
            rate.sleep()
        #change_background(69,86,255) #neded it make consecutive test, but it delete the previus square
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