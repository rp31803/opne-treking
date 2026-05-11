#!/bin/bash
# Netlify build script for OSINT Tracker

echo "🚀 Building OSINT Tracker for Netlify..."

# Install Python dependencies
pip install -r requirements.txt

# Install additional tools for static export
pip install streamlit-pydantic

# Create build directory
mkdir -p build

# Generate static HTML export
echo "Generating static export..."
streamlit run main.py --server.headless true --server.runOnSave true &
STREAMLIT_PID=$!

# Wait a moment for Streamlit to start
sleep 10

# Use curl to get the static HTML
curl -s http://localhost:8501 > build/index.html

# Kill the Streamlit process
kill $STREAMLIT_PID

# Copy static assets
cp -r .streamlit build/ 2>/dev/null || true

echo "✅ Build completed!"
echo "Static files generated in build/ directory"