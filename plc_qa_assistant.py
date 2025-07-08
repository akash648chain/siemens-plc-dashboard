import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
import json
from pathlib import Path
import pypdf
import io
from urllib.parse import urlparse
import hashlib
import pickle
from datetime import datetime
import glob
import re

# Load environment variables
load_dotenv()

class SiemensPLCQAAssistant:
    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self.qa_chain = None
        self.documents = []
        self.initialize_embeddings()
        
    def initialize_embeddings(self):
        """Initialize embeddings model"""
        # Use free HuggingFace embeddings
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
    def load_siemens_resources(self):
        """Load Siemens PLC resources from various free sources including enhanced PDF processing"""
        
        documents = []
        
        # Load local PDF files with enhanced processing
        pdf_dirs = ["./siemens_docs", "./manuals", "./pdfs"]
        
        for pdf_dir_path in pdf_dirs:
            pdf_dir = Path(pdf_dir_path)
            if pdf_dir.exists():
                documents.extend(self.load_pdfs_from_directory(pdf_dir))
        
        # Load web-based resources (kept as fallback)
        siemens_urls = [
            "https://support.industry.siemens.com/cs/document/109742464/simatic-s7-1500-system-manual?dti=0&lc=en-WW",
            "https://support.industry.siemens.com/cs/document/109478808/simatic-s7-1200-system-manual?dti=0&lc=en-WW",
            "https://support.industry.siemens.com/cs/document/109742459/simatic-s7-1500-programming-manual?dti=0&lc=en-WW"
        ]
        
        for url in siemens_urls:
            try:
                loader = WebBaseLoader(url)
                docs = loader.load()
                documents.extend(docs)
                print(f"Loaded {len(docs)} documents from {url}")
            except Exception as e:
                print(f"Error loading {url}: {e}")
        
        # Add curated PLC knowledge base
        plc_knowledge = self.get_plc_knowledge_base()
        documents.extend(plc_knowledge)
        
        print(f"Total documents loaded: {len(documents)}")
        self.documents = documents
        return documents
    
    def load_pdfs_from_directory(self, pdf_dir: Path) -> List[Document]:
        """Enhanced PDF loading with better text extraction and metadata"""
        documents = []
        
        # Support multiple PDF extensions
        pdf_patterns = ["*.pdf", "*.PDF"]
        pdf_files = []
        
        for pattern in pdf_patterns:
            pdf_files.extend(pdf_dir.glob(pattern))
        
        for pdf_file in pdf_files:
            try:
                # Use PyPDF for better text extraction
                docs = self.extract_pdf_content(pdf_file)
                documents.extend(docs)
                print(f"Loaded {len(docs)} pages from {pdf_file.name}")
            except Exception as e:
                print(f"Error loading {pdf_file}: {e}")
                # Try fallback method
                try:
                    loader = PyPDFLoader(str(pdf_file))
                    docs = loader.load()
                    documents.extend(docs)
                    print(f"Fallback: Loaded {len(docs)} pages from {pdf_file.name}")
                except Exception as fallback_error:
                    print(f"Fallback also failed for {pdf_file}: {fallback_error}")
        
        return documents
    
    def extract_pdf_content(self, pdf_path: Path) -> List[Document]:
        """Extract content from PDF with enhanced text processing"""
        documents = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    # Extract text from page
                    text = page.extract_text()
                    
                    # Clean and process text
                    cleaned_text = self.clean_pdf_text(text)
                    
                    if cleaned_text.strip():  # Only add non-empty pages
                        # Create document with rich metadata
                        doc = Document(
                            page_content=cleaned_text,
                            metadata={
                                "source": str(pdf_path),
                                "page": page_num + 1,
                                "filename": pdf_path.name,
                                "file_type": "pdf",
                                "extraction_method": "pypdf",
                                "processed_at": datetime.now().isoformat(),
                                "char_count": len(cleaned_text)
                            }
                        )
                        documents.append(doc)
                        
                except Exception as e:
                    print(f"Error extracting page {page_num + 1} from {pdf_path}: {e}")
                    continue
        
        return documents
    
    def clean_pdf_text(self, text: str) -> str:
        """Clean and normalize PDF text for better processing"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common PDF extraction issues
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between lowercase and uppercase
        text = re.sub(r'\s*\n\s*', ' ', text)  # Replace newlines with spaces
        text = re.sub(r'\s*\f\s*', ' ', text)  # Replace form feeds
        
        # Remove page numbers and headers/footers patterns
        text = re.sub(r'\b\d{1,3}\s*$', '', text)  # Remove trailing page numbers
        text = re.sub(r'^\s*\d{1,3}\s*', '', text)  # Remove leading page numbers
        
        # Remove excessive punctuation
        text = re.sub(r'[.]{3,}', '...', text)
        text = re.sub(r'[-]{3,}', '---', text)
        
        return text.strip()
    
    def upload_pdf_file(self, uploaded_file) -> List[Document]:
        """Process uploaded PDF file (for Streamlit file uploader)"""
        documents = []
        
        try:
            # Read uploaded file
            pdf_bytes = uploaded_file.read()
            pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
            
            filename = uploaded_file.name
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text = page.extract_text()
                    cleaned_text = self.clean_pdf_text(text)
                    
                    if cleaned_text.strip():
                        doc = Document(
                            page_content=cleaned_text,
                            metadata={
                                "source": f"uploaded:{filename}",
                                "page": page_num + 1,
                                "filename": filename,
                                "file_type": "pdf",
                                "extraction_method": "pypdf_upload",
                                "processed_at": datetime.now().isoformat(),
                                "char_count": len(cleaned_text)
                            }
                        )
                        documents.append(doc)
                        
                except Exception as e:
                    print(f"Error extracting page {page_num + 1} from {filename}: {e}")
                    continue
            
            print(f"Processed uploaded PDF: {filename}, {len(documents)} pages")
            
        except Exception as e:
            print(f"Error processing uploaded file {uploaded_file.name}: {e}")
            
        return documents
    
    def get_plc_knowledge_base(self):
        """Create a curated knowledge base of Siemens PLC information"""
        
        knowledge_base = [
            {
                "title": "Siemens S7-1500 Overview",
                "content": """
                The Siemens S7-1500 is a modular PLC system designed for demanding automation tasks.
                Key features:
                - High performance CPU with integrated memory
                - PROFINET interface for industrial communication
                - TIA Portal programming environment
                - Scalable I/O system
                - Integrated safety functions
                - Web server for diagnostics and HMI
                """
            },
            {
                "title": "Siemens S7-1200 Overview", 
                "content": """
                The Siemens S7-1200 is a compact PLC for small to medium automation applications.
                Key features:
                - Compact design with integrated I/O
                - PROFINET and Ethernet communication
                - TIA Portal programming
                - Built-in analog inputs/outputs
                - Pulse outputs for motion control
                - Communication modules for serial interfaces
                """
            },
            {
                "title": "TIA Portal Programming",
                "content": """
                TIA Portal (Totally Integrated Automation Portal) is Siemens' integrated engineering framework.
                Programming languages supported:
                - LAD (Ladder Logic)
                - FBD (Function Block Diagram) 
                - STL (Statement List)
                - SCL (Structured Control Language)
                - GRAPH (Sequential Function Chart)
                
                Key features:
                - Integrated development environment
                - Simulation capabilities
                - Version control
                - Library management
                - Hardware configuration
                """
            },
            {
                "title": "PROFINET Communication",
                "content": """
                PROFINET is Siemens' industrial ethernet standard for automation.
                Key aspects:
                - Real-time communication
                - Ethernet-based fieldbus
                - Integration with IT networks
                - Distributed I/O systems
                - Motion control integration
                - Diagnostic capabilities
                
                PROFINET RT (Real-Time) and IRT (Isochronous Real-Time) variants available.
                """
            },
            {
                "title": "Safety Functions",
                "content": """
                Siemens PLCs support integrated safety functions:
                - Safety Integrated technology
                - SIL 3 / PLe safety levels
                - Fail-safe I/O modules
                - Safety programming in TIA Portal
                - F-CPU for safety applications
                - Emergency stop circuits
                - Light curtain integration
                """
            },
            {
                "title": "Data Blocks and Memory",
                "content": """
                Siemens PLC memory organization:
                - Global Data Blocks (DB) for data storage
                - Instance Data Blocks for function blocks
                - Memory areas: I (Input), Q (Output), M (Memory), DB (Data Block)
                - Optimized vs. non-optimized data blocks
                - Retain memory for power-fail protection
                - Memory management and allocation
                """
            },
            {
                "title": "Common Troubleshooting",
                "content": """
                Common Siemens PLC issues and solutions:
                - Communication errors: Check network settings and cables
                - Memory errors: Review data block sizes and memory allocation
                - I/O errors: Verify hardware configuration and wiring
                - Programming errors: Use online diagnostics and force tables
                - Performance issues: Optimize scan cycle and program structure
                - Backup and restore procedures
                """
            }
        ]
        
        documents = []
        for item in knowledge_base:
            doc = Document(
                page_content=item["content"],
                metadata={"source": "knowledge_base", "title": item["title"]}
            )
            documents.append(doc)
            
        return documents
    
    def process_documents(self, documents: List[Document]):
        """Process and chunk documents for vector storage"""
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} document chunks")
        
        # Create vector store using Chroma
        self.vectorstore = Chroma.from_documents(
            chunks, 
            self.embeddings,
            persist_directory="./vectorstore"
        )
        print("Vector store created successfully")
        
        return chunks
    
    def setup_qa_chain(self):
        """Setup the QA chain with retrieval"""
        
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized. Please load and process documents first.")
        
        # Use HuggingFace pipeline for free LLM - improved for QA
        from transformers import pipeline
        
        try:
            # Try to use a better QA model first
            llm_pipeline = pipeline(
                "text2text-generation",
                model="google/flan-t5-base",
                max_length=512,
                temperature=0.3,
                do_sample=True
            )
            print("Using FLAN-T5 model for better QA performance")
        except Exception as e:
            print(f"FLAN-T5 not available ({e}), falling back to GPT-2")
            # Fallback to GPT-2 for text generation
            llm_pipeline = pipeline(
                "text-generation",
                model="gpt2",
                max_length=512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=50256
            )
        
        llm = HuggingFacePipeline(pipeline=llm_pipeline)
        
        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5}
            ),
            return_source_documents=True
        )
        
        print("QA chain setup complete")
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """Ask a question and get an answer with sources"""
        
        if self.qa_chain is None:
            raise ValueError("QA chain not initialized")
        
        # Get answer from the chain
        result = self.qa_chain({"query": question})
        
        # Extract relevant information
        answer = result.get("result", "")
        source_docs = result.get("source_documents", [])
        
        # Format sources
        sources = []
        for doc in source_docs:
            source_info = {
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata
            }
            sources.append(source_info)
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "num_sources": len(sources)
        }
    
    def save_vectorstore(self, path: str = "./vectorstore"):
        """Save the vector store to disk"""
        if self.vectorstore:
            # Chroma automatically persists to the directory specified during creation
            print(f"Vector store persisted to {path}")
    
    def load_vectorstore(self, path: str = "./vectorstore"):
        """Load vector store from disk"""
        if os.path.exists(path):
            self.vectorstore = Chroma(
                persist_directory=path,
                embedding_function=self.embeddings
            )
            print(f"Vector store loaded from {path}")
            return True
        return False

def main():
    """Main function to run the PLC QA assistant"""
    
    st.set_page_config(
        page_title="Siemens PLC QA Assistant",
        page_icon="🔧",
        layout="wide"
    )
    
    st.title("🔧 Siemens PLC Question-Answering Assistant")
    st.markdown("Ask questions about Siemens PLCs, TIA Portal, PROFINET, and automation topics!")
    
    # Initialize session state
    if 'assistant' not in st.session_state:
        st.session_state.assistant = SiemensPLCQAAssistant()
        st.session_state.initialized = False
    
    # Sidebar for initialization
    with st.sidebar:
        st.header("🚀 Setup")
        
        if st.button("Initialize Assistant"):
            with st.spinner("Loading Siemens PLC resources..."):
                try:
                    # Try to load existing vectorstore
                    if not st.session_state.assistant.load_vectorstore():
                        # Load and process documents
                        documents = st.session_state.assistant.load_siemens_resources()
                        st.session_state.assistant.process_documents(documents)
                        st.session_state.assistant.save_vectorstore()
                    
                    # Setup QA chain
                    st.session_state.assistant.setup_qa_chain()
                    st.session_state.initialized = True
                    
                    st.success("✅ Assistant initialized successfully!")
                    st.info(f"📚 Loaded {len(st.session_state.assistant.documents)} documents")
                    
                except Exception as e:
                    st.error(f"❌ Error initializing assistant: {e}")
        
        if st.session_state.initialized:
            st.success("✅ Assistant ready!")
            
            # Display some example questions
            st.subheader("💡 Example Questions")
            example_questions = [
                "What is the difference between S7-1500 and S7-1200?",
                "How do I configure PROFINET communication?",
                "What programming languages are supported in TIA Portal?",
                "How do I troubleshoot communication errors?",
                "What are the safety functions in Siemens PLCs?",
                "How do data blocks work in Siemens PLCs?"
            ]
            
            for question in example_questions:
                if st.button(question, key=f"example_{question[:20]}"):
                    st.session_state.current_question = question
    
    # Main chat interface
    if st.session_state.initialized:
        # Question input
        question = st.text_input(
            "Ask your PLC question:",
            value=st.session_state.get('current_question', ''),
            placeholder="e.g., How do I configure a safety function in TIA Portal?"
        )
        
        if st.button("🔍 Get Answer") and question:
            with st.spinner("Searching for answer..."):
                try:
                    result = st.session_state.assistant.ask_question(question)
                    
                    # Display answer
                    st.subheader("📋 Answer")
                    st.write(result["answer"])
                    
                    # Display sources
                    if result["sources"]:
                        st.subheader("📚 Sources")
                        for i, source in enumerate(result["sources"], 1):
                            with st.expander(f"Source {i}: {source['metadata'].get('title', 'Document')}"):
                                st.write(source["content"])
                                st.json(source["metadata"])
                    
                except Exception as e:
                    st.error(f"❌ Error getting answer: {e}")
        
        # Clear current question
        if 'current_question' in st.session_state:
            del st.session_state.current_question
    
    else:
        st.info("👆 Please initialize the assistant using the sidebar to get started!")
        
        # Display information about the assistant
        st.subheader("🎯 About This Assistant")
        st.markdown("""
        This AI-powered assistant helps you with Siemens PLC questions using:
        
        - **Free Resources**: Built using publicly available Siemens documentation
        - **LangChain**: Advanced retrieval-augmented generation (RAG)
        - **Local Processing**: Runs entirely on your machine
        - **Comprehensive Coverage**: S7-1500, S7-1200, TIA Portal, PROFINET, Safety
        
        **Topics Covered:**
        - PLC Programming (LAD, FBD, STL, SCL)
        - Hardware Configuration
        - Communication Protocols
        - Safety Functions
        - Troubleshooting
        - Best Practices
        """)

if __name__ == "__main__":
    main()
