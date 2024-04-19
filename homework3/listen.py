#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64, String

def float_callback(data):
    rospy.loginfo("Received Float: %.2f", data.data)

def string_callback(data):
    rospy.loginfo("Received String: %s", data.data)

def subscriber():
    rospy.init_node('subscriber_node', anonymous=True)

    rospy.Subscriber("float_topic", Float64, float_callback)
    rospy.Subscriber("string_topic", String, string_callback)

    rospy.spin()

if __name__ == '__main__':
    subscriber()

