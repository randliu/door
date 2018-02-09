#! /usr/bin/python
# -*- coding: utf-8 -*-

import face_recognition
import cv2
import RPi.GPIO as GPIO
import time
import numpy as np

import os
from datetime import datetime,timedelta
from cfg import face_codes_dir

time_mark = datetime.now()
def open_door():
    GPIO.setmode(GPIO.BCM)
    # 输出模式
    GPIO.setup(18,GPIO.OUT)
    GPIO.output(18, GPIO.HIGH)
    GPIO.cleanup()


#load face code


print "Loading face codes"

dict_face_code = {}
face_code_cnt=0
for parent,dirnames,filenames in os.walk(face_codes_dir):
    for filename in filenames:                        #输出文件信息
        #print "parent is:" + parent
        #print "filename is:" + filename
        code_file = os.path.join(parent,filename)
        print "Loading:" + code_file #输出文件路径信息
        code = np.load(code_file)

        dict_face_code[filename]=code

        face_code_cnt +=1
print "\n %d face code loaded"%face_code_cnt

#print dict_face_code

print "Connecting camera"
video_capture = cv2.VideoCapture(0)
print dir(video_capture)
process_this_frame = False
round_cnt =0
while True:


    # Grab a single frame of video
    ret, frame = video_capture.read()
    #print frame.size


    now = datetime.now()
    timespan = now - time_mark

    #print timespan.total_seconds()
    if timespan.total_seconds() <2:
        #print "continue"
        cv2.imshow('Video',frame)
        continue


    print "go"
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        round_cnt +=1
        print "Round:%d"%round_cnt
        # Find all the faces and face encodings in the current frame of video

        face_locations = face_recognition.face_locations(small_frame,number_of_times_to_upsample=1)
        #print face_locations
        print "\n Finding %d faces\n"%len(face_locations)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        #face_names = []
        face_cnt=len(face_locations)
        lst_matched_name=[]
        matched =False

        cnt =0
        for face_encoding in face_encodings:
            cnt = cnt+1
            for name,code in dict_face_code.iteritems():
                match = face_recognition.compare_faces( [code], face_encoding,tolerance=0.6)
                if match[0]:
                    print "\n\n Face %d match %s"%(cnt,str(name))
                    lst_matched_name.append(name)

                    if not matched:
                        matched = True
        if matched:
            print "\n Matched :%s"%str(lst_matched_name)
            open_door()
            time_mark = datetime.now()

        if not matched:
	    pass
            print "NOT FACE MATCHING"
            #time.sleep(1)



    process_this_frame = not process_this_frame
    cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
#程序结束后进行清理

#0000000000000000004c9f2eb7bf419a3e1bd6453e6245518ff9127b95574389
