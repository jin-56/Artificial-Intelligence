'''
Logic:

user input height : feet
user input weight : kg

bmi formula: bmi = weight / ((height/3.28)**2

obesity levels:
 
    bmi < 16: Extremely Underweight  --> Error
    16 <= bmi < 18.5: Underweight  --> Warning
    18.5 <= bmi < 25: Healthy  --> Success
    25 <= bmi < 30: Overweight --> Info
    bmi >= 30: Extremely Overweight --> Error
    
'''
import streamlit as st

st.title("This is BMI Calculator")

st.subheader("Please enter your weight in kgs and height in feet")

weight = st.number_input("Enter your weight in kgs")
height = st.number_input("Enter your height in feet")

calculate_button = st.button("Calculate BMI")
if calculate_button:
    if weight and height:
        st.success("BMI calculation:")
        bmi = weight / ((height/3.28)**2)
        st.success(f"Your BMI is: {bmi}")
        if bmi < 16:
            st.error("Extremely Underweight")
        elif 16 <= bmi < 18.5:
            st.warning("Underweight")
        elif 18.5 <= bmi < 25:
            st.success("Healthy")
        elif 25 <= bmi < 30:
            st.info("Overweight")
        else:
            st.error("Extremely Overweight")
    else:
        st.error("Please enter both weight and height.")
