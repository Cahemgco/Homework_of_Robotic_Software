#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import sys, rospy,  time
import numpy as np
from std_msgs.msg import String
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
import time

class Pose:
    def __init__(self):
        pose_topic = '/amcl_pose'
        pose_sub = rospy.Subscriber(pose_topic, PoseWithCovarianceStamped, self.pose_callback)
        self.positoin = None
        self.orientation = None
    
    def pose_callback(self, msg):
        self.positoin = msg.pose.pose.position
        self.orientation = msg.pose.pose.orientation

    def get_position(self):
        return self.positoin.x, self.positoin.y, self.positoin.z
    
    def get_orientation(self):
        return self.orientation.x, self.orientation.y, self.orientation.z, self.orientation.w   
    

if __name__ == '__main__':
    rospy.init_node('get_pose', anonymous=False)
    pose = Pose()

    rospy.spin()