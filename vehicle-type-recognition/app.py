import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# Class name order as in dataset
CLASS_NAMES = ['Bus', 'Car', 'Truck', 'Motorcycle']

# Load the model with caching
@st.cache_resource
def load_vehicle_model():
    return load_model("model.h5")

model = load_vehicle_model()

# Streamlit UI
st.title("Vehicle Type Classifier")
st.markdown("Upload an image of a vehicle to classify it into (Car, Truck, Bus, or Motorcycle).")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess image for MobileNet
    img_resized = image.resize((224, 224)) 
    img_array = np.array(img_resized).astype("float32")
    img_batch = np.expand_dims(img_array, axis=0)
    img_preprocessed = img_batch

    prediction = model.predict(img_preprocessed)
    predicted_class = CLASS_NAMES[np.argmax(prediction)]
    confidence = np.max(prediction)

    # Show results
    st.markdown(f"Prediction: {predicted_class}")
    st.markdown(f"Confidence: {confidence:.2f}")
