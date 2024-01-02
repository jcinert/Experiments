import os
import streamlit as st
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
import openai
from dotenv import load_dotenv, find_dotenv

def init():
    _ = load_dotenv(find_dotenv()) # read local .env file
    openai.api_key = os.environ['OPENAI_API_KEY']
    openai.api_base = os.environ['OPENAI_API_BASE']
    openai.api_type= os.environ['OPENAI_API_TYPE']
    openai.api_version = os.environ['OPENAI_API_VERSION']
    print(f'Openai secrets loaded, model: {os.environ["OPENAI_DEPLOYMENT_ID_LLM"]}')


st.set_page_config(page_title="Chat with IBM Generative AI Python SDK", page_icon="🖖")
st.title("🖖 Chat with IBM Generative AI Python SDK")

# Set up memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
memory = ConversationBufferMemory(chat_memory=msgs)
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

view_messages = st.expander("View the message contents in session state")

# Get an OpenAI API Key before continuing
if not openai.api_key:
    init()
    if not openai.api_key:
        st.info("No AzureOpenAI API Key found in .env file. Please add one and re-run this app.")
        st.stop()

# Set up the LLMChain, passing in memory
template = """You are an AI chatbot having a conversation with a human.

{history}
Human: {human_input}
AI: """
prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)
llm_chain = LLMChain(llm=AzureChatOpenAI(azure_deployment=os.environ["OPENAI_DEPLOYMENT_ID_LLM"]), prompt=prompt, memory=memory)

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    # Note: new messages are saved to history automatically by Langchain during run
    response = llm_chain.run(prompt)
    st.chat_message("ai").write(response)

# Draw the messages at the end, so newly generated ones show up immediately
with view_messages:
    """
    Memory initialized with:
    ```python
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    memory = ConversationBufferMemory(chat_memory=msgs)
    ```

    Contents of `st.session_state.langchain_messages`:
    """
    view_messages.json(st.session_state.langchain_messages)