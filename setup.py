#!/usr/bin/env python3
"""
Setup script for Siemens PLC QA Assistant
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is suitable"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("   Please upgrade to Python 3.8 or higher")
        return False

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found")
        return False
    
    # Install packages
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python packages"
    )

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "siemens_docs",
        "vectorstore"
    ]
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            print(f"✅ Created directory: {directory}")
        except Exception as e:
            print(f"❌ Failed to create directory {directory}: {e}")
            return False
    
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    print("🔧 Setting up environment file...")
    
    if not Path(".env").exists():
        if Path(".env.example").exists():
            try:
                # Copy .env.example to .env
                with open(".env.example", "r") as src, open(".env", "w") as dst:
                    dst.write(src.read())
                print("✅ Created .env file from .env.example")
            except Exception as e:
                print(f"❌ Failed to create .env file: {e}")
                return False
        else:
            # Create basic .env file
            with open(".env", "w") as f:
                f.write("# Siemens PLC QA Assistant Environment Variables\n")
                f.write("# Add your API keys here if needed\n")
                f.write("# OPENAI_API_KEY=your_key_here\n")
            print("✅ Created basic .env file")
    else:
        print("✅ .env file already exists")
    
    return True

def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        from plc_qa_assistant import SiemensPLCQAAssistant
        print("✅ Main module imports successfully")
        
        # Test basic functionality
        assistant = SiemensPLCQAAssistant()
        print("✅ Assistant can be instantiated")
        
        # Test knowledge base
        knowledge = assistant.get_plc_knowledge_base()
        print(f"✅ Knowledge base loaded ({len(knowledge)} documents)")
        
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def main():
    """Main setup function"""
    
    print("🚀 Siemens PLC QA Assistant Setup")
    print("=" * 50)
    
    steps = [
        ("Check Python version", check_python_version),
        ("Install dependencies", install_dependencies),
        ("Create directories", create_directories),
        ("Setup environment", create_env_file),
        ("Test installation", test_installation)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 Step: {step_name}")
        if not step_func():
            print(f"❌ Setup failed at step: {step_name}")
            return 1
    
    print("\n🎉 Setup completed successfully!")
    print("\n📖 Next steps:")
    print("   1. Run the web interface: streamlit run plc_qa_assistant.py")
    print("   2. Or use CLI: python cli_assistant.py --help")
    print("   3. Run tests: python test_assistant.py")
    print("\n📚 Read README.md for detailed usage instructions")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
