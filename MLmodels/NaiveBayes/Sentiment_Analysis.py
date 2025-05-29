import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.tokenize import word_tokenize
import re
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

#initialize tools 
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

st.title("Financial Sentiment Model ")
st.write("This is a simple Naive Bayes model for prediction of financial sentiment.")

import pickle
# Load the model from the file
with open('senti_model.pkl', 'rb') as file:
    senti_model = pickle.load(file)
with open('vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)
    

def preprocess(text):
    #lowercase
    text = text.lower()
    #remove punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    #tokenize
    tokens = word_tokenize(text)
    #remove stopwords
    cleaned = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return ' '.join(cleaned)

#input from user
user_input = st.text_input("Enter Financial text for prediction:")

if user_input:
    #preprocess the sample text
    sample_text_cleaned = preprocess(user_input)

    #vectorize
    sample_vector = vectorizer.transform([sample_text_cleaned])
    
#     #predict
# predicted_category = senti_model.predict(sample_vector)
# print("Predicted Category :", predicted_category[0])

if st.button("Predict"):
    #predict
    predicted_category = senti_model.predict(sample_vector)
    st.write("Prediction :", predicted_category[0])