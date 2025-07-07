#!/usr/bin/env python3
"""
Command-line interface for the Siemens PLC QA Assistant
"""

import argparse
import sys
from pathlib import Path
from plc_qa_assistant import SiemensPLCQAAssistant

def main():
    parser = argparse.ArgumentParser(
        description="Siemens PLC Question-Answering Assistant CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_assistant.py --init
  python cli_assistant.py --question "What is the difference between S7-1500 and S7-1200?"
  python cli_assistant.py --interactive
        """
    )
    
    parser.add_argument(
        "--init", 
        action="store_true", 
        help="Initialize the assistant by loading documents and creating vector store"
    )
    
    parser.add_argument(
        "--question", "-q", 
        type=str, 
        help="Ask a specific question"
    )
    
    parser.add_argument(
        "--interactive", "-i", 
        action="store_true", 
        help="Start interactive mode"
    )
    
    parser.add_argument(
        "--vectorstore-path", 
        type=str, 
        default="./vectorstore",
        help="Path to save/load vector store (default: ./vectorstore)"
    )
    
    args = parser.parse_args()
    
    # Create assistant instance
    assistant = SiemensPLCQAAssistant()
    
    if args.init:
        print("🚀 Initializing Siemens PLC QA Assistant...")
        try:
            # Load documents
            print("📚 Loading Siemens PLC resources...")
            documents = assistant.load_siemens_resources()
            print(f"✅ Loaded {len(documents)} documents")
            
            # Process documents
            print("⚙️ Processing documents...")
            assistant.process_documents(documents)
            
            # Save vector store
            print("💾 Saving vector store...")
            assistant.save_vectorstore(args.vectorstore_path)
            
            print("✅ Assistant initialized successfully!")
            print(f"📁 Vector store saved to: {args.vectorstore_path}")
            
        except Exception as e:
            print(f"❌ Error initializing assistant: {e}")
            sys.exit(1)
    
    elif args.question:
        print("🔍 Loading assistant...")
        try:
            # Load vector store
            if not assistant.load_vectorstore(args.vectorstore_path):
                print("❌ Vector store not found. Please run with --init first.")
                sys.exit(1)
            
            # Setup QA chain
            assistant.setup_qa_chain()
            
            # Ask question
            print(f"❓ Question: {args.question}")
            print("🤔 Thinking...")
            
            result = assistant.ask_question(args.question)
            
            print("\n📋 Answer:")
            print("-" * 50)
            print(result["answer"])
            print("-" * 50)
            
            if result["sources"]:
                print(f"\n📚 Sources ({result['num_sources']} found):")
                for i, source in enumerate(result["sources"], 1):
                    print(f"\n{i}. {source['metadata'].get('title', 'Document')}")
                    print(f"   Source: {source['metadata'].get('source', 'Unknown')}")
                    print(f"   Content: {source['content'][:150]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    elif args.interactive:
        print("🎯 Starting interactive mode...")
        print("Type 'quit' or 'exit' to end the session")
        
        try:
            # Load vector store
            if not assistant.load_vectorstore(args.vectorstore_path):
                print("❌ Vector store not found. Please run with --init first.")
                sys.exit(1)
            
            # Setup QA chain
            assistant.setup_qa_chain()
            print("✅ Assistant ready!\n")
            
            while True:
                try:
                    question = input("\n🔧 Ask your PLC question: ").strip()
                    
                    if question.lower() in ['quit', 'exit', 'q']:
                        print("👋 Goodbye!")
                        break
                    
                    if not question:
                        continue
                    
                    print("🤔 Thinking...")
                    result = assistant.ask_question(question)
                    
                    print("\n📋 Answer:")
                    print("-" * 50)
                    print(result["answer"])
                    print("-" * 50)
                    
                    if result["sources"]:
                        print(f"\n📚 Found {result['num_sources']} relevant sources")
                        show_sources = input("Show sources? (y/n): ").lower().startswith('y')
                        if show_sources:
                            for i, source in enumerate(result["sources"], 1):
                                print(f"\n{i}. {source['metadata'].get('title', 'Document')}")
                                print(f"   {source['content'][:200]}...")
                
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
