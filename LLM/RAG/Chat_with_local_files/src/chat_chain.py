import os
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
import time
import json
# from langchain.schema import StrOutputParser
from langchain.prompts import (ChatPromptTemplate, MessagesPlaceholder,
                               PromptTemplate)
from langchain.schema.runnable import (Runnable, RunnableBranch,
                                       RunnableLambda, RunnableMap)
from typing import Dict, List, Optional, Sequence
from langchain.schema import Document
from operator import itemgetter
from dotenv import load_dotenv, find_dotenv
import langchain
import datetime
import uuid
from src.vector_db import VectorDB
import src.prompts as prompts
from pathlib import Path
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent  # from src/chat_chain.py to v1/
CONFIG_FILE = PROJECT_ROOT / "config.json"

class SDKChat():
    """
        Class represeting a chatbot with following attributes:
            - remembers history of conversation
            - fetches documents local files 
            - generates answer using Google Gemini models
        Usage: xxx
    """
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.CONFIG = self.get_config(CONFIG_FILE)
        self.chain_ready = False
        self.init()
    
    def init(self):
        """
            Initialize variables, loads Gemini secrets
        """
        if self.CONFIG.get('debug', False):
            print('─' * 100)
            print('>>> CHAT INIT')
            print('debug mode on')
            langchain.debug = True

        if self.CONFIG.get('json_logging', False):
            self.message_counter = 0

        _ = load_dotenv(find_dotenv(), verbose=self.CONFIG.get('debug', False))

        if self.CONFIG.get('debug', False):
            print(f'Gemini secrets loaded, model: gemini-2.0-flash')

    def get_config(self, config_file):
        """
        Get config from config.json file and process paths
        """
        with open(config_file) as f:
            config = json.load(f)
        
        # Convert relative paths in config to absolute paths
        self.process_paths(config)
        return config
    
    def process_paths(self, config):
        """
        Convert relative paths in config to absolute paths
        """
        # Process vector_db_path
        if 'vector_db_path' in config:
            config['vector_db_path'] = str(self.project_root / config['vector_db_path'])
            
        # Process transcript_file_path
        if 'transcript_file_path' in config:
            config['transcript_file_path'] = str(self.project_root / config['transcript_file_path'])
            
        # Process local_docs_path if exists
        if 'local_docs_path' in config:
            config['local_docs_path'] = str(self.project_root / config['local_docs_path'])
            
        # Create directories if they don't exist
        for key in ['vector_db_path', 'transcript_file_path', 'local_docs_path']:
            if key in config:
                Path(config[key]).mkdir(parents=True, exist_ok=True)

    def create_chat(self, streaming=False, callbacks=[]):
        """Create chatbot"""
        if self.CONFIG.get('debug', False):
            print('─' * 100)
            print('>>> CREATE CHAT')
            
        # create vector database instance
        vector_db = VectorDB()
        # create vector database instance
        if self.CONFIG.get('vector_db', {}).get('use_offline_vector_db', False):
            vector_db.load_db_from_file()
        elif self.CONFIG.get('vector_db', {}).get('context_source') == 'file':
            print(f'Creating vector DB. This might take a minute...')
            vector_db.create_db_from_local()
        else:
            raise ValueError(f"Unsupported context_source value: {self.CONFIG.get('vector_db', {}).get('context_source')}.")
        retriever = vector_db.get_retriever()

        # create prompt and Gemini instance
        self.create_prompts()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            streaming=streaming,
            callbacks=callbacks
        )

        # 1. Create the question transformation chain
        self.condense_question_chain = (
            PromptTemplate.from_template(self.REPHRASE_TEMPLATE)
            | self.llm
            | StrOutputParser()
        )

        # 2. Create the retrieval chain
        self.retrieval_chain = RunnableLambda(
            lambda x: retriever.get_relevant_documents(x)
        )

        # 3. Create the response generation chain
        self.response_prompt = ChatPromptTemplate.from_messages([
            ("system", self.RESPONSE_TEMPLATE),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ])

        # 4. Combine chains into the final RAG chain
        self.rag_chain = (
            {
                "standalone_question": lambda x: self.condense_question_chain.invoke({
                    "chat_history": x["chat_history"],
                    "question": x["question"]
                }),
                "chat_history": lambda x: x["chat_history"],
                "question": lambda x: x["question"]
            }
            | RunnablePassthrough.assign(
                context=lambda x: self.format_docs(
                    self.retrieval_chain.invoke(x["standalone_question"])
                )
            )
            | self.response_prompt
            | self.llm
            | StrOutputParser()
        )

        self.chain_ready = True
        
        if self.CONFIG.get('json_logging', False):
            self.chat_id = str(uuid.uuid4())

        if self.CONFIG.get('debug', False):
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
        if self.CONFIG.get('debug', False):
            print('─' * 100)
            print('>>> INVOKE CHAT, question: ', input['question'])
        
        chat_history = input['chat_history']
        response = self.rag_chain.invoke({
            "chat_history": chat_history,
            "question": input['question']
        })

        if self.CONFIG.get('json_logging', False):
            self.json_log(input['question'], response)

        return response

    def format_docs(self, docs: Sequence[Document]) -> str:
        """
        Format documents for RAG with citations and links
        This method formats the context that will be sent to the LLM
        """
        formatted_docs = []
        for i, doc in enumerate(docs):
            title = doc.metadata.get('title', 'Untitled')
            url = doc.metadata.get('url', '')
            citation = f"[{i+1}]"  # Numerical citation
            doc_ref = f"{citation} {title} ({url})"
            
            # Format the document with citation
            doc_string = (
                f"<doc citation='{citation}'>\n"
                f"Reference: {doc_ref}\n"
                f"Content:\n{doc.page_content}\n"
                f"</doc>"
            )
            formatted_docs.append(doc_string)
        
        return "\n\n".join(formatted_docs)

    def create_prompts(self):
        """
            Create prompts for chatbot
        """
        self.RESPONSE_TEMPLATE = prompts.RESPONSE_TEMPLATE_V2
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

        json_file = Path(self.CONFIG.get('transcript_file_path', 'transcripts')) / 'chat_log.json'

        json_chats = []

        # save json - create file if it does not exist
        if not json_file.exists():
            json_chats.append(json_log)
            with open(json_file, mode='w') as f:
                f.write(json.dumps(json_chats, indent=2))
        else:
            with open(json_file) as existing_json:
                existing_chats = json.load(existing_json)

            existing_chats.append(json_log)
            with open(json_file, mode='w') as f:
                f.write(json.dumps(existing_chats, indent=2))
