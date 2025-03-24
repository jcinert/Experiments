import os
from dotenv import load_dotenv, find_dotenv
import openai
from pathlib import Path

# to disable SSL verification that causes problem from my laptop
from src.ssl_workaround import no_ssl_verification

# LangChain imports
from langchain_community.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import (LLMChain, SequentialChain)

# from langchain import LLMChain
# from langchain import PromptTemplate
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# formatters
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

# prompts
import src.prompts as prompts

import langchain
import warnings
import json
import datetime

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent  # from src/rag_qa.py to project root

class RAG_QA():
    """
        Class to QA RAG chat - providing a Dict of question, chat history and answer.
            - evaluates answer completeness - given the question, history and answer            
            - evaluates answer accuracy/correctness - search the answer in vector db and evaluate match
    """
    def __init__(self, config: dict):
        self.project_root = PROJECT_ROOT
        self.config = self.process_paths(config)
        self.DEBUG = config['debug']
        self.DEBUG_FILE_PATH = self.config['qa_debug_file_path']
        self.init()
        # self.load_prompt_examples()
        self.initLangChain()
    
    def process_paths(self, config):
        """
        Convert relative paths in config to absolute paths
        """
        # Create a copy of config to modify
        processed_config = config.copy()
        
        # List of paths to process
        path_keys = [
            'vector_db_path',
            'data_file',
            'qa_output_file',
            'qa_debug_file_path'
        ]
        
        # Convert each path to absolute
        for key in path_keys:
            if key in processed_config:
                processed_config[key] = str(self.project_root / processed_config[key])
                
                # Create parent directories if they don't exist
                Path(processed_config[key]).parent.mkdir(parents=True, exist_ok=True)
        
        return processed_config

    def init(self):
        """
            Initialize variables, loads OpenAI secrets
        """
        # DEBUG
        if self.DEBUG:
            langchain.debug = True
            warnings.filterwarnings("ignore")

        # load secrets from env var
        _ = load_dotenv(find_dotenv(),verbose=self.DEBUG) # read local .env file

        # for Azure OpenAI
        # for Azure OpenAI
        openai.api_key = os.environ['OPENAI_API_KEY']
        openai.api_base = os.environ['OPENAI_API_BASE']
        openai.api_type= os.environ['OPENAI_API_TYPE']
        openai.api_version = os.environ['OPENAI_API_VERSION']
        if self.DEBUG:
            print(f'Openai secrets loaded, models: {os.environ["OPENAI_DEPLOYMENT_ID_LLM"]}, {os.environ["OPENAI_DEPLOYMENT_ID_EMBED"]}')
    
    # def load_prompt_examples(self):
    #     self.QA_EXAMPLE_01 = prompt_examples.QA_EXAMPLE_01
    #     self.QA_EXAMPLE_02 = prompt_examples.QA_EXAMPLE_02

    def initLangChain(self):
        """
            Builds LangChain and prompts to QA a RAG chat
        """
        # ------------------------------------------------------------------------------------------------
        # Chain 1 - evaluate completeness - given the question, history and answer 
        # ------------------------------------------------------------------------------------------------
        
        # build formatting instructions for LLM output
        self.buildFormattingInstructionsQA()
        # DEBUG
        if self.DEBUG:
            print(self.format_instruction_qa)

        # System message
        system_message = prompts.QA_SYSTEM_MSG

        # Make SystemMessagePromptTemplate
        prompt=PromptTemplate(
            template=system_message,
            # input_variables=["fmt_instr_qa","QA_EXAMPLE_01","QA_EXAMPLE_02"]
            input_variables=["fmt_instr_qa"]
        )

        system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

        # User message (input)
        user_message = prompts.USER_RAG_QA_PROMPT
    
        # Make HumanMessagePromptTemplate
        human_message_prompt = HumanMessagePromptTemplate.from_template(user_message)
        # Create ChatPromptTemplate: Combine System + Human
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        
        chain1 = LLMChain(
            llm=AzureChatOpenAI(
                temperature=0.0, 
                azure_deployment = os.environ["OPENAI_DEPLOYMENT_ID_LLM"]),
            prompt = chat_prompt,
            output_key="qa",
            verbose=self.DEBUG
        )

        # ------------------------------------------------------------------------------------------------
        # Overall - generate evaluation (QA) of CCSS assessment 
        # ------------------------------------------------------------------------------------------------
        # not really needed for now, but can be expanded in future
        self.qa_chain = SequentialChain(
            chains=[chain1],
            # input_variables=["assessment","fmt_instr_qa","QA_EXAMPLE_01","QA_EXAMPLE_02"],
            input_variables=["chat_history","prompt","response","fmt_instr_qa"],
            output_variables=["qa"],
            verbose=self.DEBUG
        )

    def buildFormattingInstructionsQA(self):
        """
            Builds output formatting instruction for chain 1
        """
        # Define response schema
        resp_qa_passed = ResponseSchema(name="resp_qa_passed",
                                    description="Boolean value to idicate if the response is anwering the question. true = anwers, false = does not answer")
        resp_qa_reason = ResponseSchema(name="resp_qa_reason",
                                    description="Justification how response is anwering the question")

        
        response_schemas = [resp_qa_passed,resp_qa_reason]
        output_parser_qa = StructuredOutputParser.from_response_schemas(response_schemas)
        
        self.format_instruction_qa = output_parser_qa.get_format_instructions()
        self.output_parser_qa = output_parser_qa
        
    def evaluate_response(self,chat_history:list,question:str,response:str):
        """
            Evaluates (QA) of the responce to the question given history in a RAG chat setting. 
            Parameters:
                chat_history: list of ocjects [HumanMessage, AIMessage]
                    has feld content: str
                question: str
                response: str
            Returns:
                resp_qa_passed: bool - true if response is answering the question
                resp_qa_reason: str - if above is false justification how response isnt anwering the question

        """

        with no_ssl_verification():
            qa_json = self.qa_chain({"chat_history":chat_history,
                                    "prompt":question,
                                    "response":response,
                                    "fmt_instr_qa":self.format_instruction_qa})
                                    # "QA_EXAMPLE_01":self.QA_EXAMPLE_01,
                                    # "QA_EXAMPLE_02":self.QA_EXAMPLE_02})
        
        # # parse the response - TODO error handling
        qa_result = self.format_output(qa_json)

        if self.DEBUG:
            self.json_log(question,response,qa_result['resp_qa_passed'],qa_result['resp_qa_reason'])

        return qa_result
    
    def json_log(self, prompt: str, answer: str, resp_qa_passed: str, resp_qa_reason: str):
        """
            Log prompt, answer and qa result in json format
        """
        # create json log
        json_log = {
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
            "prompt": prompt,
            "answer": answer,
            "resp_qa_passed": resp_qa_passed,
            "resp_qa_reason": resp_qa_reason,
        }

        json_file = self.DEBUG_FILE_PATH
        json_chats = []

        # Create parent directory if it doesn't exist
        Path(json_file).parent.mkdir(parents=True, exist_ok=True)

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

    def format_output(self,qa_json:dict):
        """
            returns subset of fields provided by LangChain
        """

        # sometimes OpenAI returns the JSON and formatter is not needed (TODO: refine prompt)
        if type(qa_json["qa"])!=type(qa_json):
            resp_qa_passed = self.output_parser_qa.parse(qa_json['qa'])['resp_qa_passed']
            resp_qa_reason = self.output_parser_qa.parse(qa_json['qa'])['resp_qa_reason']
        else:
            try:
                resp_qa_passed = qa_json['qa']['resp_qa_passed']
                resp_qa_reason = qa_json['qa']['resp_qa_reason']
            except:
                print('WARNING: QA parsing issues. Rrying to use parser')
                resp_qa_passed = self.output_parser_qa.parse(qa_json['qa'])['resp_qa_passed']
                resp_qa_reason = self.output_parser_qa.parse(qa_json['qa'])['resp_qa_reason']
     

        return {"resp_qa_passed":resp_qa_passed,
                "resp_qa_reason":resp_qa_reason}