import airsim

import numpy as np
import os
import tempfile
import pprint
#import cv2

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

imu_data = client.getImuData()

barometer_data = client.getBarometerData()

magnetometer_data = client.getMagnetometerData()

gps_data = client.getGpsData()

print("Taking off...")
client.armDisarm(True)
client.takeoffAsync().join()

while True:
    client.moveToPositionAsync(-10, 10, -10, 5).join()
    client.hoverAsync().join()

    client.moveToPositionAsync(-10, -10, -10, 5).join()
    client.hoverAsync().join()

    client.moveToPositionAsync(10, -10, -10, 5).join()
    client.hoverAsync().join()

    client.moveToPositionAsync(10, 10, -10, 5).join()
    client.hoverAsync().join()

state = client.getMultirotorState()
