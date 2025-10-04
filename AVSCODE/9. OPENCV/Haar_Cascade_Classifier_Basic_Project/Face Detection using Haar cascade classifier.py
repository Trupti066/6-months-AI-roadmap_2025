import cv2
import numpy as np

# Load Haar Cascade (easiest method)
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load image
image = cv2.imread(r"C:\Ds & AI ( my work)\AVSCODE\9. OPENCV\Haar_Cascade_Classifier_Basic_Project\img-1.webp")

if image is None:
    print("❌ Error: Image not found! Check your path.")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

if len(faces) == 0:
    print("😕 No faces found!")
else:
    print(f"✅ Found {len(faces)} face(s).")
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (127, 0, 255), 2)

    cv2.imshow('Face Detection', image)
    cv2.waitKey(0)

cv2.destroyAllWindows()
