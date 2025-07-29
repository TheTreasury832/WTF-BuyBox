#!/usr/bin/env python3
"""
Simple script to run the Wholesale2Flip Flask application
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, init_db
    
    if __name__ == '__main__':
        # Initialize database
        print("Initializing database...")
        init_db()
        print("Database initialized successfully!")
        
        # Run the app
        print("Starting Wholesale2Flip application...")
        print("Visit: http://localhost:5000")
        
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
        
except ImportError as e:
    print(f"Import Error: {e}")
    print("Make sure you have installed the requirements:")
    print("pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1)