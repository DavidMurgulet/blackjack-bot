from ultralytics import YOLO
import cv2


# Load the YOLO model with the specified weights
model = YOLO('best.pt')

# Initialize the decision dictionary
decision = {str(i): False for i in range(1, 11)}
decision.update({"K": False, "Q": False, "J": False})

img = cv2.imread('test2.png')
img = cv2.resize(img, (800, 800))


# Run the model on the test image
results = model([img], conf=0.15, save=True)

# Extract the results
boxes = results[0].boxes.xyxy.tolist()
classes = results[0].boxes.cls.tolist()
names = results[0].names
confidences = results[0].boxes.conf.tolist()

# Print the results
print(f"Number of boxes detected: {len(boxes)}")
print(f"Detected boxes: {boxes}")
print(f"Detected classes: {classes}")
print(f"Detected confidences: {confidences}")

# Update the decision dictionary based on detected classes
for cls in classes:
    name = names[int(cls)]
    if name in decision:
        decision[name] = True

# Print the decision dictionary
print(decision)
