#!/bin/bash
# Setup script for Raspberry Pi Answer Sheet Checker

set -e  # Exit on any error

echo "=========================================="
echo "RPi Answer Sheet Checker - Setup"
echo "=========================================="

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "⚠️  Warning: Not running on Raspberry Pi OS"
    echo "This setup is optimized for Raspberry Pi"
fi

# Check Python version
echo ""
echo "📦 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
if [ ! -d "rpi_env" ]; then
    python3 -m venv rpi_env
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "⚙️  Activating virtual environment..."
source rpi_env/bin/activate

# Upgrade pip
echo ""
echo "📝 Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
cd rpi
pip install -r requirements.txt

# Test imports
echo ""
echo "🧪 Testing imports..."
python3 << EOF
import sys
try:
    import torch
    import cv2
    import flask
    from PIL import Image
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    print("✓ All imports successful")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)
EOF

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p uploads results
echo "✓ Directories created"

# Verify camera
echo ""
echo "📷 Checking camera..."
python3 << EOF
from camera import detect_available_cameras
cameras = detect_available_cameras()
if cameras:
    print(f"✓ Found {len(cameras)} camera(s): {cameras}")
else:
    print("⚠️  No cameras detected (this is OK if not using camera)")
EOF

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate environment:"
echo "   source rpi_env/bin/activate"
echo ""
echo "2. Start web server:"
echo "   cd rpi && python3 server.py"
echo ""
echo "3. Or use CLI:"
echo "   python3 cli.py --help"
echo ""
echo "Open browser to: http://localhost:5000"
echo "=========================================="
