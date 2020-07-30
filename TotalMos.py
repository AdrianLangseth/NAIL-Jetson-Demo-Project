#!/usr/bin/env python
# coding: utf-8

# # Første forsøk på sammenmosing

# In[1]:


# This is a cell we must run from the start because the robot's nvargus daemon acts up and throws camera errors like nobody's business.

import os
password = "jetbot"
command = "sudo -S systemctl restart nvargus-daemon"
os.system('echo %s | %s' % (password, command))


# ### Imports

# In[2]:


# As we are writing in a seperate folder we need to add paths to the other modules not contained in the current system paths.
import sys
sys.path.insert(1,'/home/jetbot')
sys.path.insert(1,'/home/jetbot/monodepth2')


# In[3]:


from __future__ import absolute_import, division, print_function  # unknown what this is but everything fails if i remove it.
get_ipython().run_line_magic('matplotlib', 'inline')

# Utility functions for type conversions 
from jetson.utils import cudaFromNumpy
import numpy as np


# Visualizing
import matplotlib.pyplot as plt

# Torch
import torch
import torchvision
from torchvision import transforms


# Monodepth
from monodepth2 import *
import monodepth2.networks as networks
from monodepth2.utils import download_model_if_doesnt_exist


# CAMERA
from jetbot import Camera, Robot

# Preprocessing
import cv2
import time
import PIL.Image as pil

# Source of Object Detection Net
from jetson import inference



# ## General Setups

# In[4]:


# If GPU is available, we will use it for efficiency
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

if __name__ == '__main__':
    print(device)


# In[20]:


# Instanciate camera with defined size.
camwidth, camheight = 320, 240 #224,224
cam = Camera.instance(width=camwidth, height=camheight)

try:
    print("Camspecs are to specifications: ", ((cam.width == camwidth) and (cam.height == camheight)))
    print(cam.width, cam.height)
except NameError:
    pass

# Instanciate Camera
robot = Robot()
robot.stop()

def geometric_average(l:list):
    '''
    This function returns the geometric average of the given list
    '''
    return (sum(np.array(l)**2)/len(l))**(1/2)

# We predefine the general constants used later for efficiency in the future cells.
total = []
blocking_threshold = 0.85


# ## OF Setup

# In[6]:


# Instanciate our Detection Network from the Jetson Inference package with the model name and the threshold level.
net = inference.detectNet("ssd-mobilenet-v2", threshold=0.4)


# We define the Detection bool as false to start.
det = False
accepted_classes = [47]  # classID from coco_labels.txt file


# ## Setting up CA model

# In[7]:


# In thsi block we create and customize our Collision avoidance model.
model = torchvision.models.alexnet(pretrained=False) # Load Alexnet as our model
model.classifier[6] = torch.nn.Linear(model.classifier[6].in_features, 2) #last layer wants 1000 labels, we only need 2, so we swap last layer with a linear binary layer.
model.load_state_dict(torch.load('best_model.pth')) # Load with our best trained model
model = model.to(device) # Push model onto superior GPU

# Standard Imagenet normalization
mean = 255.0 * np.array([0.485, 0.456, 0.406])
stdev = 255.0 * np.array([0.229, 0.224, 0.225])
normalize = torchvision.transforms.Normalize(mean, stdev)


def preprocess(camera_value): # Preprocessing for camera format --> Network input format
    """
    Preprocessing function for camera format --> network input format
    
    param camera_value: input from Camera
    type camera_value: np.ndarray
    """
    global device, normalize
    x = camera_value
    x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB) # For some unknown reason the camera input is on BGR format, so we change it into RGBA.
    x = x.transpose((2, 0, 1))
    x = torch.from_numpy(x).float()
    x = normalize(x)
    x = x.to(device)
    x = x[None, ...]
    return x


# ## Setting up Monodepth model

# In[8]:


# We build our monocular depth estimation model from the Monodepth module

# Define which model to use and download if not found
model_name = "mono_640x192"
download_model_if_doesnt_exist(model_name)

# Build paths to coders and instanciate from path
encoder_path = os.path.join("models", model_name, "encoder.pth")
depth_decoder_path = os.path.join("models", model_name, "depth.pth")
encoder = networks.ResnetEncoder(18, False).cuda()
depth_decoder = networks.DepthDecoder(num_ch_enc=encoder.num_ch_enc, scales=range(4)).cuda()

# Encoder and Decoder loading
loaded_dict_enc = torch.load(encoder_path, map_location='cpu')
filtered_dict_enc = {k: v for k, v in loaded_dict_enc.items() if k in encoder.state_dict()}
encoder.load_state_dict(filtered_dict_enc)
loaded_dict = torch.load(depth_decoder_path, map_location='cpu')
depth_decoder.load_state_dict(loaded_dict)

# Put the coders in evaluation mode
encoder.eval()
depth_decoder.eval();

#pull out feed size to use for processing in loop, do now for efficiency in execution 
feed_height = loaded_dict_enc['height']
feed_width = loaded_dict_enc['width']


# ## CA Prep

# In[9]:


import torch.nn.functional as Fun


def CA_update(change):
    """
    This function receives the change in the camera values and acts on it if the confidence of a blocked path is above the blocking threshold.
    This function forms the basis of the collision avoidance safety for the monocular depth perception.
    
    param change: The change observed in the camera
    type change: Dictionary
    """
    global robot, prob_blocked
    x = change['new'] 
    x = preprocess(x)
    y = model(x)
    
    # we apply the `softmax` function to normalize the output vector so it sums to 1 (which makes it a probability distribution)
    y = Fun.softmax(y, dim=1)
    
    # If the blocking confidence is higher than the set threshold the smart collision avoidance overrides the motor functions of the monocular depth estimator.
    prob_blocked = float(y.flatten()[0])
    if prob_blocked > blocking_threshold: 
        # The CA aspect chooses the turn based on its previous motor values. The basic concept being a smooth turn is the one continuing on the already progressing one. 
        if robot.left_motor.value > robot.right_motor.value:
            robot.right(0.4)
        else:
            robot.left(0.4)
        
    time.sleep(0.01)


# ## OD Prep

# In[10]:


def OD_update(change):
    """
    This function receives the change in the camera values and runs object detection. If a detection of the desired class is made,
    OD overrides the normal functionality to track down the detected object.
    This function forms the basis of the endgame override to the monocular depth perception.
    
    param change: The change observed in the camera
    type change: Dictionary
    """
    global robot, cam, det
    try: # Preprocessing of input values
        arr = change['new'] 
        frame = cv2.cvtColor(arr, cv2.COLOR_BGR2RGBA) # input is on RBGR, network needs RGBA.
        camCuda = cudaFromNumpy(frame)
        detections = net.Detect(image = camCuda, width = camwidth, height = camheight, overlay = "none")
        det = False # We set detection flag to false.
        for d in detections:
            if d.ClassID in accepted_classes:
                print("OD ACTIVATED")
                center_x, center_y = d.Center
                det = True
                break
        if det: # if we have detected the desired object, we enter into object following.
            if d.Height/camheight > 0.25:
                robot.stop()
                cam.unobserve_all()
                print("Hider Located! Victory!")
            else:
                x = center_x/camwidth - 0.5 
                robot.set_motors(
                    float(0.4 + 0.8 * x), # left
                    float(0.4 - 0.8 * x)) # Right
    except:
        pass


# # Run

# In[24]:


CA_update({'new': cam.value}) # We instanciate the update functions with the current camera values
OD_update({'new': cam.value})
cam.observe(CA_update, names='value') # Now we connect the update functions to the camera. This wil cause the update functions o be called whenever we have a change in the camera values.
cam.observe(OD_update, names='value')
while True: # Run indefinitely, only ended when we have success or we have an resignation by KeyboardInterrupt.
    try:
        if det:
            cam.unobserve(CA_update, names='value')
            break
        elif prob_blocked < blocking_threshold:
            # preprocessing: 
            inputImage = pil.fromarray(cam.value.astype('uint8'),'RGB') #.rotate(180)
            input_image_resized = inputImage.resize((feed_width, feed_height), pil.LANCZOS)
            input_image_pytorch = transforms.ToTensor()(input_image_resized).unsqueeze(0).cuda()

            # MD net
            with torch.no_grad():
                features = encoder(input_image_pytorch)
                outputs = depth_decoder(features)
            disp = outputs[("disp", 0)]
            
            # postprocessing
            disp_resized = torch.nn.functional.interpolate(disp.cpu(), (camheight, camwidth), mode="bilinear", align_corners=False).cuda()
            disp_resized_np = disp_resized.squeeze().cpu().numpy()
            
            # Algorithm for evaluating depth perceptions and pushing onto motor values
            A = []
            B = []
            C = []
            edge1 = round(camwidth/3)
            edge2 = round(2*camwidth/3)
            for w in range(camheight):
                for j in range(edge1):
                    A.append(disp_resized_np[w][j])
                for j in range(edge1, edge2):
                    B.append(disp_resized_np[w][j])
                for j in range(edge2, camwidth):
                    C.append(disp_resized_np[w][j])
            B_scale = 1 - geometric_average(B)/np.max(disp_resized_np)
            right_motor = 2*(0.5 - geometric_average(A)*B_scale)
            left_motor = 2*(0.5 - geometric_average(C)*B_scale)
            robot.set_motors(left_motor, right_motor)           
    except KeyboardInterrupt: # Set up a keyboard interrupt so that if we abort from keyboard it will dismantle properly and not SIGKILL.
        cam.unobserve_all()
        robot.stop()
        print('Loop successfully ended, loop')
        break
        
# We end up here if we successfully find our object, therefore we cant dismantle all camera observables and for safety also stop robot.
cam.unobserve_all()
robot.stop()

