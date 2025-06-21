import streamlit as st
from src.service.detection_service import DetectionService
import numpy as np
import cv2
from src.service.audio_service import AudioService
from config import DEFAULT_CAMERA

detection_service = DetectionService()
audio_service = AudioService()
last_detection_state = None

st.title("Face Mask Detection")
st.write("Upload an image, video or webcam feed to detect if a person is wearing a face mask.")

st.sidebar.title("Input Settings")

input_type = st.sidebar.radio("Input Type", ("Image", "Video", "Webcam"))

def process_image(image):
    frame, detection_classes = detection_service.detect(image)

    if "without_mask" in detection_classes:
        audio_service.play_no_mask_warning()
    if "with_mask" in detection_classes:
        audio_service.play_mask_found_message()

    return frame
def process_camera(source, output_path="output.mp4"):
    cap = cv2.VideoCapture(source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        st.error("Error: Could not open camera.")
        return

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'mp4v' for mp4 format
    fps = 30.0  # Frames per second
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Error: Could not read frame from camera.")
            break

        processed_frame = process_image(frame)

        # Write the processed frame to the output video
        out.write(processed_frame)

        # Show processed frame in Streamlit
        stframe.image(processed_frame, channels="BGR")

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if input_type == "Image":
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        processed_image = process_image(image)
        st.image(processed_image, caption="Processed Image", use_column_width=True)

if input_type == "Video":
    video_file = st.sidebar.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
    if video_file is not None:
        st.video(video_file)

if input_type == "Webcam":
    camera_source = st.sidebar.text_input("Camera source (RTSP URL or index Default: 0)", str(DEFAULT_CAMERA))
    camera_source = int(camera_source) if camera_source.isdigit() else camera_source
    process_camera(camera_source)

