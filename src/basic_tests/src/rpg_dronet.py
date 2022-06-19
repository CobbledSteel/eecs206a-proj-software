import onnx
import torch

import onnxruntime as ort
import numpy as np

import imageio

import cv2

import time


if __name__ == "__main__":
    onnx_model = onnx.load("rpg_dronet.onnx")
    onnx.checker.check_model(onnx_model)

    
    ort_sess = ort.InferenceSession('rpg_dronet.onnx')
    print(ort_sess)

    #for imfile in ['test1.png', 'test2.png', 'test3.png']:
    # for imfile in ['vid_img/sodawalk_088.png']:
    #for i in range(1,1592):
    #for i in range(1,2122):
    #for i in range(1,1070):
    for i in range(1,9999):
        imfile = 'sodawalk/sodawalk_{:04d}.png'.format(i)
        im = np.asarray(imageio.imread(imfile)[:,:,0:3])
        im_cv = cv2.imread(imfile)
        grayscale = cv2.cvtColor(im_cv, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(grayscale, (200,200), interpolation = cv2.INTER_AREA)


    
        # print(im.shape)
        # print(type(im))

        # im_f = np.zeros([224,224,3], dtype=np.float32)
        im_f = resized/255
        im_f = im_f.astype(np.float32)
        im_f = np.expand_dims(im_f,axis=0)
        im_f = np.expand_dims(im_f,axis=0)
        print(im_f.shape)
        #im_f = im_f.transpose(0,3,1,2) 
        im_f = im_f.transpose(0,3,2,1) 
        # print(im_f)
        # print(type(im_f))
        print(im_f.shape)
        # print(im_f.dtype)


        outputs = ort_sess.run(None, {'input_1': im_f})
        print(outputs)
        head = outputs[0]
        start_point = (100,100)
        end_point = (int(100-50*np.sin(head)),int(100-50*np.cos(head)))
        lined = cv2.line(resized, start_point, end_point, (0,00), 3)
        lined = cv2.line(resized, start_point, end_point, (255,00), 2)
        # cv2.imshow('test', lined)
        # cv2.waitKey(0)
        cv2.imwrite('sodawalk_anno/sodawalk_anno{:04d}.png'.format(i), lined)

