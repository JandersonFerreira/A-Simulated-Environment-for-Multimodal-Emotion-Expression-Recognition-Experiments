# -*- coding: utf-8 -*-
import vrep
import time
import cv2
from PIL import Image
import time

# PDI

def rgb2vrep(rgbValor):
  return -rgbValor + 127

im = Image.open("robo.png")
rgb = im.convert('RGB')

n,m = im.size
n = n-1;
m = m-1;

lista = []
for i in range(0,n+1):
  for j in range(0,m+1):
    r,g,b = rgb.getpixel((i,j))
    lista.append(rgb2vrep(r))
    lista.append(rgb2vrep(g))
    lista.append(rgb2vrep(b))


# VREP
vrep.simxFinish(-1)

clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if clientID!=-1:
  print 'Connected to remote API server'
  
  # get vision sensor objects
  # _, v0 = vrep.simxGetObjectHandle(clientID, 'v0', vrep.simx_opmode_oneshot_wait)
  # _, foto_enf1 = vrep.simxGetObjectHandle(clientID, 'foto_enf1', vrep.simx_opmode_oneshot_wait)
  res, foto_enf1 = vrep.simxGetObjectHandle(clientID, 'foto_enf1', vrep.simx_opmode_oneshot_wait)

  err, resolution, image = vrep.simxGetVisionSensorImage(clientID, foto_enf1, 0, vrep.simx_opmode_streaming)
  time.sleep(1)
  print len(lista)
  # err, resolution, image = vrep.simxGetVisionSensorImage(clientID, foto_enf1, 0, vrep.simx_opmode_streaming)
  err, resolution, image = vrep.simxGetVisionSensorImage(clientID, foto_enf1, 0, vrep.simx_opmode_buffer)
  time.sleep(1)
  print err
  while (vrep.simxGetConnectionId((clientID) != -1) and (err == 0)):
    err, resolution, image = vrep.simxGetVisionSensorImage(clientID, foto_enf1, 0, vrep.simx_opmode_buffer)
    if err == vrep.simx_return_ok:
      vrep.simxSetVisionSensorImage(clientID, foto_enf1, lista, 0, vrep.simx_opmode_oneshot)
    elif err == vrep.simx_return_novalue_flag:
      print "no image yet"
    else:
      print err
else:
  print "Failed to connect to remote API Server"
  vrep.simxFinish(clientID)