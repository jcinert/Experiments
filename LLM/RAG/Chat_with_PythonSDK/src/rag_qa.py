import os
from dotenv import load_dotenv, find_dotenv
import openai

# # to disable SSL verification that causes problem from my laptop
# from ssl_workaround import no_ssl_verification

# LangChain imports
from langchain.chat_models import AzureChatOpenAI
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
import src.prompts as prompts

import langchain
import warnings
import json
import datetime


class RAG_QA():
    """
        Class to QA RAG chat - providing a Dict of question, chat history and answer.
            - evaluates answer completeness - given the question, history and answer            
            - evaluates answer accuracy/correctness - search the answer in vector db and evaluate match
    """
    def __init__(self, config:dict):
        
        self.DEBUG = config['debug']
        self.DEBUG_FILE_PATH = config['qa_debug_file_path']
        self.init()
        # self.load_prompt_examples()
        # self.initLangChain()
    
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
        if self.CONFIG['debug']:
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

        # with no_ssl_verification():
        qa_json = self.qa_chain({"chat_history":chat_history,
                                "prompt":question,
                                "response":response,
                                "fmt_instr_qa":self.format_instruction_qa})
                                # "QA_EXAMPLE_01":self.QA_EXAMPLE_01,
                                # "QA_EXAMPLE_02":self.QA_EXAMPLE_02})
        
        if self.DEBUG:
            now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

            file_name = f"{DEBUG_FILE_PATH}QA_{question[:5]}_{now}.json"
            with open(file_name, "w") as file:
                json.dump(qa_json, file)


        # # parse the response - TODO error handling
        qa_result = self.format_output(qa_json)
        return qa_result

    # def batch_qa_assessment(self,assessment_batch:list,max_retries_on_error=3):
    #     """
    #         Generates evaluations (QA) summary of the multiple assessment of Common Core State Standard. 
    #         Parameters:
    #             assessment: list of dict with below fields
    #                 standard: str, e.g. "CCSS.ELA-LITERACY.W.4.9"
    #                 topic: str
    #                 context: str
    #                 frq - free response question: str
    #                 rubric: str
    #             max_retries_on_error
    #         Returns:
    #             qa_results: dict with below fileds:
    #                 count_assessments - total count of assessements evaluated
    #                 overall_qa_passed - count of assessments with all evaluation passed - context, frq, rubrics
    #                 context_qa_passed - count of assessments with context QA passed
    #                 frq_qa_passed - count of assessments with FRQ QA passed
    #                 rubric_qa_passed - count of assessments with rubric QA passed
    #     """
        
    #     # init
    #     count_assessments = len(assessment_batch)
    #     overall_qa_passed = 0
    #     context_qa_passed = 0
    #     frq_qa_passed = 0
    #     rubric_qa_passed = 0

    #     for assessment in assessment_batch:
    #         # sometimes parser fails - workaround for now: retry - TODO improve prompts
    #         run_successfull = False
    #         for i in range(max_retries_on_error):
    #             try:
    #                 qa_result = self.qa_assessment(assessment)
    #                 run_successfull = True
    #                 break
    #             except:
    #                 print(">>> Assessment QA failed - restarting")

    #         if not run_successfull:
    #             raise Exception(f"ERROR: Generate QA not successfull after {max_retries_on_error} retries.")

    #         # adding up qa results for each assessment
    #         if qa_result['overall_qa_passed'] == True or qa_result['overall_qa_passed'] == 'true':
    #             overall_qa_passed = overall_qa_passed + 1
    #         if qa_result['context_qa_passed'] == True or qa_result['context_qa_passed'] == 'true':
    #             context_qa_passed = context_qa_passed + 1
    #         if qa_result['frq_qa_passed'] == True or qa_result['frq_qa_passed'] == 'true':
    #             frq_qa_passed = frq_qa_passed + 1
    #         if qa_result['rubric_qa_passed'] == True or qa_result['rubric_qa_passed'] == 'true':
    #             rubric_qa_passed = rubric_qa_passed + 1

    #     return {"count_assessments":count_assessments,
    #             "overall_qa_passed":overall_qa_passed,
    #             "context_qa_passed":context_qa_passed,
    #             "frq_qa_passed":frq_qa_passed,
    #             "rubric_qa_passed":rubric_qa_passed}


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