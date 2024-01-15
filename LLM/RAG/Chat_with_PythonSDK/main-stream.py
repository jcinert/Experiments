from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
import streamlit as st
# from ssl_workaround import no_ssl_verification
import os
import openai
from LLM.RAG.Chat_with_PythonSDK.src.chat_chain import SDKChat
# from dotenv import load_dotenv, find_dotenv

st.set_page_config(page_title="Chat with IBM Generative AI Python SDK", page_icon="🖖")
st.title("🖖 Chat with IBM Generative AI Python SDK")

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

# def init():
#     _ = load_dotenv(find_dotenv()) # read local .env file
#     openai.api_key = os.environ['OPENAI_API_KEY']
#     openai.api_base = os.environ['OPENAI_API_BASE']
#     openai.api_type= os.environ['OPENAI_API_TYPE']
#     openai.api_version = os.environ['OPENAI_API_VERSION']
#     print(f'Openai secrets loaded, model: {os.environ["OPENAI_DEPLOYMENT_ID_LLM"]}')

@st.cache_resource
def create_chat():
    return SDKChat(debug=True)
     
sdk_chat = create_chat()

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        if not sdk_chat.chat_ready():
            sdk_chat.create_chat(streaming=True, callbacks=[stream_handler])
            print("--- chat chain created")

        response = sdk_chat.invoke({'chat_history': st.session_state.messages, 'question': prompt})
        st.session_state.messages.append(ChatMessage(role="assistant", content=response))
