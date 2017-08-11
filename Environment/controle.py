# -*- coding: utf-8 -*-
import numpy as np
import cv2
import vrep
import time

vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
fotoControle = cv2.imread('robo.png')
if clientID!=-1:
	print 'Connected to remote API server'
	_, leftMotor = vrep.simxGetObjectHandle(clientID, 'leftMotor', vrep.simx_opmode_oneshot_wait)
	_, rightMotor = vrep.simxGetObjectHandle(clientID, 'rightMotor', vrep.simx_opmode_oneshot_wait)
	print leftMotor
	while (vrep.simxGetConnectionId(clientID) != -1):
		time.sleep(0.2)
		vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0, vrep.simx_opmode_blocking)
		vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0, vrep.simx_opmode_blocking)
		cv2.imshow('frame',fotoControle)
		tecla = cv2.waitKey(40) & 0xFF
		if tecla == 27:
		    break
		elif tecla == 119:
			vrep.simxSetJointTargetVelocity(clientID, leftMotor, 20, vrep.simx_opmode_blocking)
			vrep.simxSetJointTargetVelocity(clientID, rightMotor, 20, vrep.simx_opmode_blocking)
		elif tecla == 115:
			vrep.simxSetJointTargetVelocity(clientID, leftMotor, -2, vrep.simx_opmode_blocking)
			vrep.simxSetJointTargetVelocity(clientID, rightMotor, -2, vrep.simx_opmode_blocking)
		elif tecla == 97:
			vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0, vrep.simx_opmode_blocking)
			vrep.simxSetJointTargetVelocity(clientID, rightMotor, 20, vrep.simx_opmode_blocking)
		elif tecla == 100:
			vrep.simxSetJointTargetVelocity(clientID, leftMotor, 20, vrep.simx_opmode_blocking)
			vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0, vrep.simx_opmode_blocking)
else:
	print "Failed to connect to remote API Server"
	vrep.simxFinish(clientID)
cv2.destroyAllWindows()

# a = 97; d = 100; s = 115; w = 119