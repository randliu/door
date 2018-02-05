#! /usr/bin/python
# -*- coding: utf-8 -*-


import os

import numpy as np
import face_recognition
import sys

from cfg import known_persons_dir ,face_codes_dir


cnt =0
print "Clear known face code"

for parent,dirnames,filenames in os.walk(face_codes_dir):
	for filename in filenames:                        #输出文件信息
		#print "parent is:" + parent
		#print "filename is:" + filename
		print "DELETING:" + os.path.join(parent,filename) #输出文件路径信息
		os.remove("%s/%s"%(face_codes_dir,filename))
		cnt +=1
print "\n %d code file deleted"%cnt

cnt=0
print "\n\nScan known person photos"

photo_cnt=0
for parent,dirnames,filenames in os.walk(known_persons_dir):
	for filename in filenames:                        #输出文件信息
		#print "parent is:" + parent
		#print "filename is:" + filename
		print "Scaning:" + os.path.join(parent,filename) #输出文件路径信息

		image = face_recognition.load_image_file("%s/%s"%(known_persons_dir,filename))
		try:
			face_encoding = face_recognition.face_encodings(image)[0]
		except:
			print "FAIL TO RECOGNIZE %s/%s"%(known_persons_dir,filename)
			continue
		np.save("%s/%s"%(face_codes_dir,filename),face_encoding)
		cnt +=1

print "\n %d face code Generated "%cnt

