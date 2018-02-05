#! /usr/bin/python
# -*- coding: utf-8 -*-

import face_recognition
import cv2
import RPi.GPIO as GPIO
import time
import numpy as np

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
#obama_image = face_recognition.load_image_file("obama.jpg")
#obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
"""
rand_image = face_recognition.load_image_file("rand.jpg")
#print rand_image
rand_face_encoding = face_recognition.face_encodings(rand_image)[0]
print rand_face_encoding
np.save("rand.txt",rand_face_encoding)
import  sys
sys.exit(0)

"""
rand_face_encoding = np.load("rand.txt.npy")
#alen_image = face_recognition.load_image_file("alen.jpg")
#alen_face_encoding = face_recognition.face_encodings(alen_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

dita = 0

def should_continue():
	global dita
	dita +=1
	if dita >= 8:
		dita =0
		return False
	else:
		return True

def reset_dita():
	global dita
	dita=0

def open_door():
	GPIO.setmode(GPIO.BCM)
	# 输出模式
	GPIO.setup(18,GPIO.OUT)
	GPIO.output(18, GPIO.HIGH)
	time.sleep(1)

rand =0
obama = 0
alen = 0
unknown=0
cnt =0

should_open= False

while True:
	# Grab a single frame of video
	ret, frame = video_capture.read()
	#print frame.size
	frame =cv2.resize(frame,(800,600))

	# Resize frame of video to 1/4 size for faster face recognition processing
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
	#small_frame = cv2.resize(frame, (80,60))

	# Only process every other frame of video to save time
	if process_this_frame:
		# Find all the faces and face encodings in the current frame of video
		#cv2.flip(small_frame, flipCode=-1,dst=small_frame)

		#cv2.ShowImage('180_rotation', small_frame)

		face_locations = face_recognition.face_locations(small_frame,number_of_times_to_upsample=1,model="cnn")
		#print face_locations
		face_encodings = face_recognition.face_encodings(small_frame, face_locations)

		face_names = []
		for face_encoding in face_encodings:
			# See if the face is a match for the known face(s)
			#match = face_recognition.compare_faces([obama_face_encoding,rand_face_encoding,alen_face_encoding,], face_encoding,tolerance=0.5)
			match = face_recognition.compare_faces([rand_face_encoding,], face_encoding,tolerance=0.5)
			#print match
			name = "Unknown"

			if match[0]:
				name = u"rand"
				obama+=1
			else:
				unknown+=1

			"""
			elif match[1]:
				name = u"Rand"
				rand +=1
			elif match[2]:
				name = u"Alen"
				alen+=1
			"""



			face_names.append(name)

			#print "obama=%d,rand=%d,alen=%d,unknwo"%(obama,rand,alen)
			print "obama={},rand={},alen={},unknown={}".format(obama,rand,alen,unknown)


			if unknown >=3:
				reset_dita()
				unknown=0
				rand =0
				obama=0
				alen=0

			if should_continue():
				pass
			elif unknown < 3 :
				open_door()
				unknown=0
				rand =0
				obama=0
				alen=0
				reset_dita()


	#process_this_frame = not process_this_frame

	if process_this_frame :
		process_this_frame = not process_this_frame
	else:
		cnt =cnt +1
		if cnt %3 == 0:
			cnt =0
			process_this_frame = True


	"""
	# Display the results
	for (top, right, bottom, left), name in zip(face_locations, face_names):
		# Scale back up face locations since the frame we detected in was scaled to 1/4 size
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4

		# Draw a box around the face
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

		# Draw a label with a name below the face
		cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
	"""
	# Display the resulting image
	#cv2.imshow('Video', frame)


	# Hit 'q' on the keyboard to quit!
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
#程序结束后进行清理
GPIO.cleanup()
