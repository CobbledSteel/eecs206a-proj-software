import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2
import sys

import onnx
import torch
import onnxruntime as ort
import imageio

import matplotlib.pyplot as plt
import control_drone

# read AirSim simulator IP from commandline
if len(sys.argv) > 1:
    airsim_ip = sys.argv[1]
    print("Will connect to {}".format(airsim_ip))
else:
    airsim_ip = ""

# onnx_model = onnx.load("rpg_dronet.onnx")
onnx_model = onnx.load("TrailNet.onnx")
onnx.checker.check_model(onnx_model)

control = control_drone.IntermediateDroneApi()

# ort_sess = ort.InferenceSession('rpg_dronet.onnx')
ort_sess = ort.InferenceSession('TrailNet.onnx')
print(ort_sess)

# connect to the AirSim simulator
client = airsim.MultirotorClient(ip=airsim_ip)
client.confirmConnection()
client.enableApiControl(True)


print("Taking off...")
client.armDisarm(True)
client.takeoffAsync().join()


def run_dronet(ort_sess, img):
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized  = cv2.resize(grayscale, (200,200), interpolation = cv2.INTER_AREA)
    #resized = resized.reshape((resized.shape[0], resized.shape[1], 1))
    # print(resized.shape)
    # resized = cv2.flip(scaled, 1)
    im_f = resized
    im_f = im_f.astype(np.float32)
    im_f = np.expand_dims(im_f,axis=0)
    im_f = np.expand_dims(im_f,axis=0)
    # print(im_f.shape)
    im_f = im_f.transpose(0,3,2,1) 
    # print(im_f.shape)

    # x = img_utils.load_img(os.path.join(self.directory, fname),
    #     grayscale=grayscale,
    #     crop_size=self.crop_size,
    #     target_size=self.target_size)

    # x = self.image_data_generator.random_transform(x)
    # x = self.image_data_generator.standardize(x)

    outputs = ort_sess.run(None, {'input_1': im_f})
    # print(outputs)
    head = outputs[0] #- 0.05
    #if head < 0:
    #    head *= 1.3
    start_point = (100,100)
    end_point = (int(100-50*np.sin(head)),int(100-50*np.cos(head)))
    lined = cv2.line(resized, start_point, end_point, (0,00), 3)
    lined = cv2.line(resized, start_point, end_point, (255,00), 2)
    cv2.imwrite('lined.png', lined)
    # print("Outputs[0]: {}".format(outputs[0][0][0]))
    #print("outputs: {}".format(outputs[1][0][0]))
    cmd = np.clip(-head[0][0]*30, -2,2)
    print("cmd: {}".format(cmd))
    return cmd

def run_customnet(ort_sess, img):
    img_BGR = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    im_f = img_BGR.astype(np.float32)
    im_f = np.expand_dims(im_f,axis=0)
    im_f = im_f.transpose(0, 3,1,2) 

    outputs = ort_sess.run(None, {'input': im_f})
    vals = outputs[0][0]

    print("outputs: {}".format(outputs[0][0]))
    cv2.imwrite('lined.png', img_BGR)
    return vals



def run_trailnet(ort_sess, img):
    img_BGR = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    # im_f = img_BGR/255
    im_f = img_BGR.astype(np.float32)
    im_f = np.expand_dims(im_f,axis=0)
    # print(im_f.shape)
    im_f = im_f.transpose(0, 3,1,2) 
    # print(im_f.shape)

    # x = img_utils.load_img(os.path.join(self.directory, fname),
    #     grayscale=grayscale,
    #     crop_size=self.crop_size,
    #     target_size=self.target_size)

    # x = self.image_data_generator.random_transform(x)
    # x = self.image_data_generator.standardize(x)

    outputs = ort_sess.run(None, {'input': im_f})
    vals = outputs[0][0]

    print("outputs: {}".format(outputs[0][0]))
    #print("{}\t{}\t{}\t{}\t{}\t{}".format(outputs[0], outputs[1], outputs[2], outputs[3], outputs[4, outputs[5]]))
    cv2.imwrite('lined.png', img_BGR)
    return vals
    # print(outputs)
    # head = outputs[0] #- 0.05
    # #if head < 0:
    # #    head *= 1.3
    # start_point = (100,100)
    # end_point = (int(100-50*np.sin(head)),int(100-50*np.cos(head)))
    # lined = cv2.line(resized, start_point, end_point, (0,00), 3)
    # lined = cv2.line(resized, start_point, end_point, (255,00), 2)
    # cv2.imwrite('lined.png', lined)
    # # print("Outputs[0]: {}".format(outputs[0][0][0]))
    # #print("outputs: {}".format(outputs[1][0][0]))
    # cmd = np.clip(-head[0][0]*30, -2,2)
    # print("cmd: {}".format(cmd))
    # return cmd

def normalize_outputs(outputs):
    pos_left = (0.135, 0.15)
    pos_mid = (0.765, 0.775)
    pos_right = (0.080, 0.095)
    adj = [pos_left, pos_mid, pos_right]
    for i in range(3):
        outputs[3+i] = (outputs[3+i] - adj[i][0]) / (adj[i][1] - adj[i][0])
    return outputs

client.moveToPositionAsync(0,0,-0.5,5).join()

headings = np.zeros(20)
i = 0
iters = []
ax_0 = []
ax_1 = []
ax_2 = []
ax_3 = []
ax_4 = []
ax_5 = []
data = [[],[],[],[],[],[]]
ys = []
i_val = 0
control.launchStabilizer(airsim_ip)
while True:
    rawImage = client.simGetImage("0", airsim.ImageType.Scene)
    if (rawImage == None):
        print("Camera is not returning image, please check airsim for error messages")
        sys.exit(0)
    else:
        png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_COLOR)
        print("IMAGE DATA TYPE: {}".format(png.dtype))
        cv2.imwrite('img.png', png)
        # png = cv2.cvtColor(png, cv2.COLOR_BGRA2RGBA)
        heading = run_trailnet(ort_sess, png)
        vals = heading # normalize_outputs(heading)
        iters.append(i_val)
        i_val += 1
        kin = client.simGetGroundTruthKinematics()
        ypos = kin.position.y_val
        ys.append(ypos)
        if len(ys)> 30:
            ys.pop(0)
        plt.clf()
        if len(iters)> 30:
            iters.pop(0)
        for j in range(len(vals)):
            data[j].append(vals[j])
            if len(data[j])> 30:
                data[j].pop(0)
        for j in range(len(vals)):
            plt.subplot(2,3,j+1)
            plt.plot(iters, data[j])
            plt.ylim(0,1)
        plt.draw()
        plt.pause(0.001)
        heading = 0
        headings[i] = heading
        i = (i+1) % len(headings)
        # if i < 10:
        # # client.moveByVelocityBodyFrameAsync(3,0,-0.05,0.1).join()
        #     client.moveByVelocityBodyFrameAsync(0, -1.3, -0.1, 0.5).join()
        #     # control.rotateToYaw(client, -6)
        # else:
        #     client.moveByVelocityBodyFrameAsync(0, 1.3, -0.1, 0.5).join()
        #     # control.rotateToYaw(client, 6)
        #if vals[3] > vals[5]:
        #     client.moveByVelocityBodyFrameAsync(1, 1.3, -0.1, 0.5).join()
        #else:
        #     client.moveByVelocityBodyFrameAsync(1, -1.3, -0.1, 0.5).join()
        # client.moveByVelocityBodyFrameAsync(1, 3*(vals[3] - vals[5]), -0.15, 0.5).join()
        control.targets['y_vel'] = (vals[3] - vals[5])
        control.targets['yawrate'] = vals[2] - vals[1]

        # client.moveByRollPitchYawrateThrottleAsync(...)
            
        # control.rotateToYaw(client, heading)
        # client.moveByVelocityBodyFrameAsync(3,0,-0.05,0.1).join()
        #control.moveInAngle(client, np.mean(heading), 1, 0.1)
        # cv2.imshow("Depth", png)
        # if cv2.waitKey(1) == 27:
        #     pass


