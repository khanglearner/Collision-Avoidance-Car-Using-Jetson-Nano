import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn.functional as F
import cv2
import PIL.Image
import numpy as np
import time
import serial


#=======================================================================
# UART setup
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()
lst = ["forward\n", "backward\n", "left\n", "right\n", "stop\n"]

def send_data(ser, data):
    ser.write(data.encode())

def forward():
    send_data(ser, lst[0])
    print("Forward")

def backward():
    send_data(ser, lst[1])
    print("Backward")

def right():
    send_data(ser, lst[3])
    print("Right")
    time.sleep(1)

def left():
    send_data(ser, lst[2])
    print("Left")


def stop():
    send_data(ser, lst[4])
    print("Stop")


#===========================================================
device = torch.device('cuda')

model = torchvision.models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(512, 2)
model.load_state_dict(torch.load('best_model_resnet18_second.pth'))
model = model.to(device).eval().half()

mean = torch.Tensor([0.485, 0.456, 0.406]).cuda().half()
std = torch.Tensor([0.229, 0.224, 0.225]).cuda().half()
#===========================================================

# Preprocess image
def preprocess(image):
    image = PIL.Image.fromarray(image)
    image = transforms.functional.to_tensor(image).to(device).half()
    image.sub_(mean[:, None, None]).div_(std[:, None, None])
    return image[None, ...]

# Input image, using Resnet18 model to return the probability of being blocked
def update(change):
    image = change['new'] 
    x = preprocess(image)
    y = model(x)
    y = F.softmax(y, dim=1)
    
    prob_blocked = float(y.flatten()[0])
    print(f"Probability blocked: {prob_blocked:.2f}")
    
    if prob_blocked > 0.80:
        stop()
        time.sleep(0.5)
        left()
        time.sleep(0.5)
        stop()
        time.sleep(0.5)
    else:
        forward()

    time.sleep(0.0001)
#=========================================================


# Main:
cap = cv2.VideoCapture(0)

while True:
  ret, frame = cap.read()
  cv2.imshow('Robocam', frame)
  resized = cv2.resize(frame, (224, 224))

  image_in1 = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)  # change to RGB for model

  cv2.imwrite("test.jpeg", image_in1) # create image, act like a buffer
  image_final = cv2.imread("test.jpeg")  

  update({'new': image_final})	      #upload image to process
  
  if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
