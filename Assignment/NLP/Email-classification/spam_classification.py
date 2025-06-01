import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.tokenize import word_tokenize
import re
 
nltk.download('wordnet')
nltk.download('omw-1.4')


#initialize tools 
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Streamlit
st.title("Spam Classification Model ")
st.write("This is a simple spam/ham classification model. Paste your email text below to classify it as spam or ham.")

import pickle
# Load the model from the file
with open('spam-classifier.pkl', 'rb') as file:
    spam_classifier = pickle.load(file)
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
user_input = st.text_input("Enter the mail text for prediction:")

if user_input:
    #preprocess the sample text
    sample_text_cleaned = preprocess(user_input)

    #vectorize
    sample_vector = vectorizer.transform([sample_text_cleaned])

if st.button("Predict"):
    #predict
    predicted_category = spam_classifier.predict(sample_vector)
    st.write("Prediction :", predicted_category[0])