#! /usr/bin/python
# -*- coding: utf-8 -*-

import face_recognition
import cv2
import time
import numpy as np

from cfg import face_codes_dir

class DogFrame:
    frame = None
    ts = None 
    has_face=False
    lst_names = []

    def get_face_names(self):
        if self.has_face:
            return self.lst_names
        else:
            return []

class FaceRecognizer:
    dict_face_code = {}

    def __init__(self):
        pass
    def load_face_code(self):

        print"loading face codes"

        face_code_cnt=0
        for parent,dirnames,filenames in os.walk(face_codes_dir):
            for filename in filenames:                        #输出文件信息
                code_file = os.path.join(parent,filename)
                print "Loading:" + code_file #输出文件路径信息
                code = np.load(code_file)

                self.dict_face_code[filename]=code

                face_code_cnt +=1
                print "\n %d face code loaded"%face_code_cnt

if __name__=='__main__':
    df = DogFrame()
    fr = FaceRecognizer()
    fr.load_face_code()
