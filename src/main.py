#!/usr/bin/env python3
"""
Main entry point for the Materna CRM application.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from gui.main_window import MainWindow

def main():
    """Main application entry point."""
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
