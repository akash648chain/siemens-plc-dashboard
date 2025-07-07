#!/usr/bin/env python3
"""
Test script for the Siemens PLC QA Assistant
"""

import sys
import time
from plc_qa_assistant import SiemensPLCQAAssistant

def test_basic_functionality():
    """Test basic assistant functionality"""
    
    print("🧪 Testing Siemens PLC QA Assistant")
    print("=" * 50)
    
    # Initialize assistant
    print("1️⃣ Initializing assistant...")
    assistant = SiemensPLCQAAssistant()
    print("✅ Assistant created")
    
    # Load knowledge base
    print("\n2️⃣ Loading knowledge base...")
    documents = assistant.load_siemens_resources()
    print(f"✅ Loaded {len(documents)} documents")
    
    # Process documents
    print("\n3️⃣ Processing documents...")
    chunks = assistant.process_documents(documents)
    print(f"✅ Created {len(chunks)} text chunks")
    
    # Setup QA chain
    print("\n4️⃣ Setting up QA chain...")
    try:
        assistant.setup_qa_chain()
        print("✅ QA chain initialized")
    except Exception as e:
        print(f"❌ Error setting up QA chain: {e}")
        return False
    
    # Test questions
    print("\n5️⃣ Testing with sample questions...")
    test_questions = [
        "What is the difference between S7-1500 and S7-1200?",
        "What programming languages are supported in TIA Portal?",
        "How do data blocks work in Siemens PLCs?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n   Question {i}: {question}")
        try:
            result = assistant.ask_question(question)
            print(f"   ✅ Answer: {result['answer'][:100]}...")
            print(f"   📚 Sources found: {result['num_sources']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    print("\n🎉 All tests passed!")
    return True

def test_knowledge_base():
    """Test the built-in knowledge base"""
    
    print("\n🧪 Testing Knowledge Base")
    print("=" * 30)
    
    assistant = SiemensPLCQAAssistant()
    knowledge_docs = assistant.get_plc_knowledge_base()
    
    print(f"📚 Knowledge base contains {len(knowledge_docs)} documents")
    
    for i, doc in enumerate(knowledge_docs, 1):
        title = doc.metadata.get('title', 'Unknown')
        content_length = len(doc.page_content)
        print(f"   {i}. {title} ({content_length} characters)")
    
    print("✅ Knowledge base test completed")

def test_vectorstore_persistence():
    """Test saving and loading vector store"""
    
    print("\n🧪 Testing Vector Store Persistence")
    print("=" * 40)
    
    assistant = SiemensPLCQAAssistant()
    
    # Load and process minimal data
    documents = assistant.get_plc_knowledge_base()
    assistant.process_documents(documents)
    
    # Save vector store
    print("💾 Saving vector store...")
    assistant.save_vectorstore("./test_vectorstore")
    print("✅ Vector store saved")
    
    # Create new assistant and load
    print("📂 Loading vector store...")
    new_assistant = SiemensPLCQAAssistant()
    loaded = new_assistant.load_vectorstore("./test_vectorstore")
    
    if loaded:
        print("✅ Vector store loaded successfully")
    else:
        print("❌ Failed to load vector store")
        return False
    
    # Clean up
    import shutil
    import os
    if os.path.exists("./test_vectorstore"):
        shutil.rmtree("./test_vectorstore")
        print("🧹 Cleaned up test files")
    
    return True

def benchmark_performance():
    """Benchmark assistant performance"""
    
    print("\n⏱️  Performance Benchmark")
    print("=" * 30)
    
    assistant = SiemensPLCQAAssistant()
    
    # Time document loading
    start_time = time.time()
    documents = assistant.load_siemens_resources()
    load_time = time.time() - start_time
    print(f"📚 Document loading: {load_time:.2f} seconds")
    
    # Time document processing
    start_time = time.time()
    assistant.process_documents(documents)
    process_time = time.time() - start_time
    print(f"⚙️ Document processing: {process_time:.2f} seconds")
    
    # Time QA chain setup
    start_time = time.time()
    try:
        assistant.setup_qa_chain()
        setup_time = time.time() - start_time
        print(f"🔗 QA chain setup: {setup_time:.2f} seconds")
        
        # Time question answering
        question = "What is TIA Portal?"
        start_time = time.time()
        result = assistant.ask_question(question)
        answer_time = time.time() - start_time
        print(f"❓ Question answering: {answer_time:.2f} seconds")
        
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        return False
    
    total_time = load_time + process_time + setup_time
    print(f"⏱️  Total initialization time: {total_time:.2f} seconds")
    
    return True

def main():
    """Run all tests"""
    
    print("🚀 Siemens PLC QA Assistant Test Suite")
    print("=" * 60)
    
    tests = [
        ("Knowledge Base", test_knowledge_base),
        ("Vector Store Persistence", test_vectorstore_persistence),
        ("Performance Benchmark", benchmark_performance),
        ("Basic Functionality", test_basic_functionality)  # Most comprehensive test last
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The assistant is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
