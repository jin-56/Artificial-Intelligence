'''
Spam and Ham classifier AGENT :
   -use Suitable model from grok
   -Do suitable prompt Engineering
   -Output should be in json format":
   {"email_type": "spam" or "ham",
   "reason": "reason why that email is spam or ham"}'''

import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq



# Set up Streamlit page
st.title("Email Classification")
st.write("Classify your email as Spam or Ham")

#groq client
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# Model selection
models = ["llama3-70b-8192", "llama3-13b-4096", "gemma-7b-it", "qwen-qwen1.5-32b"]
selected_model = st.sidebar.selectbox("Select LLM Model", models, index=0)

# User input
email_input = st.text_input("Paste the email text below:")

if st.button("Classify"):
        prompt = f"""
            You are the best Email classifier Agent. You are an intelligent assistant trained to classify 
            the emails based on their body content. Your task is to determine whether the email is spam or ham. Classify an 
            as spam if it contains unsolicited or irrelevant contents, scams, phishing attempts, nonsense advertisements and 
            other unwanted messages. And, if the email is relevant, have legitimate message, communication, or useful information,
            classify it as ham. Read the full content of the email and tally your classification based on the content of the email
            and the similar document provided. Respond with classification of "spam" or "ham" and provide a reason for your classification.

            Provide your classification in the following JSON format:
            {{
              "email_type": "spam" or "ham",
              
              "reason": "reason why that email is spam or ham"
            }}

            Here is the email to classify:
            {email_input}
        """

        messages = [{"role": "user", "content": prompt}]

        response = client.chat.completions.create(
            model=selected_model,
            messages=messages,
            max_tokens=500,
            temperature=0.2
        )

        response = response.choices[0].message.content
        st.chat_message("assistant").markdown(response)