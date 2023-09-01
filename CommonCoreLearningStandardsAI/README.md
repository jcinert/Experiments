# Common Core State Standard AI
## Use case 1 - generate assessment for Common Core State Standard and a topic
- Use method generate_assessment() from class AssessmentGenerator (file CCSS_Assessment_Generator.py)

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