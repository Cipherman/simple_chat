import os
from dotenv import load_dotenv

import streamlit as st
from openai import OpenAI


st.title("Simple Chat")

load_dotenv()
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

client = OpenAI(
    base_url="https://ollama.com/v1",
    api_key=OLLAMA_API_KEY,
)

# Set default model if not already set
if "chat_llm" not in st.session_state:
    st.session_state["chat_llm"] = "gemma3:12b"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
             st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["chat_llm"],
            messages=[
                {"role": msg["role"], "content": msg["content"]}
                for msg in st.session_state["messages"]
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})