#!/bin/bash
# Run tests for email classifier
set -e

echo "Running email classifier tests..."
echo ""

# Change to project directory
cd "$(dirname "$0")/.."

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Running tests..."
echo "================"
python3 -m pytest tests/ -v --tb=short

echo ""
echo "All tests passed!"
echo ""
echo "To run with coverage:"
echo "  python3 -m pytest tests/ --cov=scripts --cov-report=html"
echo ""
echo "To run specific test:"
echo "  python3 -m pytest tests/test_email_classifier.py -v -k test_verification"
