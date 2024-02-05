import os
import openai
from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from src.ssl_workaround import no_ssl_verification
from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup, SoupStrainer
from langchain.document_loaders import RecursiveUrlLoader
from langchain.utils.html import (PREFIXES_TO_IGNORE_REGEX,
                                  SUFFIXES_TO_IGNORE_REGEX)
import re
import json

# Config file path
CONFIG_FILE="C:\\Github_Projects\\Experiments\\LLM\\RAG\\Chat_with_PythonSDK\\config.json"

class VectorDB():
    """
        Class represeting vector database
            - fetches documents from IBM Generative AI SDK: https://ibm.github.io/ibm-generative-ai/index.html
            - generates embeddings using Azure OpenAI 
        Usage: 1. init, 2. create_db_from_url OR 2. create_db_from_file (if downloaded previously), 3. get_retriever
    """
    def __init__(self):
        self.CONFIG = self.get_config(CONFIG_FILE)
        self.init()

    def init(self):
        """
            Initialize variables, loads OpenAI secrets, if not loaded previously
        """
        if self.CONFIG['debug']:
            print('─' * 100)
            print('>>> VECTOR DB INIT')

        if not openai.api_key:
            # load secrets from env var
            _ = load_dotenv(find_dotenv(),verbose=self.CONFIG['debug']) # read local .env file

            # for Azure OpenAI
            openai.api_key = os.environ['OPENAI_API_KEY']
            openai.api_base = os.environ['OPENAI_API_BASE']
            openai.api_type= os.environ['OPENAI_API_TYPE']
            openai.api_version = os.environ['OPENAI_API_VERSION']
            if self.CONFIG['debug']:
                print(f' Openai secrets loaded, models: {os.environ["OPENAI_DEPLOYMENT_ID_LLM"]}, {os.environ["OPENAI_DEPLOYMENT_ID_EMBED"]}')
    
    def get_config(self, CONFIG_FILE):
        """
            get config from root folder: config.json file
        """
            
        f = open(CONFIG_FILE)
        config = json.load(f)
            
        f.close()
        return config

    def get_retriever(self):
        return self.retriever
    
    def create_db_from_url(self):
        """
            Create vector database from IBM Generative AI SDK: https://ibm.github.io/ibm-generative-ai/index.html
        """
        # load documents from IBM Generative AI SDK
        raw_docs = self.get_documents_from_url()
        # preprocess documents
        processed_docs = self.preprocess_documents(raw_docs)
        # create vector database
        self.create_vector_db(processed_docs)

    def create_db_from_file(self):
        """
            Create vector database file - see config for path
        """
        # create embeddings for all documents
        embedding=AzureOpenAIEmbeddings(azure_deployment=os.environ['OPENAI_DEPLOYMENT_ID_EMBED'],
                                        max_retries=10)
        # load vectorstore from file
        self.vectorstore = Chroma(
            persist_directory=self.CONFIG['vector_db_path'], 
            embedding_function=embedding)
        if self.CONFIG['debug']:
            print(f'>>> Vectorstore loaded from path: {self.CONFIG["vector_db_path"]}')

        self.retriever = self.vectorstore.as_retriever(
            search_type=self.CONFIG['retriever_search_type'], 
            search_kwargs={"k": self.CONFIG['retriever_num_docs']})

    def create_vector_db(self, processed_docs):
        # create embeddings for all documents
        embedding=AzureOpenAIEmbeddings(azure_deployment=os.environ['OPENAI_DEPLOYMENT_ID_EMBED'],max_retries=10,show_progress_bar=True)
        # create vector database and loads embedded documents
        with no_ssl_verification():
            self.vectorstore = Chroma.from_documents(documents=processed_docs, 
                                                     embedding=embedding, 
                                                     persist_directory=self.CONFIG['vector_db_path'])
        
        self.retriever = self.vectorstore.as_retriever(
            search_type=self.CONFIG['retriever_search_type'], 
            search_kwargs={"k": self.CONFIG['retriever_num_docs']})

        # if self.CONFIG['debug']:
            # retriever test
            # retrieved_docs = self.retriever.get_relevant_documents(
            #     "What are the parameters of Credentials?"
            # )
            # print(f'---Number of documents retrieved: {len(retrieved_docs)}')
            # print(f'---Retrieved docs source: ')
            # for doc in retrieved_docs:
            #     print(f'------Source: {doc.metadata["source"]}')
            # print(f'---Doc 1: {retrieved_docs[0].page_content}')


    def preprocess_documents(self, api_ref):
        # split documents into chunks - this in general improves LLM performance
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=200, add_start_index=True
        )
        all_splits = text_splitter.split_documents(api_ref)

        if self.CONFIG['debug']:
            # test splitter
            print(f'Number of documents created: {len(all_splits)}')
            # print(f'First document length: {len(all_splits[0].page_content)}')
            # print(f'Metadata sample: {all_splits[0].metadata}')

        return all_splits

    def simple_extractor(self, html: str) -> str:
        soup = BeautifulSoup(
            html, 
            "lxml",  
            parse_only = SoupStrainer( 
            'article', role = 'main'))
        return re.sub(r"\n\n+", "\n\n", soup.text).strip()

    def get_documents_from_url(self):
        """
            Get documents from IBM Generative AI SDK: https://ibm.github.io/ibm-generative-ai/index.html
        """
        # load documents from IBM Generative AI SDK
        api_ref = RecursiveUrlLoader(
            self.CONFIG['retriever_URL_to_get'],
            max_depth=self.CONFIG['retriever_URL_scrape_depth'],
            extractor=self.simple_extractor,
            prevent_outside=True,
            use_async=False,
            timeout=600,
            check_response_status=True,
            exclude_dirs=(
                self.CONFIG['retriever_URL_to_exclude']
            ),
            # drop trailing / to avoid duplicate pages.
            link_regex=(
                f"href=[\"']{PREFIXES_TO_IGNORE_REGEX}((?:{SUFFIXES_TO_IGNORE_REGEX}.)*?)"
                r"(?:[\#'\"]|\/[\#'\"])"
            ),
        ).load()

        if self.CONFIG['debug']:
            # test doc loading
            print('Document loading from URL')
            print(f'Nuber of docs loaded: {len(api_ref)}')
            print(f'excluded: {self.CONFIG["retriever_URL_to_exclude"]}')
            # print(f'First doc lenght: {len(api_ref[0].page_content)}')
            # print(f'Sample: {api_ref[1].page_content[:500]}')

        return api_ref