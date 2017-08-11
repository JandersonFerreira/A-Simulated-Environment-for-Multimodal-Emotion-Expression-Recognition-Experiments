import scipy.io.wavfile as wav
import numpy as np
import cv2
import vrep
(rate, sig) = wav.read('audio-video/a01.wav')
tamAudio = len(sig)
cap = cv2.VideoCapture('audio-video/a1.avi')
tamVideo = cap.get(7)
print (cap.get(3), cap.get(4))
print tamAudio // tamVideo
