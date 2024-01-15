cd C:\Github_Projects\Experiments\CondaEnv
conda activate ./env
cd C:\Github_Projects\Experiments\LLM\RAG\Chat_with_PythonSDK
streamlit run main-stream.py
pause

cd C:\Github_Projects\Experiments\CondaEnv
conda activate ./env
cd C:\Github_Projects\Experiments\LLM\RAG\Chat_with_PythonSDK
streamlit run main.py
pause

cd C:\Github_Projects\Experiments\CondaEnv
conda activate ./env
cd C:\Github_Projects\Experiments\LLM\RAG\Chat_with_PythonSDK
python main_qa.py
pause


https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/basic_memory.py

# TODO NExt
- refine prompts. sometimes links are not provided
- save vector db and refresh at certain frequency (not to delay chat session)
- handle non-skd related questions