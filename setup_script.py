#!/usr/bin/env python3
"""
Setup script for Wholesale2Flip Flask application
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required packages"""
    try:
        print("Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['templates', 'static']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'static/style.css',
        'static/script.js'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present!")
        return True

def main():
    """Main setup function"""
    print("🚀 Setting up Wholesale2Flip Flask Application...")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Check files
    if not check_files():
        print("\n❌ Setup incomplete - missing required files!")
        print("Please make sure all files are in the correct locations.")
        return False
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed - could not install requirements!")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\nTo run the application:")
    print("   python app.py")
    print("\nOr use the run script:")
    print("   python run.py")
    print("\nThen visit: http://localhost:5000")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)