from pinecone import Pinecone
from create_vectors import embed_text
from groq import Groq
import streamlit as st


import os
from dotenv import load_dotenv

load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

groq_client = Groq(api_key=groq_api_key)
pinecone_client = Pinecone(api_key=pinecone_api_key)
vector_index = pinecone_client.Index("student-kb")

st.title("RAG app")

query = st.text_input("Enter your question about student:")

if query:
    vector = embed_text(query).get("embedding", [])
    response = vector_index.query(vector= vector, top_k= 1, include_metadata= True)
    
    similar_document = ""
    for match in response["matches"]:
        text = match["metadata"]["text"]
        similar_document += text + "\n"
    print("Similar document:", similar_document)

    prompt = [
        {
            "role": "user",
            "content": f"""You are provided with some document sample which is expected to be most similar document which can be used to answer the user query. 
            If you find something relevant in the similar document use them as a text to answer the user query if the question is not about the documnet, 
            as a helpful assistant you should provide releant answer based on your knowledge and don't share anything related to document, just simply anwer the question.
            
            Similar document: {similar_document}
            User query : {query}
            Give me answer in following format:
            {{
                "answer": String // provide your answer here
            }}
            for example:
            User query: "What is the capital of Nepal?"
            AI: Kathmandu is capital of Nepal"
            """
        }
    ]
    
    print("Prompt:", prompt)
    llm_response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=prompt,
        temperature=0.7,
        max_tokens = 500
    )
    
    
    llm_answer = llm_response.choices[0].message.content
    st.write("Answer:", llm_answer)