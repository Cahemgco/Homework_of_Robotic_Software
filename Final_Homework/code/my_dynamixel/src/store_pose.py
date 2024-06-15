#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import sys, rospy,  time
import numpy as np
from std_msgs.msg import String
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
import time
from get_pose import Pose
import json
import os


class Store:
    def __init__(self) -> None:
        hear_topic = '/voiceWords'
        hear_sub = rospy.Subscriber(hear_topic, String, self.hear_callback)
        self.msg = '11'
        self.pose = Pose()

    def hear_callback(self, msg):
        self.msg = msg.data

    def store_positoin(self):
        x = self.pose.get_position.x
        y = self.pose.get_position.y
        z = self.pose.get_position.z

    def store_pose(self):
        # print(self.pose.get_orientation)
        position_x, position_y, position_z = self.pose.get_position()
        orien_x, orien_y, orien_z, orien_w = self.pose.get_orientation()

        data = [{'position_x': position_x, 'position_y': position_y, 'position_z': position_z, 'orien_x': orien_x, 'orien_y': orien_y, 'orien_z': orien_z, 'orien_w': orien_w}]

        txt_file_path = '/home/cy/catkin_ws/src/my_dynamixel/src/Pose.txt'

        file_exists = os.path.isfile(txt_file_path)

        # 如果文件不存在，则创建并写入初始数据
        # if not file_exists:
        with open(txt_file_path, 'a') as txtfile:
            for row in data:
                print('writing')
                txtfile.write(json.dumps(row) + '\n')

    def store_color(self, data):
        # print(self.pose.get_orientation)
        color = data

        txt_file_path = '/home/cy/catkin_ws/src/my_dynamixel/src/color.txt'

        file_exists = os.path.isfile(txt_file_path)

        # 如果文件不存在，则创建并写入初始数据
        # if not file_exists:
        with open(txt_file_path, 'a') as txtfile:
            for row in data:
                print('writing')
                txtfile.write(json.dumps(row) + '\n')


    def get_data(self):
        return self.msg
    
    def set_data(self, data):
        self.msg = data


if __name__ == '__main__':
    rospy.init_node('store_data', anonymous=False)

    store = Store()

    while True:
        data = store.get_data()
        # print(data)

        if('Remember' in data or 'remember' in data):
            print("-------store pose---------")
            store.store_pose()
            store.set_data('11')

        if("Stop" in data):
            print("---------Exit------------")
            break

        if("Red" in data):
            print("---------Pick Red Cup----------")
            store.store_color("red")
        

rospy.spin()
