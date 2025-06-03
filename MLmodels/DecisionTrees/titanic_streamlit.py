import streamlit as st


import pickle
with open('titanic_dataset.pkl', 'rb') as file:
    rf = pickle.load(file)
    
st.title("Titanic Survival Prediction")
st.write("This is sample model for Titanic Survival Prediction using Decision Trees.")

a=st.number_input("Enter the class of the passanger(1, 2, or 3):")
b=st.number_input("Enter the gender (0 for female, 1 for male):")
c=st.number_input("Enter the age of the passanger:")
d=st.number_input("Enter the number of siblings or spouses :")
e=st.number_input("Enter the number of parents or children :")
f=st.number_input("Enter the fare paid:")

button = st.button("Predict")

if button:
    input_data = [[a, b, c, d, e, f]]
    prediction = rf.predict(input_data)[0]  
    if prediction == 1:
        st.subheader("Titanic Drowned but the passenger survived.")
    else:
        st.subheader("Titanic Drowned so did that passenger.")

