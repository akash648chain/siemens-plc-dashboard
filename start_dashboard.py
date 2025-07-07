#!/usr/bin/env python3
"""
Simple launcher for the Siemens PLC QA Dashboard
"""

import os
import sys
import subprocess
import socket
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import psutil
        from plc_qa_assistant import SiemensPLCQAAssistant
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Please install dependencies with: pip install -r requirements.txt")
        return False

def get_network_ip():
    """Get the local network IP address"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # Fallback method
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except Exception:
            return "localhost"

def create_directories():
    """Create necessary directories"""
    directories = ["templates", "static", "siemens_docs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def main():
    print("🚀 Siemens PLC QA Dashboard Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("web_dashboard.py").exists():
        print("❌ web_dashboard.py not found in current directory")
        print("Please run this script from the project directory")
        return 1
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        return 1
    print("✅ Dependencies OK")
    
    # Create directories
    print("📁 Creating directories...")
    create_directories()
    print("✅ Directories created")
    
    # Get network information
    local_ip = get_network_ip()
    
    print("\n🌐 Dashboard will be available at:")
    print(f"   🖥️  Local:   http://localhost:8080")
    print(f"   📱 Network: http://{local_ip}:8080")
    print("\n📋 Features:")
    print("   • Responsive design for mobile and desktop")
    print("   • Real-time chat interface")
    print("   • Example questions and system monitoring")
    print("   • Session history and source references")
    print("\n🎯 Access from any device on your network!")
    print("=" * 50)
    
    # Start the dashboard
    try:
        print("🔄 Starting dashboard...")
        subprocess.run([sys.executable, "web_dashboard.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting dashboard: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
