# 
#  This file contains few-shot prompt examples for the CCSS_Assessmenet_Generator.py 
#  Examples are generated by GPT4 and validated by human
# 

# Free responce question and context examples 
EXAMPLE_FRQ_01 = """User input: Common Core State Standard is CCSS.ELA-LITERACY.W.6.3 and topic is "morning routine".
Assistant answer: ```json{
    "step-1": "The standard CCSS.ELA-LITERACY.W.6.3 requires students to write narratives to develop real or imagined experiences or events using effective technique, relevant descriptive details, and well-structured event sequences.",
    "step-2": "The assessment must test the student's ability to write a narrative that includes effective techniques, relevant descriptive details, and a well-structured event sequence.",
    "step-3": "The CONTEXT paragraph should be sufficiently detailed but not excessively long, providing enough complexity for a 6th-grade student to generate a narrative based on it.",
    "context": "Maria had a morning routine that she followed every single day. She would start her day by waking up to the sound of her melodious alarm at 6:30 a.m. After quickly turning it off, she'd head to the kitchen where her mom would already have a steaming cup of hot chocolate waiting for her. Next, she would grab her toothbrush and toothpaste and head to the bathroom to brush her teeth. The bathroom mirror would be slightly fogged up from her older brother's hot shower, making her trace smiley faces on it before wiping it clean. Once she was ready, she'd head to her room to put on her favorite outfit: a blue shirt with white stars, and jeans that had a small rip on the knee which, according to her, gave it character. After getting dressed, she would sit at her desk and skim through her planner to prepare for the day ahead, occasionally jotting down notes in the margins.",
    "frq": "Write a narrative about Maria's morning routine from her perspective. Your narrative should have a beginning, middle, and end. Make sure to use effective narrative techniques, relevant descriptive details, and structure the events in a sequential manner."
}```"""

EXAMPLE_FRQ_02 = """User input: Common Core State Standard is CCSS.ELA-LITERACY.W.4.9 and topic is ocean.
Assistant answer: ```json{
    "step-1": "The Common Core State Standard CCSS.ELA-LITERACY.W.4.9 states that 4th-grade students should 'Draw evidence from literary or informational texts to support analysis, reflection, and research.'",
    "step-2": "The assessment will test the student's ability to extract information from a context paragraph related to the ocean. The student should then use this information to support their analysis or reflection in response to a specific free-response question.",
    "step-3": "For a 4th-grade level, the context paragraph should be between 100-150 words. It should contain a mix of factual and interpretive details, providing a well-rounded basis for answering the free-response question.",
    "context": "The ocean covers more than 70% of Earth's surface and serves as home to a myriad of creatures, from microscopic plankton to massive whales. It also plays a crucial role in regulating the planet's climate by absorbing carbon dioxide. Coral reefs, often referred to as the 'rainforests of the sea,' host a variety of marine life and contribute to biodiversity. However, human activities like pollution, overfishing, and climate change are putting ocean ecosystems at risk. Notable efforts are being made to conserve this vital resource, including the creation of marine protected areas and public awareness campaigns.",
    "frq": "Based on the context provided, what are some ways the ocean is important to Earth and its inhabitants? Also, what challenges are oceans facing according to the text? Provide evidence from the text to support your answer."
}```"""

# Rubrics examples
EXAMPLE_RUBRIC_01 = """User input: Common Core State Standard is CCSS.ELA-LITERACY.W.4.9. Take into consideration the definition of this standard provided below in step-1.
CONTEXT and FREE RESPONSE QUESTION are also included in following JSON: 
{
    "step-1": "The Common Core State Standard CCSS.ELA-LITERACY.W.4.9 states that 4th-grade students should 'Draw evidence from literary or informational texts to support analysis, reflection, and research.'",
    "step-2": "The assessment will test the student's ability to extract information from a context paragraph related to the ocean. The student should then use this information to support their analysis or reflection in response to a specific free-response question.",
    "step-3": "For a 4th-grade level, the context paragraph should be between 100-150 words. It should contain a mix of factual and interpretive details, providing a well-rounded basis for answering the free-response question.",
    "context": "The ocean covers more than 70% of Earth's surface and serves as home to a myriad of creatures, from microscopic plankton to massive whales. It also plays a crucial role in regulating the planet's climate by absorbing carbon dioxide. Coral reefs, often referred to as the 'rainforests of the sea,' host a variety of marine life and contribute to biodiversity. However, human activities like pollution, overfishing, and climate change are putting ocean ecosystems at risk. Notable efforts are being made to conserve this vital resource, including the creation of marine protected areas and public awareness campaigns.",
    "frq": "Based on the context provided, what are some ways the ocean is important to Earth and its inhabitants? Also, what challenges are oceans facing according to the text? Provide evidence from the text to support your answer."
}
Assistant answer: 
    rubric: "### Assessment Rubric for Free Response Question\n\n#### Criteria for Evaluation\n\n1. **Drawing Evidence (5 points)**: Student must draw clear evidence from the context paragraph to support their answer.\n    - 5 points: Provides direct quotes or paraphrases that are highly relevant to the question.\n    - 3 points: Provides some evidence but it's either partially relevant or not directly quoted.\n    - 1 point: Makes a generalized or vague reference to the text.\n    - 0 points: Does not reference the text.\n\n2. **Analysis and Reflection (5 points)**: Student should analyze the importance of the ocean to Earth and its challenges, and may include personal reflection.\n    - 5 points: Thoroughly analyzes both the importance and challenges, possibly including personal reflection.\n    - 3 points: Partially analyzes either the importance or challenges, with some evidence.\n    - 1 point: Minimal analysis with limited or no evidence.\n    - 0 points: No analysis or reflection.\n\n3. **Clarity and Organization (3 points)**: Answer should be clear, concise, and well-organized.\n    - 3 points: Answer is clear, concise, and logically organized.\n    - 2 points: Answer is mostly clear but may lack some organization.\n    - 1 point: Answer is disorganized or unclear.\n    - 0 points: Answer is incomprehensible.\n\n4. **Grammar and Mechanics (2 points)**: The answer should be free of grammatical and spelling errors.\n    - 2 points: No errors.\n    - 1 point: Few minor errors.\n    - 0 points: Numerous errors that hinder comprehension.\n\n### Scoring Guide\n- 13-15 points: Excellent\n- 10-12 points: Good\n- 6-9 points: Needs Improvement\n- 0-5 points: Unsatisfactory"
"""

EXAMPLE_RUBRIC_02 = """Common Core State Standard is CCSS.ELA-LITERACY.W.6.3. Take into consideration the definition of this standard provided below in step-1.
CONTEXT and FREE RESPONSE QUESTION are also included in following JSON: 
{
    "step-1": "The standard CCSS.ELA-LITERACY.W.6.3 requires students to write narratives to develop real or imagined experiences or events using effective technique, relevant descriptive details, and well-structured event sequences.",
    "step-2": "The assessment must test the student's ability to write a narrative that includes effective techniques, relevant descriptive details, and a well-structured event sequence.",
    "step-3": "The CONTEXT paragraph should be sufficiently detailed but not excessively long, providing enough complexity for a 6th-grade student to generate a narrative based on it.",
    "context": "Maria had a morning routine that she followed every single day. She would start her day by waking up to the sound of her melodious alarm at 6:30 a.m. After quickly turning it off, she'd head to the kitchen where her mom would already have a steaming cup of hot chocolate waiting for her. Next, she would grab her toothbrush and toothpaste and head to the bathroom to brush her teeth. The bathroom mirror would be slightly fogged up from her older brother's hot shower, making her trace smiley faces on it before wiping it clean. Once she was ready, she'd head to her room to put on her favorite outfit: a blue shirt with white stars, and jeans that had a small rip on the knee which, according to her, gave it character. After getting dressed, she would sit at her desk and skim through her planner to prepare for the day ahead, occasionally jotting down notes in the margins.",
    "frq": "Write a narrative from Maria's perspective about a particular morning where something unexpected happens during her routine. Use effective narrative techniques, integrate relevant descriptive details, and structure the events in a sequential manner. Make sure your narrative has a beginning, middle, and end. Include dialogue, internal thoughts, or actions that help to develop the characters and events."
}
Assistant answer:
    rubric: "1. Effective Techniques (0-10 points): 0-2 points for lacking effective techniques, 3-5 for some use, 6-8 for good use, and 9-10 for excellent use.\n2. Relevant Descriptive Details (0-10 points): 0-2 points for lacking details, 3-5 for some details, 6-8 for good details, and 9-10 for excellent details.\n3. Well-Structured Event Sequences (0-10 points): 0-2 for poor structure, 3-5 for some structure, 6-8 for good structure, and 9-10 for excellent structure.\n4. Dialogue, Internal Thoughts, Actions to Develop Characters and Events (0-5 points): 0-1 for lacking elements, 2-3 for some use, and 4-5 for effective use.\n5. Beginning, Middle, and End (0-5 points): 0-1 for missing or unclear, 2-3 for present but lacking, and 4-5 for clear and effective."
"""
EXAMPLE_RUBRIC_03 = """You are an helpful assistant. User will provide you Common Core State Standard. \
You will output a RUBRIC for an assessment task as expected by the Common Core State Standard provided by user.
        
Output only the generated rubric in markdown string snippet format.

Common Core State Standard is CCSS.ELA-LITERACY.W.4.9. Take into consideration the definition of this standard provided below in step-1.
You can consider the context and free response question (frq), but it is preferable for the generated rubric to be generic, not reflecting the topic of the context and frq.
{
    "step-1": "The Common Core State Standard CCSS.ELA-LITERACY.W.4.9 states that 4th-grade students should 'Draw evidence from literary or informational texts to support analysis, reflection, and research.'",
    "step-2": "The assessment will test the student's ability to extract information from a context paragraph related to the ocean. The student should then use this information to support their analysis or reflection in response to a specific free-response question.",
    "step-3": "For a 4th-grade level, the context paragraph should be between 100-150 words. It should contain a mix of factual and interpretive details, providing a well-rounded basis for answering the free-response question.",
    "context": "The ocean covers more than 70% of Earth's surface and serves as home to a myriad of creatures, from microscopic plankton to massive whales. It also plays a crucial role in regulating the planet's climate by absorbing carbon dioxide. Coral reefs, often referred to as the 'rainforests of the sea,' host a variety of marine life and contribute to biodiversity. However, human activities like pollution, overfishing, and climate change are putting ocean ecosystems at risk. Notable efforts are being made to conserve this vital resource, including the creation of marine protected areas and public awareness campaigns.",
    "frq": "Based on the context provided, what are some ways the ocean is important to Earth and its inhabitants? Also, what challenges are oceans facing according to the text? Provide evidence from the text to support your answer."
}
Assistant answer: 
# Rubric for CCSS.ELA-LITERACY.W.4.9 Assessment

## Criteria: Identification of Importance

| Level  | Description                                                                                                                                                                                   |
|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 4      | The student identifies multiple ways the ocean is important to Earth and its inhabitants, citing specific evidence from the text for each point.                                                |
| 3      | The student identifies some ways the ocean is important but may lack full depth or specificity in citing evidence from the text.                                                                 |
| 2      | The student identifies only one way the ocean is important and cites minimal evidence from the text.                                                                                            |
| 1      | The student struggles to identify why the ocean is important to Earth and its inhabitants, and provides little to no evidence from the text.                                                     |
| 0      | The student does not attempt to identify the importance of the ocean.                                                                                                                           |

## Criteria: Identification of Challenges

| Level  | Description                                                                                                                                                                                    |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 4      | The student identifies multiple challenges that oceans are facing, citing specific evidence from the text for each point.                                                                       |
| 3      | The student identifies some challenges but may lack full depth or specificity in citing evidence from the text.                                                                                 |
| 2      | The student identifies only one challenge the ocean is facing and cites minimal evidence from the text.                                                                                          |
| 1      | The student struggles to identify challenges the ocean is facing and provides little to no evidence from the text.                                                                               |
| 0      | The student does not attempt to identify the challenges the ocean is facing.                                                                                                                    |

## Criteria: Quality of Analysis or Reflection

| Level  | Description                                                                                                                                                                                   |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 4      | The student provides a thorough analysis or reflection that is well-supported by evidence from the text, showing a deep understanding of both the importance and challenges of the ocean.         |
| 3      | The student provides some analysis or reflection supported by evidence from the text but may lack depth or full understanding of either the importance or challenges of the ocean.                |
| 2      | The student provides a basic level of analysis or reflection that is minimally supported by evidence from the text.                                                                              |
| 1      | The student attempts to analyze or reflect but does not provide evidence from the text to support their ideas.                                                                                   |
| 0      | The student does not attempt to provide any analysis or reflection on the topic.                                                                                                                |

## Criteria: Writing Conventions

| Level  | Description                                                                                                                                                                                   |
|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 4      | The student's writing is clear, well-organized, and free of grammatical errors.                                                                                                                 |
| 3      | The student's writing is mostly clear and organized, with minor grammatical errors that do not interfere with understanding.                                                                     |
| 2      | The student's writing shows some disorganization or has several grammatical errors that may interfere with understanding.                                                                        |
| 1      | The student's writing is disorganized and contains numerous grammatical errors, making it difficult to understand the analysis or reflection.                                                     |
| 0      | The student does not attempt to write a coherent response.                                                                                                                                     |

## Overall Scoring

- **13-16 points**: The student demonstrates an excellent understanding of the importance and challenges of the ocean, as well as strong analytical and writing skills.
- **9-12 points**: The student demonstrates a good understanding of the topic but may have minor gaps in analysis, evidence, or writing quality.
- **5-8 points**: The student shows a basic understanding but has notable weaknesses in analysis, use of evidence, or writing conventions.
- **1-4 points**: The student struggles significantly in understanding the topic, analyzing it, or providing evidence from the text.
- **0 points**: No attempt made to answer the question.

"""

EXAMPLE_RUBRIC_04 = """You are an helpful assistant. User will provide you Common Core State Standard. \
You will output a RUBRIC for an assessment task as expected by the Common Core State Standard provided by user.
        
Output only the generated rubric in markdown string snippet format.

Common Core State Standard is CCSS.ELA-LITERACY.W.6.3. Take into consideration the definition of this standard provided below in step-1.
You can consider the context and free response question (frq), but it is preferable for the generated rubric to be generic, not reflecting the topic of the context and frq.
{
    "step-1": "The standard CCSS.ELA-LITERACY.W.6.3 requires students to write narratives to develop real or imagined experiences or events using effective technique, relevant descriptive details, and well-structured event sequences.",
    "step-2": "The assessment must test the student's ability to write a narrative that includes effective techniques, relevant descriptive details, and a well-structured event sequence.",
    "step-3": "The CONTEXT paragraph should be sufficiently detailed but not excessively long, providing enough complexity for a 6th-grade student to generate a narrative based on it.",
    "context": "Maria had a morning routine that she followed every single day. She would start her day by waking up to the sound of her melodious alarm at 6:30 a.m. After quickly turning it off, she'd head to the kitchen where her mom would already have a steaming cup of hot chocolate waiting for her. Next, she would grab her toothbrush and toothpaste and head to the bathroom to brush her teeth. The bathroom mirror would be slightly fogged up from her older brother's hot shower, making her trace smiley faces on it before wiping it clean. Once she was ready, she'd head to her room to put on her favorite outfit: a blue shirt with white stars, and jeans that had a small rip on the knee which, according to her, gave it character. After getting dressed, she would sit at her desk and skim through her planner to prepare for the day ahead, occasionally jotting down notes in the margins.",
    "frq": "Write a narrative from Maria's perspective about a particular morning where something unexpected happens during her routine. Use effective narrative techniques, integrate relevant descriptive details, and structure the events in a sequential manner. Make sure your narrative has a beginning, middle, and end. Include dialogue, internal thoughts, or actions that help to develop the characters and events."
}
Assistant answer: 
# Rubric for Narrative Writing Based on CCSS.ELA-LITERACY.W.6.3

## Criteria: Effective Technique
- **4: Exemplary**
  - The narrative consistently employs effective techniques, such as dialogue, pacing, and internal thoughts to develop experiences or events.
- **3: Proficient**
  - The narrative mostly employs effective techniques to develop experiences or events but may lack consistency.
- **2: Developing**
  - The narrative sporadically employs effective techniques, and these are not well integrated.
- **1: Needs Improvement**
  - The narrative lacks effective techniques for developing experiences or events.

## Criteria: Relevant Descriptive Details
- **4: Exemplary**
  - The narrative is rich with relevant descriptive details that contribute meaningfully to the experiences or events.
- **3: Proficient**
  - The narrative contains some relevant descriptive details, but they may not be fully integrated into the experiences or events.
- **2: Developing**
  - The narrative includes limited relevant descriptive details, and they do not significantly contribute to the experiences or events.
- **1: Needs Improvement**
  - The narrative lacks relevant descriptive details.

## Criteria: Well-structured Event Sequence
- **4: Exemplary**
  - Events unfold naturally and logically with a clear beginning, middle, and end. Transitions are smoothly integrated.
- **3: Proficient**
  - Events mostly follow a logical sequence with a recognizable beginning, middle, and end. Some transitions may be lacking.
- **2: Developing**
  - Events do not always follow a logical sequence and transitions between events are not always clear.
- **1: Needs Improvement**
  - The narrative lacks a clear event sequence and is hard to follow.

## Overall Score
- **10-12 Points: Exemplary**
  - Demonstrates mastery of the narrative form with consistent use of effective techniques, descriptive details, and well-structured event sequences.
- **7-9 Points: Proficient**
  - Demonstrates competence in narrative writing but may have minor inconsistencies in technique, details, or structure.
- **4-6 Points: Developing**
  - Demonstrates some understanding of narrative writing but lacks consistent application of effective techniques, details, or structure.
- **1-3 Points: Needs Improvement**
  - Does not meet the expectations for effective narrative writing at the 6th-grade level.
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