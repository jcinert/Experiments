
from CCSS_Assessment_Generator import AssessmentGenerator
from CCSS_AIStudent import AIStudent

def main():

    # Generate assessment
    # gen = AssessmentGenerator(debug=True)
    # generate_assessment(gen)

    student = AIStudent(answer_quality=1,debug=True)

        
def generate_assessment(gen: AssessmentGenerator):
    gen.set_standard("CCSS.ELA-LITERACY.W.4.9")
    gen.set_topic("New Zealand")
    
    context, frq, rubric = gen.generate_assessment()
    print("----------------------------------------------")
    print(f"Context: {context}")
    print("----------------------------------------------")
    print(f"Free responce queistion: {frq}")
    print("----------------------------------------------")
    print(f"Rubrics: {rubric}")               


if __name__	== '__main__':
    main()
    print('Assessment generation complete')