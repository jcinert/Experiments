from pathlib import Path
from src.chat_chain import SDKChat
from src.rag_qa import RAG_QA
from langchain.memory import ChatMessageHistory
import datetime
import json
import time
from tqdm import tqdm

# Get project root directory
PROJECT_ROOT = Path(__file__).parent
CONFIG_FILE = PROJECT_ROOT / "evaluate" /"config_qa.json"

def main():
    config = get_config(CONFIG_FILE)
    process_paths(config)
    
    input_data = read_qa_inputs(config)
    sdk_chat = init_chat()
    qa = RAG_QA(config=config)
    qa_batch_passed_counter = 0
    qa_batch_message_counter = 0

    if config['run_single_example']:
        chat = input_data[0]
        print('─' * 100)
        print(f">>> QA of chat id: {chat['chat_id']} with {len(chat['messages'])} messages.")

        qa_msg_passed_counter, message_counter = eval_chat(config, sdk_chat, qa, input_data[0])
        json_log(config, qa_msg_passed_counter, message_counter)
    else:
        print('─' * 100)
        print(f">>> QA starting for {len(input_data)} chats.")
        
        for chat in tqdm(input_data):
            qa_msg_passed_counter, message_counter = eval_chat(config, sdk_chat, qa, chat)
            qa_batch_passed_counter += qa_msg_passed_counter
            qa_batch_message_counter += message_counter

        success_rate = qa_batch_passed_counter/qa_batch_message_counter
        print('─' * 100)
        print(f">>> QA complete: {success_rate:.2%}")

        json_log(config, qa_batch_passed_counter, qa_batch_message_counter)

def process_paths(config):
    """Convert relative paths in config to absolute paths"""
    path_keys = [
        'vector_db_path',
        'data_file',
        'qa_output_file',
        'qa_debug_file_path'
    ]
    
    for key in path_keys:
        if key in config:
            config[key] = str(PROJECT_ROOT / config[key])
            Path(config[key]).parent.mkdir(parents=True, exist_ok=True)
    
    return config

def eval_chat(config, sdk_chat, qa, chat):
    """Evaluate all messages in chat"""
    history = ChatMessageHistory()
    qa_passed_counter = 0
    message_counter = 0

    for chat_message in chat['messages']:
        message_counter += 1
        history.add_user_message(chat_message['prompt'])
        counter = int(config['max_retries_on_error'])
        while counter > 0:
            try:
                response = sdk_chat.invoke({
                    'chat_history': history.messages, 
                    'question': chat_message['prompt']
                })
                break
            except Exception as e:
                counter -= 1
                print(f"Warning - Retrying in {int(config['retry_wait_seconds'])}s. Exception {e}")
                time.sleep(int(config['retry_wait_seconds']))
        if not response:
            raise Exception("No responce from LLM. Likely quota is exhausted.")
        qa_result = qa.evaluate_response(
            chat_history=history.messages, 
            question=chat_message['prompt'],
            response=response
        )
        
        history.add_ai_message(response)
        
        if config['debug']:
            print('─' * 50)
            print(f">>> Message QA result: {qa_result}")
        
        if qa_result['resp_qa_passed']:
            qa_passed_counter += 1

    if config['debug']:
        print('─' * 100)
        print(f">>> Chat QA result: passed {qa_passed_counter}/{message_counter} ({qa_passed_counter/message_counter:.2%})")
    return qa_passed_counter, message_counter

def init_chat():
    print('─' * 100)
    print(f">>> INIT CHAT QA")
    sdk_chat = SDKChat()
    sdk_chat.create_chat()
    return sdk_chat

def read_qa_inputs(config):
    """Loads qa inputs from json file"""
    with open(config['data_file']) as f:
        return json.load(f)

def json_log(config, qa_batch_passed_counter, qa_batch_message_counter):
    """Log overall qa results in json format"""
    json_log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "total_questions": qa_batch_message_counter,
        "qa_passed": qa_batch_passed_counter,
        "success_rate": f"{(qa_batch_passed_counter / qa_batch_message_counter):.2%}",
    }

    json_file = Path(config['qa_output_file'])
    json_chats = []

    # Ensure directory exists
    json_file.parent.mkdir(parents=True, exist_ok=True)

    if json_file.exists():
        with open(json_file) as f:
            json_chats = json.load(f)
    
    json_chats.append(json_log)
    with open(json_file, 'w') as f:
        json.dump(json_chats, f, indent=2)

def get_config(config_file):
    """Get config from config_qa.json file"""
    with open(config_file) as f:
        return json.load(f)

if __name__ == '__main__':
    main()