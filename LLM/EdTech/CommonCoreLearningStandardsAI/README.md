# Common Core State Standard AI
This repo provides functionality to generate [Common Core State Standard](https://www.thecorestandards.org/about-the-standards/) assessments (use case 1), generate student answer to the assessment (use case 2), evaluate the answer (use case 3) in a end-to-end LLM powered automated workflow. in addition there is a Batch Quality assurace capability that will evaluate correctnes an accuracy of all LLM outputs (see use case 4). Focus of the repo is English langugae only assements (no math/art).

## Quick start - How to run
1. make sure you have .env file configured with valid Azure OpenAI API
2. adjust input and output path in config.json
3. provide input samples in input json file
4. run main.py

![Overall Flow (main.py)](./_images/e2e_flow.png "Overall Flow (main.py)")

## Use case 1 - generate assessment for Common Core State Standard and a topic
- Use method generate_assessment() from class AssessmentGenerator (file CCSS_Assessment_Generator.py)

![Generation Flow (CCSS_Assessment_Generator.py)](./_images/gen_flow.png "[Generation Flow (CCSS_Assessment_Generator.py)")

## Use case 2 - generate answer (simulate a student)
- Use method answer_assessment() from class AIStudent (file CCSS_AIStudent.py)

## Use case 3 - evaluate students answer (simulate a teacher)
- Use method evaluate_assessment() from class AITeacher (file CCSS_AITeacher.py)

## Use case 1 + 2 + 3 test
- use main.py to test
- see config.json to set input and output folders

## Use case 4 - perform QA on multiple output samples
- Use method qa_batch() from class BatchQA (file CCSS_BatchQA.py)
- see config_qa.json to set input and output folders
- use main_qa.py to test