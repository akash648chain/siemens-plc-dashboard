#!/usr/bin/env python3
"""
Production-ready Siemens PLC QA Dashboard with LangChain RAG
Advanced AI-powered responses using retrieval-augmented generation
"""

import os
import logging
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
from dotenv import load_dotenv
import threading
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['TEMPLATES_AUTO_RELOAD'] = False  # Disable in production

# CORS configuration - restrict in production
CORS(app, origins=os.getenv('ALLOWED_ORIGINS', '*').split(','))

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"  # Explicitly specify memory storage
)
limiter.init_app(app)

# Global assistant instance
assistant = None
assistant_ready = False
initialization_status = {"status": "not_started", "message": ""}

def initialize_assistant():
    """Initialize the RAG assistant in a background thread"""
    global assistant, assistant_ready, initialization_status
    
    try:
        initialization_status["status"] = "initializing"
        initialization_status["message"] = "Creating RAG assistant instance..."
        
        # Import here to avoid import errors if dependencies not available
        try:
            from plc_qa_assistant import SiemensPLCQAAssistant
            assistant = SiemensPLCQAAssistant()
        except ImportError:
            # Fallback to simple assistant if RAG dependencies not available
            logger.warning("LangChain dependencies not available, falling back to simple assistant")
            from simple_plc_assistant import SimplePLCQAAssistant
            assistant = SimplePLCQAAssistant()
            assistant_ready = True
            initialization_status["status"] = "ready"
            initialization_status["message"] = "Simple assistant ready! (RAG mode unavailable)"
            return
        
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
        initialization_status["message"] = "RAG assistant ready!"
        
        logger.info("RAG assistant initialized successfully")
        
    except Exception as e:
        assistant_ready = False
        initialization_status["status"] = "error"
        initialization_status["message"] = f"Error: {str(e)}"
        logger.error(f"RAG assistant initialization failed: {e}")
        
        # Try to fallback to simple assistant
        try:
            from simple_plc_assistant import SimplePLCQAAssistant
            assistant = SimplePLCQAAssistant()
            assistant_ready = True
            initialization_status["status"] = "ready"
            initialization_status["message"] = "Simple assistant ready! (RAG initialization failed)"
            logger.info("Fallback to simple assistant successful")
        except Exception as fallback_error:
            logger.error(f"Fallback to simple assistant also failed: {fallback_error}")

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('rag_dashboard.html')

@app.route('/health')
def health_check():
    """Health check endpoint for load balancers"""
    return jsonify({
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "rag_ready": assistant_ready,
        "assistant_status": initialization_status["status"]
    })

@app.route('/api/status')
def api_status():
    """Get assistant status"""
    return jsonify({
        "ready": assistant_ready,
        "status": initialization_status["status"],
        "message": initialization_status["message"],
        "rag_enabled": "plc_qa_assistant" in str(type(assistant)) if assistant else False
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
        
        return jsonify({"success": True, "message": "RAG initialization started"})
    elif assistant_ready:
        return jsonify({"success": True, "message": "Assistant already ready"})
    else:
        return jsonify({"success": False, "message": "Initialization already in progress"})

@app.route('/api/ask', methods=['POST'])
@limiter.limit("10 per minute")
def api_ask():
    """Ask a question to the RAG assistant"""
    global assistant, assistant_ready
    
    if not assistant_ready:
        return jsonify({
            "success": False, 
            "error": "Assistant not ready. Please initialize first."
        }), 400
    
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False, 
            "error": "Invalid JSON data"
        }), 400
    
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({
            "success": False, 
            "error": "Please provide a question"
        }), 400
    
    if len(question) > 1000:
        return jsonify({
            "success": False, 
            "error": "Question too long (max 1000 characters)"
        }), 400
    
    try:
        # Get answer from assistant (works with both RAG and simple)
        result = assistant.ask_question(question)
        
        # Store in session history
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        chat_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"],
            "num_sources": result["num_sources"],
            "rag_enabled": "plc_qa_assistant" in str(type(assistant))
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
            "timestamp": chat_entry["timestamp"],
            "rag_enabled": chat_entry["rag_enabled"]
        })
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        return jsonify({
            "success": False,
            "error": "An error occurred while processing your question"
        }), 500

@app.route('/api/history')
def api_history():
    """Get chat history"""
    history = session.get('chat_history', [])
    return jsonify({"history": history})

@app.route('/api/clear-history', methods=['POST'])
@limiter.limit("5 per minute")
def api_clear_history():
    """Clear chat history"""
    session['chat_history'] = []
    return jsonify({"success": True, "message": "History cleared"})

@app.route('/api/examples')
def api_examples():
    """Get example questions optimized for RAG"""
    examples = [
        {
            "category": "Advanced PLC Comparison",
            "questions": [
                "What are the detailed differences between S7-1500 and S7-1200 performance specifications?",
                "Compare the memory architecture of S7-1500 vs S7-1200 systems",
                "Which PLC should I choose for a high-speed packaging application with 200 I/O points?",
                "What are the communication capabilities of each PLC family?"
            ]
        },
        {
            "category": "TIA Portal Programming",
            "questions": [
                "How do I implement a structured safety function in TIA Portal using F-FBD?",
                "What are the best practices for optimizing scan time in large TIA Portal projects?",
                "How do I configure and use the integrated web server in S7-1500?",
                "Explain the difference between optimized and non-optimized data blocks with examples"
            ]
        },
        {
            "category": "PROFINET Configuration",
            "questions": [
                "How do I configure PROFINET IRT for deterministic motion control applications?",
                "What are the specific steps to set up PROFINET RT with QoS settings?",
                "How do I troubleshoot PROFINET topology discovery issues?",
                "What are the bandwidth requirements for different PROFINET configurations?"
            ]
        },
        {
            "category": "Safety Systems",
            "questions": [
                "How do I implement SIL 3 safety functions using F-CPU and fail-safe I/O?",
                "What are the validation procedures for safety functions in TIA Portal?",
                "How do I configure emergency stop circuits with dual-channel monitoring?",
                "Explain the difference between SIL and PLe safety classifications"
            ]
        },
        {
            "category": "Advanced Troubleshooting",
            "questions": [
                "How do I diagnose and resolve PROFINET communication error 16#8087?",
                "What are the systematic steps to troubleshoot S7-1500 CPU hardware faults?",
                "How do I analyze and optimize PLC performance using TIA Portal diagnostics?",
                "What diagnostic tools are available for motion control troubleshooting?"
            ]
        },
        {
            "category": "Integration & Networking",
            "questions": [
                "How do I integrate Siemens PLCs with Industrial Ethernet networks securely?",
                "What are the cybersecurity best practices for PROFINET networks?",
                "How do I set up remote access to S7-1500 via VPN with proper security?",
                "How do I configure time synchronization across a distributed PLC network?"
            ]
        }
    ]
    
    return jsonify({"examples": examples})

@app.route('/api/system-info')
@limiter.limit("2 per minute")
def api_system_info():
    """Get basic system information"""
    try:
        import psutil
        import platform
        
        system_info = {
            "status": "running",
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "assistant_type": "RAG" if "plc_qa_assistant" in str(type(assistant)) else "Simple",
            "vector_store": "Available" if assistant_ready and hasattr(assistant, 'vectorstore') else "Not Available",
            "uptime": "available"
        }
        
        return jsonify({"system_info": system_info})
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return jsonify({"error": "System info unavailable"}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limiting"""
    return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {e}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5003))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    logger.info(f"Starting PLC QA Dashboard with RAG support on port {port}")
    
    # In production, use gunicorn instead of Flask's development server
    if debug:
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
