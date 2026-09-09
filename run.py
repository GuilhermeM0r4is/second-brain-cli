#!/usr/bin/env python
"""
Second Brain CLI - Launcher
Run from the root directory: python run.py
"""

if __name__ == "__main__":
    from application.main import main
    from ui.header import print_info
    
    print_info()
    main()