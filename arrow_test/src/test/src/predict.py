#!/usr/bin/env python
import PIL
import torch
from torch import nn
from torchvision import transforms,datasets 
import torch.nn as nn
import torch.nn.functional as F
import cv2
import sys
import rospy
import numpy as np
#from PIL import Image
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import warnings
warnings.filterwarnings("ignore")

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        
         ## define the layers

        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)

        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)

        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)

        self.conv4 = nn.Conv2d(64, 128, 3, padding=1)

        self.conv5 = nn.Conv2d(128, 256, 3, padding=1)

        self.pool = nn.MaxPool2d(2, 2)

        self.linear1 = nn.Linear(256*7*7, 128)

        self.linear2 = nn.Linear(128, 3)

    

    def forward(self, x):

        x = self.pool(F.relu(self.conv1(x)))

        x = self.pool(F.relu(self.conv2(x)))

        x = self.pool(F.relu(self.conv3(x)))

        x = self.pool(F.relu(self.conv4(x)))

        x = self.pool(F.relu(self.conv5(x)))

        #print(x.shape)

        x = x.view(x.size(0),-1) 

        x = F.relu(self.linear1(x))

        x = self.linear2(x)

        return x

def callback(data):
    global count,bridge
    count = count + 1
    if count == 1:
        count = 0
        cv_img = bridge.imgmsg_to_cv2(data, "bgr8")
        img = transforms.ToPILImage()(cv_img)
        preprocess_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.492, 0.461, 0.417], [0.256, 0.248, 0.251])
        ])

        class_names = ['left','right','straight']

        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        #model = Net()
        model = torch.load("/home/bosonlee/data/mnist/model.pkl")
        #model.to(device)
        model.eval()


        #img_path = '/home/bosonlee/Desktop/Left arrow/23.jpg'

        #img = Image.open(img_path)
        #print(type(img))
        img_= preprocess_transform(img)
        img_.unsqueeze_(0)
        img_ = img_.to(device)
        outputs = model(img_)

        #输出概率最大的类别
        _, indices = torch.max(outputs,1)
        percentage = torch.nn.functional.softmax(outputs, dim=1)[0] * 100
        perc = percentage[int(indices)].item()
        result = class_names[indices]
        print('predicted:', result)

        #print(outputs)
        #_, indices = torch.sort(outputs, descending=True)
        # 返回每个预测值的百分数
        #percentage = torch.nn.functional.softmax(outputs, dim=1)[0] * 100

        #print([(class_names[idx], percentage[idx].item()) for idx in indices[0][:5]])
                #print(type(img))
    else:
        pass

def displayWebcam():
    rospy.init_node('predict', anonymous=True)
    # make a video_object and init the video object
    global count,bridge
    count = 0
    bridge = CvBridge()
    rospy.Subscriber('camera/image', Image, callback)
    rospy.spin()
if __name__ == '__main__':
    displayWebcam()

