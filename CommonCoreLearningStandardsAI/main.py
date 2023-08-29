
from CCSS_Assessment_Generator import AssessmentGenerator
from CCSS_AIStudent import AIStudent
from CCSS_AITeacher import AITeacher

def main():

    topic = "Sigmund Freud"
    standard = "CCSS.ELA-LITERACY.W.4.9"

    # read_sample_inputs()

    # Generate assessment
    generator = AssessmentGenerator(debug=True)
    context, frq, rubric = generate_assessment(generator=generator,
                                               standard=standard,
                                               topic=topic)

    # answer assessment
    answer_quality = 1
    student = AIStudent(debug=True)
    answer = answer_assessment(student=student,
                               standard=standard,
                               context=context,
                               frq=frq,
                               rubric=rubric,
                               answer_quality=answer_quality)

    # evaluate the answer
    teacher = AITeacher(debug=True)
    written_eval, score, score_max = evaluate_assessment(teacher=teacher,
                                                        standard=standard,
                                                        context=context,
                                                        frq=frq,
                                                        rubric=rubric,
                                                        answer=answer)
        
def generate_assessment(generator: AssessmentGenerator, standard:str, topic:str):
    generator.set_standard(standard)
    generator.set_topic(topic)
    
    context, frq, rubric = generator.generate_assessment()
    print("----------------------------------------------")
    print(">>> Assessment generation start")
    print(f"Context: {context}")
    print("----------------------------------------------")
    print(f"Free responce queistion: {frq}")
    print("----------------------------------------------")
    print(f"Rubrics: {rubric}") 
    print(">>> Assessment generation complete")
    print("----------------------------------------------")

    return context, frq, rubric             

def answer_assessment(student: AIStudent, standard, context, frq, rubric, answer_quality):
    student.set_standard(standard)
    student.set_answer_quality(answer_quality)
    answer = student.generate_answer(context,frq,rubric)
    print("----------------------------------------------")
    print(">>> Assessment answering start")
    print(f"Answer: {answer}")
    print(">>> Assessment answering complete") 
    print("----------------------------------------------")

    return answer

def evaluate_assessment(teacher: AITeacher, standard, context, frq, rubric, answer):

    written_eval, score, score_max = teacher.evaluate_answer(standard,context,frq,rubric,answer)
    print("----------------------------------------------")
    print(">>> Assessment evaluation start")
    print(f"Score: {score} (out of {score_max})")
    print(f"Evaluation: {written_eval}")
    print(">>> Assessment evaluation complete") 
    print("----------------------------------------------")

    return written_eval, score, score_max 

def read_sample_inputs():
    import json
    
    # Opening JSON file
    f = open('sample_inputs.json')
    
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    # list
    for i in data['standard']:
        print(i)
    
    # Closing file
    f.close()

if __name__	== '__main__':
    main()