PROMPT_DEFINITION = """What is common core standard {standard} definition?"""

PROMPT_1 = """Given the You need to create an assesment for a student consisting of:\
 1. context, 2. free response question, 3. rubic for evaluation.\
 Think step by step and provide context, free response question and the rubic.\
 Remember the assignmet must be according to CCSS.ELA-LITERACY.W.4.9 standard and use basketball topic."""


PROMPT_X = """You need to create an assesment for a student consisting of:\
 1. context, 2. free response question, 3. rubic for evaluation.\
 Think step by step and provide context, free response question and the rubic.\
 Remember the assignmet must be according to CCSS.ELA-LITERACY.W.4.9 standard and use basketball topic."""

PROMPT_RUBRIC = """Create a rubic for the CCSS.ELA-LITERACY.W.4.9 assesment"""

# sample combined input
# set 1
GPT4_SAMPLE_FRQ_INPUT_01 = """
You are an helpful assistant. User will provide you Common Core State Standard and a topic. \
You will output an assessment task for a student to test student knowledge consisting of:
 1. COTEXT: context paragraph that will be used by the student to answer the below free response question.\
 The COTEXT is a paragraph and must be related to topic provided by user. \
 The COTEXT must be sufficient to answer the free response question and meet complexity and length as expected by the Common Core State Standard definition provided by user.
 2. FREE RESPONSE QUESTION: The question must be related to the context article and test students ability as per the standard definition above.\

Follow these steps to create the task:

Step 1: Provide definition of Common Core State Standard provided by user

Step 2: Define what needs to be tested as part of assessment defined in steps 1 and make sure to include it in the CONTEXT and FREE RESPONSE QUESTION.

Step 3: Define what is the expected length and complexity of the CONTEXT paragraph that is provided to student

Step 4: Generate CONTEXT paragraph. It must meet the conditions defined in second and third step.

Step 5: Generate FREE RESPONSE QUESTION related to CONEXT and meeting definition in step one.

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":

```json
{
	"step-1": string  // step 1 reasoning
	"step-2": string  // step 2 reasoning
	"step-3": string  // step 3 reasoning
	"context": string  // generated context paragraph
	"frq": string  // generated free response question
}
```

Common Core State Standard is CCSS.ELA-LITERACY.W.4.9 and topic is ocean.

"""

GPT4_SAMPLE_FRQ_OUTPUT_01 = """{
	"step-1": "The Common Core State Standard CCSS.ELA-LITERACY.W.4.9 states that 4th-grade students should 'Draw evidence from literary or informational texts to support analysis, reflection, and research.'",
	"step-2": "The assessment will test the student's ability to extract information from a context paragraph related to the ocean. The student should then use this information to support their analysis or reflection in response to a specific free-response question.",
	"step-3": "For a 4th-grade level, the context paragraph should be between 100-150 words. It should contain a mix of factual and interpretive details, providing a well-rounded basis for answering the free-response question.",
	"context": "The ocean covers more than 70% of Earth's surface and serves as home to a myriad of creatures, from microscopic plankton to massive whales. It also plays a crucial role in regulating the planet's climate by absorbing carbon dioxide. Coral reefs, often referred to as the 'rainforests of the sea,' host a variety of marine life and contribute to biodiversity. However, human activities like pollution, overfishing, and climate change are putting ocean ecosystems at risk. Notable efforts are being made to conserve this vital resource, including the creation of marine protected areas and public awareness campaigns.",
	"frq": "Based on the context provided, what are some ways the ocean is important to Earth and its inhabitants? Also, what challenges are oceans facing according to the text? Provide evidence from the text to support your answer."
}"""

GPT4_SAMPLE_RUBRIC_INPUT_01 = """You are an helpful assistant. User will provide you Common Core State Standard. \
You will also be provided with CONTEXT and FREE RESPONSE QUESTION.
You will output a rubric for this assessment task as expected by the Common Core State Standard definition provided by user.

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":

```json
{
	"rubric": string  // Rubric for this assessment task as expected by the Common Core State Standard definition provided by user
}
```
Common Core State Standard is CCSS.ELA-LITERACY.W.4.9. Take into consideration the definition of this standard provided below in step-1.
CONTEXT and FREE RESPONSE QUESTION are included below: 
{
	"step-1": "The Common Core State Standard CCSS.ELA-LITERACY.W.4.9 states that 4th-grade students should 'Draw evidence from literary or informational texts to support analysis, reflection, and research.'",
	"step-2": "The assessment will test the student's ability to extract information from a context paragraph related to the ocean. The student should then use this information to support their analysis or reflection in response to a specific free-response question.",
	"step-3": "For a 4th-grade level, the context paragraph should be between 100-150 words. It should contain a mix of factual and interpretive details, providing a well-rounded basis for answering the free-response question.",
	"context": "The ocean covers more than 70% of Earth's surface and serves as home to a myriad of creatures, from microscopic plankton to massive whales. It also plays a crucial role in regulating the planet's climate by absorbing carbon dioxide. Coral reefs, often referred to as the 'rainforests of the sea,' host a variety of marine life and contribute to biodiversity. However, human activities like pollution, overfishing, and climate change are putting ocean ecosystems at risk. Notable efforts are being made to conserve this vital resource, including the creation of marine protected areas and public awareness campaigns.",
	"frq": "Based on the context provided, what are some ways the ocean is important to Earth and its inhabitants? Also, what challenges are oceans facing according to the text? Provide evidence from the text to support your answer."
}
"""
GPT4_SAMPLE_RUBRIC_OUTPUT_01 = """{
	"rubric": "### Assessment Rubric for Free Response Question\n\n#### Criteria for Evaluation\n\n1. **Drawing Evidence (5 points)**: Student must draw clear evidence from the context paragraph to support their answer.\n    - 5 points: Provides direct quotes or paraphrases that are highly relevant to the question.\n    - 3 points: Provides some evidence but it's either partially relevant or not directly quoted.\n    - 1 point: Makes a generalized or vague reference to the text.\n    - 0 points: Does not reference the text.\n\n2. **Analysis and Reflection (5 points)**: Student should analyze the importance of the ocean to Earth and its challenges, and may include personal reflection.\n    - 5 points: Thoroughly analyzes both the importance and challenges, possibly including personal reflection.\n    - 3 points: Partially analyzes either the importance or challenges, with some evidence.\n    - 1 point: Minimal analysis with limited or no evidence.\n    - 0 points: No analysis or reflection.\n\n3. **Clarity and Organization (3 points)**: Answer should be clear, concise, and well-organized.\n    - 3 points: Answer is clear, concise, and logically organized.\n    - 2 points: Answer is mostly clear but may lack some organization.\n    - 1 point: Answer is disorganized or unclear.\n    - 0 points: Answer is incomprehensible.\n\n4. **Grammar and Mechanics (2 points)**: The answer should be free of grammatical and spelling errors.\n    - 2 points: No errors.\n    - 1 point: Few minor errors.\n    - 0 points: Numerous errors that hinder comprehension.\n\n### Scoring Guide\n- 13-15 points: Excellent\n- 10-12 points: Good\n- 6-9 points: Needs Improvement\n- 0-5 points: Unsatisfactory"
}
"""

# set 2
GPT4_SAMPLE_FRQ_INPUT_02 = """
You are an helpful assistant. User will provide you Common Core State Standard and a topic. \
You will output an assessment task for a student to test student knowledge consisting of:
 1. COTEXT: context paragraph that will be used by the student to answer the below free response question.\
 The COTEXT is a paragraph and must be related to topic provided by user. \
 The COTEXT must be sufficient to answer the free response question and meet complexity and length as expected by the Common Core State Standard definition provided by user.
 2. FREE RESPONSE QUESTION: The question must be related to the context article and test students ability as per the standard definition above.\

Follow these steps to create the task:

Step 1: Provide definition of Common Core State Standard provided by user

Step 2: Define what needs to be tested as part of assessment defined in steps 1 and make sure to include it in the CONTEXT and FREE RESPONSE QUESTION.

Step 3: Define what is the expected length and complexity of the CONTEXT paragraph that is provided to student

Step 4: Generate CONTEXT paragraph. It must meet the conditions defined in second and third step.

Step 5: Generate FREE RESPONSE QUESTION related to CONEXT and meeting definition in step one.

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":

```json
{
	"step-1": string  // step 1 reasoning
	"step-2": string  // step 2 reasoning
	"step-3": string  // step 3 reasoning
	"context": string  // generated context paragraph
	"frq": string  // generated free response question
}
```

Common Core State Standard is CCSS.ELA-LITERACY.W.4.9 and topic is basketball.

"""

GPT4_SAMPLE_FRQ_OUTPUT_02 = """{
	"step-1": "The Common Core State Standard CCSS.ELA-LITERACY.W.4.9 states that students in 4th grade should 'Draw evidence from literary or informational texts to support analysis, reflection, and research.'",
	"step-2": "The task should assess the student's ability to extract relevant information from a context paragraph about basketball. The focus should be on their capacity to use this information to support analysis or reflection, as indicated by the standard. This could involve identifying key facts, events, or concepts and relating them to a specific question or prompt.",
	"step-3": "For a 4th-grade level, the context paragraph should be between 100-150 words. The paragraph should cover multiple aspects or elements of basketball and include a mix of factual and anecdotal details to provide a well-rounded basis for answering the free-response question.",
	"context": "Basketball is a widely-played sport that originated in the United States. The game's primary goal is to score by shooting a ball through the opponent's basketball hoop, which is elevated 10 feet above the floor. Teams consist of five players each, taking on roles like point guard, shooting guard, small forward, power forward, and center. Some of the greatest players in history, like Michael Jordan and LeBron James, have achieved incredible feats, from scoring game-winning shots to breaking records. Several leagues worldwide, such as the NBA in America and the EuroLeague in Europe, host tournaments that captivate millions of fans.",
	"frq": "How have basketball legends like Michael Jordan and LeBron James contributed to the sport's popularity, according to the context? Do you agree or disagree with this assessment based on your own knowledge or experiences? Provide evidence from the text to support your answer."
}"""

GPT4_SAMPLE_RUBRIC_INPUT_02 = """You are an helpful assistant. User will provide you Common Core State Standard. \
You will also be provided with CONTEXT and FREE RESPONSE QUESTION.
You will output a rubric for this assessment task as expected by the Common Core State Standard definition provided by user.

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":

```json
{
	"rubric": string  // Rubric for this assessment task as expected by the Common Core State Standard definition provided by user
}
```
Common Core State Standard is CCSS.ELA-LITERACY.W.4.9. Take into consideration the definition of this standard provided below in step-1.
CONTEXT and FREE RESPONSE QUESTION are included below: 
{
	"step-1": "The Common Core State Standard CCSS.ELA-LITERACY.W.4.9 states that students in 4th grade should 'Draw evidence from literary or informational texts to support analysis, reflection, and research.'",
	"step-2": "The task should assess the student's ability to extract relevant information from a context paragraph about basketball. The focus should be on their capacity to use this information to support analysis or reflection, as indicated by the standard. This could involve identifying key facts, events, or concepts and relating them to a specific question or prompt.",
	"step-3": "For a 4th-grade level, the context paragraph should be between 100-150 words. The paragraph should cover multiple aspects or elements of basketball and include a mix of factual and anecdotal details to provide a well-rounded basis for answering the free-response question.",
	"context": "Basketball is a widely-played sport that originated in the United States. The game's primary goal is to score by shooting a ball through the opponent's basketball hoop, which is elevated 10 feet above the floor. Teams consist of five players each, taking on roles like point guard, shooting guard, small forward, power forward, and center. Some of the greatest players in history, like Michael Jordan and LeBron James, have achieved incredible feats, from scoring game-winning shots to breaking records. Several leagues worldwide, such as the NBA in America and the EuroLeague in Europe, host tournaments that captivate millions of fans.",
	"frq": "How have basketball legends like Michael Jordan and LeBron James contributed to the sport's popularity, according to the context? Do you agree or disagree with this assessment based on your own knowledge or experiences? Provide evidence from the text to support your answer."
}
"""
GPT4_SAMPLE_RUBRIC_OUTPUT_02 = """{
	"rubric": "1. **Evidence Drawing**  \n- 4 points: The student accurately identifies multiple pieces of evidence from the text that support their analysis or reflection.\n- 3 points: The student identifies some relevant evidence but may miss some details that could strengthen their argument.\n- 2 points: The student mentions only one piece of evidence or the evidence provided is tangentially related to their argument.\n- 1 point: The student does not provide any evidence from the text.\n\n2. **Analysis and Reflection**  \n- 4 points: The student provides a thorough analysis or reflection that is deeply rooted in the text.\n- 3 points: The student's analysis or reflection is mostly consistent with the evidence but may lack depth.\n- 2 points: The student offers a superficial or partially relevant analysis or reflection.\n- 1 point: There is little to no analysis or reflection based on the text.\n\n3. **Relevance to the Question**  \n- 4 points: The student's answer is directly relevant to all aspects of the free-response question.\n- 3 points: The answer mostly addresses the question but may miss one minor aspect.\n- 2 points: The answer tangentially addresses the question but misses key aspects.\n- 1 point: The answer is not relevant to the free-response question.\n\n4. **Clarity and Organization**  \n- 4 points: The student's answer is clear, well-organized, and easy to follow.\n- 3 points: The answer is mostly clear but may have minor organizational issues.\n- 2 points: The answer lacks clarity and has some organizational problems.\n- 1 point: The answer is not clear or organized."
}"""

# set 3
GPT4_SAMPLE_FRQ_INPUT_03 = """
You are an helpful assistant. User will provide you Common Core State Standard and a topic. \
You will output an assessment task for a student to test student knowledge consisting of:
 1. COTEXT: context paragraph that will be used by the student to answer the below free response question.\
 The COTEXT is a paragraph and must be related to topic provided by user. \
 The COTEXT must be sufficient to answer the free response question and meet complexity and length as expected by the Common Core State Standard definition provided by user.
 2. FREE RESPONSE QUESTION: The question must be related to the context article and test students ability as per the standard definition above.\

Follow these steps to create the task:

Step 1: Provide definition of Common Core State Standard provided by user

Step 2: Define what needs to be tested as part of assessment defined in steps 1 and make sure to include it in the CONTEXT and FREE RESPONSE QUESTION.

Step 3: Define what is the expected length and complexity of the CONTEXT paragraph that is provided to student

Step 4: Generate CONTEXT paragraph. It must meet the conditions defined in second and third step.

Step 5: Generate FREE RESPONSE QUESTION related to CONEXT and meeting definition in step one.

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":

```json
{
	"step-1": string  // step 1 reasoning
	"step-2": string  // step 2 reasoning
	"step-3": string  // step 3 reasoning
	"context": string  // generated context paragraph
	"frq": string  // generated free response question
}
```

Common Core State Standard is CCSS.ELA-LITERACY.W.6.3 and topic is "morning routine".

"""

GPT4_SAMPLE_FRQ_OUTPUT_03 = """{
	"step-1": "The standard CCSS.ELA-LITERACY.W.6.3 requires students to write narratives to develop real or imagined experiences or events using effective technique, relevant descriptive details, and well-structured event sequences.",
	"step-2": "The assessment must test the student's ability to write a narrative that includes effective techniques, relevant descriptive details, and a well-structured event sequence.",
	"step-3": "The CONTEXT paragraph should be sufficiently detailed but not excessively long, providing enough complexity for a 6th-grade student to generate a narrative based on it.",
	"context": "Maria had a morning routine that she followed every single day. She would start her day by waking up to the sound of her melodious alarm at 6:30 a.m. After quickly turning it off, she'd head to the kitchen where her mom would already have a steaming cup of hot chocolate waiting for her. Next, she would grab her toothbrush and toothpaste and head to the bathroom to brush her teeth. The bathroom mirror would be slightly fogged up from her older brother's hot shower, making her trace smiley faces on it before wiping it clean. Once she was ready, she'd head to her room to put on her favorite outfit: a blue shirt with white stars, and jeans that had a small rip on the knee which, according to her, gave it character. After getting dressed, she would sit at her desk and skim through her planner to prepare for the day ahead, occasionally jotting down notes in the margins.",
	"frq": "Write a narrative from Maria's perspective about a particular morning where something unexpected happens during her routine. Use effective narrative techniques, integrate relevant descriptive details, and structure the events in a sequential manner. Make sure your narrative has a beginning, middle, and end. Include dialogue, internal thoughts, or actions that help to develop the characters and events."
}
"""

GPT4_SAMPLE_RUBRIC_INPUT_03 = """You are an helpful assistant. User will provide you Common Core State Standard. \
You will also be provided with CONTEXT and FREE RESPONSE QUESTION.
You will output a rubric for this assessment task as expected by the Common Core State Standard definition provided by user.

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":

```json
{
	"rubric": string  // Rubric for this assessment task as expected by the Common Core State Standard definition provided by user
}
```
Common Core State Standard is CCSS.ELA-LITERACY.W.6.3. Take into consideration the definition of this standard provided below in step-1.
CONTEXT and FREE RESPONSE QUESTION are also included in following JSON: 
{
	"step-1": "The standard CCSS.ELA-LITERACY.W.6.3 requires students to write narratives to develop real or imagined experiences or events using effective technique, relevant descriptive details, and well-structured event sequences.",
	"step-2": "The assessment must test the student's ability to write a narrative that includes effective techniques, relevant descriptive details, and a well-structured event sequence.",
	"step-3": "The CONTEXT paragraph should be sufficiently detailed but not excessively long, providing enough complexity for a 6th-grade student to generate a narrative based on it.",
	"context": "Maria had a morning routine that she followed every single day. She would start her day by waking up to the sound of her melodious alarm at 6:30 a.m. After quickly turning it off, she'd head to the kitchen where her mom would already have a steaming cup of hot chocolate waiting for her. Next, she would grab her toothbrush and toothpaste and head to the bathroom to brush her teeth. The bathroom mirror would be slightly fogged up from her older brother's hot shower, making her trace smiley faces on it before wiping it clean. Once she was ready, she'd head to her room to put on her favorite outfit: a blue shirt with white stars, and jeans that had a small rip on the knee which, according to her, gave it character. After getting dressed, she would sit at her desk and skim through her planner to prepare for the day ahead, occasionally jotting down notes in the margins.",
	"frq": "Write a narrative from Maria's perspective about a particular morning where something unexpected happens during her routine. Use effective narrative techniques, integrate relevant descriptive details, and structure the events in a sequential manner. Make sure your narrative has a beginning, middle, and end. Include dialogue, internal thoughts, or actions that help to develop the characters and events."
}
"""
GPT4_SAMPLE_RUBRIC_OUTPUT_03 = """{
	"rubric": "1. Effective Techniques (0-10 points): 0-2 points for lacking effective techniques, 3-5 for some use, 6-8 for good use, and 9-10 for excellent use.\n2. Relevant Descriptive Details (0-10 points): 0-2 points for lacking details, 3-5 for some details, 6-8 for good details, and 9-10 for excellent details.\n3. Well-Structured Event Sequences (0-10 points): 0-2 for poor structure, 3-5 for some structure, 6-8 for good structure, and 9-10 for excellent structure.\n4. Dialogue, Internal Thoughts, Actions to Develop Characters and Events (0-5 points): 0-1 for lacking elements, 2-3 for some use, and 4-5 for effective use.\n5. Beginning, Middle, and End (0-5 points): 0-1 for missing or unclear, 2-3 for present but lacking, and 4-5 for clear and effective."
}
"""

# OLD - to be deleted -----------------------------------
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

Step 5 - FREE RESPONSE QUESTION:####
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

Step 5 - FREE RESPONSE QUESTION:####
Based on the information provided in the context paragraph, explain the significance of the ocean to both the Earth's environment and human society. Include at least two specific ways in which the ocean impacts the climate and one example of how humans utilize the ocean's resources.
"""