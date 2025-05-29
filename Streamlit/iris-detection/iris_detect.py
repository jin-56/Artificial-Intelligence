import streamlit as st
import pandas as pd
import numpy as np
import joblib
from PIL import Image

# Load model
model = joblib.load("iris_model.pkl")


data = pd.read_csv('iris.csv')

st.title("Iris Flower Species Detection")

x= st.number_input("Enter Sepal Length in cm")
y= st.number_input("Enter Sepal Width in cm")
z= st.number_input("Enter Petal Length in cm")
a= st.number_input("Enter Petal Width in cm")

button = st.button("Predict")

    
if button:
    # Match column names used during training
    input_data = pd.DataFrame({
    "SepalLengthCm": [x],
    "SepalWidthCm": [y],
    "PetalLengthCm": [z],
    "PetalWidthCm": [a]
})

    prediction = model.predict(input_data)[0] #gives string not array cause predicting one sample

    st.subheader(prediction)
    
    # if prediction == "iris-setosa":
    #     st.image("Iris-setosa.jpg")
    # elif prediction == "Iris-versicolor":
    #     st.image("iris-versicolor.jpg")
    # else:
    #     st.image("iris-virginica.jpg")

    # Display corresponding image
    image_path = f"image/{prediction.lower()}.jpg"
    img = Image.open(image_path)
    st.image(img)

st.balloons()
    