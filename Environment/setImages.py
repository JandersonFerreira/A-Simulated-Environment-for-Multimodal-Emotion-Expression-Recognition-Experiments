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
					r.append(imagem[i,j,k])
				elif k == 1:
					g.append(imagem[i,j,k])
				elif k == 2:
					b.append(imagem[i,j,k])	
	for i in range(0,num_linhas*(num_cols)):
		lista.append((r[i]))
		lista.append((g[i]))
		lista.append((b[i]))

	return lista

#cap = cv2.VideoCapture(0) 
# cap = cv2.VideoCapture('/home/janderson/Documentos/Mestrado/Pesquisa/Desenvolvimento/Códigos/RelevanceFeedback/SetVideoVrep/robo_256x256.avi')

# carregar imagens
foto1 = cv2.imread('1.png')
foto2 = cv2.imread('2.png')
foto3 = cv2.imread('3.png')
foto4 = cv2.imread('4.png')
height, width, channels = foto1.shape

vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if clientID!=-1:
	print 'Connected to remote API server'

	# get vision sensor objects
	res, enf1 = vrep.simxGetObjectHandle(clientID, 'foto_enf1', vrep.simx_opmode_oneshot_wait)
	res, enf2 = vrep.simxGetObjectHandle(clientID, 'foto_enf2', vrep.simx_opmode_oneshot_wait)
	res, enf3 = vrep.simxGetObjectHandle(clientID, 'foto_enf3', vrep.simx_opmode_oneshot_wait)
	res, enf4 = vrep.simxGetObjectHandle(clientID, 'foto_enf4', vrep.simx_opmode_oneshot_wait)

	err1, resolution, frame = vrep.simxGetVisionSensorImage(clientID, enf1, 0, vrep.simx_opmode_streaming)
	err2, resolution, frame = vrep.simxGetVisionSensorImage(clientID, enf2, 0, vrep.simx_opmode_streaming)
	err3, resolution, frame = vrep.simxGetVisionSensorImage(clientID, enf3, 0, vrep.simx_opmode_streaming)
	err4, resolution, frame = vrep.simxGetVisionSensorImage(clientID, enf4, 0, vrep.simx_opmode_streaming)
  	time.sleep(1)

	while (vrep.simxGetConnectionId(clientID) != -1):
		foto_lista1 = getLista(foto1,height,width)
		foto_lista2 = getLista(foto2,height,width)
		foto_lista3 = getLista(foto3,height,width)
		foto_lista4 = getLista(foto4,height,width)
		err1, resolution, frame = vrep.simxGetVisionSensorImage(clientID, enf1, 0, vrep.simx_opmode_buffer)
		err2, resolution, frame = vrep.simxGetVisionSensorImage(clientID, enf2, 0, vrep.simx_opmode_buffer)
		err3, resolution, frame = vrep.simxGetVisionSensorImage(clientID, enf3, 0, vrep.simx_opmode_buffer)
		err4, resolution, frame = vrep.simxGetVisionSensorImage(clientID, enf4, 0, vrep.simx_opmode_buffer)

		if ((err1 == vrep.simx_return_ok) and (err2 == vrep.simx_return_ok)):
			vrep.simxSetVisionSensorImage(clientID, enf1, foto_lista1, 0, vrep.simx_opmode_oneshot)
			vrep.simxSetVisionSensorImage(clientID, enf2, foto_lista2, 0, vrep.simx_opmode_oneshot)
			vrep.simxSetVisionSensorImage(clientID, enf3, foto_lista3, 0, vrep.simx_opmode_oneshot)
			vrep.simxSetVisionSensorImage(clientID, enf4, foto_lista4, 0, vrep.simx_opmode_oneshot)
			# print 'rodou'
		elif ((err1 == vrep.simx_return_novalue_flag) and (err2 == vrep.simx_return_novalue_flag)):
			print "no image yet"
		else:
			print err

else:
	print "Failed to connect to remote API Server"
	vrep.simxFinish(clientID)