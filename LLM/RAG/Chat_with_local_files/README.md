# Chat with files
This is a RAG chat powered by Google Gemini LLMs (Google Gemini 2.0 Flash and Google embedding model). You can chat with local files. 

> **Warning:** This is a draft solution, by no means ready for production.

> **Warning 2:** Free Tier of Google Gemini 2.0 Flash has token limits - see [rate-limits](https://ai.google.dev/gemini-api/docs/rate-limits)

# How it works
## Architecture
![RAG Chat Architecture](https://github.com/jcinert/Experiments/blob/main/LLM/RAG/Chat_with_local_files/img/architecture2.png "Chat architecture")

## RAG System Flow
### 1. Initialization
- Load config & API keys
- Check vector DB setting:
  - **Existing DB**: Load from file
  - **New/Rebuild**: Create from documents (local/URL), process & save

### 2. Chat Setup
- Initialize Gemini LLM
- Create RAG chain:
  1. Question transformer
  2. Document retriever
  3. Response generator

### 3. Query Flow
1. Get user question
2. Transform question
3. Retrieve relevant docs
4. Generate response with context
5. Return answer

**Note**: Vector DB is created once and reused across sessions unless rebuild is requested

# How to run Chat - with Conda Environment
1. Clone/copy this repo
2. Update Google Gemini API key in `env_template.env`. If you dont have the key, create one for free here: [https://aistudio.google.com](https://aistudio.google.com)
3. (optional) Update folders in `config.json`
4. Open Conda prompt (or other terminal)
5. navigate to your repo folder `cd C:\<your path>\Chat_with_local_file`
6. Run command `conda env create --file environment.yml` (only once) and then `conda activate ragchat`
7. Run in conda prompt `streamlit run main.py`
8. Browser window should open with streamlit chat
9. Chat away!

Without Conda you need to install all pre-requisites listed in `environment.yml`. Then start with step 7.

# Configuration
Key configuration is done in `config.json` in root project folder. Configuration file explanation is below. In addition you can easily cange in code the following:
- You can replace the knowledge base (RAG) with __different files__. Currently supported format are HTML and Markdown files. See `config.json`
- You can replace the Google Gemini 2.0 Flash and Google embedding models with __another LLM__ - see `./src/chat-chain.py` (main model) and `./src/vector_db.py` (embedding model)
## Configuration file explained
## General Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `debug` | boolean | `false` | Enables detailed logging for debugging purposes |
| `json_logging` | boolean | `false` | Saves chat interactions to JSON file for analysis |
| `transcript_file_path` | string | `"transcripts"` | Directory path for storing chat transcripts |

## Vector Database Settings (`vector_db`)

| Setting | Type | Default | Options | Description |
|---------|------|---------|---------|-------------|
| `use_offline_vector_db` | boolean | `true` | `true`/`false` | Whether to load existing vector DB (`true`) or create new one (`false`) |
| `context_source` | string | `"file"` | `"file"` | Source of documents - only local files supported for now. |
| `vector_db_path` | string | `"vector_db"` | any valid path | Directory path for storing vector database |
| `retriever_search_type` | string | `"similarity"` | `"similarity"`/`"mmr"` | Search algorithm for retrieving documents |
| `retriever_num_docs` | integer | `4` | 1+ | Number of documents to retrieve per query |

### Document Loading Settings (`document_loading`)

| Setting | Type | Default | Options | Description |
|---------|------|---------|---------|-------------|
| `local_docs_path` | string | `"context_files"` | any valid folder | Directory containing documents that should be used in RAG |
| `file_types` | array | `["html", "md"]` | `"html"`, `"md"`, `"markdown"`, `"txt"`, `"pdf"` | Supported file types for processing |
| `chunk_size` | integer | `1000` | 100+ | Size of text chunks for processing (in characters) |
| `chunk_overlap` | integer | `100` | 10+ | Overlap between chunks to maintain context |
| `use_multithreading` | boolean | `true` | `true`/`false` | Enable parallel processing of documents |
| `use_file_urls` | boolean | `true` | `true`/`false` | Generate file:// URLs for local documents |
| `preserve_metadata` | boolean | `true` | `true`/`false` | Keep original document metadata |

### Document Downloading Settings (`document_downloading`)
relevant if `context_source` is `"url"`
| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `retriever_URL_to_get` | string | empty | Base URL to scrape documents from |
| `retriever_URL_to_exclude` | array | `[]` | URLs to skip during scraping |
| `retriever_URL_scrape_depth` | integer | `8` | How many levels deep to follow links |

# Evaluation - Batch QA
There is a batch QA (evaluation) feature that will use another isntance of LLM to evaluate the chat answer correctness and completness. It allows to submit a batch of questions at once to test the system. Initial evaluations indicate ~ 100% accuracy. That means the answer is completely answering the questions in 100% of cases. See `./evaluate/output_qa.json` for results and `./evaluate/transcripts_qa/output_qa_transcript.json` details.

# How to run Batch QA - with Conda Environment
1. to 6. same as above
7. provide / adjust batch test questions in the file `./evaluate/questions-batch.json`
8. Run in conda prompt or terminal `python main_qa.py`
9. QA results will be output to json file `./evaluate/output_qa.json` see `config-qa.json`

# References
Great Repos I drew inspiration from:
- https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/basic_memory.py

# TODO Next
- Use bigger model like ChatGPT 4 Gemini-pro for better results
- Improve Batch QA: use LLM evaluation libraries like [DeepEval](https://github.com/confident-ai/deepeval) or similar. At minimum [groundness](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness) test should be added to prevent hallucination
- Improve references and citation formatting
- Optimize chucking strategy
- Introduce logger instead of printing to console
