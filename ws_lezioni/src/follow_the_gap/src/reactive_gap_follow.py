#!/usr/bin/env python
from __future__ import print_function
import sys
import math
import numpy as np

#ROS Imports
import rospy
from sensor_msgs.msg import Image, LaserScan
from geometry_msgs.msg import Point32

past_angle = 0.0
class reactive_follow_gap:   
    
    def __init__(self):
        #Subscriptions,Publishers
        self.lidar_sub = rospy.Subscriber("/scan",LaserScan,self.lidar_callback)
        self.drive_pub = rospy.Publisher('drive_parameters', Point32, queue_size=10)
    
    def preprocess_lidar(self, ranges):
        '''filter the data of the lidar to have a better "base" to work with     
        '''
        n = 6       
        for i in range(len(ranges)):
            '''
            TODO
            # elimina traiettoria vicino a ostacoli lontani
            if abs(ranges[i]-ranges[i-1])> 4.0 and i != 0:
                ranges[i-1] = 0.1
            '''
            #average with the n near value to have a better set of data
            if i > n and i < len(ranges)-n and ranges[i] != 0.0:
                tot=0
                for k in range(i-n,i+n):                    
                    tot += ranges[k]
                ranges[i] =  tot /( (2 * n) +1)
             
        proc_ranges = ranges
        return proc_ranges

    def find_max_gap(self, start, end, l):
        """ Return the start index & end index of the max gap
            (find if the biggest gap is at the left or right of the obstacle)
        """
        if start <= l-end:
            return end,l
        else:
            return 0,start         
    
    def find_best_point(self, start_i, end_i, ranges):
        """Start_i & end_i are start and end indicies of max-gap range, respectively
        Return index of best point in ranges (furthest point)
        """
        max_value = 0        
        max_ind = 0
       
        for i in range(start_i, end_i):
            if ranges[i] > max_value and i > 180 and i < 900:
                max_value = ranges[i]
                max_ind = i

        return max_ind

    def lidar_callback(self, data):        
        global past_angle
        
        ranges = list(data.ranges)
        proc_ranges = self.preprocess_lidar(ranges)
        ranges = proc_ranges
        #Find closest point to LiDAR
        min_ind =  0
        for i in range(len(ranges)):
            if ranges[min_ind] > ranges[i]:
                min_ind = i 
                

        #Eliminate all points inside 'bubble' of the nearest object 
        alpha = math.atan2(0.8,ranges[min_ind]) #lidar ray at the end of the bubble
        alpha = math.degrees(alpha)
        x = math.ceil(alpha/0.25)
        starti = int(min_ind -x)
        l = len(ranges)

        #clamp fot the indexes of the list
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
        steer = -angle * 0.0075

        #clamp per lo steer
        if steer > 0.45: 
            steer = 0.45
        elif steer < -0.45:
            steer = -0.45

        #velocity   
        if data.ranges[direction] > 1.5:
            vel = 15000.0
        elif data.ranges[direction] > 0.5:
            vel = 0.0
        else:
            vel = 8000.0
      
        #Publish Drive message
        msg = Point32()
        msg.x = vel	
        msg.y = steer  
        self.drive_pub.publish(msg)  

def main(args):
    rospy.init_node("FollowGap_node", anonymous=True)
    rfgs = reactive_follow_gap()
    rospy.sleep(0.1)
    rospy.spin()

if __name__ == '__main__':
    main(sys.argv)
