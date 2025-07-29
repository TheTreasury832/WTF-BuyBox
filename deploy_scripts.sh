#!/bin/bash
# scripts/deploy_v1.sh - Deploy V1 FREE version

echo "🚀 Deploying Wholesale2Flip V1 FREE..."

# Navigate to V1 directory
cd v1-free

# Check if requirements exist
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found in v1-free directory"
    exit 1
fi

# Check if main app exists
if [ ! -f "app_v1.py" ]; then
    echo "❌ app_v1.py not found in v1-free directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run tests if they exist
if [