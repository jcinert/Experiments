import os
import openai
import time
import json
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import StrOutputParser
from langchain.prompts import (ChatPromptTemplate, MessagesPlaceholder,
                               PromptTemplate)
from langchain.schema.runnable import (Runnable, RunnableBranch,
                                       RunnableLambda, RunnableMap)
from typing import Dict, List, Optional, Sequence
from langchain.schema import Document
from operator import itemgetter
from src.ssl_workaround import no_ssl_verification
from dotenv import load_dotenv, find_dotenv
import langchain
import datetime
import uuid
from src.vector_db import VectorDB
import src.prompts as prompts

# Config file path
CONFIG_FILE="C:\\Github_Projects\\Experiments\\LLM\\RAG\\Chat_with_PythonSDK\\config.json"

class SDKChat():
    """
        Class represeting a chatbot with following attributes:
            - remembers history of conversation
            - fetches documents from IBM Generative AI SDK: https://ibm.github.io/ibm-generative-ai/index.html
            - generates answer using Azure OpenAI 
        Usage: xxx
    """
    def __init__(self):
        self.CONFIG = self.get_config(CONFIG_FILE)
        self.chain_ready = False
        self.init()
    
    def init(self):
        """
            Initialize variables, loads OpenAI secrets
        """
        # DEBUG
        if self.CONFIG['debug']:
            print('─' * 100)
            print('>>> CHAT INIT')
            print('debug mode on')
            langchain.debug = True

        if self.CONFIG['json_logging']:
            self.message_counter = 0

        # load secrets from env var
        _ = load_dotenv(find_dotenv(),verbose=self.CONFIG['debug']) # read local .env file

        # for Azure OpenAI
        openai.api_key = os.environ['OPENAI_API_KEY']
        openai.api_base = os.environ['OPENAI_API_BASE']
        openai.api_type= os.environ['OPENAI_API_TYPE']
        openai.api_version = os.environ['OPENAI_API_VERSION']
        if self.CONFIG['debug']:
            print(f'Openai secrets loaded, models: {os.environ["OPENAI_DEPLOYMENT_ID_LLM"]}, {os.environ["OPENAI_DEPLOYMENT_ID_EMBED"]}')

    def get_config(self, CONFIG_FILE):
        """
            get config from root folder: config.json file
        """
            
        f = open(CONFIG_FILE)
        config = json.load(f)
            
        f.close()
        return config

    def create_chat(self,streaming=False,callbacks=[]):
        """
            Create chatbot
        """
        if self.CONFIG['debug']:
            print('─' * 100)
            print('>>> CREATE CHAT')
        # create vector database instance
        vector_db = VectorDB()
        # download IBM Generative AI SDK from web embed into vector database
        if self.CONFIG['use_offline_vector_db']:
            vector_db.create_db_from_file()
        else:
            vector_db.create_db_from_url()
        retriever = vector_db.get_retriever()

        # crate prompt and Azure OpenAI instance
        self.create_prompts()
        self.llm = AzureChatOpenAI(azure_deployment=os.environ['OPENAI_DEPLOYMENT_ID_LLM'], streaming=streaming, callbacks=callbacks)

        # RAG Langchains
        # 1. rephrase user question given chat history - to handle retrival
        condense_question_chain = (
            PromptTemplate.from_template(self.REPHRASE_TEMPLATE)
            | self.llm
            | StrOutputParser()
        )

        # 2. Retriever chain - documents from vector database
        retriever_chain = condense_question_chain | retriever

        # 3. Parallel chain - retriever and passthrough of the user question and history
        self.context_chain = RunnableMap(
            {
                "context": retriever_chain | self.format_docs,
                "question": itemgetter("question"),
                "chat_history": itemgetter("chat_history"),
            }
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.RESPONSE_TEMPLATE),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )

        # 4. Response synthesizer chain - chain to combine context and question + history
        self.response_synthesizer_chain = (prompt | self.llm | StrOutputParser())
        
        # 5. Wait chain - Create chain with wait step to overcome Azure OpenAI S0 tier limit of API call frequency
        chain_wait = self.create_chain_wait()

        # 6. Overall chain
        self.answer_chain = self.context_chain | chain_wait | self.response_synthesizer_chain
        self.chain_ready = True

        if self.CONFIG['json_logging']:
            self.chat_id = str(uuid.uuid4())

        if self.CONFIG['debug']:
            print('>>> RAG Chat chain created')
    
    def chat_ready(self):
        """
            Check if chatbot is ready
        """
        return self.chain_ready

    def invoke(self, input: Dict) -> str:
        """
            Invoke chatbot with a prompt
            input: Dict with following keys:
                - chat_history: list of messages
                - question: question to be answered
        """
        if self.CONFIG['debug']:
            print('─' * 100)
            print('>>> INVOKE CHAT, question: ', input['question'])
        # # OPTION 1 - two steps RAG
        # context = self.context_chain.invoke(input)
        # time.sleep(6) # wait for 6 seconds to avoid Azure OpenAI S0 limit of API call frequency
        # answer = self.response_synthesizer_chain.invoke(context)

        # OPTION 2 - one step RAG wit wait chain
        with no_ssl_verification():
            answer = self.answer_chain.invoke(input)

        if self.CONFIG['json_logging']:
            self.json_log(input['question'], answer)

        return answer

    def create_chain_wait(self):
        """
            Workaround - Create chain with wait step to overcome Azure OpenAI S0 tier API call frequency limitation
            the limit is 1 call per 10 seconds
        """
        from langchain_core.runnables import (
            RunnableLambda,
        )

        def wait(prompt: str) -> str: # wait 10 sec
            time.sleep(10)
            return prompt

        chain_wait = RunnableLambda(wait) | {
            'context': itemgetter('context'), # Original LLM output
            'question': itemgetter('question'), # Original LLM output
            'chat_history': itemgetter('chat_history'), # Original LLM output
        }

        return chain_wait

    def format_docs(self, docs: Sequence[Document]) -> str:
        formatted_docs = []
        for i, doc in enumerate(docs):
            doc_string = f"<doc id='{i}' source='{doc.metadata['source']}'>{doc.page_content}</doc>"
            formatted_docs.append(doc_string)
        return "\n".join(formatted_docs)

    def create_prompts(self):
        """
            Create prompts for chatbot
        """
        self.RESPONSE_TEMPLATE = prompts.RESPONSE_TEMPLATE
        self.REPHRASE_TEMPLATE = prompts.REPHRASE_TEMPLATE
        self.CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(self.REPHRASE_TEMPLATE)

    def json_log(self, prompt: str, answer: str):
        """
            Log prompt and answer in json format
        """

        self.message_counter += 1

        # create json log
        json_log = {
            "chat_id": self.chat_id,
            "message_id": self.message_counter,
            "prompt": prompt,
            "answer": answer,
            "timestamp": datetime.datetime.now().isoformat(),
        }

        json_file = self.CONFIG['transcript_file_path'] + 'chat_log.json'

        json_chats = []

        # save json - create file if it does not exist
        if not os.path.isfile(json_file):
            json_chats.append(json_log)
            with open(json_file, mode='w') as f:
                f.write(json.dumps(json_chats, indent=2))
        else:
            with open(json_file) as existing_json:
                existing_chats = json.load(existing_json)

            existing_chats.append(json_log)
            with open(json_file, mode='w') as f:
                f.write(json.dumps(existing_chats, indent=2))
