
from src.chat_chain import SDKChat
from src.rag_qa import RAG_QA
from langchain.memory import ChatMessageHistory
import datetime
import os
import json
               
CONFIG_FILE = "C:\\Github_Projects\\Experiments\\LLM\\RAG\\Chat_with_PythonSDK\\src\\config_qa.json"

def main():

    config = get_config(CONFIG_FILE)
    input_data = read_qa_inputs(config)
    sdk_chat = init_chat()
    qa = RAG_QA(config=config)
    qa_batch_passed_counter = 0
    qa_batch_message_counter = 0

    if config['run_single_example']:

        # evaluate single assessment - for debug / test
        chat = input_data[0]
        print('─' * 100)
        print(f">>> QA of chat id: {chat['chat_id']} wiht {len(chat['messages'])} messages.")

        qa_msg_passed_counter, message_counter = eval_chat(config, sdk_chat, qa, input_data[0])
        json_log(config, qa_msg_passed_counter, message_counter)

    else:
        # evaluate all chats in batch input file (see config_qa.json)        
        print('─' * 100)
        print(f">>> QA starting for {len(input_data)} chats.")
        
        for chat in input_data:
            qa_msg_passed_counter, message_counter = eval_chat(config, sdk_chat, qa, chat)
            qa_batch_passed_counter += qa_msg_passed_counter
            qa_batch_message_counter += message_counter

        print('─' * 100)
        print(f">>> QA complete: {qa_batch_passed_counter/qa_batch_message_counter}")

        json_log(config, qa_batch_passed_counter, qa_batch_message_counter)

def eval_chat(config, sdk_chat, qa, chat):
    """
        Evaluate all messages in chat
        returns qa_passed_counter, message_counter
    """
    # start a new (blank) chat
    history = ChatMessageHistory()
    qa_passed_counter = 0
    message_counter = 0

    # get answer for each question and evaluate the correctness using AI
    for chat_message in chat['messages']:
        message_counter += 1
        # 1. get answer from evaluated RAG agent
        history.add_user_message(chat_message['prompt'])
        response = sdk_chat.invoke({'chat_history': history.messages, 'question': chat_message['prompt']})

        # 2. evaluate answer correctness/completenes
        #  - evaluate answer completeness - given the question, history and answer            
        #  - TODO: evaluate answer accuracy/correctness - search the answer in vector db and evaluate match
        qa_result = qa.evaluate_response(
            chat_history = history.messages, 
            question = chat_message['prompt'],
            response = response
        )
        
        history.add_ai_message(response)
        
        if config['debug']:
            print('─' * 50)
            print(f">>> Message QA result: {qa_result}")
        
        if qa_result['resp_qa_passed']:
            qa_passed_counter += 1

    if config['debug']:
        print('─' * 100)
        print(f">>> Chat QA result: passed {qa_passed_counter} out of {message_counter}")
    return qa_passed_counter, message_counter

def init_chat():
    # create a chat instance
    print('─' * 100)
    print(f">>> INIT CHAT QA")
    sdk_chat = SDKChat()
    sdk_chat.create_chat()
    return sdk_chat

def read_qa_inputs(config):
    """
        Loads qa inputs from json file
    """
    import json
    f = open(config['data_file'])
    data = json.load(f)
        
    f.close()
    return data

def json_log(config, qa_batch_passed_counter, qa_batch_message_counter):
    """
        Log overall qa results in json format
    """

    # create json log
    json_log = {
        "timestamp": datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
        "total_questions": qa_batch_message_counter,
        "qa_passed": qa_batch_passed_counter,
        "success_rate": f"{100* qa_batch_passed_counter / qa_batch_message_counter:.2f} %",
    }

    json_file = config['qa_output_file']
    json_chats = []

    # save json - create file if it does not exist
    if not os.path.isfile(json_file):
        json_chats.append(json_log)
        with open(json_file, mode='w') as f:
            f.write(json.dumps(json_chats, indent=2))
    else:
        with open(json_file) as existing_json:
            existing_chats = json.load(existing_json)

        existing_chats.append(json_log)
        with open(json_file, mode='w') as f:
            f.write(json.dumps(existing_chats, indent=2))
 
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