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

import control_drone

# read AirSim simulator IP from commandline
if len(sys.argv) > 1:
    airsim_ip = sys.argv[1]
    print("Will connect to {}".format(airsim_ip))
else:
    airsim_ip = ""

onnx_model = onnx.load("rpg_dronet.onnx")
onnx.checker.check_model(onnx_model)

control = control_drone.IntermediateDroneApi()

ort_sess = ort.InferenceSession('rpg_dronet.onnx')
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
    im_f = resized/255
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

client.moveToPositionAsync(0,0,-0.7,5).join()

headings = np.zeros(1)
i = 0
while True:
    rawImage = client.simGetImage("0", airsim.ImageType.Scene)
    if (rawImage == None):
        print("Camera is not returning image, please check airsim for error messages")
        sys.exit(0)
    else:
        png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
        cv2.imwrite('img.png', png)
        heading = run_dronet(ort_sess, png)
        headings[i] = heading
        i = (i+1) % len(headings)
        # control.rotateToYaw(client, heading)
        # client.moveByVelocityBodyFrameAsync(3,0,-0.05,0.1).join()
        control.moveInAngle(client, np.mean(heading), 1, 0.1)
        # cv2.imshow("Depth", png)
        # if cv2.waitKey(1) == 27:
        #     pass
