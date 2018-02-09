from PIL import Image
import face_recognition


# Load the jpg file into a numpy array
image = face_recognition.load_image_file("1280.jpg")

# Find all the faces in the image
#face_locations = face_recognition.face_locations(image,model="cnn")
face_locations = face_recognition.face_locations(image)

print("I found {} face(s) in this photograph.".format(len(face_locations)))

for face_location in face_locations:

    # Print the location of each face in this image
    top, right, bottom, left = face_location
    top = top-10
    if top <0:
        top = 0
    #print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right+100000))

    # You can access the actual face itself like this:
    #face_image = image[top:bottom+100, left:right+10000]
    #pil_image = Image.fromarray(face_image)
    #pil_image.show()
    #pil_image.save("test3.jpg")
    #print dir(face_image)
    #print face_image.shape

