import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.runnables import RunnablePassthrough
import langchain
import warnings
import json
import datetime
import src.prompts as prompts

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "evaluate" / "config_qa.json"

class RAG_QA():
    """
        Class to QA RAG chat - providing a Dict of question, chat history and answer.
            - evaluates answer completeness - given the question, history and answer            
            - evaluates answer accuracy/correctness - search the answer in vector db and evaluate match
    """
    def __init__(self, config:dict):
        self.DEBUG = config['debug']
        self.project_root = PROJECT_ROOT
        self.process_paths(config)
        self.init()
        self.init_langchain()
    
    def process_paths(self, config):
        """Convert relative paths in config to absolute paths"""
        path_keys = [
            'vector_db_path',
            'qa_debug_file_path'
        ]
        
        for key in path_keys:
            if key in config:
                config[key] = str(self.project_root / config[key])
                Path(config[key]).parent.mkdir(parents=True, exist_ok=True)
                
        self.DEBUG_FILE_PATH = config.get('qa_debug_file_path')

    def init(self):
        """
            Initialize variables, loads Gemini secrets
        """
        # DEBUG
        if self.DEBUG:
            langchain.debug = True
            warnings.filterwarnings("ignore")

        # load secrets from env var
        _ = load_dotenv(find_dotenv(),verbose=self.DEBUG) # read local .env file

        # Initialize Gemini if not already configured
        # if not genai._configured:
        #     genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        if self.DEBUG:
            print('Gemini secrets loaded for QA')
    
    def init_langchain(self):
        """
            Builds LangChain and prompts to QA a RAG chat
        """
        # ------------------------------------------------------------------------------------------------
        # Chain 1 - evaluate completeness - given the question, history and answer 
        # ------------------------------------------------------------------------------------------------
        
        # build formatting instructions for LLM output
        self.build_formatting_instructions_qa()
        # DEBUG
        if self.DEBUG:
            print(self.format_instruction_qa)

        # System message
        system_template = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=prompts.QA_SYSTEM_MSG,
                input_variables=["fmt_instr_qa"]
            )
        )

        # User message (input)
        human_template = HumanMessagePromptTemplate.from_template(prompts.USER_RAG_QA_PROMPT)
        
        # Create ChatPromptTemplate: Combine System + Human
        chat_prompt = ChatPromptTemplate.from_messages([
            system_template,
            human_template
        ])
        
        # Create the LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.0
        )

        # ------------------------------------------------------------------------------------------------
        # Overall - generate evaluation (QA) of CCSS assessment 
        # ------------------------------------------------------------------------------------------------
        # not really needed for now, but can be expanded in future
        self.qa_chain = (
            {
                "chat_history": RunnablePassthrough(),
                "prompt": RunnablePassthrough(),
                "response": RunnablePassthrough(),
                "fmt_instr_qa": lambda _: self.format_instruction_qa
            }
            | chat_prompt
            | self.llm
            | self.parse_output
        )

    def build_formatting_instructions_qa(self):
        """
            Builds output formatting instruction for chain 1
        """
        # Define response schema
        response_schemas = [
            ResponseSchema(
                name="resp_qa_passed",
                description="Boolean value to indicate if the response is answering the question. true = answers, false = does not answer"
            ),
            ResponseSchema(
                name="resp_qa_reason",
                description="Justification how response is answering the question"
            )
        ]
        
        self.output_parser_qa = StructuredOutputParser.from_response_schemas(response_schemas)
        self.format_instruction_qa = self.output_parser_qa.get_format_instructions()

    def parse_output(self, output):
        """Parse the LLM output into structured format"""
        try:
            if isinstance(output.content, dict):
                return output.content
            return self.output_parser_qa.parse(output.content)
        except Exception as e:
            if self.DEBUG:
                print(f"Warning: Error parsing output: {e}")
            return {
                "resp_qa_passed": False,
                "resp_qa_reason": "Error parsing LLM response"
            }

    def evaluate_response(self, chat_history:list, question:str, response:str):
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
        result = self.qa_chain.invoke({
            "chat_history": chat_history,
            "prompt": question,
            "response": response
        })

        if self.DEBUG:
            self.json_log(question, response, result['resp_qa_passed'], result['resp_qa_reason'])

        return result
    
    def json_log(self, prompt: str, answer: str, resp_qa_passed: str, resp_qa_reason: str):
        """Log prompt, answer and qa result in json format"""
        json_log = {
            "timestamp": datetime.datetime.now().isoformat(),
            "prompt": prompt,
            "answer": answer,
            "resp_qa_passed": resp_qa_passed,
            "resp_qa_reason": resp_qa_reason,
        }

        json_file = Path(self.DEBUG_FILE_PATH)
        existing_chats = []

        # Ensure directory exists
        json_file.parent.mkdir(parents=True, exist_ok=True)

        if json_file.exists():
            with open(json_file) as f:
                existing_chats = json.load(f)
        
        existing_chats.append(json_log)
        with open(json_file, 'w') as f:
            json.dump(existing_chats, f, indent=2)