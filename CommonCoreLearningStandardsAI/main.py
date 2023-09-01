
from CCSS_Assessment_Generator import AssessmentGenerator
from CCSS_AIStudent import AIStudent
from CCSS_AITeacher import AITeacher

CONFIG_FILE = "C:\\Github_Projects\\Experiments\\CommonCoreLearningStandardsAI\\config.json"

def main():

    config = get_config(CONFIG_FILE)
    input_data = read_sample_inputs(config)

    for assessment in input_data:
        print('─' * 100)
        print(f">>> NEW assessment: Standard: {assessment['standard']} Topic: {assessment['topic']}")
        # Generate assessment
        generator = AssessmentGenerator(debug=config['debug'])
        context, frq, rubric = generate_assessment(config = config,
                                                   generator=generator,
                                                   standard=assessment['standard'],
                                                   topic=assessment['topic'])

        # answer assessment
        student = AIStudent(debug=config['debug'])
        answer = answer_assessment(config = config,
                                   student=student,
                                   standard=assessment['standard'],
                                   context=context,
                                   frq=frq,
                                   rubric=rubric,
                                   answer_quality=assessment['student_answer_quality'])

        # evaluate the answer
        teacher = AITeacher(debug=config['debug'])
        written_eval, score, score_max = evaluate_assessment(config = config,
                                                             teacher=teacher,
                                                             standard=assessment['standard'],
                                                             context=context,
                                                             frq=frq,
                                                             rubric=rubric,
                                                             answer=answer)

        output_dict = create_dict(assessment['standard'], assessment['topic'], context, frq, rubric, answer, written_eval, score, score_max)
        save_output(config,output_dict)
        if config['run_single_example']:
            break
        
def generate_assessment(config:dict, generator: AssessmentGenerator, standard:str, topic:str):
    generator.set_standard(standard)
    generator.set_topic(topic)
    run_successfull = False
    
    for i in range(config['max_retries_on_error']):
        try:
            print('─' * 50)
            print(">>> Assessment generation start")
            context, frq, rubric = generator.generate_assessment()
            print(f"Context: {context}")
            print('─' * 50)
            print(f"Free responce question: {frq}")
            print('─' * 50)
            print(f"Rubrics: {rubric}") 
            print(">>> Assessment generation complete")
            print('─' * 50)
            run_successfull = True
            break
        except:
            print(">>> Assessment generation failed - restarting")

    if not run_successfull:
        raise Exception(f"ERROR: Generate assessment not successfull after {config['max_retries_on_error']} retries.")

    return context, frq, rubric             

def answer_assessment(config:dict, student: AIStudent, standard, context, frq, rubric, answer_quality):
    student.set_standard(standard)
    student.set_answer_quality(answer_quality)
    run_successfull = False

    for i in range(config['max_retries_on_error']):
        try:
            print('─' * 50)
            print(">>> Assessment answering start")
            answer = student.generate_answer(context,frq,rubric)
            print(f"Answer: {answer}")
            print(">>> Assessment answering complete") 
            print('─' * 50)
            run_successfull = True
            break
        except:
            print(">>> Assessment answering failed - restarting")

    if not run_successfull:
        raise Exception(f"ERROR: Generate answer not successfull after {config['max_retries_on_error']} retries.")

    return answer

def evaluate_assessment(config:dict, teacher: AITeacher, standard, context, frq, rubric, answer):
    run_successfull = False

    for i in range(config['max_retries_on_error']):
        try:
            print('─' * 50)
            print(">>> Assessment evaluation start")
            written_eval, score, score_max = teacher.evaluate_answer(standard,context,frq,rubric,answer)
            print(f"Score: {score} (out of {score_max})")
            print(f"Evaluation: {written_eval}")
            print(">>> Assessment evaluation complete") 
            print('─' * 50)
            run_successfull = True
            break
        except:
            print(">>> Assessment evaluation failed - restarting")

    if not run_successfull:
        raise Exception(f"ERROR: Generate evaluation not successfull after {config['max_retries_on_error']} retries.")

    return written_eval, score, score_max 

def read_sample_inputs(config):
    """
        Loads sample inputs from sample_inputs.json file
    """
    import json
    f = open(config['test_data_file'])
    data = json.load(f)
        
    f.close()
    return data

def save_output(config,new_output):
    """
        save single output to outputs.json file (append)
        used for batch test
    """
    import json   
    file_name = config['test_output_file']
    # data = json.load(f)
    
    with open(file_name,'r+') as file:
        # load existing data into a dict.
        file_data = json.load(file)
        file_data["output"].append(new_output)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
 
def create_dict(standard, topic, context, frq, rubric, answer, written_eval, score, score_max):
    return {"standard":standard, 
            "topic":topic, 
            "context":context, 
            "frq":frq, 
            "rubric":rubric, 
            "answer":answer, 
            "written_eval":written_eval, 
            "score":score, 
            "score_max":score_max}  

def get_config(CONFIG_FILE):
    """
        get config from root folder: config.json file
    """
    import json
        
    f = open(CONFIG_FILE)
    config = json.load(f)
        
    f.close()
    return config

if __name__	== '__main__':
    main()