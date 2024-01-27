from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
import streamlit as st
import openai, os
from langchain.chat_models import  AzureChatOpenAI
from dotenv import load_dotenv, find_dotenv

# ------ INIT ------
@st.cache_resource
def init():
    _ = load_dotenv(find_dotenv()) # read local .env file
    openai.api_key = os.environ['OPENAI_API_KEY']
    openai.api_base = os.environ['OPENAI_API_BASE']
    openai.api_type= os.environ['OPENAI_API_TYPE']
    openai.api_version = os.environ['OPENAI_API_VERSION']
    print(f'Openai secrets loaded, models: {os.environ["OPENAI_DEPLOYMENT_ID_LLM"]}, {os.environ["OPENAI_DEPLOYMENT_ID_EMBED"]}')
init()

llm = AzureChatOpenAI(azure_deployment=os.environ['OPENAI_DEPLOYMENT_ID_LLM'],
                      temperature=0, 
                      streaming=True)
tools = load_tools(["ddg-search"])
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True
)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(prompt, callbacks=[st_callback])
        st.write(response)