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

# TEST - QA

GPT4_SAMPLE_RUBRIC_QA_INPUT_01 = """
You are an helpfull assistant. User will provide you Common Core State Standard (CCSS). \
You will also be provided with RUBRICS related to the CCSS.
You will evaluate if provided RUBRICS meets the provided CCSS requirements i.e. if it is covering expected skills and competencies outlined by the provided CCSS standard itself.
If the RUBRICS meets or mostly meets the CCSS requirements you will output "True". Otherwise output False. You must use below format:
```json
{
	"rubric_qa_passed": string  // Boolean value to idicate if the RUBRIC is meeting the Common Core State Standard provided by user. True = meets, False = Does not meet
	"rubric_qa_reason": string  // Justification why RUBRICS is or isnt meeting Common Core State Standard
}
```
Common Core State Standard is CCSS.ELA-LITERACY.W.4.9. Rubrics to be evaluated is in JSON format: 
```json\n{\n\t\"rubric\": \"### Assessment Rubric for Free Response Question\n\n#### Criteria for Evaluation\n\n1. **Drawing Evidence (5 points)**: Student must draw clear evidence from the context paragraph to support their answer.\n    - 5 points: Provides direct quotes or paraphrases that are highly relevant to the question.\n    - 3 points: Provides some evidence but it's either partially relevant or not directly quoted.\n    - 1 point: Makes a generalized or vague reference to the text.\n    - 0 points: Does not reference the text.\n\n2. **Analysis and Reflection (5 points)**: Student should analyze the adaptations of desert animals and plants and the threats to desert ecosystems, and may include personal reflection.\n    - 5 points: Thoroughly analyzes both the adaptations and threats, possibly including personal reflection.\n    - 3 points: Partially analyzes either the adaptations or threats, with some evidence.\n    - 1 point: Minimal analysis with limited or no evidence.\n    - 0 points: No analysis or reflection.\n\n3. **Clarity and Organization (3 points)**: Answer should be clear, concise, and well-organized.\n    - 3 points: Answer is clear, concise, and logically organized.\n    - 2 points: Answer is mostly clear but may lack some organization.\n    - 1 point: Answer is disorganized or unclear.\n    - 0 points: Answer is incomprehensible.\n\n4. **Grammar and Mechanics (2 points)**: The answer should be free of grammatical and spelling errors.\n    - 2 points: No errors.\n    - 1 point: Few minor errors.\n    - 0 points: Numerous errors that hinder comprehension.\n\n### Scoring Guide\n- 13-15 points: Excellent\n- 10-12 points: Good\n- 6-9 points: Needs Improvement\n- 0-5 points: Unsatisfactory\"\n}\n```
"""

GPT4_SAMPLE_RUBRIC_QA_OUTPUT_01 = """
{
	"rubric_qa_passed": "True",
	"rubric_qa_reason": "The rubric covers drawing evidence and analysis, which align directly with the expectations outlined in CCSS.ELA-LITERACY.W.4.9. Although it includes additional criteria like clarity and grammar that are not explicitly mentioned in the standard, these are consistent with broader CCSS writing competencies."
}"""


# AI Student prompts - GPT 4
# SET 1 - EXCELLENT
# system
"""
You are a student completing the Common Core State Standard assessment: CCSS.ELA-LITERACY.W.4.9\
The assessment consists of: context, free response question (FRQ) and rubrics. \
You need to read the CONTEXT respond to FRQ. \
Work in this order: 
1. Define what grade student you should pretend be to based on the standard. 
2. Understand how a student of this grade would answer. Remember student grade will impact complexity and lenght of the answer, amogh other aspects of your answer.
3. You must answer in a way a student of this grade would to achieve EXCELLENT score. Review the Rubrics to plan the answer.
3. Respond to FRQ using the CONTEXT as instructed. 

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":

```json
{
	"Answer": string  // Your answer to the FRQ pretending to be a student.
}
```
"""
# input
"""
Context: New Zealand is a country located in the southwestern Pacific Ocean. It is made up of two main islands, the North Island and the South Island, as well as many smaller islands. The indigenous people of New Zealand are the Maori, who arrived in the country more than 1,000 years ago. Today, Maori culture is an important part of New Zealand's identity. The country is known for its stunning natural scenery, which includes mountains, beaches, and geothermal features. New Zealand is also home to many unique animals, such as the kiwi bird and the tuatara lizard.
----------------------------------------------
Free responce queistion: Based on the context provided, what are some unique features of New Zealand? How does the Maori culture contribute to the country's identity? Use evidence from the text to support your answer.
----------------------------------------------
Rubrics: : "### Assessment Rubric for Free Response Question

#### Criteria for Evaluation

1. **Drawing Evidence (5 points)**: Student must draw clear evidence from the context paragraph to support their answer.
    - 5 points: Provides direct quotes or paraphrases that are highly relevant to the question.
    - 3 points: Provides some evidence but it's either partially relevant or not directly quoted.
    - 1 point: Makes a generalized or vague reference to the text.
    - 0 points: Does not reference the text.

2. **Analysis and Reflection (5 points)**: Student should analyze the unique features of New Zealand and how Maori culture contributes to the country's identity.
    - 5 points: Thoroughly analyzes both the unique features and the contribution of Maori culture, possibly including personal reflection.
    - 3 points: Partially analyzes either the unique features or the contribution of Maori culture, with some evidence.
    - 1 point: Minimal analysis with limited or no evidence.
    - 0 points: No analysis or reflection.

3. **Clarity and Organization (3 points)**: Answer should be clear, concise, and well-organized.
    - 3 points: Answer is clear, concise, and logically organized.
    - 2 points: Answer is mostly clear but may lack some organization.
    - 1 point: Answer is disorganized or unclear.
    - 0 points: Answer is incomprehensible.

4. **Grammar and Mechanics (2 points)**: The answer should be free of grammatical and spelling errors.
    - 2 points: No errors.
    - 1 point: Few minor errors.
    - 0 points: Numerous errors that hinder comprehension.

### Scoring Guide
- 13-15 points: Excellent
- 10-12 points: Good
- 6-9 points: Needs Improvement
- 0-5 points: Unsatisfactory
"""

# Answer - EXCELLENT
{
	"Answer": "New Zealand is an amazing place with lots of special things. First, it has really 'stunning natural scenery.' That means it has cool mountains and pretty beaches. You can even see things that come out of the ground like hot springs! Another thing that's special are the animals. New Zealand has 'kiwi bird and the tuatara lizard,' which are animals you can't find anywhere else. That's super cool!\n\nThe Maori people are a big part of what makes New Zealand special. They 'arrived in the country more than 1,000 years ago.' And now, 'Maori culture is an important part of New Zealand's identity.' That means they help make the country what it is, like how they celebrate and what they believe in.\n\nSo, to sum it up, New Zealand is unique because of its beautiful nature, special animals, and the Maori culture. All these things make New Zealand a place like no other!"
}

# Answer - Good
{
	"Answer": "New Zealand has some cool things that make it special. The place has awesome nature like 'mountains, beaches, and geothermal features.' I think that means stuff like hot springs. It also has cool animals like the kiwi bird and tuatara lizard. These animals are only in New Zealand!\n\nThe Maori people are also important there. They came 'more than 1,000 years ago' and their culture is a big part of New Zealand now. So they help make New Zealand special with their own ways and traditions.\n\nSo, New Zealand has pretty nature, unique animals, and the Maori people make it even more special. It's a pretty interesting place to know about!"
}

# AI Teacher prompts - GPT 4
# SET 1
# system
"""
You are a teacher evaluating students answer to the Common Core State Standard assessment. \
The assessment consists of: context, free response question (FRQ) and rubric. \
You need to understand the CONTEXT, FRQ and RUBRIC. \
You need to evaluate the ANSWER using the RUBRIC \
Work in this order: 
1. Evaluate ANSWER using the RUBRIC. Evaluate the ANSWER by each RUBRIC section.
2. Ensure the ANSWER is related to FRQ and CONTEXT as expected by RUBRIC
3. Output what is the written evaluation feedback to student. Include what was good and what needs an improvement. Write in a posive helpful tone.
4. Output total achieved score
5. Output maximum possible score

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":

```json
{
	"Written_eval": string  // Written evaluation feedback to student
    "Score": int // Score achieved by student
    "Score_max" : int // Maximum score possible for this assessment
}
```
"""
"""
Context: New Zealand is a country located in the southwestern Pacific Ocean. It is made up of two main islands, the North Island and the South Island, as well as many smaller islands. The indigenous people of New Zealand are the Maori, who arrived in the country more than 1,000 years ago. Today, Maori culture is an important part of New Zealand's identity. The country is known for its stunning natural scenery, which includes mountains, beaches, and geothermal features. New Zealand is also home to many unique animals, such as the kiwi bird and the tuatara lizard.
----------------------------------------------
Free responce queistion (FRQ): Based on the context provided, what are some unique features of New Zealand? How does the Maori culture contribute to the country's identity? Use evidence from the text to support your answer.
----------------------------------------------
Rubric: : "### Assessment Rubric for Free Response Question

#### Criteria for Evaluation

1. **Drawing Evidence (5 points)**: Student must draw clear evidence from the context paragraph to support their answer.
    - 5 points: Provides direct quotes or paraphrases that are highly relevant to the question.
    - 3 points: Provides some evidence but it's either partially relevant or not directly quoted.
    - 1 point: Makes a generalized or vague reference to the text.
    - 0 points: Does not reference the text.

2. **Analysis and Reflection (5 points)**: Student should analyze the unique features of New Zealand and how Maori culture contributes to the country's identity.
    - 5 points: Thoroughly analyzes both the unique features and the contribution of Maori culture, possibly including personal reflection.
    - 3 points: Partially analyzes either the unique features or the contribution of Maori culture, with some evidence.
    - 1 point: Minimal analysis with limited or no evidence.
    - 0 points: No analysis or reflection.

3. **Clarity and Organization (3 points)**: Answer should be clear, concise, and well-organized.
    - 3 points: Answer is clear, concise, and logically organized.
    - 2 points: Answer is mostly clear but may lack some organization.
    - 1 point: Answer is disorganized or unclear.
    - 0 points: Answer is incomprehensible.

4. **Grammar and Mechanics (2 points)**: The answer should be free of grammatical and spelling errors.
    - 2 points: No errors.
    - 1 point: Few minor errors.
    - 0 points: Numerous errors that hinder comprehension.

### Scoring Guide
- 13-15 points: Excellent
- 10-12 points: Good
- 6-9 points: Needs Improvement
- 0-5 points: Unsatisfactory
"""

# Answer - EXCELLENT
{
	"Answer": "New Zealand is an amazing place with lots of special things. First, it has really 'stunning natural scenery.' That means it has cool mountains and pretty beaches. You can even see things that come out of the ground like hot springs! Another thing that's special are the animals. New Zealand has 'kiwi bird and the tuatara lizard,' which are animals you can't find anywhere else. That's super cool!\n\nThe Maori people are a big part of what makes New Zealand special. They 'arrived in the country more than 1,000 years ago.' And now, 'Maori culture is an important part of New Zealand's identity.' That means they help make the country what it is, like how they celebrate and what they believe in.\n\nSo, to sum it up, New Zealand is unique because of its beautiful nature, special animals, and the Maori culture. All these things make New Zealand a place like no other!"
}

# Eval - EXCELLENT
{
	"Written_eval": "Great job on your assessment! You've done an excellent job drawing evidence from the text to support your statements, which were both clear and logically organized. While you've touched on both the unique features of New Zealand and how the Maori culture contributes to its identity, you could aim to deepen your analysis in the future. This will add richness to your answers and make them even more engaging. Keep up the good work!",
	"Score": 14,
	"Score_max": 15
}

# Answer - Good
{
	"Answer": "New Zealand has some cool things that make it special. The place has awesome nature like 'mountains, beaches, and geothermal features.' I think that means stuff like hot springs. It also has cool animals like the kiwi bird and tuatara lizard. These animals are only in New Zealand!\n\nThe Maori people are also important there. They came 'more than 1,000 years ago' and their culture is a big part of New Zealand now. So they help make New Zealand special with their own ways and traditions.\n\nSo, New Zealand has pretty nature, unique animals, and the Maori people make it even more special. It's a pretty interesting place to know about!"
}

# Eval - Good
{
	"Written_eval": "Well done on your assessment! You did an excellent job drawing evidence from the provided context to support your statements. Your analysis covers the unique features of New Zealand and the Maori culture, although you could aim to deepen this analysis in the future. Your answer is clearly structured and free of grammatical errors. Keep up the fantastic work!",
	"Score": 14,
	"Score_max": 15
}

# Answer - my mix poor
{
	"Answer": "New Zealand is an amazing place.  it has really nice nature. That means it has nice mountains and nice baches. You can even see nice things! Animals are nicer too. New Zaeland has all kinds of animals. That's super cool!\n\nThe Maori live there. They arrived some time ago. they like to celebrate. \n\nSo, to sum it up, New Zealand is beautiful nature, special animals, and the Maori people.!"
}

# Eval - my mix
{
	"Written_eval": "Thank you for submitting your assessment. It's evident that you find New Zealand to be an interesting and beautiful place. To improve, try to directly reference evidence from the provided text, add more depth to your analysis, and carefully proofread for grammar and spelling. Keep trying, and I'm sure you'll do better next time!",
	"Score": 3,
	"Score_max": 15
}

## QA
# set 1
system_message = """
You are an helpful assistant. User will provide you Common Core State Standard (CCSS) and a topic. \
        You will also be provided with CONTEXT paragraph and Free Response Question (FRQ).
        You will evaluate if provided CONTEXT and FRQ are meeting the CCSS requirements, i.e. if it allignes with skills and competencies outlined by the provided CCSS standard itself.

        Follow these steps to complete the task:
        1. Understand the provided CCSS definition, skills and competencies it should test
        2. Understand the expected CONTEXT complexity, lenght and topic
        3. Validate if CONTEXT broadly meets the CCSS requirements.
        4. Validate if FRQ broadly meets the requirements and is relevant to the CONTEXT

        If the CONTEXT meets or mostly meets the CCSS requirements you will output "True". Otherwise output "False" in field context_qa_passed.
        If the FRQ meets or mostly meets the CCSS requirements you will output "True". Otherwise output "False" in field frq_qa_passed.
        In case you respond "False" also provide justification what is missing or is incorrect.

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":
```json
{
	"context_qa_passed": string  // Boolean value to idicate if the COTEXT is meeting the Common Core State Standard provided by user. True = meets, False = Does not meet
    "context_qa_reason": string  // Justification why COTEXT is or isnt meeting Common Core State Standard
    "frq_qa_passed": string  // Boolean value to idicate if the FRQ is meeting the Common Core State Standard provided by user. True = meets, False = Does not meet
	"frq_qa_reason": string  // Justification why FRQ is or isnt meeting Common Core State Standard
}
```
User inputs are in following JSON:
{
	"standard": "CCSS.ELA-LITERACY.W.4.9",
	"topic": "Basketball",
	"context": "Basketball is a game that is played with a ball and two hoops. It is a popular sport around the world and can be played indoors or outdoors. The game is usually played with two teams of five players each, who try to score points by throwing the ball into the opposing team's hoop. The team with the most points at the end of the game wins. Basketball players need to be quick, agile, and have good hand-eye coordination. They also need to be able to work well with their teammates and have good sportsmanship. Some of the most famous basketball players include Michael Jordan, LeBron James, and Kobe Bryant.",
	"frq": "What are some of the key skills and qualities that basketball players need to have in order to be successful? Provide evidence from the context to support your answer."
}

"""

QA_FRQ_EXAMPLE_01 = """
User inputs are in following JSON:
{
	"standard": "CCSS.ELA-LITERACY.W.4.9",
	"topic": "Basketball",
	"context": "Basketball is a game that is played with a ball and two hoops. It is a popular sport around the world and can be played indoors or outdoors. The game is usually played with two teams of five players each, who try to score points by throwing the ball into the opposing team's hoop. The team with the most points at the end of the game wins. Basketball players need to be quick, agile, and have good hand-eye coordination. They also need to be able to work well with their teammates and have good sportsmanship. Some of the most famous basketball players include Michael Jordan, LeBron James, and Kobe Bryant.",
	"frq": "What are some of the key skills and qualities that basketball players need to have in order to be successful? Provide evidence from the context to support your answer.",
}
Assistant answer:
{
	"context_qa_passed": "True",
    "context_qa_reason": "The context is appropriate for a 4th-grade level and provides sufficient information on the topic of basketball for students to extract evidence for answering the FRQ.",
    "frq_qa_passed": "True",
	"frq_qa_reason": "The FRQ directly aligns with the CCSS.ELA-LITERACY.W.4.9 standard, as it asks students to draw evidence from the provided text to support their analysis."
}
"""

# set 2
system_message = """
You are an helpful assistant. User will provide you Common Core State Standard (CCSS) and a topic. \
You will also be provided with CONTEXT paragraph and Free Response Question (FRQ).
You will evaluate if provided CONTEXT and FRQ are meeting the CCSS requirements, i.e. if it aligns with skills and competencies outlined by the provided CCSS standard itself.

        Follow these steps to complete the task:
        1. Understand the provided CCSS definition, skills and competencies it should test
        2. Understand the expected CONTEXT complexity, length and topic
        3. Validate if CONTEXT broadly meets the CCSS requirements.
        4. Validate if FRQ broadly meets the requirements and is relevant to the CONTEXT

        If the CONTEXT meets or mostly meets the CCSS requirements you will output "True". Otherwise output "False" in field context_qa_passed.
        If the FRQ meets or mostly meets the CCSS requirements you will output "True". Otherwise output "False" in field frq_qa_passed.
        Also provide reason (justification) for both True and False.

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":
```json
{
	"context_qa_passed": string  // Boolean value to indicate if the COTEXT is meeting the Common Core State Standard provided by user. True = meets, False = Does not meet
    "context_qa_reason": string  // Justification why COTEXT is or isnt meeting Common Core State Standard
    "frq_qa_passed": string  // Boolean value to indicate if the FRQ is meeting the Common Core State Standard provided by user. True = meets, False = Does not meet
	"frq_qa_reason": string  // Justification why FRQ is or isnt meeting Common Core State Standard
}
```
User inputs are in following JSON:
{
	"standard": "CCSS.ELA-LITERACY.W.6.3",
	"topic": "An unexpected encounter at Waterloo Station",
	"context": "It was a typical morning at Waterloo Station in London, with commuters rushing to catch their trains and travelers dragging their luggage to the platforms. As I was making my way through the crowds, I suddenly felt something bump into me. I turned around to see a man in his mid-thirties, who looked just as surprised as I was. He apologized and explained that he was in a hurry to catch his train to Paris. We struck up a conversation, and I learned that he was a professor of history at a university in Paris. He was in London for a conference, and we discovered that we shared a love for history. As we chatted, I couldn't help but notice the interesting details about his appearance - a small scar above his left eyebrow, a vintage watch on his wrist, and a distinct accent that I couldn't place. Before I knew it, his train arrived, and he had to hurry to catch it. As he disappeared into the crowd, I couldn't help but feel that this unexpected encounter was something special.",
	"frq": "Write a narrative about the unexpected encounter at Waterloo Station from the perspective of either the protagonist or the history professor. Your narrative should have a beginning, middle, and end. Make sure to use effective narrative techniques, relevant descriptive details, and structure the events in a sequential manner."
}

"""


QA_FRQ_EXAMPLE_02 = """
User inputs are in following JSON:
{
	"standard": "CCSS.ELA-LITERACY.W.6.3",
	"topic": "An unexpected encounter at Waterloo Station",
	"context": "It was a typical morning at Waterloo Station in London, with commuters rushing to catch their trains and travelers dragging their luggage to the platforms. As I was making my way through the crowds, I suddenly felt something bump into me. I turned around to see a man in his mid-thirties, who looked just as surprised as I was. He apologized and explained that he was in a hurry to catch his train to Paris. We struck up a conversation, and I learned that he was a professor of history at a university in Paris. He was in London for a conference, and we discovered that we shared a love for history. As we chatted, I couldn't help but notice the interesting details about his appearance - a small scar above his left eyebrow, a vintage watch on his wrist, and a distinct accent that I couldn't place. Before I knew it, his train arrived, and he had to hurry to catch it. As he disappeared into the crowd, I couldn't help but feel that this unexpected encounter was something special.",
	"frq": "Write a narrative about the unexpected encounter at Waterloo Station from the perspective of either the protagonist or the history professor. Your narrative should have a beginning, middle, and end. Make sure to use effective narrative techniques, relevant descriptive details, and structure the events in a sequential manner."
}
Assistant answer:
{
	"context_qa_passed": "True",
    "context_qa_reason": "The CONTEXT describes an unexpected encounter at Waterloo Station in a detailed and sequential manner, providing ample material for narrative writing, thus meeting the CCSS W.6.3 standard.",
    "frq_qa_passed": "True",
	"frq_qa_reason": "The FRQ instructs students to write a narrative using effective techniques, relevant details, and a structured event sequence, which aligns well with the requirements of CCSS W.6.3."
}
"""


# set 3 
"""
You are an helpful assistant. User will provide you Common Core State Standard (CCSS) and a topic. \
You will also be provided with CONTEXT paragraph and Free Response Question (FRQ).
You will evaluate if provided CONTEXT and FRQ are meeting the CCSS requirements, i.e. if it aligns with skills and competencies outlined by the provided CCSS standard itself.

        Follow these steps to complete the task:
        1. Understand the provided CCSS definition, skills and competencies it should test
        2. Understand the expected CONTEXT complexity, length and topic
        3. Validate if CONTEXT broadly meets the CCSS requirements.
        4. Validate if FRQ broadly meets the requirements and is relevant to the CONTEXT

        If the CONTEXT meets or mostly meets the CCSS requirements you will output "True". Otherwise output "False" in field context_qa_passed.
        If the FRQ meets or mostly meets the CCSS requirements you will output "True". Otherwise output "False" in field frq_qa_passed.
        Also provide reason (justification) for both True and False.

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":
```json
{
	"context_qa_passed": string  // Boolean value to indicate if the COTEXT is meeting the Common Core State Standard provided by user. True = meets, False = Does not meet
    "context_qa_reason": string  // Justification why COTEXT is or isnt meeting Common Core State Standard
    "frq_qa_passed": string  // Boolean value to indicate if the FRQ is meeting the Common Core State Standard provided by user. True = meets, False = Does not meet
	"frq_qa_reason": string  // Justification why FRQ is or isnt meeting Common Core State Standard
}
```
User inputs are in following JSON:
{
	"standard": "CCSS.ELA-LITERACY.W.4.4",
	"topic": "New Zealand",
	"context": "New Zealand, located in the southwestern Pacific Ocean, is a land of stunning natural beauty and diverse wildlife. The country is made up of two main islands, the North Island and the South Island, and several smaller islands. The landscape is characterized by rugged mountains, lush forests, and pristine beaches. New Zealand is home to many unique and endemic species, such as the kiwi bird, the tuatara reptile, and the kakapo parrot. The country has a rich Maori culture, which is evident in its art, language, and traditions. New Zealand is also known for its adventure tourism, with activities such as bungee jumping, skydiving, and white water rafting attracting visitors from around the world.",
	"frq": "Write a short article about New Zealand. Your text should describe the country's geography, wildlife, culture, and tourism.",
}"""



QA_FRQ_EXAMPLE_03 = """
User inputs are in following JSON:
{
	"standard": "CCSS.ELA-LITERACY.W.4.4",
	"topic": "New Zealand",
	"context": "New Zealand, located in the southwestern Pacific Ocean, is a land of stunning natural beauty and diverse wildlife. The country is made up of two main islands, the North Island and the South Island, and several smaller islands. The landscape is characterized by rugged mountains, lush forests, and pristine beaches. New Zealand is home to many unique and endemic species, such as the kiwi bird, the tuatara reptile, and the kakapo parrot. The country has a rich Maori culture, which is evident in its art, language, and traditions. New Zealand is also known for its adventure tourism, with activities such as bungee jumping, skydiving, and white water rafting attracting visitors from around the world.",
	"frq": "Write a short article about New Zealand. Your text should describe the country's geography, wildlife, culture, and tourism.",
}
Assistant answer:
{
	"context_qa_passed": "True",
    "context_qa_reason": "The CONTEXT is well-developed, organized, and appropriate for a fourth-grade audience, which aligns with the requirements of CCSS.ELA-LITERACY.W.4.4.",
    "frq_qa_passed": "False",
	"frq_qa_reason": "While the FRQ covers the topics mentioned in the CONTEXT and allows room for development and organization, it does not specify that the writing should be suitable for a fourth-grade audience in terms of development, organization, and style, which is a requirement of CCSS.ELA-LITERACY.W.4.4."
}
"""

test = """
You are an helpful assistant. User will provide you Common Core State Standard (CCSS) and a topic. \
        You will also be provided with CONTEXT paragraph and Free Response Question (FRQ).
        You will evaluate if provided CONTEXT and FRQ are meeting the CCSS requirements, i.e. if it allignes with skills and competencies outlined by the provided CCSS standard itself.

        Follow these steps to complete the task:
        1. Understand the provided CCSS definition, skills and competencies it should test
        2. Understand the expected CONTEXT complexity, lenght and topic
        3. Validate if CONTEXT broadly meets the CCSS requirements.
        4. Validate if FRQ broadly meets the requirements and is relevant to the CONTEXT

        If the CONTEXT meets or mostly meets the CCSS requirements you will output "True". Otherwise output "False" in field context_qa_passed.
        If the FRQ meets or mostly meets the CCSS requirements you will output "True". Otherwise output "False" in field frq_qa_passed.
        In case you respond "False" also provide justification what is missing or is incorrect.

The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":
```json
{
	"context_qa_passed": string  // Boolean value to idicate if the COTEXT is meeting the Common Core State Standard provided by user. True = meets, False = Does not meet
    "context_qa_reason": string  // Justification why COTEXT is or isnt meeting Common Core State Standard
    "frq_qa_passed": string  // Boolean value to idicate if the FRQ is meeting the Common Core State Standard provided by user. True = meets, False = Does not meet
	"frq_qa_reason": string  // Justification why FRQ is or isnt meeting Common Core State Standard
}
```

Here are two examples of good answer:
############
EXAMPLE 1:
User inputs are in following JSON:
{
	"standard": "CCSS.ELA-LITERACY.W.4.4",
	"topic": "New Zealand",
	"context": "New Zealand, located in the southwestern Pacific Ocean, is a land of stunning natural beauty and diverse wildlife. The country is made up of two main islands, the North Island and the South Island, and several smaller islands. The landscape is characterized by rugged mountains, lush forests, and pristine beaches. New Zealand is home to many unique and endemic species, such as the kiwi bird, the tuatara reptile, and the kakapo parrot. The country has a rich Maori culture, which is evident in its art, language, and traditions. New Zealand is also known for its adventure tourism, with activities such as bungee jumping, skydiving, and white water rafting attracting visitors from around the world.",
	"frq": "Write a short article about New Zealand. Your text should describe the country's geography, wildlife, culture, and tourism.",
}
Assistant answer:
{
	"context_qa_passed": "True",
    "context_qa_reason": "The CONTEXT is well-developed, organized, and appropriate for a fourth-grade audience, which aligns with the requirements of CCSS.ELA-LITERACY.W.4.4.",
    "frq_qa_passed": "False",
	"frq_qa_reason": "While the FRQ covers the topics mentioned in the CONTEXT and allows room for development and organization, it does not specify that the writing should be suitable for a fourth-grade audience in terms of development, organization, and style, which is a requirement of CCSS.ELA-LITERACY.W.4.4."
}
############
EXAMPLE 2:
User inputs are in following JSON:
{
	"standard": "CCSS.ELA-LITERACY.W.4.9",
	"topic": "Basketball",
	"context": "Basketball is a game that is played with a ball and two hoops. It is a popular sport around the world and can be played indoors or outdoors. The game is usually played with two teams of five players each, who try to score points by throwing the ball into the opposing team's hoop. The team with the most points at the end of the game wins. Basketball players need to be quick, agile, and have good hand-eye coordination. They also need to be able to work well with their teammates and have good sportsmanship. Some of the most famous basketball players include Michael Jordan, LeBron James, and Kobe Bryant.",
	"frq": "What are some of the key skills and qualities that basketball players need to have in order to be successful? Provide evidence from the context to support your answer.",
}
Assistant answer:
{
	"context_qa_passed": "True",
    "context_qa_reason": "The context is appropriate for a 4th-grade level and provides sufficient information on the topic of basketball for students to extract evidence for answering the FRQ.",
    "frq_qa_passed": "True",
	"frq_qa_reason": "The FRQ directly aligns with the CCSS.ELA-LITERACY.W.4.9 standard, as it asks students to draw evidence from the provided text to support their analysis."
}
############

User inputs are in following JSON:
{
	"standard": "CCSS.ELA-LITERACY.W.4.9",
	"topic": "Basketball",
	"context": "Basketball is a game that is played with a ball and two hoops. It is a popular sport around the world and can be played indoors or outdoors. The game is usually played with two teams of five players each, who try to score points by throwing the ball into the opposing team's hoop. The team with the most points at the end of the game wins. Basketball players need to be quick, agile, and have good hand-eye coordination. They also need to be able to work well with their teammates and have good sportsmanship. Some of the most famous basketball players include Michael Jordan, LeBron James, and Kobe Bryant.",
	"frq": "What are some of the key skills and qualities that basketball players need to have in order to be successful? Provide evidence from the context to support your answer."
}
"""

answer_gpt4 = """
{
	"context_qa_passed": "True",
    "context_qa_reason": "The context is appropriate for a 4th-grade level and provides sufficient information on the topic of basketball for students to extract evidence for answering the FRQ.",
    "frq_qa_passed": "True",
	"frq_qa_reason": "The FRQ directly aligns with the CCSS.ELA-LITERACY.W.4.9 standard, as it asks students to draw evidence from the provided text to support their analysis."
}

"""
