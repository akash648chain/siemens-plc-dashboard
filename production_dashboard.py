#!/usr/bin/env python3
"""
Production-ready Siemens PLC QA Dashboard
Configured for cloud deployment with security features
"""

import os
import logging
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
from simple_plc_assistant import SimplePLCQAAssistant
from dotenv import load_dotenv

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
try:
    from simple_plc_assistant import SimplePLCQAAssistant
    assistant = SimplePLCQAAssistant()
    logger.info("✅ Simple PLC Assistant loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load assistant: {e}")
    assistant = None

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('simple_dashboard.html')

@app.route('/health')
def health_check():
    """Health check endpoint for load balancers"""
    return jsonify({
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "version": "simple",
        "ready": True
    })

@app.route('/api/status')
def api_status():
    """Get assistant status"""
    return jsonify({
        "ready": True,
        "status": "ready",
        "message": "Simple PLC Assistant ready!",
        "version": "1.0.0"
    })

@app.route('/api/ask', methods=['POST'])
@limiter.limit("10 per minute")
def api_ask():
    """Ask a question to the assistant"""
    global assistant
    
    if not assistant:
        return jsonify({
            "success": False, 
            "error": "Assistant not available. Please try again later."
        }), 500
    
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
    """Get example questions"""
    examples = [
        {
            "category": "PLC Comparison",
            "questions": [
                "What is the difference between S7-1500 and S7-1200?",
                "Which PLC should I choose for my application?",
                "What are the key features of S7-1500?",
                "What are S7-1200 applications?"
            ]
        },
        {
            "category": "Programming",
            "questions": [
                "What programming languages are supported in TIA Portal?",
                "How do I use ladder logic?",
                "What is function block diagram?",
                "Explain SCL programming language"
            ]
        },
        {
            "category": "Communication",
            "questions": [
                "How do I configure PROFINET communication?",
                "What is the difference between PROFINET RT and IRT?",
                "How to set up Ethernet communication?",
                "PROFINET configuration steps"
            ]
        },
        {
            "category": "Safety",
            "questions": [
                "What are the safety functions in Siemens PLCs?",
                "How do I configure a safety function?",
                "What is Safety Integrated technology?",
                "Explain SIL and PLe safety levels"
            ]
        },
        {
            "category": "Troubleshooting",
            "questions": [
                "How do I troubleshoot communication errors?",
                "Why is my PLC not responding?",
                "How to diagnose I/O errors?",
                "CPU fault troubleshooting"
            ]
        },
        {
            "category": "Data Management",
            "questions": [
                "How do data blocks work in Siemens PLCs?",
                "What is the difference between optimized and non-optimized data blocks?",
                "Explain PLC memory organization",
                "What is retain memory?"
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
        
        # Only show basic info in production
        system_info = {
            "status": "running",
            "platform": platform.system(),
            "python_version": platform.python_version(),
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
    port = int(os.getenv('PORT', 5002))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    logger.info(f"Starting PLC QA Dashboard on port {port}")
    
    # Run Flask app (Gunicorn handles this in production)
    app.run(host='0.0.0.0', port=port, debug=debug)
