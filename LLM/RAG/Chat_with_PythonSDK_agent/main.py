import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
import openai, os
from langchain.chat_models import  AzureChatOpenAI
from dotenv import load_dotenv, find_dotenv

import os
import openai
import bs4
from langchain import hub
from langchain.chat_models import  AzureChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.schema import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
# from langchain_core.runnables import RunnablePassthrough
from langchain.schema.runnable  import RunnablePassthrough
from ssl_workaround import no_ssl_verification
from dotenv import load_dotenv, find_dotenv
from src.vector_db import VectorDB

# ------ INIT ------
st.set_page_config(page_title="Chat with IBM Generative AI Python SDK", page_icon="🖖")
st.title("🖖 Chat with IBM Generative AI Python SDK")

@st.cache_resource
def init():
    _ = load_dotenv(find_dotenv()) # read local .env file
    openai.api_key = os.environ['OPENAI_API_KEY']
    openai.api_base = os.environ['OPENAI_API_BASE']
    openai.api_type= os.environ['OPENAI_API_TYPE']
    openai.api_version = os.environ['OPENAI_API_VERSION']
    print(f'Openai secrets loaded, models: {os.environ["OPENAI_DEPLOYMENT_ID_LLM"]}, {os.environ["OPENAI_DEPLOYMENT_ID_EMBED"]}')

    # Set up memory
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    memory = ConversationBufferMemory(chat_memory=msgs)

    # load vector DB
    vector_db = VectorDB()
    vector_db.create_db_from_file()
    retriever = vector_db.get_retriever()
    # retriever test
    retrieved_docs = retriever.get_relevant_documents(
        "What are parameters of class Credentials?"
    )
    print(f'---Number of documents retrieved: {len(retrieved_docs)}')
    print(f'---Doc 0 length: {len(retrieved_docs[0].page_content)}')
    print(f'---Doc 0: {retrieved_docs[0].page_content}')
    print(f'---Doc 1 length: {len(retrieved_docs[1].page_content)}')
    print(f'---Doc 1: {retrieved_docs[1].page_content}')

    # create a chat instance
    llm = AzureChatOpenAI(azure_deployment=os.environ['OPENAI_DEPLOYMENT_ID_LLM'],
                        temperature=0, 
                        streaming=True)
    tools = load_tools(["ddg-search"])
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True
    )
    return agent, msgs

agent, msgs = init()

if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

# ------ RENDER MESSAGES ------
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# ------ CHAT ------
if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    msgs.add_user_message(prompt)

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        st.write(response)

    # st.chat_message("ai").write(response)
    msgs.add_ai_message(response)
    print(msgs.messages)