# -*- coding: utf-8 -*-
import face_recognition
import cv2
import ft2
import datetime

inteval = datetime.timedelta(seconds=1)
time_stamp = datetime.datetime.now()
video_capture = cv2.VideoCapture(0)
#ret=video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1920)  
ret=video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)  
 
print ret 
#ret=video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,1080)  
ret=video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,720)  

print ret
found_face=False
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
cnt =0
v_size =(int(video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
       int(video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

print v_size
(time_start_x,time_start_y)=v_size
time_start_x=time_start_x/2
time_start_y=time_start_y/12*11

print "!"

writer = None

#On linux I used to take "M","J","P","G" as fourcc
ft = ft2.put_chinese_text('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc')

def save_img():
    pass
while True:
    found_face=False
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25,interpolation=cv2.INTER_AREA)
    #small_frame=frame

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame,number_of_times_to_upsample=2)
        
        faces = len(face_locations)
        print "find %d faces"%faces
        if faces >0:
            found_face = True

        #face_encodings = face_recognition.face_encodings(small_frame, face_locations)
        
        for (top,right,bottom,left) in face_locations:
                cv2.rectangle(frame,(left*4,top*4),(right*4,bottom*4),(0,0,255),5)
                frame=ft.draw_text(frame,((left+right)*2,bottom*4),u'波音',20,(0,255,0))
        now_time = datetime.datetime.now()
        now_str = "%s%s%s %s:%s:%s"%(now_time.year,now_time.month,now_time.day,now_time.hour,now_time.minute,now_time.second)
        cv2.putText(frame,now_str,(time_start_x,time_start_y),cv2.FONT_HERSHEY_DUPLEX,1.0,(255,255,255),1)
        cv2.imwrite("%s_%d.jpg"%(now_str,faces),frame)
        cnt=cnt+1
    if process_this_frame:
        process_this_frame=False
    else:
        process_this_frame=True
    
    if writer is None:
        fps=20.0
        
        #fourcc = cv2.ViceoWriter_fourcc(*'XVID')
        #writer = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
        #videoWriter = cv2.VideoWriter('oto_other.mpg', cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'), fps, v_size)
        #writer = cv2.VideoWriter('oto_other.avi', cv2.cv.CV_FOURCC(*'XVID'), fps, v_size)
        #print type(writer)
 
        #writer=cv2.cv.CreateVideoWriter("output.avi", cv2.cv.CV_FOURCC("D", "I", "B", " "), 5, cv2.cv.GetSize(frame), 1)
        #On linux I used to take "M","J","P","G" as fourcc
    else:
        #cv2.cv.WriteFrame(writer,frame)
        writer.write(frame)



    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
writer.release()
