#!/usr/bin/env python3
# Code created by https://linktr.ee/saran709
"""
Offline Voting System
Main entry point for the application

This is a secure offline voting system that uses SQLite for data storage.
Features include voter authentication, candidate management, and real-time results.

Usage:
    python main.py

Requirements:
    - Python 3.7 or higher
    - All required libraries are built into Python (sqlite3, tkinter, datetime, hashlib)

Author: Voting System Development Team
Version: 1.0
"""

import sys
import os
from gui import VotingGUI

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)

def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter as tk
        # Test if tkinter is working
        test_root = tk.Tk()
        test_root.withdraw()  # Hide the test window
        test_root.destroy()
        return True
    except ImportError:
        print("Error: tkinter is not available.")
        print("Please install tkinter or use a Python distribution that includes it.")
        return False
    except Exception as e:
        print(f"Error: tkinter test failed: {e}")
        return False

def main():
    """Main application entry point"""
    print("Starting Offline Voting System...")
    
    # Check system requirements
    check_python_version()
    
    if not check_tkinter():
        sys.exit(1)
    
    try:
        # Create and run the GUI application
        app = VotingGUI()
        print("Application initialized successfully.")
        print("Contact system administrator for admin credentials.")
        print("GUI is now running...")
        
        app.run()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: Failed to start application: {e}")
        print("Please check that all required files are present:")
        print("- database_manager.py")
        print("- voting_system.py") 
        print("- gui.py")
        print("- admin_panel.py")
        sys.exit(1)

if __name__ == "__main__":
    main()