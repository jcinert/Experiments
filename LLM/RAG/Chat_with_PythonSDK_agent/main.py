import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
import openai, os
from langchain.chat_models import  AzureChatOpenAI
from dotenv import load_dotenv, find_dotenv

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

    # create a chat instance
    # TODO 
    return msgs

msgs = init()

if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

# ------ GEN AI ------
llm = AzureChatOpenAI(azure_deployment=os.environ['OPENAI_DEPLOYMENT_ID_LLM'],
                      temperature=0, 
                      streaming=True)
tools = load_tools(["ddg-search"])
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True
)

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