import airsim
import time
import numpy as np
import os
import tempfile
import pprint
import cv2

import sys

# read AirSim simulator IP from commandline
# sys.argv[0]: command 
# sys.argv[1]: simulator IP 

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

print("pausing simulator...")
client.simPause(True)

for i in range(20):
	# Step one forward
	time.sleep(1)
        # input("waiting on user input")
	client.simContinueForFrames(1)
	print("one step forward")
	print("Location Data {}: {}".format(i, client.getImuData()))

   
state = client.getMultirotorState()
