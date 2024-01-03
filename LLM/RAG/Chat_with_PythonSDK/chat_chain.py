import os
import openai
import bs4
import time
from langchain import hub
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.schema import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.prompts import (ChatPromptTemplate, MessagesPlaceholder,
                               PromptTemplate)
from langchain.schema.runnable import (Runnable, RunnableBranch,
                                       RunnableLambda, RunnableMap)
from langchain.schema.runnable  import RunnablePassthrough
from typing import Dict, List, Optional, Sequence
from langchain.schema import Document
from operator import itemgetter
# from ssl_workaround import no_ssl_verification
from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup, SoupStrainer
from langchain.document_loaders import RecursiveUrlLoader, SitemapLoader
from langchain.utils.html import (PREFIXES_TO_IGNORE_REGEX,
                                  SUFFIXES_TO_IGNORE_REGEX)
import langchain
import re

# DEBUG
DEBUG_FILE_PATH = "C:\\Github_Projects\\Experiments\\LLM\\RAG\\transcripts\\"
DEBUG=True

class SDKChat():
    """
        Class represeting a chatbot with following attributes:
            - remembers history of conversation
            - fetches documents from IBM Generative AI SDK: https://ibm.github.io/ibm-generative-ai/index.html
            - generates answer using Azure OpenAI 
        Usage: xxx
    """
    def __init__(self, debug=False):
        self.DEBUG = debug
        self.chain_ready = False
        self.init()
    
    def init(self):
        """
            Initialize variables, loads OpenAI secrets
        """
        # DEBUG
        if self.DEBUG:
            print('------ INIT -------')
            print('--- debug mode on')
            langchain.debug = True

        # load secrets from env var
        _ = load_dotenv(find_dotenv(),verbose=self.DEBUG) # read local .env file

        # for Azure OpenAI
        openai.api_key = os.environ['OPENAI_API_KEY']
        openai.api_base = os.environ['OPENAI_API_BASE']
        openai.api_type= os.environ['OPENAI_API_TYPE']
        openai.api_version = os.environ['OPENAI_API_VERSION']
        if self.DEBUG:
            print(f'--- Openai secrets loaded, models: {os.environ["OPENAI_DEPLOYMENT_ID_LLM"]}, {os.environ["OPENAI_DEPLOYMENT_ID_EMBED"]}')

    def create_chat(self,callbacks=[]):
        """
            Create chatbot
        """
        if self.DEBUG:
            print('------ CREATE CHAT -------')
        # create vector database
        vector_db = VectorDB(debug=self.DEBUG)
        vector_db.create_db_from_url()
        retriever = vector_db.get_retriever()
        self.create_prompts()
        self.llm = AzureChatOpenAI(azure_deployment=os.environ['OPENAI_DEPLOYMENT_ID_LLM'], streaming=True, callbacks=callbacks)

        condense_question_chain = (
            PromptTemplate.from_template(self.REPHRASE_TEMPLATE)
            | self.llm
            | StrOutputParser()
        )

        retriever_chain = condense_question_chain | retriever

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

        self.response_synthesizer_chain = (prompt | self.llm | StrOutputParser())
        self.chain_ready = True
        if self.DEBUG:
            print('--- chat chain created')
    
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
        context = self.context_chain.invoke(input)
        time.sleep(6)
        answer = self.response_synthesizer_chain.invoke(context)

        return answer

    def create_chain_wait(self):
        """
            Workaround - Create chain with wait step to overcome Azure OpenAI limitations
        """
        from langchain_core.runnables import (
            RunnableLambda,
            RunnableParallel,
            RunnablePassthrough,
        )

        def wait(prompt: str) -> str: # wait 1 second
            time.sleep(1)
            return prompt

        chain_wait = RunnableLambda(wait) | {
            'context': itemgetter('context'), # Original LLM output
            'question': itemgetter('question'), # Original LLM output
            'chat_history': itemgetter('chat_history'), # Original LLM output
        }

        # # ERROR - this does not work due to the S0 limit of API call frequency
        self.answer_chain = self.context | chain_wait | self.response_synthesizer_chain



    def format_docs(self, docs: Sequence[Document]) -> str:
        formatted_docs = []
        for i, doc in enumerate(docs):
            doc_string = f"<doc id='{i}'>{doc.page_content}</doc>"
            formatted_docs.append(doc_string)
        return "\n".join(formatted_docs)

    def create_prompts(self):
        """
            Create prompts for chatbot
        """
        self.RESPONSE_TEMPLATE = """\
        You are an expert programmer and problem-solver, tasked with answering any question \
        about IBM generative AI Python SDK.

        Generate a comprehensive and informative answer of 80 words or less for the \
        given question based solely on the provided search results (URL and content). You must \
        only use information from the provided search results. Use an unbiased and \
        journalistic tone. Combine search results together into a coherent answer. Do not \
        repeat text. Cite search results using [${{number}}] notation. Only cite the most \
        relevant results that answer the question accurately. Place these citations at the end \
        of the sentence or paragraph that reference them - do not put them all at the end. If \
        different results refer to different entities within the same name, write separate \
        answers for each entity.

        You should use bullet points in your answer for readability. Put citations where they apply
        rather than putting them all at the end.

        If there is nothing in the context relevant to the question at hand, just say "Hmm, \
        I'm not sure." Don't try to make up an answer.

        Anything between the following `context`  html blocks is retrieved from a knowledge \
        bank, not part of the conversation with the user. 

        <context>
            {context} 
        <context/>

        REMEMBER: If there is no relevant information within the context, just say "Hmm, I'm \
        not sure." Don't try to make up an answer. Anything between the preceding 'context' \
        html blocks is retrieved from a knowledge bank, not part of the conversation with the \
        user.\
        """

        self.REPHRASE_TEMPLATE = """\
        Given the following conversation and a follow up question, rephrase the follow up \
        question to be a standalone question.

        Chat History:
        {chat_history}
        Follow Up Input: {question}
        Standalone Question:"""
        self.CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(self.REPHRASE_TEMPLATE)


class VectorDB():
    """
        Class represeting vector database
            - fetches documents from IBM Generative AI SDK: https://ibm.github.io/ibm-generative-ai/index.html
            - generates embeddings using Azure OpenAI 
        Usage: 1. init, 2. create_db_from_url, 3. get_retriever
    """
    def __init__(self, debug=False):
        self.DEBUG = debug
        self.init()

    def init(self):
        """
            Initialize variables, loads OpenAI secrets, if not loaded previously
        """
        if self.DEBUG:
            print('--- vector db init')

        if not openai.api_key:
            # load secrets from env var
            _ = load_dotenv(find_dotenv(),verbose=self.DEBUG) # read local .env file

            # for Azure OpenAI
            openai.api_key = os.environ['OPENAI_API_KEY']
            openai.api_base = os.environ['OPENAI_API_BASE']
            openai.api_type= os.environ['OPENAI_API_TYPE']
            openai.api_version = os.environ['OPENAI_API_VERSION']
            if self.DEBUG:
                print(f'--- Openai secrets loaded, models: {os.environ["OPENAI_DEPLOYMENT_ID_LLM"]}, {os.environ["OPENAI_DEPLOYMENT_ID_EMBED"]}')
    
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

    def create_vector_db(self, processed_docs):
        # create embeddings for all documents
        embedding=AzureOpenAIEmbeddings(azure_deployment=os.environ['OPENAI_DEPLOYMENT_ID_EMBED'])
        # create vector database and loads embedded documents
        self.vectorstore = Chroma.from_documents(documents=processed_docs, embedding=embedding)
        self.retriever = self.vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 4})
        # TODO: save vectorstore to file

        if self.DEBUG:
            # retriever test
            retrieved_docs = self.retriever.get_relevant_documents(
                "What are the parameters of Credentials?"
            )
            print(f'---Number of documents retrieved: {len(retrieved_docs)}')
            print(f'---Retrieved docs source: ')
            for doc in retrieved_docs:
                print(f'------Source: {doc.metadata["source"]}')
            print(f'---Doc 1: {retrieved_docs[0].page_content}')


    def preprocess_documents(self, api_ref):
        # split documents into chunks - this in general improves LLM performance
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=200, add_start_index=True
        )
        all_splits = text_splitter.split_documents(api_ref)

        if self.DEBUG:
            # test splitter
            print(f'Number of documents created: {len(all_splits)}')
            print(f'First document length: {len(all_splits[0].page_content)}')
            print(f'Metadata sample: {all_splits[0].metadata}')

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
            "https://ibm.github.io/ibm-generative-ai/",
            max_depth=8,
            extractor=self.simple_extractor,
            prevent_outside=True,
            use_async=False,
            timeout=600,
            check_response_status=True,
            exclude_dirs=(
                "https://www.ibm.com/products/watsonx-ai",
                "https://ibm.github.io/ibm-generative-ai/genindex.html",
                "https://ibm.github.io/ibm-generative-ai/py-modindex.html",
                "https://ibm.github.io/ibm-generative-ai/search.html",
            ),
            # drop trailing / to avoid duplicate pages.
            link_regex=(
                f"href=[\"']{PREFIXES_TO_IGNORE_REGEX}((?:{SUFFIXES_TO_IGNORE_REGEX}.)*?)"
                r"(?:[\#'\"]|\/[\#'\"])"
            ),
        ).load()

        if DEBUG:
            # test doc loading
            print('---------Document loading from URL--------------')
            print(f'Nuber of docs loaded: {len(api_ref)}')
            print(f'First doc lenght: {len(api_ref[0].page_content)}')
            print(f'Sample: {api_ref[1].page_content[:500]}')

        return api_ref