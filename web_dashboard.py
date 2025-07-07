#!/usr/bin/env python3
"""
Web dashboard for Siemens PLC QA Assistant
Accessible from any device on the network
"""

from flask import Flask, render_template, request, jsonify, session
import os
import json
import threading
import time
from datetime import datetime
from plc_qa_assistant import SiemensPLCQAAssistant
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)
app.secret_key = 'plc_qa_dashboard_secret_key_2024'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Global assistant instance
assistant = None
assistant_ready = False
initialization_status = {"status": "not_started", "message": ""}

def initialize_assistant():
    """Initialize the assistant in a background thread"""
    global assistant, assistant_ready, initialization_status
    
    try:
        initialization_status["status"] = "initializing"
        initialization_status["message"] = "Creating assistant instance..."
        
        assistant = SiemensPLCQAAssistant()
        
        initialization_status["message"] = "Loading documents..."
        
        # Try to load existing vectorstore first
        if not assistant.load_vectorstore():
            initialization_status["message"] = "Loading Siemens PLC resources..."
            documents = assistant.load_siemens_resources()
            
            initialization_status["message"] = "Processing documents..."
            assistant.process_documents(documents)
            
            initialization_status["message"] = "Saving vector store..."
            assistant.save_vectorstore()
        
        initialization_status["message"] = "Setting up QA chain..."
        assistant.setup_qa_chain()
        
        assistant_ready = True
        initialization_status["status"] = "ready"
        initialization_status["message"] = "Assistant ready!"
        
        logger.info("Assistant initialized successfully")
        
    except Exception as e:
        assistant_ready = False
        initialization_status["status"] = "error"
        initialization_status["message"] = f"Error: {str(e)}"
        logger.error(f"Assistant initialization failed: {e}")

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """Get assistant status"""
    return jsonify({
        "ready": assistant_ready,
        "status": initialization_status["status"],
        "message": initialization_status["message"]
    })

@app.route('/api/initialize', methods=['POST'])
def api_initialize():
    """Initialize the assistant"""
    global assistant_ready, initialization_status
    
    if not assistant_ready and initialization_status["status"] != "initializing":
        # Start initialization in background thread
        thread = threading.Thread(target=initialize_assistant)
        thread.daemon = True
        thread.start()
        
        return jsonify({"success": True, "message": "Initialization started"})
    elif assistant_ready:
        return jsonify({"success": True, "message": "Assistant already ready"})
    else:
        return jsonify({"success": False, "message": "Initialization already in progress"})

@app.route('/api/ask', methods=['POST'])
def api_ask():
    """Ask a question to the assistant"""
    global assistant, assistant_ready
    
    if not assistant_ready:
        return jsonify({
            "success": False, 
            "error": "Assistant not ready. Please initialize first."
        }), 400
    
    data = request.get_json()
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({
            "success": False, 
            "error": "Please provide a question"
        }), 400
    
    try:
        # Get answer from assistant
        result = assistant.ask_question(question)
        
        # Store in session history
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        chat_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"],
            "num_sources": result["num_sources"]
        }
        
        session['chat_history'].append(chat_entry)
        
        # Keep only last 20 entries
        if len(session['chat_history']) > 20:
            session['chat_history'] = session['chat_history'][-20:]
        
        return jsonify({
            "success": True,
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"],
            "num_sources": result["num_sources"],
            "timestamp": chat_entry["timestamp"]
        })
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        return jsonify({
            "success": False,
            "error": f"Error processing question: {str(e)}"
        }), 500

@app.route('/api/history')
def api_history():
    """Get chat history"""
    history = session.get('chat_history', [])
    return jsonify({"history": history})

@app.route('/api/clear-history', methods=['POST'])
def api_clear_history():
    """Clear chat history"""
    session['chat_history'] = []
    return jsonify({"success": True, "message": "History cleared"})

@app.route('/api/examples')
def api_examples():
    """Get example questions"""
    examples = [
        {
            "category": "PLC Comparison",
            "questions": [
                "What is the difference between S7-1500 and S7-1200?",
                "Which PLC should I choose for my application?",
                "What are the key features of S7-1500?"
            ]
        },
        {
            "category": "Programming",
            "questions": [
                "What programming languages are supported in TIA Portal?",
                "How do I create a function block in LAD?",
                "What is the difference between LAD and FBD?"
            ]
        },
        {
            "category": "Communication",
            "questions": [
                "How do I configure PROFINET communication?",
                "What is the difference between PROFINET RT and IRT?",
                "How to set up Ethernet communication?"
            ]
        },
        {
            "category": "Safety",
            "questions": [
                "What are the safety functions in Siemens PLCs?",
                "How do I configure a safety function in TIA Portal?",
                "What is Safety Integrated technology?"
            ]
        },
        {
            "category": "Troubleshooting",
            "questions": [
                "How do I troubleshoot communication errors?",
                "Why is my PLC not responding?",
                "How to diagnose I/O errors?"
            ]
        },
        {
            "category": "Data Management",
            "questions": [
                "How do data blocks work in Siemens PLCs?",
                "What is the difference between optimized and non-optimized data blocks?",
                "How do I backup and restore PLC data?"
            ]
        }
    ]
    
    return jsonify({"examples": examples})

@app.route('/api/system-info')
def api_system_info():
    """Get system information"""
    import psutil
    import platform
    
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        system_info = {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "cpu_usage": f"{cpu_percent}%",
            "memory_usage": f"{memory.percent}%",
            "memory_available": f"{memory.available / (1024**3):.1f} GB",
            "disk_usage": f"{disk.percent}%",
            "disk_free": f"{disk.free / (1024**3):.1f} GB"
        }
        
        return jsonify({"system_info": system_info})
    except Exception as e:
        return jsonify({"error": f"Could not get system info: {str(e)}"})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🚀 Starting Siemens PLC QA Dashboard...")
    print("🌐 Access from any device on your network!")
    print("📱 Mobile-friendly interface included")
    print("=" * 50)
    
    # Get local IP address
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"🖥️  Local access: http://localhost:8080")
    print(f"📱 Network access: http://{local_ip}:8080")
    print("=" * 50)
    
    # Run Flask app
    app.run(
        host='0.0.0.0',  # Allow access from any device on network
        port=8080,
        debug=False,
        threaded=True
    )
