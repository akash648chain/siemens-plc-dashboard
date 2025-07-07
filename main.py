#!/usr/bin/env python3
"""
Sample Python file for testing virtual environment
"""

import sys
import os

def main():
    print("Hello from Python!")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in a virtual environment!")
        print(f"Virtual env path: {sys.prefix}")
    else:
        print("❌ Not running in a virtual environment")

if __name__ == "__main__":
    main()
