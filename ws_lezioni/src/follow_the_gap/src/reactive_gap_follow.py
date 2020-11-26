#!/usr/bin/env python
from __future__ import print_function
import sys
import math
import numpy as np

#ROS Imports
import rospy
from sensor_msgs.msg import Image, LaserScan
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive

past_angle = 0.0
class reactive_follow_gap:

     
    
    
    
    def __init__(self):
        #Topics & Subscriptions,Publishers
        lidarscan_topic = '/scan'
        drive_topic = '/nav'

        self.lidar_sub = rospy.Subscriber("/car_1/scan",LaserScan,self.lidar_callback)
        self.drive_pub = rospy.Publisher('/car_1/offboard/command', AckermannDrive, queue_size=10)
    
    def preprocess_lidar(self, ranges):
        """ Preprocess the LiDAR scan array. Expert implementation includes:
            1.Setting each value to the mean over some window
            2.Rejecting high values (eg. > 3m)
        """
        n = 6
       
        for i in range(len(ranges)):
            '''TODO
            # elimina traiettoria vicino a ostacoli lontani
            if abs(ranges[i]-ranges[i-1])> 4.0 and i != 0:
                ranges[i-1] = 0.1
            '''
            #media
            if i > n and i < len(ranges)-n and ranges[i] != 0.0:
                tot=0
                for k in range(i-n,i+n):                    
                    tot += ranges[k]
                ranges[i] =  tot /( (2 * n) +1)
            
                    
           

                    
        proc_ranges = ranges
        return proc_ranges

    def find_max_gap(self, start, end, l):
        """ Return the start index & end index of the max gap in free_space_ranges
        """
        if start <= l-end:
            return end,l
        else:
            return 0,start         
    
    def find_best_point(self, start_i, end_i, ranges):
        """Start_i & end_i are start and end indicies of max-gap range, respectively
        Return index of best point in ranges
	    Naive: Choose the furthest point within ranges and go there
        """
        max_value = 0        
        max_ind = 0
       
        for i in range(start_i, end_i):
            if ranges[i] > max_value and i > 180 and i < 900:
                max_value = ranges[i]
                max_ind = i
            
      


        return max_ind

    def lidar_callback(self, data):
        """ Process each LiDAR scan as per the Follow Gap algorithm & publish an
         AckermannDriveStamped Message
        """
        global past_angle
        
        ranges = list(data.ranges)
        proc_ranges = self.preprocess_lidar(ranges)
        ranges = proc_ranges
        #Find closest point to LiDAR
        min_ind =  0
        
        for i in range(len(ranges)):
            if ranges[min_ind] > ranges[i]:
                min_ind = i 
                

        #Eliminate all points inside 'bubble' (set them to zero) 
        alpha = math.atan2(0.8,ranges[min_ind])
        alpha = math.degrees(alpha)
        x = math.ceil(alpha/0.25)
        starti = int(min_ind -x)
        l = len(ranges)
        #clamp per gli indici
        if starti < 0: starti=0
        endi= int(min_ind +x)
        if endi > l: endi = l

        for i in range(starti,endi):
            ranges[i] = 0.0
        #Find max length gap
        s,e = self.find_max_gap(starti,endi, l)
       
        #Find the best point in the gap 
        direction = self.find_best_point(s,e,ranges)               
        angle = (float(direction) * 0.25) -135
         
        #pid angle        
        steer = angle * 0.02 # + (angle - past_angle) * 0.1
        past_angle = steer 
        #clamp per lo steer
        if steer > 100: 
            steer = 100
        elif steer < -100:
            steer = -100
        
        #print(ranges) 
        print(min_ind)
       
        

        vel = ranges[540] / 10.0
        #clamp velocita
        if vel < 0.3: vel = 0.3
        if vel > 0.8: vel = 0.8
        #Publish Drive message
       
        msg = AckermannDrive()
        msg.speed = vel
        msg.steering_angle = steer
        self.drive_pub.publish(msg)  
	    

    

def main(args):
    rospy.init_node("FollowGap_node", anonymous=True)
    rfgs = reactive_follow_gap()
    rospy.sleep(0.1)
    rospy.spin()

if __name__ == '__main__':
    main(sys.argv)
