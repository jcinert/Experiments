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


class BatchQA():
    """
        Class to QA over assessments of Common Core State Standard (CCSS) consisting of:
            - context paragraph
            - free response question (FRQ)
            - rubrics to evaluate answer
        Intended use is to provide a JSON of assessment. Each context, FRQ and rubrics will be evaluated if it meeting the CCSS standards
    """
    def __init__(self, debug=False):
        
        self.DEBUG = debug

        self.init()
        self.load_prompt_examples()
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
    
    def load_prompt_examples(self):
        self.QA_EXAMPLE_01 = prompt_examples.QA_EXAMPLE_01
        self.QA_EXAMPLE_02 = prompt_examples.QA_EXAMPLE_02

    def initLangChain(self):
        """
            Builds LangChain and prompts to QA a CCSS assessment
        """
        # ------------------------------------------------------------------------------------------------
        # Chain 1 - generate QA of CCSS assessment
        # ------------------------------------------------------------------------------------------------
        
        self.buildFormattingInstructionsQA()
        # DEBUG
        if self.DEBUG:
            print(self.format_instruction_qa)

        # System message
        system_message = """
        You are an helpful assistant. User will provide you Common Core State Standard (CCSS) and a topic. \
        You will also be provided with CONTEXT paragraph, Free Response Question (FRQ) and RUBRIC.
        You will evaluate if provided CONTEXT, FRQ and RUBRIC are meeting the CCSS requirements, i.e. if it aligns with skills and competencies outlined by the provided CCSS standard itself.

        Follow these steps to complete the task:
        1. Understand the provided CCSS definition, skills and competencies it should test
        2. Understand the expected CONTEXT complexity, length and topic
        3. Validate if CONTEXT broadly meets the CCSS requirements.
        4. Validate if FRQ broadly meets the requirements and is relevant to the CONTEXT
        5. Validate if RUBRIC broadly meets the requirements and can be used to evaluate to FRQ answer

        If the CONTEXT meets or mostly meets the CCSS requirements you will output "true". Otherwise output "false" in field context_qa_passed.
        If the FRQ meets or mostly meets the CCSS requirements you will output "true". Otherwise output "false" in field frq_qa_passed.
        If the RUBRIC meets or mostly meets the CCSS requirements you will output "true". Otherwise output "false" in field rubric_qa_passed.
        In case you respond "false" also provide justification what is missing or is incorrect.
        Return only the this output defined here:
        {fmt_instr_qa}

        Here are two examples of good answer:
        ############
        EXAMPLE 1:
        {QA_EXAMPLE_01}
        EXAMPLE 2:
        {QA_EXAMPLE_02}
        """

        # Make SystemMessagePromptTemplate
        prompt=PromptTemplate(
            template=system_message,
            input_variables=["fmt_instr_qa","QA_EXAMPLE_01","QA_EXAMPLE_02"]
        )

        system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

        # User message (input)
        CCSS_QA = """User inputs are in following JSON:
        {assessment}
        """

        # Make HumanMessagePromptTemplate
        human_message_prompt = HumanMessagePromptTemplate.from_template(CCSS_QA)
        # Create ChatPromptTemplate: Combine System + Human
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain1 = LLMChain(
            llm=ChatOpenAI(
                temperature=0.0, 
                openai_api_base = self.OPENAI_API_BASE,
                openai_api_key = self.OPENAI_API_KEY,
                deployment_id = self.OPENAI_DEPLOYMENT_ID),
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
            input_variables=["assessment","fmt_instr_qa","QA_EXAMPLE_01","QA_EXAMPLE_02"],
            output_variables=["qa"],
            verbose=self.DEBUG
        )

    def buildFormattingInstructionsQA(self):
        """
            Builds output formatting instruction for chain 1
        """
        # Define response schema
        context_qa_passed = ResponseSchema(name="context_qa_passed",
                                    description="Boolean value to idicate if the COTEXT is meeting the Common Core State Standard provided by user. true = meets, false = Does not meet")
        context_qa_reason = ResponseSchema(name="context_qa_reason",
                                    description="Justification why COTEXT is or isnt meeting Common Core State Standard")
        frq_qa_passed = ResponseSchema(name="frq_qa_passed",
                                    description="Boolean value to idicate if the FRQ is meeting the Common Core State Standard provided by user. true = meets, false = Does not meet")
        frq_qa_reason = ResponseSchema(name="frq_qa_reason",
                                    description="Justification why FRQ is or isnt meeting Common Core State Standard")
        rubric_qa_passed = ResponseSchema(name="rubric_qa_passed",
                                    description="Boolean value to indicate if the RUBRIC is meeting the Common Core State Standard provided by user. true = meets, false = Does not meet")
        rubric_qa_reason = ResponseSchema(name="rubric_qa_reason",
                                    description="Justification why RUBRIC is or isnt meeting Common Core State Standard")
        
        response_schemas = [context_qa_passed,context_qa_reason,frq_qa_passed,frq_qa_reason,rubric_qa_passed,rubric_qa_reason]
        output_parser_qa = StructuredOutputParser.from_response_schemas(response_schemas)
        
        self.format_instruction_qa = output_parser_qa.get_format_instructions()
        self.output_parser_qa = output_parser_qa
        
    def qa_assessment(self,assessment):
        """
            Generates evaluation (QA) of the assessment of Common Core State Standard. 
            Parameters:
                assessment: dict with below fields
                    standard: str, e.g. "CCSS.ELA-LITERACY.W.4.9"
                    topic: str
                    context: str
                    frq - free response question: str
                    rubric: str
            Returns:
                qa_results: dict with below fileds:
                    overall_qa_passed - all evaluation passed - context, frq, rubrics
                    context_qa_passed - context QA passed
                    frq_qa_passed - context FRQ passed
                    rubric_qa_passed - context rubric passed
                    context_qa_reason - justification why COTEXT is or isnt meeting Common Core State Standard 
                    frq_qa_reason - justification why FRQ is or isnt meeting Common Core State Standard 
                    rubric_qa_reason - justification why RUBRIC is or isnt meeting Common Core State Standard 
        """

        with no_ssl_verification():
            qa_json = self.qa_chain({"assessment":assessment,
                                     "fmt_instr_qa":self.format_instruction_qa,
                                     "QA_EXAMPLE_01":self.QA_EXAMPLE_01,
                                     "QA_EXAMPLE_02":self.QA_EXAMPLE_02})
        
        if self.DEBUG:
            now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

            file_name = f"{DEBUG_FILE_PATH}QA_{assessment['standard']}_{now}.json"
            with open(file_name, "w") as file:
                json.dump(qa_json, file)


        # # parse the response - TODO error handling
        qa_result = self.format_output(qa_json)
        return qa_result

    def batch_qa_assessment(self,assessment_batch:list,max_retries_on_error=3):
        """
            Generates evaluations (QA) summary of the multiple assessment of Common Core State Standard. 
            Parameters:
                assessment: list of dict with below fields
                    standard: str, e.g. "CCSS.ELA-LITERACY.W.4.9"
                    topic: str
                    context: str
                    frq - free response question: str
                    rubric: str
                max_retries_on_error
            Returns:
                qa_results: dict with below fileds:
                    count_assessments - total count of assessements evaluated
                    overall_qa_passed - count of assessments with all evaluation passed - context, frq, rubrics
                    context_qa_passed - count of assessments with context QA passed
                    frq_qa_passed - count of assessments with FRQ QA passed
                    rubric_qa_passed - count of assessments with rubric QA passed
        """
        
        # init
        count_assessments = len(assessment_batch)
        overall_qa_passed = 0
        context_qa_passed = 0
        frq_qa_passed = 0
        rubric_qa_passed = 0

        for assessment in assessment_batch:
            # sometimes parser fails - workaround for now: retry - TODO improve prompts
            run_successfull = False
            for i in range(max_retries_on_error):
                try:
                    qa_result = self.qa_assessment(assessment)
                    run_successfull = True
                    break
                except:
                    print(">>> Assessment QA failed - restarting")

            if not run_successfull:
                raise Exception(f"ERROR: Generate QA not successfull after {max_retries_on_error} retries.")

            # adding up qa results for each assessment
            if qa_result['overall_qa_passed'] == True or qa_result['overall_qa_passed'] == 'true':
                overall_qa_passed = overall_qa_passed + 1
            if qa_result['context_qa_passed'] == True or qa_result['context_qa_passed'] == 'true':
                context_qa_passed = context_qa_passed + 1
            if qa_result['frq_qa_passed'] == True or qa_result['frq_qa_passed'] == 'true':
                frq_qa_passed = frq_qa_passed + 1
            if qa_result['rubric_qa_passed'] == True or qa_result['rubric_qa_passed'] == 'true':
                rubric_qa_passed = rubric_qa_passed + 1

        return {"count_assessments":count_assessments,
                "overall_qa_passed":overall_qa_passed,
                "context_qa_passed":context_qa_passed,
                "frq_qa_passed":frq_qa_passed,
                "rubric_qa_passed":rubric_qa_passed}


    def format_output(self,qa_json:dict):
        """
            returns subset of fields provided by LangChain
        """

        # sometimes OpenAI returns the JSON and formatter is not needed (TODO: refine prompt)
        if type(qa_json["qa"])!=type(qa_json):
            context_qa_passed = self.output_parser_qa.parse(qa_json['qa'])['context_qa_passed']
            frq_qa_passed = self.output_parser_qa.parse(qa_json['qa'])['frq_qa_passed']
            context_reason = self.output_parser_qa.parse(qa_json['qa'])['context_qa_reason']
            frq_reason = self.output_parser_qa.parse(qa_json['qa'])['frq_qa_reason']
            rubric_qa_passed = self.output_parser_qa.parse(qa_json['qa'])['rubric_qa_passed']
            rubric_reason = self.output_parser_qa.parse(qa_json['qa'])['rubric_qa_reason']
        else:
            try:
                context_qa_passed = qa_json['qa']['context_qa_passed']
                frq_qa_passed = qa_json['qa']['frq_qa_passed']
                context_reason = qa_json['qa']['context_reason']
                frq_reason = qa_json['qa']['frq_reason']
                rubric_qa_passed = qa_json['qa']['rubric_qa_passed']
                rubric_reason = qa_json['qa']['rubric_qa_reason']
            except:
                print('WARNING: QA parsing issues. Rrying to use parser')
                context_qa_passed = self.output_parser_qa.parse(qa_json['qa'])['context_qa_passed']
                frq_qa_passed = self.output_parser_qa.parse(qa_json['qa'])['frq_qa_passed']
                context_reason = self.output_parser_qa.parse(qa_json['qa'])['context_qa_reason']
                frq_reason = self.output_parser_qa.parse(qa_json['qa'])['frq_qa_reason']
                rubric_qa_passed = self.output_parser_qa.parse(qa_json['qa'])['rubric_qa_passed']
                rubric_reason = self.output_parser_qa.parse(qa_json['qa'])['rubric_qa_reason']

        # overall QA passed if context and frq and rubric is correct
        overall_qa_passed = context_qa_passed and frq_qa_passed and rubric_qa_passed

        return {"overall_qa_passed":overall_qa_passed,
                "context_qa_passed":context_qa_passed,
                "frq_qa_passed":frq_qa_passed,
                "context_reason":context_reason,
                "frq_reason":frq_reason,
                "rubric_qa_passed":rubric_qa_passed,
                "rubric_reason":rubric_reason}