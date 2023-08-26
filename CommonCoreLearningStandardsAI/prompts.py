PROMPT_DEFINITION = """What is common core standard {standard} definition?"""

PROMPT_1 = """Given the You need to create an assesment for a student consisting of:\
 1. context, 2. free responce question, 3. rubic for evaluation.\
 Think step by step and provide context, free responce question and the rubic.\
 Remember the assignmet must be according to CCSS.ELA-LITERACY.W.4.9 standard and use basketball topic."""


PROMPT_X = """You need to create an assesment for a student consisting of:\
 1. context, 2. free responce question, 3. rubic for evaluation.\
 Think step by step and provide context, free responce question and the rubic.\
 Remember the assignmet must be according to CCSS.ELA-LITERACY.W.4.9 standard and use basketball topic."""

PROMPT_RUBRIC = """Create a rubic for the CCSS.ELA-LITERACY.W.4.9 assesment"""

# example prompts from web ChatGPT 3.5
EXAMPLE_GPT35_01 = """
Step 1:#### Define Common Core State Standard
CCSS.ELA-LITERACY.W.4.9: Draw evidence from literary or informational texts to support analysis, reflection, and research.

Step 2:#### Define Expected Length and Complexity of CONTEXT Paragraph
The CONTEXT paragraph should be a detailed and informative passage that presents information related to the topic in a way that challenges the student's ability to analyze and reflect on the content. It should be approximately 150-200 words in length, using age-appropriate vocabulary and sentence structures.

Step 3:#### Define What Needs to be Tested
The assessment needs to test the student's ability to draw evidence from the provided context paragraph to support their analysis and reflection on the topic.

Step 4 - CONTEXT:####
Basketball is a popular team sport that has captured the hearts of millions worldwide. Played on a rectangular court with hoops on opposite ends, the objective is to shoot the ball through the opponent's hoop to score points. Two teams compete, each aiming to outscore the other within a designated time. The sport demands teamwork, strategy, and athleticism. Players must dribble the ball while avoiding defenders, passing to teammates, and taking well-timed shots. The game's fast pace and continuous action keep players and spectators engaged. Moreover, basketball fosters camaraderie among team members and teaches valuable life skills like communication and perseverance. Aspiring players often look up to legendary figures like Michael Jordan and LeBron James for inspiration, recognizing their significant contributions to the sport's legacy.

Step 5 - FREE RESPONCE QUESTION:####
Based on the information provided in the context paragraph, explain how basketball promotes both physical skills and personal development. Include at least two examples from the paragraph to support your answer.
"""

EXAMPLE_GPT35_02 = """
Step 1:#### Define Common Core State Standard CCSS.ELA-LITERACY.W.4.9
The Common Core State Standard CCSS.ELA-LITERACY.W.4.9 states that fourth-grade students should be able to "draw evidence from literary or informational texts to support analysis, reflection, and research."

Step 2:#### Define Expected Length and Complexity of the CONTEXT Paragraph
The CONTEXT paragraph should be around 100-150 words and provide relevant information about the ocean that students can use to answer the free response question. It should include key facts and details about the ocean's characteristics, importance, and features.

Step 3:#### Define What Needs to be Tested in the Assessment
The assessment needs to test the student's ability to draw evidence from the provided context and use it to construct a coherent and informative response. The student should be able to analyze and explain the significance of the ocean based on the context paragraph.

Step 4 - CONTEXT:####
The ocean, covering more than 70% of the Earth's surface, is a vast and vital component of our planet. With its diverse ecosystems and complex marine life, the ocean plays a crucial role in regulating the Earth's climate and providing habitat for countless species. Its currents distribute heat around the globe, influencing weather patterns and supporting marine food chains. Additionally, the ocean serves as a source of inspiration, resources, and recreational opportunities for people worldwide.

Step 5 - FREE RESPONCE QUESTION:####
Based on the information provided in the context paragraph, explain the significance of the ocean to both the Earth's environment and human society. Include at least two specific ways in which the ocean impacts the climate and one example of how humans utilize the ocean's resources.
"""