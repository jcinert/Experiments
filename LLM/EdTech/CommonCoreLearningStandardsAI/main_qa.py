
from CCSS_BatchQA import BatchQA

CONFIG_FILE = "C:\\Github_Projects\\Experiments\\CommonCoreLearningStandardsAI\\config_qa.json"

def main():

    config = get_config(CONFIG_FILE)
    input_data = read_qa_inputs(config)
    qa = BatchQA(debug=config['debug'])

    if config['run_single_example']:
        assessment = input_data[0]
        print('─' * 100)
        print(f">>> NEW assessment qa: Standard: {assessment['standard']} Topic: {assessment['topic']}")
        # evaluate single assessment
        qa_result = qa_assessment(config = config,
                                  qa = qa,
                                  assessment = assessment)
    else:
        print('─' * 100)
        print(f">>> QA starting for {len(input_data)} assessments.")
        qa_result = qa_batch(config = config,
                             qa = qa,
                             assessment_batch = input_data)
        
        # export QA outcome as defined in confiq_qa.json
        save_output(config=config,
                    output=qa_result)
          
def qa_assessment(config:dict, qa: BatchQA, assessment):
    run_successfull = False

    # sometimes parser fails - workaround for now: retry - TODO improve prompts
    for i in range(config['max_retries_on_error']):
        try:
            print('─' * 50)
            print(">>> Assessment QA start")
            qa_result = qa.qa_assessment(assessment=assessment)
            
            print(f"QA overall passed: {qa_result['overall_qa_passed']}")
            print(f"QA passed context / frq / rubric: {qa_result['context_qa_passed']} / {qa_result['frq_qa_passed']} / {qa_result['rubric_qa_passed']}")
            print(">>> Assessment QA complete") 
            print('─' * 50)
            run_successfull = True
            break
        except:
            print(">>> Assessment QA failed - restarting")

    if not run_successfull:
        raise Exception(f"ERROR: Generate QA not successfull after {config['max_retries_on_error']} retries.")

    return qa_result

def qa_batch(config:dict, qa: BatchQA, assessment_batch:list):

    print('─' * 50)
    print(">>> Assessment QA start")
    qa_result = qa.batch_qa_assessment(assessment_batch=assessment_batch, 
                                       max_retries_on_error=config['max_retries_on_error'])

    print(f"QA overall passed: {qa_result['overall_qa_passed']} out of {qa_result['count_assessments']}")
    print(f"QA pass score: {qa_result['overall_qa_passed'] / qa_result['count_assessments'] * 100} %")
    print('─' * 20)
    print(f"QA context passed: {qa_result['context_qa_passed']} out of {qa_result['count_assessments']}")
    print(f"QA frq passed: {qa_result['frq_qa_passed']} out of {qa_result['count_assessments']}")
    print(f"QA rubric passed: {qa_result['rubric_qa_passed']} out of {qa_result['count_assessments']}")
    print('─' * 50)

    return qa_result

def read_qa_inputs(config):
    """
        Loads qa inputs from json file
    """
    import json
    f = open(config['data_file'])
    data = json.load(f)
        
    f.close()
    return data['output']

def save_output(config,output):
    """
        save qa output to json file (append)
        used for batch qa
    """
    import json   
    file_name = config['qa_output_file']
    # data = json.load(f)
    
    with open(file_name,'w') as file:
        json.dump(output, file, indent = 4)
 
def get_config(CONFIG_FILE):
    """
        get config from root folder: config_qa.json file
    """
    import json
        
    f = open(CONFIG_FILE)
    config = json.load(f)
        
    f.close()
    return config

if __name__	== '__main__':
    main()