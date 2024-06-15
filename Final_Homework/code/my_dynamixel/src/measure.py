#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import rospy,sys,cv2,time
import math
from std_msgs.msg import String
from std_msgs.msg import Float64
from dynamixel_msgs.msg import JointState
tilt=0
shoulder=0
elbow=0
wrist=0
wrist_turn=0
hand=0

def get_tilt(data):
	global tilt
	#print(data)
	tilt = data

def get_shoulder(data):
	global shoulder
	shoulder = data

def get_elbow(data):
	global elbow
	elbow = data

def get_wrist(data):
	global wrist
	wrist = data

def get_wrist_turn(data):
	global wrist_turn
	wrist_turn = data

def get_hand(data):
	global hand
	hand = data
def listen():
	rospy.Subscriber('/tilt_controller/state',JointState,get_tilt)
	rospy.Subscriber('/shoulder_controller/state',JointState,get_shoulder)
	rospy.Subscriber('/elbow_controller/state',JointState,get_elbow)
	rospy.Subscriber('/wrist_controller/state',JointState,get_wrist)
	rospy.Subscriber('/wrist_turn_controller/state',JointState,get_wrist_turn)
	rospy.Subscriber('/hand_controller/state',JointState,get_hand)
	
if __name__ =='__main__':
	rospy.init_node('motor_show',anonymous=True)
	#global tilt
	#global shoulder
	#global elbow
	#global wrist
	#global wrist_turn
	#global hand
	listen()
	for i in range (5):
		print(tilt)
		print(shoulder)
		print(elbow)
		print(wrist)
		print(wrist_turn)
		print(hand)
		print("--------------------------------")
		rospy.sleep(1)

