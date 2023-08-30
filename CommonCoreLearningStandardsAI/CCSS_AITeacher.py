import os
from dotenv import load_dotenv, find_dotenv

# to disable SSL verification that causes problem from my laptop
from ssl_workaround import no_ssl_verification

# LangChain imports
from langchain.chat_models import ChatOpenAI
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
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
# formatters
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

# prompts
import prompt_examples

# DEBUG
DEBUG_FILE_PATH = "C:\\Github_Projects\\Experiments\\CommonCoreLearningStandardsAI\\transcripts\\"
import langchain
import warnings
import json
import datetime


class AITeacher():
    """
        Class to evaluate the answer to Common Core State Standard assessment consisting of:
            - context paragraph
            - free response question
            - rubrics to evaluate answer
            - answer
        Intended use is to provide a student (AIStudent) evaluation of the aswer
    """
    def __init__(self, debug=False):
        
        self.DEBUG = debug

        self.init()
        # self.load_prompt_examples()
        self.initLangChain()
    
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
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
        self.OPENAI_API_TYPE= os.getenv("OPENAI_API_TYPE")
        self.OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
        self.OPENAI_DEPLOYMENT_ID = os.getenv("OPENAI_DEPLOYMENT_ID")
    
    def initLangChain(self):
        """
            Builds LangChain and prompts to respond to CCSS assessment
        """
        # ------------------------------------------------------------------------------------------------
        # Chain 1 - generate answer to CCSS assessment
        # ------------------------------------------------------------------------------------------------
        
        self.buildFormattingInstructionsEval()
        # DEBUG
        if self.DEBUG:
            print(self.format_instruction_eval)

        # System message
        system_message = """
        You are a teacher evaluating students answer to the Common Core State Standard assessment. \
        The assessment consists of: context, free response question (FRQ) and rubric. \
        You need to understand the CONTEXT, FRQ and RUBRIC. \
        You need to evaluate the ANSWER using the RUBRIC \
        Work in this order: 
        1. Evaluate ANSWER using the RUBRIC. Evaluate the ANSWER by each RUBRIC section.
        2. Ensure the ANSWER is related to FRQ and CONTEXT as expected by RUBRIC
        3. Output what is the written evaluation feedback to student. Include what was good and what needs an improvement. Write in a posive helpful tone.
        4. Output total achieved score. only output a single integer number
        5. Output maximum possible score. The total score is sometimes mentioned below the rubric table or you can calculate it summing up maximum points from each section.

        {fmt_instr_eval}
        """

        # Make SystemMessagePromptTemplate
        prompt=PromptTemplate(
            template=system_message,
            input_variables=["fmt_instr_eval"]
        )

        system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

        # User message (input)
        CCSS_EVAL = """
        Standard: {standard} 
        Context: {context} 
        Free responce question (FRQ): {frq}
        Answer: {answer}
        Rubric: {rubric}"""
        # Make HumanMessagePromptTemplate
        human_message_prompt = HumanMessagePromptTemplate.from_template(CCSS_EVAL)
        # Create ChatPromptTemplate: Combine System + Human
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain1 = LLMChain(
            llm=ChatOpenAI(
                temperature=0.7, 
                openai_api_base = self.OPENAI_API_BASE,
                openai_api_key = self.OPENAI_API_KEY,
                deployment_id = self.OPENAI_DEPLOYMENT_ID),
            prompt = chat_prompt,
            output_key="eval",
            verbose=self.DEBUG
        )

        # ------------------------------------------------------------------------------------------------
        # Overall - generate evaluation of CCSS assessment answer
        # ------------------------------------------------------------------------------------------------
        # not really needed for now, but can be expanded in future
        self.evaluate_chain = SequentialChain(
            chains=[chain1],
            input_variables=["standard","answer","context","frq","rubric","fmt_instr_eval"],
            output_variables=["eval"],
            verbose=self.DEBUG
        )

    def buildFormattingInstructionsEval(self):
        """
            Builds output formatting instruction for chain 1
        """
        # Define response schema
        written_eval_json = ResponseSchema(name="written_eval",
                                    description="Written evaluation feedback to student")
        score_json = ResponseSchema(name="score",
                                    description="Score achieved by student")
        score_max_json = ResponseSchema(name="score_max",
                                    description="Maximum score possible for this assessment")
        
        response_schemas = [written_eval_json,score_json,score_max_json]
        output_parser_eval = StructuredOutputParser.from_response_schemas(response_schemas)
        
        self.format_instruction_eval = output_parser_eval.get_format_instructions()
        self.output_parser_eval = output_parser_eval
        
    def evaluate_answer(self,standard,context,frq,rubric,answer):
        """
            Generates evaluation of the answer of Common Core State Standard. 
            Parameters:
                standard: str, e.g. "CCSS.ELA-LITERACY.W.4.9"
                context: str
                frq - free response question: str
                rubric: str
                answer: str
            Returns:
                evaluation - written evaluation feedback
                score - numeric score value
                score_max - numeric maximum possible score value
        """

        with no_ssl_verification():
            eval_json = self.evaluate_chain({"standard":standard,
                                        "answer":answer,
                                        "context":context,
                                        "frq":frq,
                                        "rubric":rubric,
                                        "fmt_instr_eval":self.format_instruction_eval})
        
        # print(eval_json)
        # saves full answer to /transcripts folder
        if self.DEBUG:
            now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

            file_name = f"{DEBUG_FILE_PATH}Eval_{standard}_{now}.json"
            with open(file_name, "w") as file:
                json.dump(eval_json, file)


        # parse the response - TODO error handling
        written_eval, score, score_max = self.parse_output(eval_json)
        return written_eval, score, score_max
    
    def parse_output(self,eval_json:dict):
        """
            returns subset of fields provided by LangChain
        """
        written_eval = self.output_parser_eval.parse(eval_json['eval'])['written_eval']
        score = self.output_parser_eval.parse(eval_json['eval'])['score']
        score_max = self.output_parser_eval.parse(eval_json['eval'])['score_max']
        return written_eval, score, score_max