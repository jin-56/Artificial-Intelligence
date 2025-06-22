import tempfile
import cv2
import streamlit as st
from config import DEFAULT_CAMERA
from src.service.audio_service import AudioService
from src.service.detection_service import DetectionService
import numpy as np

detection_service = DetectionService()
audio_service = AudioService()

st.title("Secure ATM - Helment Detection")
st.write("Upload an image or video or use your webcam to detect if a helmet is worn. If a helmet is detected, the ATM will be locked or beep sound is played.")

st.sidebar.title("Input Settings")

input_type = st.sidebar.radio("Input Type", ("Image", "Video", "Camera"))


def process_image(image):
    frame, detection_classes = detection_service.detect(image)

    if "helmet" in detection_classes:
        # st.error("Helmet detected! ATM is locked")
        audio_service.play_beep()
        
    return frame

def process_camera(source):
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        st.error("Error: Could not open camera.")
        return

    stframe = st.empty()

    while True:
        ret, frame = cap. read()

        if not ret:
            st.error("Error: Could not read frame from camera.")
            break

        processed_frame = process_image(frame)
        stframe.image(processed_frame, channels="BGR")

    cap.release()
    cv2.destroyAllWindows ()

def process_video(source):
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())
    source = tfile.name
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        st.error("Error: Could not open video.")
        return

    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Error: Could not read frame from video.")
            break

        processed_frame = process_image(frame)
        stframe.image(processed_frame, channels="BGR")


    cap.release()
    cv2.destroyAllWindows ()


if input_type == "Image":
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"] )

    if uploaded_file is not None:
        image = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        processed_image = process_image(image)
        st.image(processed_image, caption="Processed Image")

if input_type == "Camera":
    camera_source = st.sidebar.text_input("Camera source (RTSP URL or index Default: 0)", str(DEFAULT_CAMERA) )

    camera_source = int(camera_source) if camera_source.isdigit() else camera_source
    process_camera(camera_source)

if input_type == "Video":
    video_file = st.sidebar.file_uploader("Upload an video", type=["mp4","mov"] )
    if video_file is not None:
        processed_video = process_video(video_file)
        # st.image(processed_video, caption="Processed Video")