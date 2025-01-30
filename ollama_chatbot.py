import streamlit as st
import os
import ollama
from config import Config
from helpers.llm_helper import chat, stream_parser

st.set_page_config(
    page_title=Config.PAGE_TITLE,
    initial_sidebar_state="expanded"
)

st.title(Config.PAGE_TITLE)

import httpx

def test_ollama_connection():
    try:
        with httpx.Client(timeout=60.0) as client:  # Set a longer timeout
            response = client.post(
                "http://172.205.182.197:11434/api/generate",
                json={"model": "codellama:7b", "prompt": "Hello!"}
            )
        st.write(response.json())  # Print response if successful
    except httpx.ReadTimeout:
        st.write("❌ Ollama is taking too long to respond!")
    except httpx.ConnectError:
        st.write("❌ Cannot connect to Ollama!")

test_ollama_connection()

os.environ['OLLAMA_HOST'] = 'http://172.205.182.197:11434'
st.write("OLLAMA_HOST:", os.getenv("OLLAMA_HOST"))

def testchat(user_prompt, model):
    stream = ollama.chat(
        model=model,
        messages=[
            {'role': 'assistant', 'content': "System prompt here"},
            {'role': 'user', 'content': f"Model being used is {model}.{user_prompt}"}
        ],
        stream=True,
    )
    return stream

#st.write(testchat('Hello','codellama:7b'))

# sets up sidebar nav widgets
with st.sidebar:   
    st.markdown("# Chat Options")
    
    # widget - https://docs.streamlit.io/library/api-reference/widgets/st.selectbox
    model = st.selectbox('What model would you like to use?', Config.OLLAMA_MODELS)

# checks for existing messages in session state
# https://docs.streamlit.io/library/api-reference/session-state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from session state
# https://docs.streamlit.io/library/api-reference/chat/st.chat_message
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("What would you like to ask?"):
    # Display user prompt in chat message widget
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # adds user's prompt to session state
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.spinner('Generating response...'):
        # retrieves response from model
        llm_stream = chat(user_prompt, model=model)

        # streams the response back to the screen
        stream_output = st.write_stream(stream_parser(llm_stream))

        # appends response to the message list
        st.session_state.messages.append({"role": "assistant", "content": stream_output})
