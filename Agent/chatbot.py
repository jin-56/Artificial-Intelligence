import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

from langchain_groq import ChatGroq
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent


# setting page configuration
st.set_page_config(page_title="Chatbot", layout="centered")
st.title("Chatbot")
st.sidebar.title("Chatbot Settings")

# API key load from .env file
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

#toggle button
search_tool = st.toggle("Enable Web Search", value=True)

# Choose tools based on toggle
if search_tool:
    tools = [search_tool]
else:
    tools = []


groq_llm = ChatGroq(
    api_key=groq_api_key,
    model="llama3-70b-8192",
    temperature=1.5,
    max_tokens=500
)
# web search tool
search = SerpAPIWrapper(serpapi_api_key=SERPAPI_KEY)

search_tool = Tool(
    name="Web Search",
    func=search.run,
    description="Searches the web for the latest information.",
    handle_parsing_errors=True
)


memory = ConversationBufferMemory(memory_key="history")

agent = initialize_agent(
    tools=tools,
    llm=groq_llm,
    memory=memory,
    verbose=True
)
# Groq client initialization    
client = Groq(api_key=groq_api_key)

# user can select the models 
models = ["llama3-70b-8192", "llama3-13b-4096", "gemma-7b-it", "qwen-qwen1.5-32b"]
selected_model = st.sidebar.selectbox("Select Model", models)

# system prompt
system_prompt = {
    "role": "system",
    "content": (
        "You are Chatbot, a friendly and intelligent assistant who can understand English and Nepali. "
        "Begin your replies with 'AI: Sure! I can help you with that.'"
    )
}

# saving chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [system_prompt]
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# Display previous messages
for msg in st.session_state.chat_history[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# user_input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Show user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    response = client.chat.completions.create(
            model=selected_model,
            messages=st.session_state.chat_history,
            max_tokens=500,
            temperature=1.2
        )
    ai_response = response.choices[0].message.content

    # Show AI response
    st.chat_message("assistant").markdown(ai_response)

    # Save to session state
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    st.session_state.chat_log.append({"query": user_input, "response": ai_response})



