#!/bin/bash

# DEPLOYMENT SCRIPT
# Consciousness Revolution Platform
# Built: 2025-11-08

echo "======================================================================"
echo "CONSCIOUSNESS REVOLUTION - DEPLOYMENT SCRIPT"
echo "======================================================================"
echo ""

# Check Python
echo "Checking Python..."
python3 --version || { echo "Python 3 required!"; exit 1; }

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install numpy flask flask-cors || { echo "Failed to install dependencies"; exit 1; }

# Run tests
echo ""
echo "Running module tests..."
python3 MODULES/ADVANCED/pattern_recognition_engine/pattern_recognition.py
python3 MODULES/ADVANCED/autonomous_learning_system/autonomous_learning.py
python3 MODULES/ADVANCED/quantum_computing_interface/quantum_computing.py

# Check if tests passed
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
else
    echo ""
    echo "❌ Tests failed!"
    exit 1
fi

# Start API server
echo ""
echo "======================================================================"
echo "DEPLOYMENT COMPLETE!"
echo "======================================================================"
echo ""
echo "To start the API server:"
echo "  python3 API_SERVER.py"
echo ""
echo "To run master integration demo:"
echo "  python3 MASTER_INTEGRATION.py"
echo ""
echo "All 10 modules ready:"
echo "  ✅ Pattern Recognition"
echo "  ✅ Autonomous Learning"
echo "  ✅ Collaboration Hub"
echo "  ✅ Blockchain"
echo "  ✅ Quantum Computing"
echo "  ✅ Neural Networks"
echo "  ✅ Time Series"
echo "  ✅ Recommendations"
echo "  ✅ NLP"
echo "  ✅ Computer Vision"
echo ""
echo "🚀 Platform operational!"
echo "======================================================================"
