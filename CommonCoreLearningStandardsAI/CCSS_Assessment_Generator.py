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


class AssessmentGenerator():
    """
        Class to create Common Core State Standard assessment consisting of:
            - context paragraph
            - free response question
            - rubric to evaluate answer
        Usage: set topic and standard first, then call generate_assessment()
    """
    def __init__(self, topic=None, standard=None, debug=False):
        self.standard = standard
        self.topic = topic
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
        self.EXAMPLE_RUBRIC_01 = prompt_examples.EXAMPLE_RUBRIC_01
        self.EXAMPLE_RUBRIC_02 = prompt_examples.EXAMPLE_RUBRIC_02
        self.EXAMPLE_RUBRIC_03 = prompt_examples.EXAMPLE_RUBRIC_03
        self.EXAMPLE_RUBRIC_04 = prompt_examples.EXAMPLE_RUBRIC_04
        self.EXAMPLE_FRQ_01 = prompt_examples.EXAMPLE_FRQ_01
        self.EXAMPLE_FRQ_02 = prompt_examples.EXAMPLE_FRQ_02
    
    def initLangChain(self):
        """
            Builds LangChain and prompts to create CCSS assessment
        """
        # ------------------------------------------------------------------------------------------------
        # Chain 1 - generate context and free responce question
        # ------------------------------------------------------------------------------------------------
        
        self.buildFormattingInstructionsFRQ()
        # DEBUG
        if self.DEBUG:
            print(self.format_instruction_frq)

        # to avoid Lanchain considering JSON as nather variable format and examples are passed in as input 
        fmt_instr_frq_var = "{fmt_instr_frq}"
        EXAMPLE_FRQ_01_var = "{EXAMPLE_FRQ_01}"
        EXAMPLE_FRQ_02_var = "{EXAMPLE_FRQ_02}"

        # System message
        system_message = f"""
        You are an helpful assistant. User will provide you Common Core State Standard and a topic. \
        You will output an assesment task for a student to test student knowledge consisting of:
        1. COTEXT: context paragraph that will be used by the student to answer the below free responce question.\
        The COTEXT is a paragraph and must be related to topic provided by user. \
        The COTEXT must be sufficient to answer the free responce question and meet complexity and length as expected by the Common Core State Standard definition provided by user.
        2. FREE RESPONCE QUESTION: The question must be related to the context article and test students ability as per the standard definition above.\

        Follow these steps to create the task:

        Step 1: Provide definition of Common Core State Standard provided by user

        Step 3: Define what needs to be tested as part of assement defined in steps 1 and make sure to include it in the CONTEXT and FREE RESPONSE QUESTION.

        Step 2: Define what is the expected lenght and complexity of the CONTEXT paragraph that is provided to student

        Step 4: Generate CONTEXT paragraph. It must meet the conditions defined in second and third step.

        Step 5: Generate FREE RESPONSE QUESTION related to CONEXT and meeting definition in step one.

        {fmt_instr_frq_var}

        Here are EXAMPLES of good answer:
        #### EXAMPLE 1
        {EXAMPLE_FRQ_01_var}
        #### EXAMPLE 2
        {EXAMPLE_FRQ_02_var}
        """

        # Make SystemMessagePromptTemplate
        prompt=PromptTemplate(
            template=system_message,
            input_variables=["fmt_instr_frq","EXAMPLE_FRQ_01","EXAMPLE_FRQ_02"]
        )

        system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

        # User message (input)
        CCSS_TOPIC = """Common Core State Standard is {standard} and topic is {topic}."""
        # Make HumanMessagePromptTemplate
        human_message_prompt = HumanMessagePromptTemplate.from_template(CCSS_TOPIC)
        # Create ChatPromptTemplate: Combine System + Human
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain1 = LLMChain(
            llm=ChatOpenAI(
                temperature=0.7, 
                openai_api_base = self.OPENAI_API_BASE,
                openai_api_key = self.OPENAI_API_KEY,
                deployment_id = self.OPENAI_DEPLOYMENT_ID),
            prompt = chat_prompt,
            output_key="reasoning_context_frq",
            verbose=self.DEBUG
        )

        # # DEBUG
        # chain1
        # with no_ssl_verification():
        #     response = chain1.predict(standard = "CCSS.ELA-LITERACY.W.4.9", topic="basketball", fmt_instr_frq = fmt_instr_frq, EXAMPLE_FRQ_01=EXAMPLE_FRQ_01, EXAMPLE_FRQ_02=EXAMPLE_FRQ_02)
        # print(response)

        # ------------------------------------------------------------------------------------------------
        # Chain 2 - generate rubric
        # ------------------------------------------------------------------------------------------------

        # build expected output schema (JSON)
        # self.buildFormattingInstructionsRubric()
        # # DEBUG
        # if self.DEBUG:
        #     print(self.format_instruction_rubric)      

        # to avoid Lanchain considering JSON definition as variable
        # fmt_instr_rubric_var = "{fmt_instr_rubric}"
        # EXAMPLE_RUBRIC_01_var = "{EXAMPLE_RUBRIC_01}"
        # EXAMPLE_RUBRIC_02_var = "{EXAMPLE_RUBRIC_02}"

        system_message = """
        You are an helpful assistant. User will provide you Common Core State Standard. \
        You will output a RUBRIC for an assessment task as expected by the Common Core State Standard provided by user.
        
        {fmt_instr_rubric}
        
        Here are EXAMPLES of good answer:
        #### EXAMPLE 1
        {EXAMPLE_RUBRIC_01}
        #### EXAMPLE 2
        {EXAMPLE_RUBRIC_02}
        """

        self.format_instruction_rubric = "Output only the generated rubric in markdown string snippet format."

        # Make SystemMessagePromptTemplate
        prompt=PromptTemplate(
            template=system_message,
            input_variables=["fmt_instr_rubric","EXAMPLE_RUBRIC_01","EXAMPLE_RUBRIC_02"]
        )

        system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

        CCSS_RUBRIC = """Common Core State Standard is {standard}. Take into consideration the definition of this standard provided below in step-1.
        You can consider the context and free response question (frq), but it is preferable for the generated rubric to be generic, not reflecting the topic of the context and frq.
        {reasoning_context_frq}."""

        # Make HumanMessagePromptTemplate
        human_message_prompt = HumanMessagePromptTemplate.from_template(CCSS_RUBRIC)

        # Create ChatPromptTemplate: Combine System + Human
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain2 = LLMChain(
            llm=ChatOpenAI(
                temperature=0.0, 
                openai_api_base = self.OPENAI_API_BASE,
                openai_api_key = self.OPENAI_API_KEY,
                deployment_id = self.OPENAI_DEPLOYMENT_ID),
            prompt = chat_prompt,
            output_key="rubric",
            verbose=self.DEBUG
        )

        # ------------------------------------------------------------------------------------------------
        # Chain 3 - QA of generated assessment (free responce question and context)
        # ------------------------------------------------------------------------------------------------

        self.buildFormattingInstructionsFRQQA()
        # DEBUG
        if self.DEBUG:
            print(self.format_instruction_frq_qa)

        system_message = """
        You are an helpful assistant. User will provide you Common Core State Standard (CCSS) and a topic. \
        You will also be provided with CONTEXT paragraph and Free Response Question (FRQ).
        You will evaluate if provided CONTEXT and FRQ are meeting the CCSS requirements, i.e. if it allignes with skills and competencies outlined by the provided CCSS standard itself.

        Follow these steps to complete the task:
        1. Understand the provided CCSS definition, skills and competencies it should test
        2. Understand the expected CONTEXT complexity, lenght and topic
        3. Validate if CONTEXT broadly meets the requirements
        4. Validate if FRQ broadly meets the requirements and is relevant to the CONTEXT

        If the CONTEXT and FRQ meet or mostly meet the CCSS requirements you will output "True". Otherwise output "False". 
        In case you respond "False" also provide:
        1. Justification what is missing or incorrect.
        2. Adjusted CONTEXT and FRQ, that will be based on the existing, but enhanced to align better to the provided CCSS and user topic.
        Remember: If the CONTEXT or FRQ doesnt meet the CCSS requirements, you must adjust both to keep the FRQ relevant to the CONTEXT.

        {fmt_instr_frq_qa}
        """

        # Make SystemMessagePromptTemplate
        prompt=PromptTemplate(
            template=system_message,
            input_variables=["fmt_instr_frq_qa"]
        )

        system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

        CCSS_FRQ_QA = """Common Core State Standard is {standard}. Topic is {topic}. 
        CONTEXT paragraph to be evaluated and Free Response Question (FRQ) to be evaluated are in the below JSON: 
        {reasoning_context_frq}"""

        # Make HumanMessagePromptTemplate
        human_message_prompt = HumanMessagePromptTemplate.from_template(CCSS_FRQ_QA)

        # Create ChatPromptTemplate: Combine System + Human
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain3 = LLMChain(
            llm=ChatOpenAI(
                temperature=0.0, 
                openai_api_base = self.OPENAI_API_BASE,
                openai_api_key = self.OPENAI_API_KEY,
                deployment_id = self.OPENAI_DEPLOYMENT_ID),
            prompt = chat_prompt,
            output_key="frq_qa",
            verbose=self.DEBUG
        )

        # ------------------------------------------------------------------------------------------------
        # Chain 4 - QA of generated assessment (free responce question and context)
        # ------------------------------------------------------------------------------------------------

        self.buildFormattingInstructionsRubricQA()
        # DEBUG
        if self.DEBUG:
            print(self.format_instruction_rubric_qa)

        system_message = """
        You are an helpful assistant. User will provide you Common Core State Standard (CCSS).\
        You will also be provided with RUBRIC related to the CCSS.
        You will evaluate if provided RUBRIC alignes CCSS requirements, i.e. if it allignes with skills and competencies outlined by the provided CCSS standard itself.
        If the RUBRIC meets or mostly meets the CCSS requirements you will output "True". Otherwise output "False". 
        In case you respond "False" also provide:
        1. Justification what is missing or incorrect.
        2. Adjusted Rubric, that will be based on the existing, but enhanced to align better to the provided CCSS.
        {fmt_instr_rubric_qa}
        """

        # Make SystemMessagePromptTemplate
        prompt=PromptTemplate(
            template=system_message,
            input_variables=["fmt_instr_rubric_qa"]
        )

        system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

        CCSS_RUBRIC_QA = """Common Core State Standard is {standard}. Rubric to be evaluated is in markdown format: 
        {rubric}."""

        # Make HumanMessagePromptTemplate
        human_message_prompt = HumanMessagePromptTemplate.from_template(CCSS_RUBRIC_QA)

        # Create ChatPromptTemplate: Combine System + Human
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain4 = LLMChain(
            llm=ChatOpenAI(
                temperature=0.0, 
                openai_api_base = self.OPENAI_API_BASE,
                openai_api_key = self.OPENAI_API_KEY,
                deployment_id = self.OPENAI_DEPLOYMENT_ID),
            prompt = chat_prompt,
            output_key="rubric_qa",
            verbose=self.DEBUG
        )

        self.assessment_chain = SequentialChain(
            chains=[chain1, chain2, chain3, chain4],
            input_variables=["standard","topic","fmt_instr_rubric","fmt_instr_frq","fmt_instr_frq_qa","fmt_instr_rubric_qa","EXAMPLE_FRQ_01","EXAMPLE_FRQ_02","EXAMPLE_RUBRIC_01","EXAMPLE_RUBRIC_02"],
            output_variables=["rubric","reasoning_context_frq","frq_qa","rubric_qa"],
            verbose=self.DEBUG
        )

    def buildFormattingInstructionsFRQ(self):
        """
            Builds output formatting instruction for chain 1
        """
        # Define response schema
        step1_json = ResponseSchema(name="step-1",
                                    description="step 1 reasoning")
        step2_json = ResponseSchema(name="step-2",
                                    description="step 2 reasoning")
        step3_json = ResponseSchema(name="step-3",
                                    description="step 3 reasoning")
        context_json = ResponseSchema(name="context",
                                    description="generated context paragraph")
        frq_json = ResponseSchema(name="frq",
                                    description="generated free respoce question")
        
        response_schemas = [step1_json,step2_json,step3_json,context_json,frq_json]
        output_parser_frq = StructuredOutputParser.from_response_schemas(response_schemas)
        
        self.format_instruction_frq = output_parser_frq.get_format_instructions()
        self.output_parser_frq = output_parser_frq

    def buildFormattingInstructionsRubric(self):
        """
            Builds output formatting instruction for chain 2 - NOT USED 
        """
        rubric_json = ResponseSchema(name="rubric",
                                description="Rubric for this assesment task as expected by the Common Core State Standard definition provided by user")

        response_schemas = [rubric_json]
        output_parser_rubric = StructuredOutputParser.from_response_schemas(response_schemas)

        self.format_instruction_rubric = output_parser_rubric.get_format_instructions()
        self.output_parser_rubric = output_parser_rubric

    def buildFormattingInstructionsFRQQA(self):
        """
            Builds output formatting instruction for chain 3
        """
        # Define response schema
        frq_qa_json = ResponseSchema(name="frq_qa_passed",
                                    description="Boolean value to idicate if the CONTEXT and FRQ is meeting the Common Core State Standard and topic provided by user. True = meets, False = Does not meet")
        frq_qa_reason_json = ResponseSchema(name="frq_qa_reason",
                                    description="Justification why the CONTEXT and/or the FRQ isnt meeting Common Core State Standard. If both the CONTEXT and the FRQ are meeting CCSS provide value N/A")
        adjusted_context_json = ResponseSchema(name="adjusted_context",
                                    description="Adjusted CONTEXT meeting the user provided Common Core State Standard using and the topic. If original CONTEXT is meeting CCSS provide value N/A")
        adjusted_frq_json = ResponseSchema(name="adjusted_frq",
                                    description="Adjusted FRQ meeting the user provided Common Core State Standard and the topic. NEW FRQ must be related to the NEW CONTEXT. If original FRQ is meeting CCSS provide value N/A")


        response_schemas = [frq_qa_json,frq_qa_reason_json,adjusted_context_json,adjusted_frq_json]
        output_parser_frq_qa = StructuredOutputParser.from_response_schemas(response_schemas)

        self.format_instruction_frq_qa = output_parser_frq_qa.get_format_instructions()
        self.output_parser_frq_qa = output_parser_frq_qa

    def buildFormattingInstructionsRubricQA(self):
        """
            Builds output formatting instruction for chain 4
        """
        # Define response schema
        rubric_qa_json = ResponseSchema(name="rubric_qa_passed",
                                    description="Boolean value to idicate if the RUBRIC is meeting the Common Core State Standard provided by user. True = meets, False = Does not meet")
        rubric_qa_reason_json = ResponseSchema(name="rubric_qa_reason",
                                    description="Justification why RUBRIC isnt meeting Common Core State Standard. If the Rubric is meeting CCSS provide value N/A")
        rubric_qa_new_json = ResponseSchema(name="rubric_qa_new",
                                    description="New regenerated Rubric in markdown snippet format. If the original Rubric is meeting CCSS provide value N/A")

        response_schemas = [rubric_qa_json,rubric_qa_reason_json,rubric_qa_new_json]
        output_parser_rubric_qa = StructuredOutputParser.from_response_schemas(response_schemas)

        self.format_instruction_rubric_qa = output_parser_rubric_qa.get_format_instructions()
        self.output_parser_rubric_qa = output_parser_rubric_qa

    def set_standard(self, standard):
        self.standard = standard
    
    def set_topic(self, topic):
        self.topic = topic
                
    def generate_assessment(self):
        """
            Generates assessment of Common Core State Standard. Uses provided topic of interest to generate the assessment.
            Make sure to use set_topic() and set_standard() prior to calling this finction
            Returns:
                context - a paragraph of text based on topic and standard
                free responce question (FRQ) - question related to the context to assess students skills as per provided standard
                rubric - rubric in markdown format (str)
        """
        if (self.topic == None) or (self.standard == None):
            raise ValueError("Standard and topic must be set first to generate the assessement. Use set_topic() and set_standard().")

        with no_ssl_verification():
            answer = self.assessment_chain({"standard":self.standard, 
                                    "topic":self.topic, 
                                    "fmt_instr_frq":self.format_instruction_frq,
                                    "fmt_instr_rubric":self.format_instruction_rubric, 
                                    "fmt_instr_frq_qa":self.format_instruction_frq_qa,
                                    "fmt_instr_rubric_qa":self.format_instruction_rubric_qa, 
                                    "EXAMPLE_FRQ_01":self.EXAMPLE_FRQ_01, 
                                    "EXAMPLE_FRQ_02":self.EXAMPLE_FRQ_02,
                                    "EXAMPLE_RUBRIC_01":self.EXAMPLE_RUBRIC_03, 
                                    "EXAMPLE_RUBRIC_02":self.EXAMPLE_RUBRIC_04})
        
        # saves full answer to /transcripts folder
        if self.DEBUG:
            now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

            file_name = f"{DEBUG_FILE_PATH}AssessmentGen_{self.standard}_{now}.json"
            with open(file_name, "w") as file:
                json.dump(answer, file)

        # parse the response - TODO error handling
        context, frq, rubric, frq_qa, rubric_qa = self.parse_output(answer)

        context_out, frq_out = self.qa_frq(context, frq, frq_qa)
        rubric_out = self.qa_rubric(rubric, rubric_qa)

        return context_out, frq_out, rubric_out
    
    def parse_output(self,answer:dict):
        """
            returns subset of fields provided by LangChain
        """
        context = self.output_parser_frq.parse(answer['reasoning_context_frq'])['context']
        frq = self.output_parser_frq.parse(answer['reasoning_context_frq'])['frq']
        rubric = self.parse_rubric(answer['rubric'])
        frq_qa = self.output_parser_frq_qa.parse(answer['frq_qa'])
        rubric_qa = self.output_parser_rubric_qa.parse(answer['rubric_qa'])
        return context, frq, rubric, frq_qa, rubric_qa
    
    def parse_rubric(self, rubric_md):
        """
            temporary solution to parse the rubric. there is an error in LangChain parser
        """
        # return rubric_json[22:-7]
        return rubric_md
    
    def qa_frq(self, context, frq, frq_qa):
        """
            Validate if the context and free responce quesion (FRQ) passed the QA. If not use fixed version of context and FRQ
        """
        if frq_qa['frq_qa_passed'] == True:
            context_out = context
        else:
            context_out = frq_qa['adjusted_context']
        
        if frq_qa['frq_qa_passed'] == True:
            frq_out = frq
        else:
            frq_out = frq_qa['adjusted_frq']

        return context_out, frq_out 
    
    def qa_rubric(self, rubric, rubric_qa):
        """
            Validate if the Rubric passed the QA. If not use fixed version of Rubric
        """
        if rubric_qa['rubric_qa_passed'] == True:
            rubric_out = rubric
        else:
            rubric_out = rubric_qa['rubric_qa_new']

        return rubric_out