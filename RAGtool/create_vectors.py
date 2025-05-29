from pinecone import Pinecone
import fitz 
import google.generativeai as genai

import os
from dotenv import load_dotenv

load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")


def extract_text_from_pdf(pdf_path):
    text =""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text() + "\n"
    return text

model = "models/text-embedding-004"

genai.configure(api_key= gemini_api_key)

def embed_text(text):
    response = genai.embed_content(
        model=model,
        content=text,
        task_type = "retrieval_document"
    )
    return response

pinecone_client = Pinecone(api_key=pinecone_api_key)

vector_index = pinecone_client.Index("student-kb")

def upsert_vectors_to_pinecone(document_text):  
    upsert_data = []
    
    for idx, (file,text) in enumerate(document_text.items()):
        vector = embed_text(text).get ("embedding",[])
        meta_data = {
            "text": text
        }
        upsert_data.append((f"doc-{idx}", vector, meta_data))

    vector_index.upsert(vectors=upsert_data)  # Upsert vectors to Pinecone
    print("Vectors upserted successfully.")



if __name__ == "__main__":
    document_text = {}
    
    for file in os.listdir("documents"):
        text = extract_text_from_pdf("documents/" + file)
        document_text[file] = text
    upsert_vectors_to_pinecone(document_text)
    print("All documents processed and vectors upserted.")
