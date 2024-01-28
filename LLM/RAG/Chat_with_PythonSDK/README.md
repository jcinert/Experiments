# Chat with web site
This is a RAG chat powered by Azure OpenAI LLMs. You can chat with [Generative AI Python SDK](https://github.com/IBM/).

There is a batch QA (evaluation) - see below How to run Batch QA.

This is a draft solution, by no means reacy for production.

# How it works
![alt text](https://github.com/jcinert/Experiments/blob/main/LLM/RAG/Chat_with_PythonSDK/docs/architecture2.png "Chat architecture")

# Modifications possible
- You can replace the knowledge base (RAG) with __another web site__ - see `config.json`
- You can replace the Azure OpenAI with __another LLM__ - see `chat-chain.py` (main model) and `vector_db.py` (embedding model)

# How to run Chat - with Conda Environment
1. Clone/copy this repo
2. Open Conda prompt (or VS code)
3. navigate to your repo environment folder `cd C:\<your path>\CondaEnv`
4. `conda activate ./env`
5. navigate to your repo chat folder `cd C:\<your path>\Chat_with_PythonSDK`
6. Run in conda prompt `streamlit run main.py`
7. Browser window should open with streamlit chat

Without Conda you need to install all pre-requisites listed in `./CondaEnv/environment.yml`. Then start with step 5.

# How to run Batch QA - with Conda Environment
1. - 5. same as above
6. provide / adjust chat logs (questions and answers) in the file `./evaluate/questions-batch.json` (can be adjusted in `config-qa.json`)
7. Run in conda prompt `python main_qa.py`
7. QA results will be output to json file `./evaluate/output_qa.json` see `config-qa.json`

# References
Great Repos I drew inspiration from:
- https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/basic_memory.py

# TODO Next
- Refine prompts. Sometimes links are not provided
- Add refresh frequency to vector DB
- Handle non-IBM SDK related questions