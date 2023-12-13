import streamlit as st
from ssl_workaround import no_ssl_verification
import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain


st.title("🦜🔗 Langchain - Next Question Recommender")

# openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

def init():
    _ = load_dotenv(find_dotenv()) # read local .env file
    openai.api_key = os.environ['OPENAI_API_KEY']
    openai.api_base = os.environ['OPENAI_API_BASE']
    openai.api_type= os.environ['OPENAI_API_TYPE']
    openai.api_version = os.environ['OPENAI_API_VERSION']

def recommend_next(question):
    # # Instantiate LLM model
    # llm = OpenAI(model_name="text-davinci-003", openai_api_key=openai_api_key)
    # # Prompt
    # template = "As an experienced data scientist and technical writer, generate an outline for a blog about {topic}."
    # prompt = PromptTemplate(input_variables=["topic"], template=template)
    # prompt_query = prompt.format(topic=topic)
    # # Run LLM model
    # response = llm(prompt_query)
    # # Print results
    
    #Option 1 Without history
    template = """You are a helpful assistant in predicting next question based on current question. 
                    You always provide predicted question on new line"""
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain = LLMChain(
        llm=ChatOpenAI(
            deployment_id=os.environ['OPENAI_DEPLOYMENT_ID'],
            temperature=1),
        prompt=chat_prompt,
        verbose=True
    )

    with no_ssl_verification():
        response = chain.run(question)

    return st.info(response)


with st.form("myform"):
    init()
    topic_text = st.text_input("Enter prompt:", "")
    submitted = st.form_submit_button("Submit")
    if not openai.api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        recommend_next(topic_text)