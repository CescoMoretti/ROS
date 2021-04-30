#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", len(data.ranges))
     
def listener():
 
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("scan", LaserScan, callback)
    
    rospy.spin()
 
if __name__ == '__main__':
    listener()
