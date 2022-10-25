import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2
import time

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

pose = client.simGetVehiclePose()
pose.position.y_val = 0
# client.simSetVehiclePose(pose, ignore_collision=True)
# print("Taking off...")
# client.armDisarm(True)
# client.takeoffAsync().join()
# client.moveToPositionAsync(0, 0, 0, 5).join()
# client.rotateToYawAsync(160).join()
time.sleep(1)

def get_data(client, label, lateral, yaw, height=0):
    client.moveToPositionAsync(0, lateral, -10, 5).join()
    client.moveToPositionAsync(0, lateral, height, 5).join()
    client.rotateToYawAsync(yaw)
    time.sleep(4)
    client.moveToPositionAsync(-55, lateral, height, 0.5)
    for i in range(1000):
        rawImage = client.simGetImage("0", airsim.ImageType.Scene)
        png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_COLOR)
        cv2.imwrite('data/{}/img_lat_{}_yaw_{}_height_{}_{:05}.png'.format(label, lateral, yaw, height, i), png)
        print('wrote data/{}/img_lat_{}_yaw_{}_height_{}_{:05}.png'.format(label, lateral, yaw, height, i))
    print("Done getting pics")
    client.hoverAsync().join()

def get_samples(client, i):
    angle_var = 0.4
    pose_var = 0.5
    pose = client.simGetVehiclePose()
    for pos in [("sc", 0.25, 0), ("lc", 1.5, -0.6), ("rc", -1, 0.6)]:
        sc_mod = 1
        if pos[0] == "sc":
            sc_mod = 0.3
        pose.position.y_val = pos[1] + np.random.normal(0, pose_var*sc_mod)
        pose.position.x_val = -20 + np.random.normal(0, 10*pose_var)
        pose.position.z_val = np.random.normal(0, pose_var)
        pose.orientation = airsim.utils.to_quaternion(np.random.normal(0,angle_var*sc_mod),np.random.normal(0,angle_var*sc_mod),np.random.normal(0,angle_var*sc_mod)+np.pi+pos[2])
        collision = client.simSetVehiclePose(pose, ignore_collision=False)
        client.simContinueForFrames(1)
        pose = client.simGetVehiclePose()
        # print(f"pose: {pose}, euler: {airsim.utils.to_eularian_angles(pose.orientation)}")
        rawImage = client.simGetImage("0", airsim.ImageType.Scene)
        png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_COLOR)
        cv2.imwrite('data/train/{}/{:04}_img.png'.format(pos[0], i), png)

def get_multihead_samples(client, dir, i):
    angle_var = 0.3
    pose_var = 0.5
    pose = client.simGetVehiclePose()

    for pos in [("lateral/sc", 0.15, 0), ("lateral/lc", 1.2, 0), ("lateral/rc", -1, 0), ("angular/sc", 0.25, 0), ("angular/lc", 0.25, -0.7), ("angular/rc", 0.25, 0.7)]:
        sc_mod = 1
        if "sc" in pos[0]:
            sc_mod = 0.3
        lat_mod = 1
        if "angular" in pos[0]:
            lat_mod = 2
        pose.position.y_val = pos[1] + np.random.normal(0, pose_var*sc_mod*lat_mod) 
        pose.position.x_val = -20 + np.random.normal(0, 10*pose_var)
        pose.position.z_val = np.random.normal(0, pose_var)
        pose.orientation = airsim.utils.to_quaternion(np.random.normal(0,angle_var*sc_mod),np.random.normal(0,angle_var*sc_mod),np.random.normal(0,angle_var*sc_mod)+np.pi+pos[2])
        collision = client.simSetVehiclePose(pose, ignore_collision=False)
        client.simContinueForFrames(1)
        pose = client.simGetVehiclePose()
        # print(f"pose: {pose}, euler: {airsim.utils.to_eularian_angles(pose.orientation)}")
        rawImage = client.simGetImage("0", airsim.ImageType.Scene)
        png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_COLOR)
        cv2.imwrite('{}/{}/{:04}_img.png'.format(dir, pos[0], i), png)



for k in range(1):
    client.simPause(True)
    pose = client.simGetVehiclePose()
    pose.position.x_val = -10
    pose.position.y_val = 0
    pose.position.z_val = 0
    client.simSetVehiclePose(pose, ignore_collision=True)
    client.simContinueForFrames(1)
    for i in range(2000):
        print(f"writing train {i}")
        get_multihead_samples(client, "multihead_data/train", i)
    for i in range(200):
        print(f"writing test {i}")
        get_multihead_samples(client, "multihead_data/test", i)
    # get_data(client, "sc", 0, 180)
    # get_data(client, "sc", 0, 180, height=-0.1)
    # get_data(client, "sc", 0, 180, height=-0.2)
    # get_data(client, "sc", 0, 180, height=-0.3)
    # get_data(client, "lc", 1, 160)
    # get_data(client, "lc", 1, 180)
    # get_data(client, "lc", 0, 160)
    # get_data(client, "lc", 0, 120)
    # get_data(client, "rc", -1, 200)
    # get_data(client, "rc", -1, 180)
    # get_data(client, "rc", 0, 200)
    # get_data(client, "rc", 0, 220)

    # pose = client.simGetVehiclePose()
    # print(f"before move: {pose}")
    # pose.position.y_val = 99.0
    # print(f"after move: {pose}")
    # client.moveToPositionAsync(0, 1.0, 0, 5.0, lookahead=0, adaptive_lookahead=0).join()
    # client.simSetVehiclePose(pose, ignore_collision=True)
    # client.hoverAsync().join()
    # time.sleep(4)
    # pose = client.simGetVehiclePose()
    # print(f"after wait: {pose}")
    # get_data(client, "lc", 3, 160)
    # client.moveToPositionAsync(-55, 0, 0, 0.5)
    # for i in range(1000):
    #     rawImage = client.simGetImage("0", airsim.ImageType.Scene)
    #     png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_COLOR)
    #     cv2.imwrite('data/sc/img_{:05}.png'.format(i), png)
    #     print('wrote data/sc/img_{:05}.png'.format(i))
    # print("Done getting pics")
    # client.hoverAsync().join()

state = client.getMultirotorState()
