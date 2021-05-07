#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
def callback(data):
    size = len(data.ranges)
    rospy.loginfo("lidar: %s - %s -%s",data.ranges[0],  data.ranges[int(size/2)], data.ranges[size-1]  )
     
def listener():
 
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("scan", LaserScan, callback)
    
    rospy.spin()
 
if __name__ == '__main__':
    listener()
