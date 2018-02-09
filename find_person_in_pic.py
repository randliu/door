#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
from PIL import Image
import face_recognition
import numpy as np

print "Loading face codes"

dict_face_code = {}
face_code_cnt=0
for parent,dirnames,filenames in os.walk('./27_code/'):
    for filename in filenames:                        #输出文件信息
        #print "parent is:" + parent
        #print "filename is:" + filename
        code_file = os.path.join(parent,filename)
        print "Loading:" + code_file #输出文件路径信息
        code = np.load(code_file)

        dict_face_code[filename]=code

        face_code_cnt +=1
print "\n %d face code loaded"%face_code_cnt

lst_img=[]
for parent,dirnames,filenames in os.walk('./27/'):
    for filename in filenames:                        #输出文件信息
        #print "parent is:" + parent
        #print "filename is:" + filename
        img_file = os.path.join(parent,filename)
        print "Loading:" + img_file #输出文件路径信息
	lst_img.append(img_file)
       

for image_file in lst_img:
    image = face_recognition.load_image_file(image_file)
    
    face_locations = face_recognition.face_locations(image)

    print("I found {} face(s) in this photograph.".format(len(face_locations)))

    face_encodings = face_recognition.face_encodings(image,face_locations)
    matched = False

    for face_encoding in face_encodings:
        for file,code in dict_face_code.iteritems():
            match = face_recognition.compare_faces([code],face_encoding,tolerance=0.35)
            if match[0]:
		print match 
                print "\n %s matches %s"%(image_file,file)
		matched = True

    if not matched:
        print "\n %s not matches "%(image_file)
	
    # You can access the actual face itself like this:
    #face_image = image[top:bottom+100, left:right+10000]
    #pil_image = Image.fromarray(face_image)
    #pil_image.show()
    #pil_image.save("test3.jpg")
    #print dir(face_image)
    #print face_image.shape

