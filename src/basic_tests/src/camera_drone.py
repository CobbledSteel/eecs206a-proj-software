import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2

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
    rawImage = client.simGetImage("0", airsim.ImageType.Scene)
    if (rawImage == None):
        print("Camera is not returning image, please check airsim for error messages")
        sys.exit(0)
    else:
        png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
        cv2.imshow("Depth", png)
        if cv2.waitKey(1) == 27:
          break

    client.moveToPositionAsync(-10, 10, -10, 5).join()
    client.hoverAsync().join()

    client.moveToPositionAsync(-10, -10, -10, 5).join()
    client.hoverAsync().join()

    client.moveToPositionAsync(10, -10, -10, 5).join()
    client.hoverAsync().join()

    client.moveToPositionAsync(10, 10, -10, 5).join()
    client.hoverAsync().join()

state = client.getMultirotorState()
