#!/usr/bin/env python

import sys, rospy, time


from std_msgs.msg import Float64
from geometry_msgs.msg import Twist


class Manipulation:
	def __init__(self):
		rospy.on_shutdown(self.clean_up)

		
		
		self.joint_tilt = rospy.Publisher('/tilt_controller/command', Float64, queue_size=10)
		self.joint_shoulder = rospy.Publisher('/shoulder_controller/command', Float64, queue_size=10)
		self.joint_elbow = rospy.Publisher('/elbow_controller/command', Float64, queue_size=10)
		self.joint_wrist = rospy.Publisher('/wrist_controller/command', Float64, queue_size=10)
		self.joint_hand = rospy.Publisher('/hand_controller/command', Float64, queue_size=10)
		rospy.sleep(2)
		self.pose = Float64()


	def move_tilt(self, pose):
		self.pose = pose
		self.joint_tilt.publish(self.pose)
		#rospy.sleep(3)


	def move_shoulder(self, pose):
		self.pose = pose
		self.joint_shoulder.publish(self.pose)
		#rospy.sleep(3)


	def move_elbow(self, pose):
		self.pose = pose
		self.joint_elbow.publish(self.pose)
		#rospy.sleep(3)


	def move_wrist(self, pose):
		self.pose = pose
		self.joint_wrist.publish(self.pose)
		#rospy.sleep(3)


	def move_hand(self, pose):
		self.pose = pose
		self.joint_hand.publish(self.pose)
		#rospy.sleep(3)
		

	def clean_up(self):
		rospy.loginfo('Shutting down robot arm.')


	def init_arm(self):
		self.move_tilt(4.203)
		self.move_shoulder(3.482)
		self.move_elbow(5.062)
		self.move_wrist(3.973)
		self.move_hand(2.756)
		rospy.sleep(5)

	def prepare_catch(self):
		self.move_tilt(4.172)
		self.move_shoulder(0.0)
		self.move_elbow(3.886)
		self.move_wrist(1.641)
		self.move_hand(1.917)
		rospy.sleep(5)

	# def catch(self):
	# 	self.move_tilt(4.228)
	# 	self.move_shoulder(0.490)
	# 	self.move_elbow(4.310)
	# 	self.move_wrist(1.948)
	# 	self.move_hand(3.017)
	# 	rospy.sleep(5)
	def catch(self):
		self.move_tilt(4.172)
		self.move_shoulder(0.0)
		self.move_elbow(3.886)
		self.move_wrist(1.641)
		self.move_hand(3.017)
		rospy.sleep(5)

	def pre_withdraw(self):
		self.move_tilt(4.213)
		self.move_shoulder(1.820)
		self.move_elbow(4.407)
		self.move_wrist(3.073)
		self.move_hand(3.068)
		rospy.sleep(5)

	def withdraw(self):
		self.move_tilt(4.274)
		self.move_shoulder(2.684)
		self.move_elbow(5.077)
		self.move_wrist(3.150)
		self.move_hand(3.073)
		rospy.sleep(5)

	def prepare_give(self):
		self.move_tilt(4.310)
		self.move_shoulder(1.600)
		self.move_elbow(4.535)
		self.move_wrist(2.782)
		self.move_hand(3.078)
		rospy.sleep(5)

	def give(self):
		self.move_tilt(4.310)
		self.move_shoulder(1.600)
		self.move_elbow(4.535)
		self.move_wrist(2.782)
		self.move_hand(1.917)
		rospy.sleep(5)


if __name__ == '__main__':
	rospy.init_node('photo', anonymous=False)
	manipulation = Manipulation()
	manipulation.init_arm()
	manipulation.prepare_catch()
	manipulation.catch()
	manipulation.pre_withdraw()
	manipulation.withdraw()
	manipulation.prepare_give()
	manipulation.give()
	manipulation.init_arm()
