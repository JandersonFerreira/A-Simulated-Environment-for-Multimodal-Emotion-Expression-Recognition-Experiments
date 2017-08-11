# -*- coding: utf-8 -*-
import numpy as np
import cv2
import vrep
import time

def rgb2vrep(rgbValor):
	return -rgbValor + 127

def getLista(imagem, num_linhas, num_cols):
	r = []
	g = []
	b = []
	lista = []
	for k in range(0,3):
		for i in range(0,num_linhas):
			for j in range(0,num_cols):
				if k == 0:
					#print(i,j,k)
					r.append(imagem[i,j,k])
				elif k == 1:
					g.append(imagem[i,j,k])
				elif k == 2:
					b.append(imagem[i,j,k])	
	for i in range(0,num_linhas*(num_cols)):
		lista.append(rgb2vrep(r[i]))
		lista.append(rgb2vrep(g[i]))
		lista.append(rgb2vrep(b[i]))

	return lista

#cap = cv2.VideoCapture(0) 
cap = cv2.VideoCapture('/home/janderson/Documentos/Mestrado/Pesquisa/Desenvolvimento/Códigos/RelevanceFeedback/SetVideoVrep/robo_256x256.avi')


vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if clientID!=-1:
	print 'Connected to remote API server'

	# get vision sensor objects
	res, v0 = vrep.simxGetObjectHandle(clientID, 'v0', vrep.simx_opmode_oneshot_wait)
	res, v1 = vrep.simxGetObjectHandle(clientID, 'foto_enf1', vrep.simx_opmode_oneshot_wait)

	err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_streaming)
  	time.sleep(1)

	while (vrep.simxGetConnectionId(clientID) != -1):
		# Capture frame-by-frame
		ret, frame = cap.read()
		imagem_lista = []
		imagem_lista = getLista(frame,int(cap.get(3)),int(cap.get(4)))
		print len(imagem_lista)
		err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_buffer)
		if err == vrep.simx_return_ok:
			vrep.simxSetVisionSensorImage(clientID, v1, imagem_lista, 0, vrep.simx_opmode_oneshot)
		elif err == vrep.simx_return_novalue_flag:
			print "no image yet"
		else:
			print err
		# Display the resulting frame
		cv2.imshow('frame',frame)
		tecla = cv2.waitKey(40) & 0xFF
		if tecla == 27:
		    break

else:
	print "Failed to connect to remote API Server"
	vrep.simxFinish(clientID)
cap.release()
cv2.destroyAllWindows()