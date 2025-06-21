from config import MODEL_PATH, DETECTION_THRESHOLD
import cv2
from ultralytics import YOLO

class DetectionService:
    def __init__(self, model_path: str = MODEL_PATH):
        self.model = YOLO(model_path)
        self.class_names = {
            0: "with_mask",
            1: "without_mask"
        }

    def detect(self, image):
        results = self.model(image)[0]

        detection_classes = []

        print("=== Detection Results ===")
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result

            print(f"Class ID: {class_id}, Score: {score}")  # DEBUG output

            if score >= DETECTION_THRESHOLD:
                class_name = self.class_names.get(int(class_id), "unknown")
                detection_classes.append(class_name)

                # Draw bounding box
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

                # Label it
                cv2.putText(image, class_name, (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        print("Detected classes:", detection_classes)  # DEBUG output
        return image, detection_classes
