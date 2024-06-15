#!/usr/bin/env python

import actionlib       # Use the actionlib package for client and server
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import json

import sys, rospy, cv2, time
import numpy as np
from std_msgs.msg import String
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from darknet_ros_msgs.msg import BoundingBox
from darknet_ros_msgs.msg import BoundingBoxes

# from lsr import listener
from control_arm import Manipulation

# 文件路径
file_path_pose = '/home/cy/catkin_ws/src/my_dynamixel/src/pose.txt'
# 初始化GoalPoints变量
GoalPoints = []

# 读取文件并解析每行JSON数据
with open(file_path_pose, 'r') as file:
    for line in file:
        # 解析JSON数据
        data = json.loads(line.strip())
        
        # 提取position和orientation数据
        position = (data['position_x'], data['position_y'], data['position_z'])
        orientation = (data['orien_x'], data['orien_y'], data['orien_z'], data['orien_w'])
        
        # 将提取的数据添加到GoalPoints列表中
        GoalPoints.append([position, orientation])

class RGBD_myImage:
    def __init__(self, label):
        # self.image_handle = RGBD_Image()
        image_topic = '/camera1/rgb/image_raw'
        depth_topic = '/camera1/depth_registered/image_raw'
        dete_topic = '/darknet_ros/bounding_boxes'

        # self.xmin = {'red': 0.0, 'green': 0.0}
        # self.ymin = {'red': 0.0, 'green': 0.0}
        # self.w = {'red': 0.0, 'green': 0.0}
        # self.h = {'red': 0.0, 'green': 0.0}

        self.xmin = 0.0
        self.ymin = 0.0
        self.w = 0.0
        self.h = 0.0
        self.label = label
        #self.depth_image = None

        image_sub = rospy.Subscriber(image_topic, Image, self.image_call_back)
        depth_sub = rospy.Subscriber(depth_topic, Image, self.depth_call_back)
        dete_sub = rospy.Subscriber(dete_topic, BoundingBoxes, self.dete_call_back)
        # rospy.spin()

        # print('RGBD_Image Init.')
        rospy.sleep(3)

    def image_call_back(self, data):
        # print("rgb call back")
        try:
            bridge = CvBridge()
            self.rgb_image = bridge.imgmsg_to_cv2(data, 'bgr8')
        except:
            pass

        # rospy.spin()

    def depth_call_back(self, data):
        # print("depth call back")
        try:
            bridge = CvBridge()
            self.depth_image = bridge.imgmsg_to_cv2(data, '32FC1')
        except:
            pass

        # rospy.spin()

    def dete_call_back(self, msg):
        rate = rospy.Rate(100)
        # print("dete call back")
        try:
            dep = self.get_depth_image()
            self.xmin = 100000

            for item in msg.bounding_boxes:
                x_center = (item.xmin+item.xmax)/2
                y_center = (item.ymin + item.ymax) / 2

                self.xmin = item.xmin
                self.ymin = item.ymin
                self.w = item.xmax - item.xmin
                self.h = item.ymax - item.ymin

                region = dep[self.ymin:self.ymin+self.h, self.xmin:self.xmin+self.w]

                valid_values = region[~np.isnan(region)]

                if valid_values.size > 0:
                    # mean_value = np.mean(valid_values)
                    mean_value = np.min(valid_values)
                else:
                    mean_value = np.nan 

                d_center = mean_value

                # print(x_center, y_center, d_center)

                # if item.Class in [self.label] and (y_center<=350 and y_center>=100) and d_center<=2500 and item.xmin<self.xmin:
                #     self.xmin = item.xmin
                #     self.ymin = item.ymin
                #     self.w = item.xmax - item.xmin
                #     self.h = item.ymax - item.ymin
                #     continue

            # print(self.xmin, self.ymin)
        except:
            pass
        rate.sleep()

        # rospy.spin()

    def get_image(self):
        return self.rgb_image

    def get_depth_image(self):
        return self.depth_image

    def get_dete_information(self):
         return self.xmin, self.ymin, self.w, self.h

    def get_label(self):
        return self.label

class bottle_Detection:
    def __init__(self, label):
        self.label = label
        self.image_handle = RGBD_myImage(self.label)
        # self.msg = 1
        # self.msg = 0
        # hear_topic = '/color'
        # hear_sub = rospy.Subscriber(hear_topic, Float64, self.hear_callback)

        # print(hear_sub)

    def get_position(self):
        dep = self.image_handle.get_depth_image()

        x_min, y_min, width, height = self.image_handle.get_dete_information()
        # print(x_min, y_min, width, height)
        x_min, y_min, width, height = int(x_min), int(y_min), int(width), int(height) 
        # print(x_min, y_min, width, height)
        
        region = dep[int(y_min+height/3):int(y_min+2*height/3), int(x_min+width/3):int(x_min+2*width/3)]

        valid_values = region[~np.isnan(region)]

        if valid_values.size > 0:
            mean_value = np.mean(valid_values)
        else:
            mean_value = np.nan 

        d_center = mean_value

        #print(x_min, y_min)

        x = int(x_min + width / 2)
        y = int(y_min + height / 2)

        return x, y, d_center

    def get_color(self, x, y):
        rgbimage = self.image_handle.get_image()
        b, g, r = rgbimage[y, x]
        return b, g, r

    def x_registration(self, goal_x=305):
        # detection = cup_Detection()
        print('--------------enter registration-------------')
        cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        move_cmd = Twist()

        while True:
            x, y, z = self.get_position()
            print(x, y, z)

            bound = 3
            if x < goal_x - bound:
                move_cmd.linear.x = 0
                move_cmd.angular.z = 0.3
                lateral_error = 1
            elif x > goal_x + bound:
                move_cmd.linear.x = 0
                move_cmd.angular.z = -0.3
                lateral_error = 1
            else:
                move_cmd.linear.x = 0.0
                move_cmd.angular.z = 0.0
                lateral_error = 0

            cmd_vel.publish(move_cmd)
            rospy.sleep(0.1)

            if lateral_error == 0:
                print("--------------x is ok----------------")
                return z

def move_forward(z):
    print("distance: ", z)
    print('move_forward')
    rate = 10
    r = rospy.Rate(rate)
    distance = z

    rate = rospy.Rate(10)
    move_cmd.linear.x = 0.1

    duration = distance / move_cmd.linear.x
    # print(duration)
    start_time = rospy.Time.now().to_sec()
    while rospy.Time.now().to_sec() - start_time < duration:
        cmd_vel.publish(move_cmd)
        rate.sleep()

def move_backward(z):
    print("move backward")
    rate = 10
    r = rospy.Rate(rate)
    distance = z

    rate = rospy.Rate(10)
    move_cmd.linear.x = -0.1

    duration = distance / (-move_cmd.linear.x)
    # print(duration)
    start_time = rospy.Time.now().to_sec()
    while rospy.Time.now().to_sec() - start_time < duration:
        cmd_vel.publish(move_cmd)
        rate.sleep()

def assign_goal(pose):  

    goal_pose = MoveBaseGoal()        
    goal_pose.target_pose.header.frame_id = 'map'
    goal_pose.target_pose.pose.position.x = pose[0][0]
    goal_pose.target_pose.pose.position.y = pose[0][1]
    goal_pose.target_pose.pose.position.z = pose[0][2]
    goal_pose.target_pose.pose.orientation.x = pose[1][0]
    goal_pose.target_pose.pose.orientation.y = pose[1][1]
    goal_pose.target_pose.pose.orientation.z = pose[1][2]
    goal_pose.target_pose.pose.orientation.w = pose[1][3]

    return goal_pose


if __name__ == '__main__':
    rospy.init_node('registration', anonymous=False)
    # # -----------导航-----------
    # print("---------To Goal----------")
    # print(GoalPoints)
    # client = actionlib.SimpleActionClient('move_base', MoveBaseAction)  
    # client.wait_for_server()
    # # rospy.sleep(10)
    # print("------Navigation------")
     
    # for TBpose in GoalPoints:  
    #     TBgoal = assign_goal(TBpose)   # For each goal point assign pose
    #     client.send_goal(TBgoal)
    #     client.wait_for_result()
    
    # if(client.get_state() == actionlib.GoalStatus.SUCCEEDED):
    #     rospy.loginfo("success")
    # else:
    #     rospy.loginfo("failed")


    # -----------PID-----------
    # 文件路径
    file_path_color = '/home/cy/catkin_ws/src/my_dynamixel/src/color.txt'

    # 读取文件并解析每行JSON数据
    with open(file_path_color, 'r') as file:
        label = file.read()

    print("label:",label)
    print("------PID------")

    detection = bottle_Detection(label=label)
    manipulation = Manipulation()

    # while True:
    #     x, y, z = detection.get_position()

    #     print(x, y, z)
    #     c = cv2.waitKey(1)
    #     if c == 27:
    #         break
    #     rospy.sleep(1)

    cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
    move_cmd = Twist()

    voice = rospy.Publisher('/voiceWords', String, queue_size=10)

    move_forward(0.2)

    z = detection.x_registration()

    if z<0.65:
        pass
    else:
        z = 0.5
    
    manipulation.init_arm()
    manipulation.prepare_catch()
    move_forward(z)
    rospy.sleep(3)
    # z = detection.x_registration()
    # move_forward(z-20)
    
    manipulation.catch()
    manipulation.pre_withdraw()
    # manipulation.withdraw()
    rate = rospy.Rate(10)

    voice.publish("Grasp")
    rate.sleep()
    voice.publish("Grasp")
    rate.sleep()
    voice.publish("Grasp")
    rate.sleep()
    # voice.publish("Grasp")
    # rate.sleep()

    # rospy.sleep(5)

    move_backward(z)

    # # -----------返回---------------
    # GoalPoints.reverse()
    # # 输出GoalPoints
    # print(GoalPoints)

    # for TBpose in GoalPoints:  
    #     TBgoal = assign_goal(TBpose)   # For each goal point assign pose
    #     client.send_goal(TBgoal)
        
    #     client.wait_for_result()
    
    # if(client.get_state() == actionlib.GoalStatus.SUCCEEDED):
    #     rospy.loginfo("success")
    # else:
    #     rospy.loginfo("failed")

    manipulation.prepare_give()
    manipulation.give()
    manipulation.init_arm()

    # voice.publish("Navigation")
    # rate.sleep()
    # voice.publish("Navigation")
    # rate.sleep()
    # voice.publish("Navigation")
    # rate.sleep()
    # voice.publish("Navigation")
    # rate.sleep()
