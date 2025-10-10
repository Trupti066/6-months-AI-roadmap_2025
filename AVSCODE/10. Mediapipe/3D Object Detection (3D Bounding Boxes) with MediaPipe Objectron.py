import cv2
import mediapipe as mp

# -----------------------------
# MediaPipe Objectron setup
# -----------------------------
mp_objectron = mp.solutions.objectron
mp_drawing = mp.solutions.drawing_utils

# Initialize Objectron for 3D bounding box detection (default model: "Cup")
objectron = mp_objectron.Objectron(
    static_image_mode=True,   # True since we are using a single image
    max_num_objects=5,
    min_detection_confidence=0.5,
    model_name='Cup'
)

# -----------------------------
# Load local image
# -----------------------------
image_path = r"C:\Ds & AI ( my work)\AVSCODE\10. Mediapipe\cup.jpeg"
image = cv2.imread(image_path)

if image is None:
    print("❌ Failed to load image. Check the path!")
    exit()

# Convert BGR to RGB for MediaPipe
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# -----------------------------
# Process image with Objectron
# -----------------------------
results = objectron.process(rgb_image)

# -----------------------------
# Draw 3D bounding boxes if detected
# -----------------------------
if results.detected_objects:
    for detected_object in results.detected_objects:
        mp_drawing.draw_landmarks(
            image,
            detected_object.landmarks_2d,
            mp_objectron.BOX_CONNECTIONS
        )
    print(f"✅ Detected {len(results.detected_objects)} object(s)")
else:
    print("⚠️ No objects detected in the image")

# -----------------------------
# Show image
# -----------------------------
cv2.imshow("MediaPipe Objectron 3D Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# -----------------------------
# Release Objectron
# -----------------------------
objectron.close()


