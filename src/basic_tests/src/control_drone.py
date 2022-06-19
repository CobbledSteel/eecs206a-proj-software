import airsim
import numpy as np
import os
import tempfile
import pprint
#import cv2
import sys
class IntermediateDroneApi: 
	
	def __init__(self):
		self.global_heading = 0

	# (yaw, timeout_sec=3e+38, margin=5, vehicle_name='')
	def rotateToYaw(self, client, theta):
		angle = client.simGetGroundTruthKinematics()
		
		yaw = airsim.to_eularian_angles(angle.orientation)[2] * 180/np.pi
		print("Yaw: {}\t Theta: {}".format(yaw,  yaw+theta))
		client.rotateToYawAsync(yaw + theta).join()
		# self.global_heading = self.global_heading + theta

	    #def moveByManualAsync(self, vx_max, vy_max, z_min, duration, drivetrain = DrivetrainType.MaxDegreeOfFreedom, yaw_mode = YawMode(), vehicle_name = ''):
		# def moveByVelocityAsync(self, vx, vy, vz, duration, drivetrain = DrivetrainType.MaxDegreeOfFreedom, yaw_mode = YawMode(), vehicle_name = ''):
	def moveInAngle(self, client, theta, speed, time):

		kin = client.simGetGroundTruthKinematics()
		
		height = kin.position.z_val
		print("height: {}".format(height))
		yaw = airsim.to_eularian_angles(kin.orientation)[2] * 180/np.pi
		heading = yaw + theta
		print("Heading: {}".format(heading))
		vx = np.cos(heading*np.pi/180) * speed
		vy = np.sin(heading*np.pi/180) * speed
		vz = -0.5 - height

		# client.rotateToYawAsync(yaw + theta).join()

		client.moveByVelocityAsync(vx, vy, vz, time, drivetrain = airsim.DrivetrainType.ForwardOnly, yaw_mode=airsim.YawMode(False, 0)).join()
