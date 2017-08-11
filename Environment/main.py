# -*- coding: utf-8 -*-
import scipy.io.wavfile as wav
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
        lista.append((b[i]))
        lista.append((g[i]))
        lista.append((r[i]))

    return lista

_, pessoaAudio1 = wav.read('audio-video/a01.wav')
_, pessoaAudio2 = wav.read('audio-video/a01.wav')

pessoaVideo1 = cv2.VideoCapture('audio-video/a1.avi')
pessoaVideo2 = cv2.VideoCapture('audio-video/a1.avi')

tamAudio = len(pessoaAudio1)
tamVideo = pessoaVideo1.get(7)
height = pessoaVideo1.get(3)
width = pessoaVideo1.get(4)

janelaAudio = int(tamAudio // tamVideo)

vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if clientID!=-1:
    print 'Connected to remote API server'

    _, luzA = vrep.simxGetObjectHandle(clientID, 'DefaultLightD', vrep.simx_opmode_oneshot_wait)
    # get joints
    _, leftMotor = vrep.simxGetObjectHandle(clientID, 'leftMotor', vrep.simx_opmode_oneshot_wait)
    _, rightMotor = vrep.simxGetObjectHandle(clientID, 'rightMotor', vrep.simx_opmode_oneshot_wait)
    # get vision sensor objects
    _, person1 = vrep.simxGetObjectHandle(clientID, 'fotoFace1', vrep.simx_opmode_oneshot_wait)
    _, person2 = vrep.simxGetObjectHandle(clientID, 'fotoFace2', vrep.simx_opmode_oneshot_wait)
    _, Vision_sensor = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
    # _, ouvido = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)

    _, distanciaPessoa1 = vrep.simxGetDistanceHandle(clientID, 'Distance1',vrep.simx_opmode_blocking)
    _, distanciaPessoa2 = vrep.simxGetDistanceHandle(clientID, 'Distance2',vrep.simx_opmode_blocking)

    err1, resolution, frame = vrep.simxGetVisionSensorImage(clientID, person1, 0, vrep.simx_opmode_streaming)
    err2, resolution, frame = vrep.simxGetVisionSensorImage(clientID, person2, 0, vrep.simx_opmode_streaming)
    _, resOlho, olho = vrep.simxGetVisionSensorImage(clientID, Vision_sensor, 0, vrep.simx_opmode_streaming)
    ouvido = []

    time.sleep(1)
    cont = 0
    while (vrep.simxGetConnectionId(clientID) != -1):
        
        print luzA
        vrep.simxSetJointTargetVelocity(clientID, leftMotor, 0, vrep.simx_opmode_blocking)
        vrep.simxSetJointTargetVelocity(clientID, rightMotor, 0, vrep.simx_opmode_blocking)

        ouvido = []
        _, foto1 = pessoaVideo1.read()
        _, foto2 = pessoaVideo2.read()
        
        foto_lista1 = getLista(foto1,int(width),int(height))
        foto_lista2 = getLista(foto2,int(width),int(height))
        
        err1, resolution, frame = vrep.simxGetVisionSensorImage(clientID, person1, 0, vrep.simx_opmode_buffer)
        err2, resolution, frame = vrep.simxGetVisionSensorImage(clientID, person2, 0, vrep.simx_opmode_buffer)
        _, resOlho, olho = vrep.simxGetVisionSensorImage(clientID, Vision_sensor, 0, vrep.simx_opmode_buffer)
        
        olho = np.array(olho, dtype=np.uint8)
        olho.resize([resOlho[0],resOlho[1],3])
        olho = np.rot90(olho,2)
        olho = np.fliplr(olho)
        olho = cv2.cvtColor(olho, cv2.COLOR_RGB2BGR)

        distancia1 = vrep.simxReadDistance(clientID, distanciaPessoa1, vrep.simx_opmode_blocking)[1]
        distancia2 = vrep.simxReadDistance(clientID, distanciaPessoa2, vrep.simx_opmode_blocking)[1]
        escutando = 'Silence'
        if (distancia1 < 3) and (distancia2 < 3):
            aux1 = pessoaAudio1[(cont*janelaAudio):((cont+1)*janelaAudio)]
            aux2 = pessoaAudio2[(cont*janelaAudio):((cont+1)*janelaAudio)]
            ouvido.append(aux1+aux2)
            escutando = 'Listening Person 1 e 2'
        elif (distancia1 < 3):
            ouvido.append(pessoaAudio1[(cont*janelaAudio):((cont+1)*janelaAudio)])
            escutando = 'Listening Person 1'
        elif (distancia2 < 3):
            ouvido.append(pessoaAudio2[(cont*janelaAudio):((cont+1)*janelaAudio)])
            escutando = 'Listening Person 2'
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(olho,escutando,(10,50), font, 0.7,(0,255,0),1,0)
        cv2.imshow('Monitor',olho)
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
        if ((err1 == vrep.simx_return_ok) and (err2 == vrep.simx_return_ok)):
            vrep.simxSetVisionSensorImage(clientID, person1, foto_lista1, 0, vrep.simx_opmode_oneshot)
            vrep.simxSetVisionSensorImage(clientID, person2, foto_lista1, 0, vrep.simx_opmode_oneshot)
        elif ((err1 == vrep.simx_return_novalue_flag) and (err2 == vrep.simx_return_novalue_flag)):
            print "no image yet"
        else:
            print err1
        cont += 1

else:
    print "Failed to connect to remote API Server"
    vrep.simxFinish(clientID)