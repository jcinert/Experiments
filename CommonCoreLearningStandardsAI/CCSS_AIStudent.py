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


class AIStudent():
    """
        Class to respond to Common Core State Standard assessment consisting of:
            - context paragraph
            - free response question
            - rubrics to evaluate answer
        Intended use is simulation of student responding to assessment
        Parameters
            answer_quality:int / only can have values [1,2,3,4]
                1 - Exceeding Standards (Excellent)
                2 - Meeting Standards
                3 - Approaching Standards (Progressing)               
                4 - Not Meeting Standards (Needs Improvement)

        Usage: set required testing set_standard() and answer_quality(), then call answer_assessment()
    """
    def __init__(self, answer_quality=2, debug=False):
        
        self.set_answer_quality(answer_quality)
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

    # def load_prompt_examples(self):
    #     # self.EXAMPLE_RUBRIC_01 = prompt_examples.EXAMPLE_RUBRIC_01
    #     # self.EXAMPLE_RUBRIC_02 = prompt_examples.EXAMPLE_RUBRIC_02
    #     # self.EXAMPLE_FRQ_01 = prompt_examples.EXAMPLE_FRQ_01
    #     # self.EXAMPLE_FRQ_02 = prompt_examples.EXAMPLE_FRQ_02
    
    def initLangChain(self):
        """
            Builds LangChain and prompts to respond to CCSS assessment
        """
        # ------------------------------------------------------------------------------------------------
        # Chain 1 - generate answer to CCSS assessment
        # ------------------------------------------------------------------------------------------------
        
        self.buildFormattingInstructionsAnswer()
        # DEBUG
        if self.DEBUG:
            print(self.format_instruction_answer)

        # System message
        system_message = """
        You are a student completing the Common Core State Standard assessment: {standard}\
        The assessment consists of: context, free response question (FRQ) and rubrics. \
        You need to read the CONTEXT respond to FRQ. \
        Work in this order: 
        1. Define what grade student you should pretend be to based on the standard. 
        2. Understand how a student of this grade would answer. Remember student grade will impact complexity and lenght of the answer, amogh other aspects of your answer.
        3. You must answer in a way a student of this grade would to achieve {answer_quality} score. Review the Rubrics to plan the answer.
        4. Answer to FRQ using the CONTEXT as instructed. The Answer must not include any evaluation of itself.

        {fmt_instr_answer}
        """

        # Make SystemMessagePromptTemplate
        prompt=PromptTemplate(
            template=system_message,
            input_variables=["standard","answer_quality","fmt_instr_answer"]
        )

        system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

        # User message (input)
        CCSS_ASSESSMENT = """Context: {context} 
        Free responce question (FRQ): {frq}
        Rubric: {rubric}"""
        # Make HumanMessagePromptTemplate
        human_message_prompt = HumanMessagePromptTemplate.from_template(CCSS_ASSESSMENT)
        # Create ChatPromptTemplate: Combine System + Human
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        chain1 = LLMChain(
            llm=ChatOpenAI(
                temperature=1, 
                openai_api_base = self.OPENAI_API_BASE,
                openai_api_key = self.OPENAI_API_KEY,
                deployment_id = self.OPENAI_DEPLOYMENT_ID),
            prompt = chat_prompt,
            output_key="answer",
            verbose=self.DEBUG
        )

        # ------------------------------------------------------------------------------------------------
        # Overall - generate answer to CCSS assessment
        # ------------------------------------------------------------------------------------------------
        # not really needed for now, but can be expanded in future
        self.answer_chain = SequentialChain(
            chains=[chain1],
            input_variables=["standard","answer_quality","context","frq","rubric","fmt_instr_answer"],
            output_variables=["answer"],
            verbose=self.DEBUG
        )

        # # DEBUG
        # chain1
        # with no_ssl_verification():
        #     response = chain1.predict(standard = "CCSS.ELA-LITERACY.W.4.9", 
        #                               answer_quality = self.answer_quality, 
        #                               fmt_instr_answer = self.format_instruction_answer,
        #                               context="New Zealand is a country located in the southwestern Pacific Ocean. It is made up of two main islands, the North Island and the South Island, as well as many smaller islands. The indigenous people of New Zealand are the Maori, who arrived in the country more than 1,000 years ago. Today, Maori culture is an important part of New Zealand's identity. The country is known for its stunning natural scenery, which includes mountains, beaches, and geothermal features. New Zealand is also home to many unique animals, such as the kiwi bird and the tuatara lizard.", 
        #                               frq="Based on the context provided, what are some unique features of New Zealand? How does the Maori culture contribute to the country's identity? Use evidence from the text to support your answer.",
        #                               rubric="""### Assessment Rubric for Free Response Question\n\n#### Criteria for Evaluation\n\n1. **Drawing Evidence (5 points)**: Student must draw clear evidence from literary or informational texts to support their answer.\n    - 5 points: Provides direct quotes or paraphrases that are highly relevant to the question and are drawn from multiple sources.\n    - 3 points: Provides some evidence but it's either partially relevant or not directly quoted, or is drawn from a single source.\n    - 1 point: Makes a generalized or vague reference to the text, or the evidence provided is not relevant to the question.\n    - 0 points: Does not reference the text.\n\n2. **Analysis and Reflection (5 points)**: Student should analyze the unique features of New Zealand's natural environment and the contribution of indigenous Maori culture to the country's history and identity, and reflect on the implications of this information.\n    - 5 points: Thoroughly analyzes both the natural environment and Maori culture, with evidence to support their analysis, and reflects on the implications of this information.\n    - 3 points: Partially analyzes either the natural environment or Maori culture, with some evidence, and reflects on the implications of this information.\n    - 1 point: Minimal analysis with limited or no evidence, or minimal reflection on the implications of the information.\n    - 0 points: No analysis or reflection.\n\n3. **Clarity and Organization (3 points)**: Answer should be clear, concise, and well-organized.\n    - 3 points: Answer is clear, concise, and logically organized.\n    - 2 points: Answer is mostly clear but may lack some organization.\n    - 1 point: Answer is disorganized or unclear.\n    - 0 points: Answer is incomprehensible.\n\n4. **Grammar and Mechanics (2 points)**: The answer should be free of grammatical and spelling errors.\n    - 2 points: No errors.\n    - 1 point: Few minor errors.\n    - 0 points: Numerous errors that hinder comprehension.\n\n### Scoring Guide\n- 13-15 points: Excellent\n- 10-12 points: Good\n- 6-9 points: Needs Improvement\n- 0-5 points: Unsatisfactory""")
        # print(response)


    def buildFormattingInstructionsAnswer(self):
        """
            Builds output formatting instruction for chain 1
        """
        # Define response schema
        answer_json = ResponseSchema(name="answer",
                                    description="generated anwer")
        
        response_schemas = [answer_json]
        output_parser_answer = StructuredOutputParser.from_response_schemas(response_schemas)
        
        self.format_instruction_answer = output_parser_answer.get_format_instructions()
        self.output_parser_answer = output_parser_answer

    def set_standard(self, standard):
        self.standard = standard
    
    def set_answer_quality(self, answer_quality):
        if answer_quality == 1:
            self.answer_quality = "1 - Exceeding Standards (Excellent)"
        elif answer_quality == 2:
            self.answer_quality = "2 - Meeting Standards"
        elif answer_quality == 3:
            self.answer_quality = "3 - Approaching Standards (Progressing)"
        elif answer_quality == 4:
            self.answer_quality = "4 - Not Meeting Standards (Needs Improvement)"
        else:
            raise ValueError("answer_quality must be 1, 2, 3 or 4")
        
    def generate_answer(self,context,frq,rubric):
        """
            Generates assessment of Common Core State Standard. Uses provided topic of interest to generate the assessment.
            Make sure to use set_topic() and set_standard() prior to calling this finction
            Returns:
                context - a paragraph of text based on topic and standard
                frq - free responce question - question related to the context to assess students skills as per provided standard
                rubric - evaluation rubric
        """
        if (self.standard == None):
            raise ValueError("Standard must be set first to generate the assessement. Use set_standard().")

        with no_ssl_verification():
            answer_json = self.answer_chain({"standard":self.standard,
                                        "answer_quality":self.answer_quality,
                                        "context":context,
                                        "frq":frq,
                                        "rubric":rubric,
                                        "fmt_instr_answer":self.format_instruction_answer})
        
        # saves full answer to /transcripts folder
        if self.DEBUG:
            now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

            file_name = f"{DEBUG_FILE_PATH}Answer_{self.standard}_{now}.json"
            with open(file_name, "w") as file:
                json.dump(answer_json, file)


        # parse the response - TODO error handling
        answer = self.parse_output(answer_json)
        return answer
    
    def parse_output(self,answer_json:dict):
        """
            returns subset of fields provided by LangChain
        """
        answer = self.output_parser_answer.parse(answer_json['answer'])['answer']
        return answer