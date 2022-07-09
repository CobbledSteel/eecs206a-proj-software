import airsim

import numpy as np
import os
import tempfile
import pprint
#import cv2

import control_drone

import sys

# read AirSim simulator IP from commandline
if len(sys.argv) > 1:
    airsim_ip = sys.argv[1]
    print("Will connect to {}".format(airsim_ip))
else:
    airsim_ip = ""

# connect to the AirSim simulator
client = airsim.MultirotorClient(ip=airsim_ip)
client.confirmConnection()
client.enableApiControl(True)

state = client.getMultirotorState()
print("state")
# print(state.kinematics_estimated.orientation)

print(client.simGetGroundTruthKinematics())

imu_data = client.getImuData()

barometer_data = client.getBarometerData()

magnetometer_data = client.getMagnetometerData()

gps_data = client.getGpsData()

print("Taking off...")
client.armDisarm(True)
client.takeoffAsync().join()

control = control_drone.IntermediateDroneApi()

control.launchStabilizer(client)

while True:
    pass
    #client.moveByVelocityAsync(-5, -5, 0, duration=1, drivetrain = airsim.DrivetrainType.ForwardOnly, yaw_mode=airsim.YawMode(False, 0)).join()

    #client.moveByVelocityAsync(-5, 5, 0, duration=1, drivetrain = airsim.DrivetrainType.ForwardOnly, yaw_mode=airsim.YawMode(False, 0)).join()
    #client.moveByRollPitchYawrateThrottleAsync(0,0.01,0,0.6,1) while True:
    rawImage = client.simGetImage("0", airsim.ImageType.Scene)
    byte_arr = airsim.string_to_uint8_array(rawImage).tobytes()
    print(type(byte_arr))
    print(byte_arr)
state = client.getMultirotorState()
