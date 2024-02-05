import streamlit as st
import os
import openai
# from src.ssl_workaround import no_ssl_verification
from dotenv import load_dotenv, find_dotenv
from src.vector_db import VectorDB
from langchain.agents import initialize_agent, Tool
from langchain.chains import RetrievalQA
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

# ------ INIT ------
st.set_page_config(page_title="Chat with IBM Generative AI Python SDK", page_icon="🖖")
st.title("🖖 Chat with IBM Generative AI Python SDK")

@st.cache_resource # run just once
def init():
    _ = load_dotenv(find_dotenv()) # read local .env file
    openai.api_key = os.environ['OPENAI_API_KEY']
    openai.api_base = os.environ['OPENAI_API_BASE']
    openai.api_type= os.environ['OPENAI_API_TYPE']
    openai.api_version = os.environ['OPENAI_API_VERSION']
    print(f'>>> Openai secrets loaded, models: {os.environ["OPENAI_DEPLOYMENT_ID_LLM"]}, {os.environ["OPENAI_DEPLOYMENT_ID_EMBED"]}')

    # ------ load vector DB ------
    vector_db = VectorDB()
    try:
        vector_db.create_db_from_file()
        print(f'>>> Vector DB loaded from file')
    except:
        vector_db.create_db_from_url()
        print(f'>>> Vector DB loaded from url')

    retriever = vector_db.get_retriever()

    # ------ create a chat instance ------
    llm = AzureChatOpenAI(azure_deployment=os.environ['OPENAI_DEPLOYMENT_ID_LLM'],
                        temperature=0, 
                        max_retries=10,
                        streaming=True)
    # ------ retrieval qa chain ------
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )

    # ------ load tools ------
    wrapper = DuckDuckGoSearchAPIWrapper(time="y", max_results=3) # one year search
    search = DuckDuckGoSearchResults(api_wrapper=wrapper)
    tools = [
        Tool(
            name='Knowledge Base',
            func=qa.run,
            description=(
                'First tool to use when answering questions about LLM, LLM apps, generative AI frameworks and python APIs'
            )
        ),
        Tool(
            name='Web Search',
            func=search.run,
            description=(
                'Tool to use for generic questions, mainly for recent events and information.'
            )
        )
    ]

    # ------ Set up memory ------
    msgs = StreamlitChatMessageHistory(key="chat_history")
    memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
    )

    # ------ create agent ------
    agent = initialize_agent(
        agent='chat-conversational-react-description',
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=4,
        early_stopping_method='generate',
        memory=memory,
        handle_parsing_errors=True
    )


    # ------ create custom sys mesage ------
    # steering agent to use the Knowlege base, but not limiting it to answer any question or use web search
    sys_msg = """Assistant is a large language model.
Assistant is designed to be able to assist with a wide range of tasks related to LLMs, machine learning and programming , \
from answering simple questions to providing in-depth explanations, example code and links to documentation. \
As a language model, Assistant is able to generate human-like text based on the input it receives, \
allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
Assistant can use code spippets and URL links.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. \
It is able to process and understand large amounts of text, and can use this knowledge to provide accurate \
and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input \
it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

If the question is related to LLM, LLM apps, generative AI frameworks and python APIs Assistant has to first use the Knowledge Base. \
If no relevant answer is found in the Knowlege Base, Assistant can use Web Search tool to find an answer on the internet. \
If the question is not related to LLMs, machine learning and programming Assistant can use Web Search tool to find an answer on the internet.

"""

    new_prompt = agent.agent.create_prompt(
        system_message=sys_msg,
        tools=tools
    )
    agent.agent.llm_chain.prompt = new_prompt

    print(f'>>> sys. msg: {agent.agent.llm_chain.prompt.messages[0].prompt.template}')
    print(f'>>> INIT complete - agent created')
    return agent, msgs, memory

# ------ MAIN ------
# run init
agent, msgs, memory = init()

if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

# ------ RENDER MESSAGES ------
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# ------ CHAT ------
if prompt := st.chat_input():
    # write prompt to UI
    st.chat_message("user").write(prompt)
    msgs.add_user_message(prompt)

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(input=prompt, callbacks=[st_callback])
        st.write(response)
        print(f'>>> hist: {memory.chat_memory.messages}')

    # write responce to UI
    st.chat_message("ai").write(response)
    msgs.add_ai_message(response)