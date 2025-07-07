#!/usr/bin/env python3
"""
Simple web dashboard for Siemens PLC QA Assistant
Uses basic knowledge base without complex dependencies
"""

from flask import Flask, render_template, request, jsonify, session
import os
import json
import time
from datetime import datetime
from simple_plc_assistant import SimplePLCQAAssistant
import logging
import socket

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)
app.secret_key = 'simple_plc_qa_dashboard_2024'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Global assistant instance
assistant = SimplePLCQAAssistant()

def get_network_ip():
    """Get the local network IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except Exception:
            return "localhost"

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('simple_dashboard.html')

@app.route('/api/status')
def api_status():
    """Get assistant status - always ready for simple version"""
    return jsonify({
        "ready": True,
        "status": "ready",
        "message": "Simple PLC Assistant ready!"
    })

@app.route('/api/ask', methods=['POST'])
def api_ask():
    """Ask a question to the assistant"""
    global assistant
    
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
def api_system_info():
    """Get basic system information"""
    try:
        import psutil
        import platform
        
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
    
    print("🚀 Starting Simple Siemens PLC QA Dashboard...")
    print("🌐 Access from any device on your network!")
    print("📱 Mobile-friendly interface included")
    print("=" * 50)
    
    # Get network information
    local_ip = get_network_ip()
    
    print(f"🖥️  Local access: http://localhost:5001")
    print(f"📱 Network access: http://{local_ip}:5001")
    print("\n📋 Features:")
    print("   • Instant startup - no initialization required")
    print("   • Built-in Siemens PLC knowledge base")
    print("   • Mobile-responsive design")
    print("   • Real-time chat interface")
    print("   • Session history and source references")
    print("=" * 50)
    
    # Run Flask app
    app.run(
        host='0.0.0.0',  # Allow access from any device on network
        port=5001,
        debug=False,
        threaded=True
    )
