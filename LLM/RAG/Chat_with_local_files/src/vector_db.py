import os
from pathlib import Path
from typing import Dict, List, Type, Optional, Sequence
from langchain_core.documents import Document
from google import genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup, SoupStrainer
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain.utils.html import (PREFIXES_TO_IGNORE_REGEX,
                                  SUFFIXES_TO_IGNORE_REGEX)
import re
import json
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import BSHTMLLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
import glob
from typing import Dict, List, Type, Optional
import datetime
from urllib.parse import urljoin

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent  # from src/vector_db.py to v1/
CONFIG_FILE = PROJECT_ROOT / "config.json"

class VectorDB():
    """
        Class represeting vector database
            - fetches documents from local files or a webpage
            - generates embeddings using Google Gemini embedding model 
        Usage: 1. init, 2. create_db_from_url/create_db_from_local_html OR 2. load_db_from_file (if downloaded previously), 3. get_retriever
    """
    # Define supported loader mappings
    LOADER_MAPPING = {
        'html': BSHTMLLoader,
        'md': UnstructuredMarkdownLoader,
        'markdown': UnstructuredMarkdownLoader,
        'txt': TextLoader,
        'pdf': PyPDFLoader,
        # Add more mappings as needed
    }

    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.CONFIG = self.get_config(CONFIG_FILE)
        self.init()

    def init(self):
        """
            Initialize variables, loads Gemini secrets
        """
        self.DEBUG = self.CONFIG.get('debug', False)

        if self.DEBUG:
            print('─' * 100)
            print('>>> VECTOR DB INIT')

        # load secrets from env var if not already loaded
        _ = load_dotenv(find_dotenv(), verbose=self.DEBUG)
        
        # # Initialize Gemini if not already configured
        # if not genai._configured:
        #     genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        if self.DEBUG:
            print('Gemini secrets loaded for embeddings')

    def get_config(self, config_file):
        """
        Get config from config.json file and process paths
        """
        with open(config_file) as f:
            config = json.load(f)
        
        # Convert relative paths in config to absolute paths
        self.process_paths(config)
        return config
    
    def process_paths(self, config):
        """
        Convert relative paths in config to absolute paths
        """
        # Process vector_db path
        vector_db = config.get('vector_db', {})
        if 'vector_db_path' in vector_db:
            vector_db['vector_db_path'] = str(self.project_root / vector_db['vector_db_path'])
            
        # Process transcript_file_path
        if 'transcript_file_path' in config:
            config['transcript_file_path'] = str(self.project_root / config['transcript_file_path'])
            
        # Process docs path
        doc_loading = config.get('document_loading', {})
        if 'local_docs_path' in doc_loading:
            doc_loading['local_docs_path'] = str(self.project_root / doc_loading['local_docs_path'])
            
        # Create directories if they don't exist
        paths_to_create = [
            config.get('vector_db', {}).get('vector_db_path'),
            config.get('transcript_file_path'),
            config.get('document_loading', {}).get('local_docs_path')
        ]
        
        for path in paths_to_create:
            if path:
                Path(path).mkdir(parents=True, exist_ok=True)

    def get_retriever(self):
        return self.retriever
    
    def create_db_from_url(self):
        """
            Create vector database from a URL e.g. https://spark.apache.org/docs/latest/api/python/reference/index.html
        """
        # load documents from IBM Generative AI SDK
        raw_docs = self.get_documents_from_url()
        # preprocess documents
        processed_docs = self.preprocess_documents(raw_docs)
        # create vector database
        self.create_vector_db(processed_docs)

    def load_db_from_file(self):
        """
            Loads vector database file - see config for path
        """
        # create embeddings using Gemini
        embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # load vectorstore from file
        vector_db_path = self.CONFIG.get('vector_db', {}).get('vector_db_path')

        self.vectorstore = Chroma(
            persist_directory=vector_db_path, 
            embedding_function=embedding)
        
        if self.DEBUG:
            print(f'>>> Vectorstore loaded from path: {vector_db_path}')

        self.retriever = self.vectorstore.as_retriever(
            search_type=self.CONFIG.get('vector_db', {}).get('retriever_search_type', 'similarity'), 
            search_kwargs={"k": self.CONFIG.get('vector_db', {}).get('retriever_num_docs', 4)}
        )

    def create_vector_db(self, processed_docs):
        # create embeddings using Gemini
        embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
         # create vector database and loads embedded documents
        vector_db_path = self.CONFIG.get('vector_db', {}).get('vector_db_path')
        self.vectorstore = Chroma.from_documents(
            documents=processed_docs, 
            embedding=embedding, 
            persist_directory=vector_db_path
        )
        
        self.retriever = self.vectorstore.as_retriever(
            search_type=self.CONFIG.get('vector_db', {}).get('retriever_search_type', 'similarity'),
            search_kwargs={"k": self.CONFIG.get('vector_db', {}).get('retriever_num_docs', 4)}
        )

    def simple_extractor(self, html: str) -> str:
        soup = BeautifulSoup(
            html, 
            "lxml",  
            parse_only = SoupStrainer( 
            'article', role = 'main'))
        return re.sub(r"\n\n+", "\n\n", soup.text).strip()

    def get_documents_from_url(self):
        """
            Get documents from URL
        """
        # load documents from IBM Generative AI SDK
        api_ref = RecursiveUrlLoader(
            self.CONFIG.get('document_downloading', {}).get('retriever_URL_to_get'),
            max_depth=self.CONFIG.get('document_downloading', {}).get('retriever_URL_scrape_depth', 4),
            extractor=self.simple_extractor,
            prevent_outside=True,
            use_async=False,
            timeout=600,
            check_response_status=True,
            exclude_dirs=(
                self.CONFIG.get('document_downloading', {}).get('retriever_URL_to_exclude', [])
            ),
            # drop trailing / to avoid duplicate pages.
            link_regex=(
                f"href=[\"']{PREFIXES_TO_IGNORE_REGEX}((?:{SUFFIXES_TO_IGNORE_REGEX}.)*?)"
                r"(?:[\#'\"]|\/[\#'\"])"
            ),
        ).load()

        if self.DEBUG:
            # test doc loading
            print('Document loading from URL')
            print(f'Nuber of docs loaded: {len(api_ref)}')
            print(f"excluded: {self.CONFIG.get('document_downloading', {}).get('retriever_URL_to_exclude', [])}")
            # print(f'First doc lenght: {len(api_ref[0].page_content)}')
            # print(f'Sample: {api_ref[1].page_content[:500]}')

        return api_ref

    def create_db_from_local(self, directory_path=None):
        """
        Create vector database from local files based on config-specified file types
        Args:
            directory_path: Path to directory containing files. 
                          If None, uses path from config.
        """
        if directory_path is None:
            directory_path = self.CONFIG.get('document_loading', {}).get('local_docs_path')
            if directory_path is None:
                raise ValueError("No directory path provided and no default path in config")
        
        # Convert to Path object and resolve to absolute path
        base_path = Path(directory_path).resolve()
        
        if self.DEBUG:
            print(f'Loading documents from directory: {base_path}')

        file_types = self.CONFIG.get('document_loading', {}).get('file_types', ['html', 'md'])
        if isinstance(file_types, dict):
            file_types = [ft for ft, enabled in file_types.items() if enabled]
        
        if not file_types:
            raise ValueError("No file types specified in config")

        # Load documents for each file type
        raw_docs = []
        total_files = 0
        
        for file_type in file_types:
            file_type = file_type.lower().strip('.')
            if file_type not in self.LOADER_MAPPING:
                if self.DEBUG:
                    print(f'Warning: Unsupported file type: {file_type}')
                continue

            try:
                # Get all files of this type
                files = list(base_path.rglob(f"*.{file_type}"))
                
                for file_path in files:
                    try:
                        # Load individual file with enhanced metadata
                        docs = self._load_single_file(file_path, base_path, file_type)
                        raw_docs.extend(docs)
                        total_files += 1
                        
                        if self.DEBUG:
                            print(f'Loaded file {file_path}')
                            
                    except Exception as e:
                        if self.DEBUG:
                            print(f'Error loading file {file_path}: {str(e)}')
                
                if self.DEBUG:
                    print(f'Loaded {len(files)} .{file_type} files')
                
            except Exception as e:
                if self.DEBUG:
                    print(f'Error processing {file_type} files: {str(e)}')

        if not raw_docs:
            raise ValueError(f"No supported documents found in {base_path}")
        
        if self.DEBUG:
            print(f'Total files loaded: {total_files}')
            self._print_file_type_statistics(raw_docs)
        
        # Preprocess documents
        processed_docs = self.preprocess_documents(raw_docs)
        
        # Create vector database
        self.create_vector_db(processed_docs)

    def _extract_content_from_html(self,file_path):
        """
            Extract content from HTML files - adjusted approach for kafka documentation, where the content isnt in the standard sections (e.g. main)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
        except Exception as e:
            print(f"Failed to read {file_path}: {e}")
            return None

        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract content from script sections
        script_content = ""
        for script in soup.find_all('script'):
            if script.string:
                # Remove HTML tags and comments
                content = re.sub(r'<.*?>', '', script.string)  # Remove HTML tags
                content = re.sub(r'<!--.*?-->', '', content)  # Remove HTML comments
                content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
                script_content += content.strip() + "\n"

        # Extract content from main sections
        main_content = soup.find('main')
        if main_content:
            main_text = main_content.get_text(strip=True)
        else:
            main_text = ""

        # Extract content from other sections (e.g., divs)
        other_content = ""
        for section in soup.find_all(['div', 'section']):
            if section.get_text(strip=True):
                other_content += section.get_text(strip=True) + "\n"

        # Combine all extracted content
        content = main_text + "\n" + script_content + "\n" + other_content

        return content.strip()
    
    def _load_single_file(self, file_path: Path, base_path: Path, file_type: str) -> List[Document]:
        """
        Load a single file with enhanced metadata
        """
        if self.DEBUG:
            print(f'Loading file: {file_path}')
        
        # Get loader class
        loader_cls = self.LOADER_MAPPING[file_type]
        
        # Special handling for HTML files
        if file_type == 'html':
            try:
                text = self._extract_content_from_html(file_path)
                
                # Create document
                doc = Document(
                    page_content=text,
                    # metadata={
                    #     'source': str(file_path),
                    #     'relative_path': str(file_path.relative_to(base_path)),
                    #     'file_name': file_path.name,
                    #     'file_type': file_type,
                    #     'title': self._extract_title(doc, file_path),
                    #     'last_modified': datetime.datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    #     'size': file_path.stat().st_size
                    # }
                )
                docs = [doc]
                
            except Exception as e:
                if self.DEBUG:
                    print(f"Error processing HTML file {file_path}: {str(e)}")
                raise
        else:
            # For non-HTML files, use the default loader
            loader = loader_cls(str(file_path))
            docs = loader.load()
        
        # Enhance metadata for each document
        for doc in docs:
            # Calculate relative path from base directory
            rel_path = file_path.relative_to(base_path)
            
            # Generate URL/link based on config
            url = self._generate_document_url(file_path, base_path, rel_path)
            
            # Enhanced metadata
            doc.metadata.update({
                'source': str(file_path),
                'relative_path': str(rel_path),
                'file_name': file_path.name,
                'file_type': file_type,
                'url': url,
                'title': self._extract_title(doc, file_path),
                'last_modified': datetime.datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                'size': file_path.stat().st_size,
                'project_root': str(self.project_root)
            })
        
        return docs

    def _generate_document_url(self, file_path: Path, base_path: Path, rel_path: Path) -> str:
        """
        Generate local file URL relative to project root
        Args:
            file_path: Full path to the file
            base_path: Base directory of documents
            rel_path: Relative path from base directory
        Returns:
            str: Local file URL or path
        """
        # Get docs directory from config
        docs_dir = self.CONFIG.get('document_loading', {}).get('local_docs_path', 'docs')
        
        # Create path relative to project root
        doc_path = Path(docs_dir) / rel_path
        
        if self.CONFIG.get('document_loading', {}).get('use_file_urls', True):
            # Use file:// URL format
            absolute_path = (self.project_root / doc_path).resolve()
            return f"file:///{absolute_path.as_posix()}"
        else:
            # Use relative path from project root
            return str(doc_path)

    def _extract_title(self, doc, file_path: Path) -> str:
        """
        Extract title from document filename
        """
        # Fallback to filename without extension
        return file_path.stem

    def _print_file_type_statistics(self, docs: List[Document]) -> None:
        """Print statistics about loaded documents by file type"""
        if not self.DEBUG:
            return
        
        stats: Dict[str, int] = {}
        for doc in docs:
            file_type = Path(doc.metadata.get('source', '')).suffix.lower().strip('.')
            stats[file_type] = stats.get(file_type, 0) + 1
        
        for file_type, count in stats.items():
            print(f'  - {file_type}: {count} files')

    def preprocess_documents(self, docs: List[Document]) -> List[Document]:
        """
        Preprocess documents while preserving enhanced metadata
        """
        chunk_size = self.CONFIG.get('document_loading', {}).get('chunk_size', 2000)
        chunk_overlap = self.CONFIG.get('document_loading', {}).get('chunk_overlap', 200)

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Split documents while preserving metadata
        all_splits = text_splitter.split_documents(docs)

        # Enhance chunk metadata
        for i, chunk in enumerate(all_splits):
            chunk.metadata['chunk_id'] = i
            chunk.metadata['chunk_size'] = len(chunk.page_content)
            
            # Create a content preview
            preview = chunk.page_content[:100].replace('\n', ' ').strip()
            chunk.metadata['preview'] = f"{preview}..."

        if self.DEBUG:
            self._print_chunk_statistics(all_splits)

        return all_splits

    def _print_chunk_statistics(self, chunks: List[Document]) -> None:
        """Print detailed statistics about document chunks"""
        if not self.DEBUG:
            return

        print('\nChunk statistics:')
        stats_by_type: Dict[str, Dict[str, int]] = {}
        
        for chunk in chunks:
            doc_type = chunk.metadata.get('source_type', 'unknown')
            if doc_type not in stats_by_type:
                stats_by_type[doc_type] = {
                    'count': 0,
                    'total_size': 0,
                    'min_size': float('inf'),
                    'max_size': 0
                }
            
            chunk_size = len(chunk.page_content)
            stats = stats_by_type[doc_type]
            stats['count'] += 1
            stats['total_size'] += chunk_size
            stats['min_size'] = min(stats['min_size'], chunk_size)
            stats['max_size'] = max(stats['max_size'], chunk_size)

        for doc_type, stats in stats_by_type.items():
            avg_size = stats['total_size'] / stats['count']
            print(f'  Count: {stats["count"]}')
            print(f'  Average size: {avg_size:.0f} characters')
            print(f'  Min size: {stats["min_size"]} characters')
            print(f'  Max size: {stats["max_size"]} characters')

    def _generate_document_metadata(self, file_path: Path, base_path: Path, file_type: str) -> Dict:
        """
        Generate metadata for a document
        """
        rel_path = file_path.relative_to(base_path)
        url = self._generate_document_url(file_path, base_path, rel_path)
        title = self._extract_title(file_path)
        
        return {
            'source': str(file_path),
            'relative_path': str(rel_path),
            'file_name': file_path.name,
            'file_type': file_type,
            'url': url,
            'title': title,
            'last_modified': datetime.datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            'size': file_path.stat().st_size
        }