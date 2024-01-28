# Chat with web site
This is a RAG chat powered by Azure OpenAI LLMs. You can chat with [Generative AI Python SDK](https://github.com/IBM/).

There is a batch QA (evaluation) - see below How to run Batch QA.

> **Warning:** This is a draft solution, by no means ready for production.

> **Warning 2:** Due to limited version of my Azure OpenAI model (S0 tier), there is a delay in chat response (~ 10s ). this can be solved by upgrading the tier AND removing wait chain from `./src/chat-chain.py`

# How it works
![alt text](https://github.com/jcinert/Experiments/blob/main/LLM/RAG/Chat_with_PythonSDK/docs/architecture2.png "Chat architecture")

# Modifications possible
- You can replace the knowledge base (RAG) with __another web site__ - see `config.json`
- You can replace the Azure OpenAI with __another LLM__ - see `./src/chat-chain.py` (main model) and `./src/vector_db.py` (embedding model)

# How to run Chat - with Conda Environment
1. Clone/copy this repo
1. update Auzre Open AI details in `env_template.env` and file path in `config.json`
3. Open Conda prompt (or VS code)
4. navigate to your repo environment folder `cd C:\<your path>\CondaEnv`
5. `conda activate ./env`
6. navigate to your repo chat folder `cd C:\<your path>\Chat_with_PythonSDK`
7. Run in conda prompt `streamlit run main.py`
8. Browser window should open with streamlit chat

Without Conda you need to install all pre-requisites listed in `./CondaEnv/environment.yml`. Then start with step 5.

# How to run Batch QA - with Conda Environment
1. to 6. same as above
7. provide / adjust chat logs (questions and answers) in the file `./evaluate/questions-batch.json` (can be adjusted in `config-qa.json`)
8. Run in conda prompt `python main_qa.py`
9. QA results will be output to json file `./evaluate/output_qa.json` see `config-qa.json`

# QA results
Initial evaluations indicate ~ 90% accutacy. That means the answer is completely answering the questions in 90% of cases. See `./evaluate/output_qa.json` for details.

# References
Great Repos I drew inspiration from:
- https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/basic_memory.py

# TODO Next
- Sometimes links are not provided &rarr Refine prompts, perhaps add examples (few-shot)
- Add refresh frequency to vector DB
- Handle non-IBM SDK related questions
- Use ChatGPT 4
- Improve Batch QA with groundness test - ensuring no hallucination. Search "TODO" in `rag-qa.py`