# Chat with an agent over a web site
This is a RAG chat with agent, powered by Azure OpenAI LLMs. You can chat with [Generative AI Python SDK](https://github.com/IBM/).
Agent can search web as well.

> **Warning:** This is a draft solution, by no means ready for production.

> **Warning 2:** Due to limited version of my Azure OpenAI model (S0 tier), there is a delay in chat response (~ 10s ). this can be solved by upgrading the tier

> **Info:** Standard RAG chat (no agent) version might perform better - a version is here: [RAG chat with web site](https://github.com/jcinert/Experiments/tree/main/LLM/RAG/Chat_with_PythonSDK).

# Modifications possible
- You can replace the knowledge base (RAG) with __another web site__ - see `config.json`
- You can replace the Azure OpenAI with __another LLM__ - see `./src/chat-chain.py` (main model) and `./src/vector_db.py` (embedding model)

# How to run Chat - with Conda Environment
1. Clone/copy this repo
1. update Auzre Open AI details in `env_template.env` and file path in `config.json`
3. Open Conda prompt (or VS code)
4. navigate to your repo environment folder `cd C:\<your path>\CondaEnv`
5. `conda activate ./env`
6. navigate to your repo chat folder `cd C:\<your path>\Chat_with_PythonSDK_agent`
7. Run in conda prompt `streamlit run main.py`
8. Browser window should open with streamlit chat

Without Conda you need to install all pre-requisites listed in `./CondaEnv/environment.yml`. Then start with step 5.

# References
Great Repos I drew inspiration from:
- https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/basic_memory.py

# TODO Next
- Add refresh frequency to vector DB
- Improve istory handling - sometimes the history is not correctly taken into account. forcing the agent to rephrase first should help (or use GPT4)
- Code snippets and examples are rarely provided. few shot learning might help
- Use ChatGPT 4
